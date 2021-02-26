# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 2021/2/25 18:22
# @Description   :
import base64
from io import BytesIO
from random import randint
from datetime import datetime
from datetime import timedelta
from string import ascii_letters, digits
from typing import Set, Optional, NoReturn

from aioredis import Redis
from fastapi import HTTPException, status
from captcha.image import ImageCaptcha, Image

from stardew.settings import settings
from stardew.models.system import SysUser
from stardew.core.db.crud import CURDService
from stardew.common.constants import Constant
from stardew.core.web.schemas import CaptchaInfo
from stardew.schemas.system import UserSimpleSchema
from stardew.common.utils import StringUtil, SecurityUtil
from stardew.services.common.interfaces import LoginService
from stardew.core.web.schemas import BearerToken, LoginUser


class LoginServiceImpl(LoginService):
    """ AdminService具体实现 """

    def __init__(
        self,
        curd: CURDService,
        redis: Redis
    ) -> None:
        self.curd = curd
        self.curd.set_model_class(SysUser)
        self.redis = redis

    async def login(
        self,
        email: str,
        password: str
    ) -> BearerToken:
        """ 登录逻辑 """
        query_set = self.curd.filter(where_clause={"email": email})
        if len(query_set) == 0:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "用户不存在")
        user: SysUser = query_set[0]
        if not SecurityUtil.verify_password(password, user.password):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "用户名或密码错误")
        roles: Set[str] = {role.name for role in user.roles}
        perms: Set[str] = {"*:*:*"} if user.is_super else {
            menu.perm for role in user.roles for menu in role.perms if menu.perm != ""
        }

        schema: UserSimpleSchema = UserSimpleSchema.from_orm(user)
        login_user: LoginUser = LoginUser(
            login_time=datetime.utcnow(),
            sys_user=schema,
            roles=roles,
            perms=perms
        )
        uid: str = StringUtil.get_unique_key()
        await self.redis.set(key=Constant.LOGIN_REDIS_KEY + uid, value=login_user.json())
        token: str = SecurityUtil.create_token(subject=uid)
        return BearerToken(access_token=token, token_type=settings.JWT_PREFIX)

    async def create_captcha(
            self,
            width: Optional[int] = 160,
            height: Optional[int] = 60,
    ) -> CaptchaInfo:
        """ 创建验证码 """
        width = width
        height = height
        char: str = ""
        allowed_letters: str = digits + ascii_letters
        for i in range(settings.CAPTCHA_CHAR_LENGTH):
            index: int = randint(0, len(allowed_letters) - 1)
            char += allowed_letters[index]
        image_captcha: ImageCaptcha = ImageCaptcha(width, height)
        image: Image = image_captcha.generate_image(char)
        f: BytesIO = BytesIO()
        image.save(f, format='png')
        base64_str: str = base64.b64encode(f.getvalue()).decode(Constant.UTF8)
        f.close()
        key: str = StringUtil.get_unique_key()
        expired_minutes: timedelta = timedelta(minutes=settings.CAPTCHA_EXPIRED_MINUTES)
        await self.redis.set(key=Constant.CAPTCHA_REDIS_KEY + key, value=char, expire=expired_minutes.seconds)

        return CaptchaInfo(uid=key, image=base64_str)

    async def verify_captcha(
            self,
            uid: str,
            code: str
    ) -> NoReturn:
        """ 校验验证码, 不存在或不一致时抛出错误 """
        redis_code = await self.redis.get(Constant.CAPTCHA_REDIS_KEY + uid, encoding=Constant.UTF8)
        if redis_code is None:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="验证码已失效")
        if not redis_code.lower() == code.lower():
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="验证码错误")
