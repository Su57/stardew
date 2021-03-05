# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 2021/3/2 14:32
# @Description   :
from typing import List, Optional
from abc import ABC, abstractmethod

from stardew.models.system import SysMenu
from stardew.schemas.system import MenuCreateSchema, MenuUpdateSchema
from stardew.core.web.schemas import TreeNode


class MenuService(ABC):

    @abstractmethod
    def get_menu_list(
            self,
            page_no: Optional[int] = 0,
            page_size: Optional[int] = 100
    ) -> List[SysMenu]:
        """
        获取菜单列表
        :param page_no: 页码
        :param page_size: 每页数量
        :return: 分页数据
        """
        pass

    @abstractmethod
    def get_menu(self, menu_id: str) -> SysMenu:
        """
        获取菜单信息
        :param menu_id: 菜单id
        :return:
        """

    @abstractmethod
    def update_menu(self, menu_id: str, update_schema: MenuUpdateSchema) -> None:
        """
        更新菜单
        :param menu_id: 菜单id
        :param update_schema:
        :return:
        """
        pass

    @abstractmethod
    def add_menu(self, create_schema: MenuCreateSchema) -> None:
        """
        添加菜单
        :param create_schema: 添加数据
        :return:
        """
        pass

    @abstractmethod
    def delete_menu(self, menu_id: str) -> None:
        """
        删除菜单
        :param menu_id: 菜单id
        :return:
        """
        pass

    @abstractmethod
    def build_menu_tree(self) -> List[TreeNode]:
        """
        构建菜单树
        :return:
        """

    @abstractmethod
    def get_role_menus(self, role_id: str) -> List[str]:
        """
        获取某角色所有的menu的id
        :param role_id: 角色id
        :return:
        """

