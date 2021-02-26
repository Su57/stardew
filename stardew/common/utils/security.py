# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 2021/1/29 16:21
# @Description   :
from typing import Union, Any, Dict
from datetime import timedelta, datetime

from jose.constants import ALGORITHMS
from passlib.context import CryptContext
from fastapi import HTTPException, status
from jose import jwt, ExpiredSignatureError, JWTError

from stardew.settings import settings


class SecurityUtil:

	""" 安全相关的功能集合 """

	_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

	@staticmethod
	def create_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
		"""
		签发token
		:param subject: token信息
		:param expires_delta: 过期时间
		:return:
		"""
		if expires_delta:
			expire = datetime.utcnow() + expires_delta
		else:
			expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRED_MINUTES)
		payload = {"exp": expire, "sub": str(subject)}
		token = jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHMS.HS256)
		return token

	@staticmethod
	def parse_token(token: str) -> Dict:
		"""
		解析token,获取token携带的信息
		:param token: 待解析的token
		:return: 解析后的信息
		"""
		try:
			return jwt.decode(token, key=settings.SECRET_KEY, algorithms=[ALGORITHMS.HS256])
		# 令牌过期
		except ExpiredSignatureError:
			raise HTTPException(status.HTTP_401_UNAUTHORIZED, "登录信息已过期，请重新登录")
		# 无效令牌
		except JWTError:
			raise HTTPException(status.HTTP_401_UNAUTHORIZED, "无效的身份信息，请重新登录")

	@classmethod
	def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
		""" 校验密码 """
		return cls._pwd_context.verify(plain_password, hashed_password)

	@classmethod
	def generate_password(cls, password: str) -> str:
		""" 生成哈希密码 """
		return cls._pwd_context.hash(password)
