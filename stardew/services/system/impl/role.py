# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 2021/3/2 11:52
# @Description   :
from typing import Optional, List

from fastapi import HTTPException, status

from stardew.models.system import SysRole
from stardew.repository.system import RoleRepository
from stardew.services.system.role import RoleService
from stardew.schemas.system import RoleCreateSchema, RoleUpdateSchema


class RoleServiceImpl(RoleService):

    def __init__(self, repository: RoleRepository):
        self.repository = repository

    def get_role_list(self, page_no: Optional[int] = 0, page_size: Optional[int] = 100) -> List[SysRole]:
        return self.repository.get_multi(page_no=page_no, page_size=page_size)

    def get_roles_by_ids(self, identities: List[str]) -> List[SysRole]:
        return self.repository.get_by_ids(identities=identities)

    def get_role(self, role_id: str) -> SysRole:
        role: Optional[SysRole] = self.repository.get_by_id(identity=role_id)
        if role is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="未找到相关角色")
        return role

    def add_role(self, create_schema: RoleCreateSchema) -> None:
        return self.repository.add(create_schema=create_schema)

    def update_role(self, role: SysRole, update_schema: RoleUpdateSchema) -> None:
        self.repository.update(role=role, update_schema=update_schema)

    def delete_role(self, identity: str) -> None:
        return self.repository.delete(identity=identity)
