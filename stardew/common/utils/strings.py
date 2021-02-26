# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 2021/2/4 15:29
# @Description   :
import re
from uuid import uuid4, UUID


class StringUtil:

	@staticmethod
	def get_unique_key() -> str:
		""" 获取全局唯一key(去除中划线) """
		unique_key: UUID = uuid4()
		return unique_key.hex

	@staticmethod
	def remove_blank(raw_string: str) -> str:
		""" 去除字符串中的空白符 """
		return re.sub(r"\s", "", raw_string)
