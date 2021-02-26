# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 2021/2/25 14:49
# @Description   :
from abc import ABC, abstractmethod
from typing import Optional, NoReturn

from stardew.core.web.schemas import BearerToken
from stardew.core.web.schemas import CaptchaInfo


class LoginService(ABC):

    @abstractmethod
    async def login(
            self,
            email: str,
            password: str
    ) -> BearerToken:
        """ 登录逻辑 """

    @abstractmethod
    async def create_captcha(
            self,
            width: Optional[int] = None,
            height: Optional[int] = None,
    ) -> CaptchaInfo:
        """
        创建二维码
        :param width: 二维码宽度
        :param height: 二维码高度
        :return:
        """

    @abstractmethod
    async def verify_captcha(
            self,
            uid: str,
            code: str
    ) -> NoReturn:
        """
        校验验证码, 不存在或不一致时抛出错误
        :param uid: redis中的键名
        :param code: 验证码内容
        :return:
        """
