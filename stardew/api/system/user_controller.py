# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 2021/2/8 12:38
# @Description   : 系统用户管理
from typing import List, Optional

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Response, status

from stardew.models.system import SysUser
from stardew.core.deps.security import permission_required
from stardew.services.system.interfaces import UserService
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
        page_no: Optional[int] = 0,
        page_size: Optional[int] = 10,
        user_service: UserService = Depends(Provide[Container.user_service])
) -> List[UserSimpleSchema]:
    """ 获取用户列表 """
    users: List[SysUser] = user_service.get_user_list(page_no=page_no, page_size=page_size)
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
        user_service: UserService = Depends(Provide[Container.user_service]),
) -> UserSimpleSchema:
    """ 获取用户详情 """
    user: SysUser = user_service.get_user(identity=user_id)
    return UserSimpleSchema.from_orm(user)


@user_router.post(
    path="/",
    name="创建新用户",
    dependencies=[Depends(permission_required("sys:user:add"))]
)
@inject
async def create_user(
        create_schema: UserCreationSchema,
        user_service: UserService = Depends(Provide[Container.user_service])
):
    """ 创建新用户 """
    user_service.add_user(create_schema=create_schema)
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
        user_service: UserService = Depends(Provide[Container.user_service])
):
    """ 修改用户信息 """
    user_service.update_user(identity=user_id, update_schema=update_schema)
    return Response(status_code=status.HTTP_200_OK)


@user_router.delete(
    path="/{user_id}",
    name="删除系统用户",
    dependencies=[Depends(permission_required("sys:user:delete"))]
)
@inject
async def delete_user(
        user_id: str,
        user_service: UserService = Depends(Provide[Container.user_service])
):
    """ 删除系统用户 """
    user_service.delete_user(identity=user_id)
    return Response(status_code=status.HTTP_200_OK)