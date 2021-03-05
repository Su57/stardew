# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 2021/1/29 10:33
# @Description   :
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from stardew import api
from stardew.core import deps
from stardew.core.container import IocContainer


def create_app() -> FastAPI:
    """ 实例化fastapi app """
    app = FastAPI(title="STARDEW")
    # 装配路由
    app.include_router(api.api)
    # 初始化IOC容器。参考 https://python-dependency-injector.ets-labs.org/wiring.html#wiring
    container = IocContainer()
    container.wire(packages=[
        api,
        deps
    ])

    custom_openapi(app)

    return app


def custom_openapi(app: FastAPI):
    if not app.openapi_schema:
        openapi_schema = get_openapi(
            title="STARDEW API DOCS",
            version="0.1.0",
            description="This is a very custom OpenAPI schema",
            routes=app.routes,
        )
        openapi_schema["info"]["x-logo"] = {
            "url": "https://img.3dmgame.com/uploads/allimg/170506/316-1F506161K9.png"
        }
        app.openapi_schema = openapi_schema
