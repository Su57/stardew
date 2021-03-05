# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 2021/3/3 10:16
# @Description   :
from typing import Callable, ContextManager, Optional, List, Union, Dict, Any

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder

from stardew.models.system import SysUser, SysRole
from stardew.schemas.system import UserCreateSchema, UserUpdateSchema


class UserRepository:

    def __init__(self, session_factory: Callable[..., ContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def get_multi(self, page_no: Optional[int] = 0, page_size: Optional[int] = 100) -> List[SysUser]:
        """
        查询用户列表
        :param page_no: 页码
        :param page_size: 每页数据
        :return: 分页后的数据
        """
        offset: int = page_no * page_size
        with self.session_factory() as session:
            return session.query(SysUser).offset(offset).limit(page_size).all()

    def get_by_id(self, identity: str) -> Optional[SysUser]:
        with self.session_factory() as session:
            return session.get(SysUser, ident=identity)

    def get_by_email(self, email: str) -> Optional[SysUser]:
        """
        通过邮箱查找用户
        :param email: 用户邮箱
        :return:
        """
        with self.session_factory() as session:
            return session.query(SysUser).filter(SysUser.email == email).first()

    def add(self, create_schema: Union[UserCreateSchema, Dict[str, Any]]) -> None:
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

            user = SysUser(**input_data)

            # 处理角色信息 直接操作关联表
            role_ids: List[str] = input_data.pop("roles", None)
            if role_ids is not None:
                role_list: List[SysRole] = session.query(SysRole).where(SysRole.id.in_(role_ids)).all()
                user.roles = role_list
            session.add(user)
            session.commit()

    def update(self, identity: str, update_schema: Union[UserUpdateSchema, Dict[str, Any]]) -> SysUser:
        """
        更新user
        :param identity: 待更新的user对象的id
        :param update_schema: 更新所需的数据
        :return: 更新后的user
        """
        with self.session_factory() as session:
            user: SysUser = session.get(entity=SysUser, ident=identity)
            if user is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="未找到相关用户")
            original_data = jsonable_encoder(user)
            if isinstance(update_schema, dict):
                update_data = update_schema
            else:
                update_data = update_schema.dict(exclude_unset=True)

            # 处理角色信息
            role_ids: List[str] = update_data.pop("roles", None)
            if role_ids is not None:
                role_list: List[SysRole] = session.query(SysRole).where(SysRole.id.in_(role_ids)).all()
                user.roles = role_list

            for field in original_data:
                if field in update_data:
                    setattr(user, field, update_data[field])

            session.add(user)
            session.commit()
            session.refresh(user)
            return user

    def delete(self, identity: str) -> None:
        """
        通过删除用户
        :param identity: 待删除用户的id
        :return:
        """
        with self.session_factory() as session:
            user: SysUser = session.query(SysUser).get(ident=identity)
            session.delete(user)
            session.commit()
