# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 2021/2/25 11:46
# @Description   :
from dependency_injector import containers, providers

from stardew.settings import settings
from stardew.core.db.base import Database
from stardew.models.system import SysUser
from stardew.core.redis import init_redis_pool
from stardew.services.common.impl import LoginServiceImpl
from stardew.core.db.crud import CRUDService, AsyncCRUDService
from stardew.services.system.impl import UserServiceImpl, AsyncUserServiceImpl


class IocContainer(containers.DeclarativeContainer):
    """
    IOC容器。
    关于IOC， 参考 https://docs.spring.io/spring-framework/docs/current/reference/html/core.html#beans
    主要作用就是进行依赖注入。
    """
    db = providers.Singleton(
        Database,
        dsn=settings.SQLALCHEMY_DATABASE_URI
    )

    redis_pool = providers.Resource(
        init_redis_pool,
        redis_dsn=settings.REDIS_DSN
    )

    login_service = providers.Factory(
        LoginServiceImpl,
        crud=providers.Factory(
            CRUDService,
            model_class=SysUser,
            session_factory=db.provided.session
        ),
        redis=redis_pool
    )

    user_service = providers.Factory(
        UserServiceImpl,
        crud=providers.Factory(
            CRUDService,
            model_class=SysUser,
            session_factory=db.provided.session
        ),
    )

    async_user_service = providers.Factory(
        AsyncUserServiceImpl,
        crud=providers.Factory(
            AsyncCRUDService,
            model_class=SysUser,
            session_factory=db.provided.async_session
        ),
    )

