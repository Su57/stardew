# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 2021/3/2 11:32
# @Description   :
from typing import Optional, List
from abc import ABC, abstractmethod

from stardew.models.system import SysRole
from stardew.schemas.system import RoleCreateSchema, RoleUpdateSchema


class RoleService(ABC):

    @abstractmethod
    def get_role_list(
            self,
            page_no: Optional[int] = 0,
            page_size: Optional[int] = 100
    ) -> List[SysRole]:
        """
        查询角色列表
        :param page_no: 页码
        :param page_size: 每页数量
        :return: 分页数据
        """
        pass

    @abstractmethod
    def get_roles_by_ids(self, identities: List[str]) -> List[SysRole]:
        """
        通过id获取role列表
        :param identities: id列表
        :return:
        """

    @abstractmethod
    def get_role(self, role_id: str) -> SysRole:
        """
        根据id获取角色。查询结果为None时抛出HttpException
        :param role_id: 角色id
        :return: 角色
        """

    @abstractmethod
    def add_role(self, create_schema: RoleCreateSchema) -> None:
        """
        新增角色
        :param create_schema: 新增时的数据
        :return::
        """

    @abstractmethod
    def update_role(self, identity: str, update_schema: RoleUpdateSchema) -> None:
        """
        更新用户
        :param identity: 待更新对象的id
        :param update_schema:  更新的数据
        :return:
        """
        pass

    @abstractmethod
    def delete_role(self, identity: str) -> None:
        """
        删除角色
        :param identity: 角色id
        :return:
        """