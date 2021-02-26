# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 2021/2/8 12:38
# @Description   : 系统用户管理
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Response, status

from stardew.services.system.interfaces import UserService
from stardew.core.deps.security import permission_required
from stardew.core.container import IocContainer as Container
from stardew.schemas.system import UserSimpleSchema, UserCreationSchema, UserUpdateSchema


user_router: APIRouter = APIRouter(tags=["user"])


@user_router.get(
    path="/",
    name="获取用户列表",
    dependencies=[Depends(permission_required("sys:user:list"))]
)
@inject
async def get_user_list(
        user_service: UserService = Depends(Provide[Container.async_user_service])
):
    """ 获取用户列表 """
    users = await user_service.get_user_list()
    return [UserSimpleSchema.from_orm(user) for user in users]


@user_router.get(
    path="/{user_id}",
    name="获取用户详情信息",
    response_model=UserSimpleSchema,
    dependencies=[Depends(permission_required("sys:user:query"))]
)
@inject
async def get_user(
        user_id: str,
        user_service: UserService = Depends(Provide[Container.async_user_service]),
):
    """ 获取用户详情 """
    user = await user_service.get_user(identity=user_id)
    return UserSimpleSchema.from_orm(user)


@user_router.post(
    path="/",
    name="创建新用户",
    dependencies=[Depends(permission_required("sys:user:add"))]
)
@inject
async def create_user(
        create_schema: UserCreationSchema,
        user_service: UserService = Depends(Provide[Container.async_user_service])
):
    """ 创建新用户 """
    await user_service.add_user(create_schema=create_schema)
    return Response(status_code=status.HTTP_201_CREATED)


@user_router.put(
    path="/{user_id}",
    name="修改用户信息",
    dependencies=[Depends(permission_required("sys:user:update"))]
)
@inject
async def update_user(
        user_id: str,
        update_schema: UserUpdateSchema,
        user_service: UserService = Depends(Provide[Container.async_user_service])
):
    """ 修改用户信息 """
    user = await user_service.get_user(identity=user_id)
    fresh_user = await user_service.update_user(model=user, update_schema=update_schema)
    return fresh_user
