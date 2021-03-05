# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 2021/2/25 11:46
# @Description   :
from dependency_injector import containers, providers

from stardew.repository.system import UserRepository, RoleRepository
from stardew.settings import settings
from stardew.core.db.base import Database
from stardew.core.redis import init_redis_pool
from stardew.services.common.impl import LoginServiceImpl
from stardew.models.system import SysUser, SysRole, SysMenu
from stardew.core.db.crud import CRUDService, AsyncCRUDService
from stardew.services.system.impl import (
    UserServiceImpl, RoleServiceImpl, MenuServiceImpl
)


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

    user_repository = providers.Factory(
        UserRepository,
        session_factory=db.provided.session,
    )

    role_repository = providers.Factory(
        RoleRepository,
        session_factory=db.provided.session,
    )

    user_service = providers.Factory(
        UserServiceImpl,
        repository=user_repository
    )

    role_service = providers.Factory(
        RoleServiceImpl,
        repository=role_repository
    )

    menu_service = providers.Factory(
        MenuServiceImpl,
        crud=providers.Factory(
            CRUDService,
            model_class=SysMenu,
            session_factory=db.provided.session
        )
    )
