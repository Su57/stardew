# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 2021/2/1 11:54
# @Description   :
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Table, String, Boolean, Integer, SmallInteger, ForeignKey

from stardew.core.db.base import Base
from stardew.common.utils import StringUtil
from stardew.common.enums import StatusEnum, GenderEnum


# 用户-角色关系表
user_role: Table = Table(
	"sys_user_role",
	Base.metadata,
	Column("user_id", String(32), ForeignKey('sys_user.id'), primary_key=True),
	Column("role_id", String(32), ForeignKey('sys_role.id'), primary_key=True)
)

# 角色-权限关系表
role_menu: Table = Table(
	"sys_role_menu",
	Base.metadata,
	Column("role_id", String(32), ForeignKey('sys_role.id'), primary_key=True),
	Column("menu_id", String(32), ForeignKey('sys_menu.id'), primary_key=True)
)


class SysUser(Base):

	__tablename__ = "sys_user"

	id = Column(String(32), default=StringUtil.get_unique_key, index=True, primary_key=True, comment="用户表主键")
	username = Column(String(50), nullable=False, comment="用户名")
	nickname = Column(String(50), comment="昵称")
	email = Column(String(120), unique=True, nullable=False, index=True, comment="邮箱")
	mobile = Column(String(11), comment="手机号")
	gender = Column(SmallInteger, default=GenderEnum.unknown.value, comment="性别， 0：男， 1：女")
	avatar = Column(String(150), comment="头像URI")
	password = Column(String(64), comment="密码")
	status = Column(SmallInteger, default=StatusEnum.enable.value, comment="用户状态，0正常 1禁用或停用")
	is_super = Column(Boolean, default=False, nullable=False, comment="是否为超级管理员")
	remark = Column(String(50), nullable=True, comment="备注")
	del_flag = Column(Boolean, default=False, comment="是否删除,0：未删除， 1：已删除")

	roles = relationship('SysRole', secondary=user_role, backref=backref("users", lazy=True), lazy="subquery")

	def __str__(self):
		return f"SysUser <username :{self.username}, status: {self.status}>"


class SysRole(Base):
	""" 系统角色 """
	__tablename__ = "sys_role"

	id = Column(String(32), default=StringUtil.get_unique_key, index=True, primary_key=True, comment="主键")
	name = Column(String(50), nullable=False, comment="角色名称")
	key = Column(String(50), nullable=False, comment="角色权限字符串")
	status = Column(SmallInteger, default=StatusEnum.enable.value, comment="角色状态，0正常，1停用")
	del_flag = Column(Boolean, default=False, comment="删除标志（0:存在 1:删除）")

	# 定义多对多关系
	perms = relationship('SysMenu', secondary=role_menu, backref=backref("roles", lazy=True), lazy="subquery")

	def __str__(self) -> str:
		return f"SysRole <name: {self.name}, key: {self.key}>"


class SysMenu(Base):
	""" 菜单 / 权限 """
	__tablename__ = "sys_menu"

	id = Column(String(32), default=StringUtil.get_unique_key, index=True, primary_key=True, comment="主键")
	name = Column(String(50), nullable=False, comment="菜单/按钮 名称")
	parent_id = Column(String(32), ForeignKey('sys_menu.id', ondelete='CASCADE'), comment='父菜单id')
	order_num = Column(Integer, default=0, autoincrement=True, nullable=False, comment="显示顺序")
	path = Column(String(256), nullable=False, comment="对应路由地址")
	menu_type = Column(String(1), nullable=False, default="F", comment="类型 (M目录 C菜单 F按钮)")
	visible = Column(Boolean, default=True, nullable=False, comment="是否显示")
	status = Column(SmallInteger, default=StatusEnum.enable.value, comment="菜单状态（0正常 1停用）")
	perm = Column(String(100), default="", nullable=False, comment="对应的权限名")
	icon = Column(String(256), default="", nullable=False, comment="图标")
	# 自引用
	parent = relationship('SysMenu', backref='children', remote_side=[id])

	def __str__(self) -> str:
		return f"SysMenu <name: {self.name}, url: {self.path}>"
