# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 2021/2/4 15:56
# @Description   :
from datetime import datetime
from typing import Optional, List, Any, Set

from pydantic import BaseModel, Field
from stardew.schemas.system import UserSimpleSchema


class LoginUser(BaseModel):
	""" 登录后的用户信息，即之后后台使用的用户信息 """

	# 最后登录时间
	login_time: datetime = datetime.utcnow()

	# 数据库中的用户信息
	sys_user: UserSimpleSchema

	# 该用户所有可用的按钮树结构
	perms: Set[str]

	roles: Set[str]


class TreeNode(BaseModel):
	""" 前端树结构 """
	# 节点id
	id: int
	# 节点标签
	label: str = Field(alias="name")
	# 子节点
	children: List['TreeNode'] = []

	class Config:
		orm_mode = True


class BearerToken(BaseModel):
	access_token: str
	token_type: str


class TokenPayload(BaseModel):
	sub: Optional[Any] = None


class CaptchaInfo(BaseModel):
	uid: str
	image: str


TreeNode.update_forward_refs()
