# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 2021/2/1 10:26
# @Description   :
from string import ascii_letters, digits


class Constant:
	UTF8 = "utf-8"
	LOGIN_REDIS_KEY = "login_key: "
	CAPTCHA_REDIS_KEY = "captcha_key: "
	HTTP_PROTOCOL = "http://"
	HTTPS_PROTOCOL = "https://"
	CAPTCHA_LETTERS = ascii_letters + digits

	SUPER_PERMISSION = "{*:*:*}"
