# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 2021/1/29 10:33
# @Description   :
from fastapi import FastAPI

from stardew import api
from stardew.core import deps
from stardew.core.container import IocContainer


def create_app() -> FastAPI:
    """ 实例化fastapi app """
    app = FastAPI()
    # 装配路由
    app.include_router(api.api)
    # 初始化IOC容器。参考 https://python-dependency-injector.ets-labs.org/wiring.html#wiring
    container = IocContainer()
    container.wire(packages=[
        api,
        deps
    ])

    return app
