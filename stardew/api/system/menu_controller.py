# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 2021/3/2 15:11
# @Description   :
from typing import List, Optional, Dict

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Query, Response, status

from stardew.core.web.schemas import TreeNode
from stardew.models.system import SysMenu, SysRole
from stardew.services.system import RoleService
from stardew.services.system.menu import MenuService
from stardew.core.container import IocContainer as Container
from stardew.core.deps.security import role_required, permission_required
from stardew.schemas.system import MenuSimpleSchema, MenuCreateSchema, MenuUpdateSchema, MenuSchema

menu_router = APIRouter(tags=["menu"])


@menu_router.get(
    path="/",
    name="查询所有menu",
    dependencies=[Depends(role_required("admin"))]
)
@inject
def get_menu_list(
        page_no: Optional[int] = Query(0, description="对应页码"),
        page_size: Optional[int] = Query(10, description="每页数据"),
        menu_service: MenuService = Depends(Provide[Container.menu_service])
) -> List[MenuSchema]:
    """ 查询所有menu """
    menus: List[SysMenu] = menu_service.get_menu_list(page_no=page_no, page_size=page_size)
    return [MenuSchema.from_orm(menu) for menu in menus]


@menu_router.post(
    path="/",
    name="添加menu",
    dependencies=[Depends(role_required("admin"))]
)
@inject
def add_menu(
        create_schema: MenuCreateSchema,
        menu_service: MenuService = Depends(Provide[Container.menu_service])
):
    """ 添加新menu """

    menu_service.add_menu(create_schema=create_schema)
    return Response(status_code=status.HTTP_201_CREATED)


@menu_router.get(
    path="/{menu_id}",
    name="查询menu信息",
    dependencies=[Depends(role_required("admin"))]
)
@inject
def get_menu(
        menu_id: str = Query(..., description="菜单id"),
        menu_service: MenuService = Depends(Provide[Container.menu_service])
) -> MenuSimpleSchema:
    """ 查询menu详细信息 """
    menu = menu_service.get_menu(menu_id=menu_id)
    return MenuSimpleSchema.from_orm(menu)


@menu_router.put(
    path="/{menu_id}",
    name="更新menu信息",
    dependencies=[Depends(role_required("admin"))]
)
@inject
def update_menu(
        menu_id: str,
        update_schema: MenuUpdateSchema,
        menu_service: MenuService = Depends(Provide[Container.menu_service])
):
    menu_service.update_menu(menu_id=menu_id, update_schema=update_schema)
    return Response(status_code=status.HTTP_200_OK)


@menu_router.delete(
    path="/{menu_id}",
    name="删除menu",
    dependencies=[Depends(role_required("admin"))]
)
@inject
def delete_menu(
        menu_id: str,
        menu_service: MenuService = Depends(Provide[Container.menu_service])
):
    menu_service.delete_menu(menu_id=menu_id)
    return Response(status_code=status.HTTP_200_OK)


@menu_router.get(
    path="/tree",
    name="获取权限树结构",
    dependencies=[Depends(permission_required("sys:menu:tree"))]
)
@inject
def get_menu_tree(
        menu_service: MenuService = Depends(Provide[Container.menu_service]),
) -> List[TreeNode]:
    """ 获取权限树结构 """
    tree: List[TreeNode] = menu_service.build_menu_tree()
    return tree


@menu_router.get(
    path="/tree_with_role/{role_id}",
    name="获取某用户的权限树结构",
    dependencies=[Depends(role_required("admin"))]
)
@inject
def tree_with_role(
        role_id: str,
        menu_service: MenuService = Depends(Provide[Container.menu_service]),
        role_service: RoleService = Depends(Provide[Container.role_service])
) -> Dict:
    """ 获取某角色的权限树 """
    role: SysRole = role_service.get_role(role_id=role_id)
    checked_keys: List[str] = [menu.id for menu in role.perms]
    tree = menu_service.build_menu_tree()
    return {
        "tree": tree,
        "checked_keys": checked_keys
    }
