# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 2021/2/1 11:55
# @Description   :
from contextlib import contextmanager, asynccontextmanager
from typing import Callable, ContextManager, AsyncContextManager, Any

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import scoped_session, Session
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine

from stardew.common.utils import logger


@as_declarative()
class Base:
    """ 所有的orm模型都需要一个id作为主键 """
    id: Any


class Database:
    """
    数据库会话支持
    """

    def __init__(self, dsn: str) -> None:
        """
        初始化数据库
        :param dsn: 连接URI。参考 https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls
        """
        self._engine: Engine = create_engine(dsn, future=True, echo=True)
        self._async_engine: AsyncEngine = create_async_engine(dsn, future=True, echo=True)
        self._session_factory = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )
        self._async_session_factory = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                class_=AsyncSession,
                bind=self._async_engine,
            ),
        )

    @contextmanager
    def session(self) -> Callable[..., ContextManager[Session]]:
        """ sqlalchemy数据库会话上下文管理 """
        session: Session = self._session_factory()
        try:
            yield session
        except Exception:
            logger.exception('Session rollback because of exception')
            session.rollback()
            raise
        finally:
            session.close()

    @asynccontextmanager
    async def async_session(self) -> Callable[..., AsyncContextManager[AsyncSession]]:
        """ sqlalchemy异步数据库会话上下文管理 # TODO typing annotation """
        async_session: AsyncSession = self._async_session_factory()
        try:
            yield async_session
        except Exception:
            logger.exception('Session rollback because of exception')
            await async_session.rollback()
            raise
        finally:
            await async_session.close()
