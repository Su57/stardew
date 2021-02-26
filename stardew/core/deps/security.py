# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 2021/2/9 21:53
# @Description   :
from typing import Union, List, Set, Dict, Optional, Callable

import orjson
from jose import jwt
from aioredis import Redis
from pydantic import ValidationError
from jose.constants import ALGORITHMS
from fastapi import Depends, HTTPException, status
from dependency_injector.wiring import inject, Provide
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from stardew.settings import settings
from stardew.common.enums import StatusEnum
from stardew.common.constants import Constant
from stardew.core.container import IocContainer as Container
from stardew.core.web.schemas import TokenPayload, LoginUser

http_bearer = HTTPBearer(scheme_name=settings.JWT_PREFIX, auto_error=False)


@inject
async def login_required(
        redis: Redis = Depends(Provide[Container.redis_pool]),
        authorization_credentials: Optional[HTTPAuthorizationCredentials] = Depends(http_bearer)
) -> LoginUser:
    """
    登录校验
    :param redis: redis客户端， 通常为 `aioredis.commands.Redis` 实例
    :param authorization_credentials: 身份凭证
    :return: 当前登录者的信息
    """
    if authorization_credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="请先登录",
        )
    try:
        payload = jwt.decode(
            token=authorization_credentials.credentials,
            key=settings.SECRET_KEY,
            algorithms=ALGORITHMS.HS256
        )
        token_data = TokenPayload(sub=payload["sub"])
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无效的身份信息",
        )
    redis_key: str = Constant.LOGIN_REDIS_KEY + token_data.sub
    redis_value: str = await redis.get(redis_key)

    if not redis_value:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="登录信息已过期，请重新登录。")

    info: Dict = orjson.loads(redis_value)
    login_user: LoginUser = LoginUser(**info)

    if not login_user.sys_user.status == StatusEnum.enable:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="当前用户不可用，请联系管理员。")
    return login_user


def role_required(key: Union[str, List[str]]) -> Callable:
    """
    角色校验。若当前登录者的角色(roles)属性中包含所需角色则视为通过校验。
    Example:
        1: 在具体逻辑中不需要使用到登录者具体信息时，可以放在路由装饰器的dependencies参数中:
            @some_router.get(
                path="/some-path",
                dependencies=[Depends(role_required("some_role_key"))]
            )
            async def some_func(): ...
        2: 在具体逻辑中需要使用登录者信息的时候，可以在路由函数中使用它:
            @some_router.get(path="/some-path")
            async def some_func(
                current_user = Depends(role_required("some_role_key"))
            ): ...
    :param key: 所需角色名
    :return: 校验通过则返回当前登录者信息，否则抛出403异常
    """

    async def wrapper(current_user: LoginUser = Depends(login_required)) -> LoginUser:
        roles: Set[str] = current_user.roles
        key_set: Set = set(tuple(key)) if isinstance(key, str) else set(key)
        if not set(key_set).issubset(roles) and current_user.sys_user.is_super:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足，请联系管理员")
        return current_user

    return wrapper


def permission_required(key: str) -> Callable:
    """
    权限校验。若当前登录者的权限(perms)属性中包含所需角色则视为通过校验。
    Example:
        1: 在具体逻辑中不需要使用到登录者具体信息时，可以放在路由装饰器的dependencies参数中:
            @some_router.get(
                path="/some-path",
                dependencies=[Depends(permission_required("some_permission_key"))]
            )
            async def some_func(): ...
        2: 在具体逻辑中需要使用登录者信息的时候，可以在路由函数中使用它:
            @some_router.get(path="/some-path")
            async def some_func(
                current_user = Depends(permission_required("some_permission_key"))
            ): ...
    :param key: 所需权限名
    :return: 校验通过则返回当前登录者信息，否则抛出403异常
    """

    async def wrapper(current_user: LoginUser = Depends(login_required)) -> LoginUser:
        permissions: Set[str] = current_user.perms
        if key not in permissions and not current_user.sys_user.is_super:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足，请联系管理员")
        return current_user

    return wrapper
