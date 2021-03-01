# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 2021/2/26 12:58
# @Description   :
from typing import List, Optional

from stardew.models.system import SysUser
from stardew.common.utils import SecurityUtil
from stardew.services.system.interfaces import UserService
from stardew.core.db.crud import AsyncCRUDService, CRUDService
from stardew.schemas.system import UserCreationSchema, UserUpdateSchema


class UserServiceImpl(UserService):

    def __init__(self, crud: CRUDService):
        self.crud = crud

    def get_user_list(self, page_no: Optional[int] = 0, page_size: Optional[int] = 100) -> List[SysUser]:
        return self.crud.get_multi(page_no=page_no, page_size=page_size)

    def get_user(self, identity: str) -> SysUser:
        return self.crud.get_by_id(identify=identity)

    def add_user(self, create_schema: UserCreationSchema) -> None:
        create_schema.password = SecurityUtil.generate_password(create_schema.password)
        return self.crud.add(create_schema=create_schema)

    def update_user(self, identity, update_schema: UserUpdateSchema) -> None:
        return self.crud.update(identity=identity, update_schema=update_schema)

    def delete_user(self, identity: str) -> None:
        return self.crud.delete_by_id(identity=identity)


class AsyncUserServiceImpl(UserService):

    def __init__(self, crud: AsyncCRUDService):
        self.crud = crud

    async def get_user_list(self, page_no: Optional[int] = 0, page_size: Optional[int] = 100) -> List[SysUser]:
        return await self.crud.get_multi(page_no=page_no, page_size=page_size)

    async def get_user(self, identity: str) -> SysUser:
        return await self.crud.get_by_id(identify=identity)

    async def add_user(self, create_schema: UserCreationSchema) -> None:
        create_schema.password = SecurityUtil.generate_password(create_schema.password)
        return await self.crud.add(create_schema=create_schema)

    async def update_user(self, identity, update_schema: UserUpdateSchema) -> None:
        return await self.crud.update(identity=identity, update_schema=update_schema)

    async def delete_user(self, identity: str) -> None:
        return await self.crud.delete_by_id(identity=identity)
