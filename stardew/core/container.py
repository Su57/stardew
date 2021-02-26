# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 2021/2/25 11:46
# @Description   :
from dependency_injector import containers, providers

from stardew.settings import settings
from stardew.core.db.base import Database
from stardew.core.deps.redis import init_redis_pool
from stardew.services.common.impl import LoginServiceImpl
from stardew.core.db.crud import CURDService, AsyncCURDService
from stardew.services.system.impl import UserServiceImpl, AsyncUserServiceImpl


class IocContainer(containers.DeclarativeContainer):
    db = providers.Singleton(
        Database,
        dsn=settings.SQLALCHEMY_DATABASE_URI
    )

    redis_pool = providers.Resource(
        init_redis_pool,
        redis_dsn=settings.REDIS_DSN
    )

    curd = providers.Factory(
        CURDService,
        session_factory=db.provided.session
    )

    async_curd = providers.Factory(
        AsyncCURDService,
        session_factory=db.provided.async_session
    )

    login_service = providers.Factory(
        LoginServiceImpl,
        curd=curd,
        redis=redis_pool
    )

    user_service = providers.Factory(
        UserServiceImpl,
        curd=curd
    )

    async_user_service = providers.Factory(
        AsyncUserServiceImpl,
        curd=async_curd
    )

