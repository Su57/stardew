# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 2021/2/26 12:58
# @Description   :
from typing import List, NoReturn, Optional

from stardew.models.system import SysUser
from stardew.common.utils import SecurityUtil
from stardew.services.system.interfaces import UserService
from stardew.core.db.crud import AsyncCURDService, CURDService
from stardew.schemas.system import UserCreationSchema, UserUpdateSchema


class UserServiceImpl(UserService):
    """ 用户相关业务逻辑 """

    def __init__(self, curd: CURDService):
        self.curd = curd
        self.curd.set_model_class(SysUser)

    def get_user_list(self, page_no: Optional[int] = 0, page_size: Optional[int] = 100) -> List[SysUser]:
        return self.curd.get_multi(page_no=page_no, page_size=page_size)

    def get_user(self, identity: str) -> SysUser:
        return self.curd.get_by_id(identify=identity)

    def add_user(self, create_schema: UserCreationSchema) -> NoReturn:
        create_schema.password = SecurityUtil.generate_password(create_schema.password)
        return self.curd.add(create_schema=create_schema)

    def update_user(self, model, update_schema: UserUpdateSchema) -> SysUser:
        return self.curd.update(model=model, update_schema=update_schema)

    def delete_user(self, identity: str) -> NoReturn:
        return self.curd.delete_by_id(identity=identity)


class AsyncUserServiceImpl(UserService):

    def __init__(self, curd: AsyncCURDService):
        self.curd = curd
        self.curd.set_model_class(SysUser)

    async def get_user_list(self, page_no: Optional[int] = 0, page_size: Optional[int] = 100) -> List[SysUser]:
        return await self.curd.get_multi(page_no=page_no, page_size=page_size)

    async def get_user(self, identity: str) -> SysUser:
        return await self.curd.get_by_id(identify=identity)

    async def add_user(self, create_schema: UserCreationSchema) -> NoReturn:
        create_schema.password = SecurityUtil.generate_password(create_schema.password)
        return await self.curd.add(create_schema=create_schema)

    async def update_user(self, model, update_schema: UserUpdateSchema) -> SysUser:
        return await self.curd.update(model=model, update_schema=update_schema)

    async def delete_user(self, identity: str) -> NoReturn:
        return await self.curd.delete_by_id(identity=identity)
