# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 2021/2/1 11:02
# @Description   :
from pydantic import Field, EmailStr

from .base import BaseValidationSchema


class LoginSchema(BaseValidationSchema):
	""" 登录 """
	email: EmailStr = Field(..., description="邮箱")
	password: str = Field(..., description="密码")
	uid: str = Field(..., description="验证码uid")
	code: str = Field(..., description="验证码")
