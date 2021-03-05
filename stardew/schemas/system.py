# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 2021/2/1 14:59
# @Description   :
from typing import Optional, Set, List

from pydantic import EmailStr, Field
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from stardew.models.system import SysUser, SysRole, SysMenu
from stardew.common.enums import GenderEnum, StatusEnum, MenuTypeEnum
from stardew.schemas.base import SerializationConfig, BaseValidationSchema

UserSimpleSchema = sqlalchemy_to_pydantic(
    db_model=SysUser,
    config=SerializationConfig,
    exclude={"password", "del_flag"},
)

RoleSimpleSchema = sqlalchemy_to_pydantic(
    db_model=SysRole,
    config=SerializationConfig,
    exclude={'del_flag'}
)

MenuSimpleSchema = sqlalchemy_to_pydantic(
    db_model=SysMenu,
    config=SerializationConfig,
    exclude={'del_flag'}
)


class UserSchema(UserSimpleSchema):
    roles: Set[str] = {}
    perms: Set[str] = {}


class RoleSchema(RoleSimpleSchema):
    perms: Set[str] = {}


class MenuSchema(MenuSimpleSchema):
    children: List['MenuSchema']


class _UserValidationSchema(BaseValidationSchema):
    nickname: Optional[str] = Field(None, max_length=50, min_length=4, description="昵称")
    mobile: Optional[str] = Field("", description="用户手机号码")
    gender: Optional[GenderEnum] = Field(GenderEnum.unknown, description="性别 0:未知 1:男 2:女")
    avatar: Optional[str] = Field("", max_length=150, description="头像")
    roles: Optional[List[str]] = Field(None, description="角色id列表")


class UserCreateSchema(_UserValidationSchema):
    """ 创建用户schema """
    email: EmailStr = Field(..., description="用户邮箱")
    username: str = Field(..., max_length=50, min_length=4, description="用户名")
    password: str = Field(..., min_length=6, max_length=20, description="密码")


class UserUpdateSchema(_UserValidationSchema):
    """ 更新用户schema """
    username: Optional[str] = Field(None, max_length=50, min_length=4, description="用户名")
    status: Optional[int] = Field(None, description="账号状态")
    remark: Optional[str] = Field(None, max_length=100, description="账号备注")


class _RoleValidationSchema(BaseValidationSchema):
    status: Optional[StatusEnum] = Field(StatusEnum.enable, description="角色状态，0正常，1停用")
    perms: Optional[List[str]] = Field(None, description="菜单权限id列表")


class RoleCreateSchema(_RoleValidationSchema):
    """ 创建角色schema """
    name: str = Field(..., max_length=50, description="角色名称")
    key: str = Field(..., max_length=50, comment="角色权限字符串")


class RoleUpdateSchema(_RoleValidationSchema):
    name: Optional[str] = Field(None, max_length=50, description="角色名称")
    key: Optional[str] = Field(None, max_length=50, description="角色字符串")


class _MenuValidationSchema(BaseValidationSchema):
    status: Optional[StatusEnum] = Field(StatusEnum.enable, description="菜单状态（0正常 1停用）")
    icon: Optional[str] = Field(None, description="图标")
    is_frame: Optional[bool] = Field(False, description="是否为外链")
    menu_type: Optional[MenuTypeEnum] = Field(MenuTypeEnum.category, description="类型 (0目录 1菜单 2按钮)")


class MenuCreateSchema(_MenuValidationSchema):
    name: str = Field(..., description="菜单、按钮名称")
    parent_id: int = Field(..., ge=0, description=">=0，表示最高层级菜单")
    order_num: int = Field(..., description="显示顺序")
    path: str = Field(None, description="对应路由地址")
    component: str = Field(None, description="组件路径")
    visible: bool = Field(True, description="是否显示")
    perm: str = Field(..., min_length=3, max_length=100, description="对应的权限名")


class MenuUpdateSchema(_MenuValidationSchema):
    name: Optional[str] = Field(None, description="菜单、按钮名称")
    parent_id: Optional[int] = Field(None, ge=0, description=">=0，表示最高层级菜单")
    order_num: Optional[int] = Field(None, description="显示顺序")
    path: Optional[str] = Field(None, description="对应路由地址")
    component: Optional[str] = Field(None, description="组件路径")
    visible: Optional[bool] = Field(True, description="是否显示")
    perm: Optional[str] = Field(None, min_length=3, max_length=100, description="对应的权限名")


MenuSchema.update_forward_refs()
