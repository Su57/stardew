# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 2021/3/3 10:46
# @Description   :
from typing import Callable, ContextManager, Optional, List, Union, Dict, Any

from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from sqlalchemy.sql import select, Select, insert, Insert, delete, Delete, update, Update, text, Executable
from stardew.models.system import SysRole
from stardew.schemas.system import RoleCreateSchema, RoleUpdateSchema


class RoleRepository:

    def __init__(self, session_factory: Callable[..., ContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def get_multi(self, page_no: Optional[int] = 0, page_size: Optional[int] = 100) -> List[SysRole]:
        """
        查询role列表
        :param page_no: 页码
        :param page_size: 每页数据
        :return: 分页后的数据
        """
        offset: int = page_no * page_size
        with self.session_factory() as session:
            return session.query(SysRole).offset(offset).limit(page_size).all()

    def get_by_ids(self, identities: List[str]) -> List[SysRole]:
        """
        通过id列表查询对应的角色列表
        :param identities: id列表
        :return: 角色列表
        """
        with self.session_factory() as session:
            stmt: Select = select(SysRole).where(SysRole.id.in_(identities))
            res = session.execute(stmt).fetchall()
            return [i[0] for i in res]

    def get_by_id(self, identity: str) -> Optional[SysRole]:
        """
        通过id查询role
        :param identity: role id
        :return: 对应的role
        """
        with self.session_factory() as session:
            return session.get(SysRole, ident=identity)

    def add(self, create_schema: Union[RoleCreateSchema, Dict[str, Any]]) -> None:
        """
        创建user
        :param create_schema: 创建用户所需的数据
        :return:
        """
        with self.session_factory() as session:
            input_data: Dict
            if isinstance(create_schema, dict):
                input_data = create_schema
            else:
                input_data = create_schema.dict(exclude_unset=True)
            user = SysRole(**input_data)
            session.add(user)
            session.commit()

    def update(self, role: SysRole, update_schema: Union[RoleUpdateSchema, Dict[str, Any]]) -> SysRole:
        """
        更新role
        :param role: 待更新的role对象
        :param update_schema: 更新所需的数据
        :return: 更新后的role
        """
        with self.session_factory() as session:
            original_data = jsonable_encoder(role)
            if isinstance(update_schema, dict):
                update_data = update_schema
            else:
                update_data = update_schema.dict(exclude_unset=True)

            for field in original_data:
                if field in update_data:
                    setattr(role, field, update_data[field])
            # stmt: Update = update(self.Model).where(self.Model.id == identity).values(**update_data)
            session.add(role)
            session.commit()
            session.refresh(role)
            return role

    def delete(self, identity: str) -> None:
        """
        通过id删除角色
        :param identity: 待删除角色的id
        :return:
        """
        with self.session_factory() as session:
            stmt: Delete = delete(SysRole).where(SysRole.id == identity)
            session.execute(text(stmt))
            session.commit()