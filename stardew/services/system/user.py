# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 2021/2/26 12:52
# @Description   :
from typing import List, Optional, Union, Any, Dict
from abc import ABC, abstractmethod

from stardew.models.system import SysUser, SysRole
from stardew.schemas.system import UserCreateSchema, UserUpdateSchema


class UserService(ABC):
    """ 用户相关业务逻辑 """

    # TODO 这里的类型注解需要重新考虑，既要支持同步又要支持异步。。。

    @abstractmethod
    def get_user_list(
            self,
            page_no: Optional[int] = 0,
            page_size: Optional[int] = 100
    ) -> List[SysUser]:
        """
        获取用户列表(可分页)
        :param page_no: 页码
        :param page_size: 每页数量
        :return: 分页数据
        """
        pass

    @abstractmethod
    def get_user(self, identity: str) -> SysUser:
        """
        根据id获取用户。查询结果为None时抛出HttpException
        :param identity: 用户id
        :return:
        """
        pass

    @abstractmethod
    def add_user(self, create_schema: Union[UserCreateSchema, Dict[str, Any]]) -> None:
        """
        新增用户
        :param create_schema: 新增时的数据
        :return:
        """
        pass

    @abstractmethod
    def update_user(
            self,
            identity: str,
            update_schema: Union[UserUpdateSchema, Dict[str, Any]],
    ) -> SysUser:
        """
        更新用户
        :param identity: 待更新对象的id
        :param update_schema:  更新的数据
        :return: 更新后的对象
        """
        pass

    @abstractmethod
    def delete_user(self, identity: str) -> None:
        """
        根据id删除用户
        :param identity: 用户id
        :return:
        """
        pass
