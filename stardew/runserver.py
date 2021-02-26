# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 2021/2/1 10:32
# @Description   :
from stardew.app import create_app

app = create_app()

if __name__ == '__main__':
	import uvicorn

	uvicorn.run(app)
