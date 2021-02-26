# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 2021/2/1 14:59
# @Description   :
from typing import Optional, Set

from pydantic import EmailStr, Field
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from stardew.models.system import SysUser, SysRole
from stardew.common.enums import GenderEnum, StatusEnum
from stardew.schemas.base import SerializationConfig, BaseValidationSchema

UserSimpleSchema = sqlalchemy_to_pydantic(
    db_model=SysUser,
    config=SerializationConfig,
    exclude={"id", "password", "del_flag"},
)

RoleSimpleSchema = sqlalchemy_to_pydantic(
    db_model=SysRole,
    config=SerializationConfig,
    exclude={'id', 'del_flag'}
)


class UserSchema(UserSimpleSchema):
    roles: Set[str] = {}
    perms: Set[str] = {}


class RoleSchema(RoleSimpleSchema):
    perms: Set[str] = {}


class UserValidationSchema(BaseValidationSchema):
    username: str = Field(..., max_length=50, min_length=6, description="用户名")
    nickname: Optional[str] = Field(None, max_length=50, min_length=6, description="昵称")
    email: EmailStr = Field(..., description="用户邮箱")
    mobile: Optional[str] = Field("", description="用户手机号码")
    gender: Optional[GenderEnum] = Field(GenderEnum.unknown, description="性别 0:未知 1:男 2:女")
    avatar: Optional[str] = Field("", max_length=150, description="头像")


class UserCreationSchema(UserValidationSchema):
    """ 创建用户schema """
    password: str = Field(..., min_length=6, max_length=20, description="密码")


class UserUpdateSchema(UserValidationSchema):
    """ 更新用户schema """
    status: Optional[int] = Field(None, description="账号状态")
    remark: Optional[str] = Field(None, max_length=100, description="账号备注")


class RoleCreationSchema(BaseValidationSchema):
    """ 创建角色schema """
    name: str = Field(..., max_length=50, description="角色名称")
    key: str = Field(..., max_length=50, comment="角色权限字符串")
    status: Optional[StatusEnum] = Field(default=StatusEnum.enable, description="角色状态，0正常，1停用")


class RoleUpdateSchema(BaseValidationSchema):
    name: Optional[str] = Field(None, max_length=50, description="角色名称")
    key: Optional[str] = Field(None, max_length=50, description="角色权限字符串")
    status: Optional[StatusEnum] = Field(None, description="角色状态，0正常，1停用")
