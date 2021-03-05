# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 2021/3/2 11:58
# @Description   :
from typing import Optional, List

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Response, Query, status

from stardew.models.system import SysRole
from stardew.services.system import RoleService
from stardew.core.deps.security import permission_required
from stardew.core.container import IocContainer as Container
from stardew.schemas.system import RoleSimpleSchema, RoleCreateSchema, RoleUpdateSchema

role_router: APIRouter = APIRouter(tags=["role"])


@role_router.get(
    path="/",
    name="获取角色列表",
    # dependencies=[Depends(permission_required("sys:role:list"))]
)
@inject
def get_role_list(
        page_no: Optional[int] = Query(0, description="对应页码"),
        page_size: Optional[int] = Query(10, description="每页数据"),
        role_service: RoleService = Depends(Provide[Container.role_service])
) -> List[RoleSimpleSchema]:
    """ 获取角色列表 """
    roles: List[SysRole] = role_service.get_role_list(page_no=page_no, page_size=page_size)
    return [RoleSimpleSchema.from_orm(role) for role in roles]


@role_router.get(
    path="/{role_id}",
    name="获取角色信息",
    dependencies=[Depends(permission_required("sys:role:query"))]
)
@inject
def get_role(
        role_id: str = Query(..., description="角色id"),
        role_service: RoleService = Depends(Provide[Container.role_service])
) -> RoleSimpleSchema:
    """ 获取角色信息 """
    role: SysRole = role_service.get_role(role_id=role_id)
    return RoleSimpleSchema.from_orm(role)


@role_router.post(
    path="/",
    name="添加角色",
    # dependencies=[Depends(permission_required("sys:role:add"))]
)
@inject
def add_role(
        create_schema: RoleCreateSchema,
        role_service: RoleService = Depends(Provide[Container.role_service])
):
    """ 添加角色 """
    role_service.add_role(create_schema=create_schema)
    return Response(status_code=status.HTTP_201_CREATED)


@role_router.put(
    path="/{role_id}",
    name="更新角色",
    # dependencies=[Depends(permission_required("sys:role:update"))]
)
@inject
def update_role(
        role_id: str,
        update_schema: RoleUpdateSchema,
        role_service: RoleService = Depends(Provide[Container.role_service])
):
    """ 更新角色 """
    role_service.update_role(identity=role_id, update_schema=update_schema)
    return Response(status_code=status.HTTP_200_OK)


@role_router.delete(
    path="/{role_id}",
    name="删除角色",
    dependencies=[Depends(permission_required("sys:role:delete"))]
)
@inject
def delete_role(role_id: str, role_service: RoleService = Depends(Provide[Container.role_service])):
    """ 删除角色 """
    role_service.delete_role(identity=role_id)
    return Response(status_code=status.HTTP_200_OK)
