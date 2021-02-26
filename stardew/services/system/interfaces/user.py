# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 2021/2/26 12:52
# @Description   :
from abc import ABC, abstractmethod
from typing import List, NoReturn, Optional, Awaitable, Union

from stardew.models.system import SysUser
from stardew.schemas.system import UserCreationSchema, UserUpdateSchema


class UserService(ABC):

    @abstractmethod
    def get_user_list(
            self,
            page_no: Optional[int] = 0,
            page_size: Optional[int] = 100
    ) -> Union[List[SysUser], Awaitable[List[SysUser]]]:
        """
        # TODO 这里的类型注解是不是有点...太菜了...
        获取用户列表(可分页)
        :param page_no: 页码
        :param page_size: 每页数量
        :return: 分页数据
        """

    @abstractmethod
    def get_user(self, identity: str) -> SysUser:
        """
        根据id获取用户
        :param identity: 用户id
        :return:
        """

    @abstractmethod
    def add_user(self, create_schema: UserCreationSchema) -> NoReturn:
        """
        新增用户
        :param create_schema: 新增时的数据
        :return:
        """

    @abstractmethod
    def update_user(self, model, update_schema: UserUpdateSchema) -> SysUser:
        """
        更新用户
        :param model: 待更新对象
        :param update_schema:  更新的数据
        :return: 更新后的对象
        """

    @abstractmethod
    def delete_user(self, identity: str) -> NoReturn:
        """
        根据id删除用户
        :param identity: 用户id
        :return:
        """
