# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 2021/2/26 12:58
# @Description   :
from typing import List, Optional, Dict, Any, Union

from fastapi import HTTPException, status

from stardew.models.system import SysUser, SysRole
from stardew.common.utils import SecurityUtil
from stardew.repository.system import UserRepository
from stardew.services.system.user import UserService
from stardew.schemas.system import UserCreateSchema, UserUpdateSchema


class UserServiceImpl(UserService):

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_user_list(self, page_no: Optional[int] = 0, page_size: Optional[int] = 100) -> List[SysUser]:
        return self.repository.get_multi(page_no=page_no, page_size=page_size)

    def get_user(self, identity: str) -> SysUser:
        user: Optional[SysUser] = self.repository.get_by_id(identity=identity)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="未找到相关用户")
        return user

    def add_user(self, create_schema: Union[UserCreateSchema, Dict[str, Any]]) -> None:
        self._check_email_available(create_schema.email)
        create_schema.password = SecurityUtil.generate_password(create_schema.password)
        return self.repository.add(create_schema=create_schema)

    def update_user(
            self,
            identity: str,
            update_schema: Union[UserUpdateSchema, Dict[str, Any]],
    ) -> SysUser:
        return self.repository.update(identity=identity, update_schema=update_schema)

    def delete_user(self, identity: str) -> None:
        return self.repository.delete(identity=identity)

    def _check_email_available(self, email: str):
        """
        校验email是否可用
        :param email: 目标email
        :return:
        """
        if self.repository.get_by_email(email=email) is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="该邮箱已注册")

#
# class AsyncUserServiceImpl(UserService):
#
#     def __init__(self, crud: AsyncCRUDService):
#         self.crud = crud
#
#     async def get_user_list(self, page_no: Optional[int] = 0, page_size: Optional[int] = 100) -> List[SysUser]:
#         return await self.crud.get_multi(page_no=page_no, page_size=page_size)
#
#     async def get_user(self, identity: str) -> Optional[SysUser]:
#         return await self.crud.get_by_id(identify=identity)
#
#     async def add_user(self, create_schema: UserCreateSchema) -> None:
#         create_schema.password = SecurityUtil.generate_password(create_schema.password)
#         return await self.crud.add(create_schema=create_schema)
#
#     async def update_user(self, identity, update_schema: UserUpdateSchema) -> None:
#         return await self.crud.update(identity=identity, update_schema=update_schema)
#
#     async def delete_user(self, identity: str) -> None:
#         return await self.crud.delete_by_id(identity=identity)
