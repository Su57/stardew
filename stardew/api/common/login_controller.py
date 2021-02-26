# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 2021/2/1 11:52
# @Description   :
from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide

from stardew.schemas.common import LoginSchema
from stardew.services.common.interfaces import LoginService
from stardew.core.container import IocContainer as Container
from stardew.core.web.schemas import BearerToken, CaptchaInfo

login_router = APIRouter(tags=['login'])


@login_router.get("/captcha", name="获取验证码接口")
@inject
async def create_captcha(
        login_service: LoginService = Depends(Provide[Container.login_service])
) -> CaptchaInfo:
    """ 生成验证码 """
    captcha = await login_service.create_captcha()
    return captcha


@login_router.post("/login", name="登录接口")
@inject
async def login(
        body: LoginSchema,
        login_service: LoginService = Depends(Provide[Container.login_service])
) -> BearerToken:
    """ 登录 """
    # 检验验证码
    await login_service.verify_captcha(body.uid, body.code)
    # 执行登录，获取令牌
    token = await login_service.login(email=body.email, password=body.password)
    return token
