# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 2021/3/2 14:59
# @Description   :
from typing import List, Optional

from fastapi import HTTPException, status

from stardew.core.db.crud import CRUDService
from stardew.core.web.schemas import TreeNode
from stardew.models.system import SysMenu
from stardew.schemas.system import MenuCreateSchema, MenuUpdateSchema
from stardew.services.system.menu import MenuService


class MenuServiceImpl(MenuService):



    def __init__(self, crud: CRUDService):
        self.crud = crud

    def get_menu_list(self, page_no: Optional[int] = 0, page_size: Optional[int] = 100) -> List[SysMenu]:
        return self.crud.get_multi(page_no=page_no, page_size=page_size)

    def get_menu(self, menu_id: str) -> SysMenu:
        menu: Optional[SysMenu] = self.crud.get_by_id(identity=menu_id)
        if menu is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="未能找到相关按钮/菜单")
        return menu

    def update_menu(self, menu_id: str, update_schema: MenuUpdateSchema) -> None:
        # TODO 菜单字段之间的约束
        return self.crud.update(identity=menu_id, update_schema=update_schema)

    def add_menu(self, create_schema: MenuCreateSchema) -> None:
        self._check_perm_available(create_schema.perm)
        return self.crud.add(create_schema=create_schema)

    def delete_menu(self, menu_id: str) -> None:
        return self.crud.delete_by_id(identity=menu_id)

    def build_menu_tree(self) -> List[TreeNode]:
        # 查询最顶级menu即可，其他所有menu会包括与其上级menu
        menus: List[SysMenu] = self.crud.filter(where_clause={"parent_id": 0})
        menu_tree: List[TreeNode] = [TreeNode.from_orm(menu) for menu in menus]
        return menu_tree

    def _check_perm_available(self, perm: str) -> None:
        """ 检测权限字符串是否可用 """
        if len(self.crud.filter(where_clause={"perm": perm})) > 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="该权限字符串已被占用")
