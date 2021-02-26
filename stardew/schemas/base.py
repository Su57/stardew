# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 2021/2/1 11:02
# @Description   :

import orjson
from pydantic import BaseConfig, BaseModel, Extra


def orjson_dumps(v, *, default):
	return orjson.dumps(v, default=default).decode()


class SerializationConfig(BaseConfig):
	""" 用于进行序列化的schema """
	orm_mode = True
	json_loads = orjson.loads
	json_dumps = orjson_dumps
	use_enum_values = True


class BaseValidationSchema(BaseModel):
	class Config:
		extra = Extra.ignore
		# 直接使用enum的value
		use_enum_values = True
		# 去除str和byte的首位空白符
		anystr_strip_whitespace = True
