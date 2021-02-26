# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 2021/2/1 14:39
# @Description   : 数据库增删改查
from abc import ABC, abstractmethod
from typing import (
    Any, Dict, Generic, List, Optional, Type, TypeVar,
    Union, NoReturn, Callable, AsyncContextManager, ContextManager
)

from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.engine.result import Result
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql import select, insert, delete, update, Executable, text

from stardew.core.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class AbstractCURDService(ABC):

    @abstractmethod
    def set_model_class(self, model_class: Type[ModelType]) -> NoReturn:
        """
        设定查询的db Model
        :param model_class: 数据库Model类
        :return:
        """

    @abstractmethod
    def filter(self, *, where_clause: Dict) -> List[ModelType]:
        """
        自定义过滤条件
        :param where_clause: 过滤条件
        :return: 符合条件的对象列表
        """

    @abstractmethod
    def get_by_id(self, *, identify: Any) -> Optional[ModelType]:
        """
        通过id进行查询
        :param identify: 对象id
        :return:
        """

    @abstractmethod
    def get_multi(self, *, page_no: int = 0, page_size: int = 100) -> List[ModelType]:
        """
        获取分页数据
        :param page_no: 页码
        :param page_size: 每页条目
        :return:
        """

    @abstractmethod
    def update(self, *, model: ModelType, update_schema: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        """
        更新条目
        :param model: 待更新的对象实例
        :param update_schema: 更新所需schema
        :return: 更新后的对象
        """

    @abstractmethod
    def add(self, *, create_schema: CreateSchemaType) -> NoReturn:
        """
        创建对象
        :param create_schema: 创建对象所提供的数据(schema)
        :return: 创建的对象
        """

    @abstractmethod
    def delete_by_id(self, *, identity: str) -> NoReturn:
        """
        通过id进行删除操作
        :param identity: 对象id
        :return:
        """


class CURDService(Generic[ModelType, CreateSchemaType, UpdateSchemaType], AbstractCURDService):
    """ CURD逻辑(同步) """

    __slots__ = ("Model", "session_factory")

    def __init__(
            self,
            *,
            session_factory: Callable[..., ContextManager[Session]],
            model_class: Optional[Type[ModelType]] = None
    ) -> None:
        self.Model = model_class
        self.session_factory = session_factory

    def set_model_class(self, model_class: Type[ModelType]) -> NoReturn:
        self.Model = model_class

    def filter(self, *, where_clause: Dict) -> List[ModelType]:
        with self.session_factory() as session:
            clauses: List = []
            for k, v in where_clause.items():
                clauses.append(f"{k} = '{v}'")
            stmt: str = " AND ".join(clauses)
            return session.query(self.Model).filter(text(stmt)).all()

    def get_by_id(self, *, identify: Any) -> Optional[ModelType]:
        with self.session_factory() as session:
            return session.query(self.Model).filter(self.Model.id == identify).first()

    def get_multi(self, *, page_no: int = 0, page_size: int = 100) -> List[ModelType]:
        offset: int = page_no * page_size
        with self.session_factory() as session:
            return session.query(self.Model).offset(offset).limit(page_size).all()

    def add(self, *, create_schema: CreateSchemaType) -> NoReturn:
        with self.session_factory() as session:
            input_data = jsonable_encoder(create_schema)
            user = self.Model(**input_data)
            session.add(user)
            session.commit()

    def update(self, *, model: ModelType, update_schema: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        with self.session_factory() as session:
            original_data = jsonable_encoder(model)
            if isinstance(update_schema, dict):
                update_data = update_schema
            else:
                update_data = update_schema.dict(exclude_unset=True)
            for field in original_data:
                if field in update_data:
                    setattr(model, field, update_data[field])
            session.add(model)
            session.commit()
            session.refresh(model)
            return model

    def delete_by_id(self, *, identity: str) -> NoReturn:

        with self.session_factory() as session:
            obj = session.query(self.Model).get(identify=identity)
            session.delete(obj)
            session.commit()


class AsyncCURDService(Generic[ModelType, CreateSchemaType, UpdateSchemaType], AbstractCURDService):
    """ CURD逻辑(异步) 未测试 """

    __slots__ = ("Model", "session_factory")

    def __init__(
            self,
            *,
            session_factory: Callable[..., AsyncContextManager[AsyncSession]],
            model_class: Optional[Type[ModelType]] = None
    ) -> None:
        self.Model = model_class
        self.session_factory = session_factory

    def set_model_class(self, model_class: Type[ModelType]) -> NoReturn:
        self.Model = model_class

    async def get_by_id(self, *, identify: Any) -> Optional[ModelType]:
        async with self.session_factory() as session:
            stmt: Executable = select(self.Model).where(self.Model.id == identify)
            return await session.scalar(stmt)

    async def filter(self, *, where_clause: Dict) -> List[ModelType]:
        """
        自定义过滤条件
        :param where_clause: 过滤条件
        :return: 符合条件的对象列表
        """
        async with self.session_factory() as session:
            clauses: List = []
            for k, v in where_clause.items():
                clauses.append(f"{k} = '{v}'")
            where_stmt: str = " AND ".join(clauses)
            stmt: Executable = select(self.Model).where(text(where_stmt))
            result: Result = session.execute(stmt)
            return [x[0] for x in result.fetchall()]

    async def get_multi(self, *, page_no: int = 0, page_size: int = 100) -> List[ModelType]:
        async with self.session_factory() as session:
            offset: int = page_no * page_size
            stmt: Executable = select(self.Model).offset(offset).limit(page_size)
            result: Result = await session.execute(stmt)
            # ORM模式下的select，其返回结果与Core模式不同
            # 具体信息，参考 https://docs.sqlalchemy.org/en/14/tutorial/data.html#selecting-orm-entities-and-columns
            return [x[0] for x in result.fetchall()]

    async def update(self, *, model: ModelType, update_schema: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        async with self.session_factory() as session:
            update_data = update_schema if isinstance(update_schema, dict) else update_schema.dict(exclude_unset=True)
            stmt: Executable = update(model).where(self.Model.id == model.id).values(**update_data)
            await session.execute(stmt)
            await session.refresh(model)
            return model

    async def add(self, *, create_schema: CreateSchemaType) -> NoReturn:
        async with self.session_factory() as session:
            obj_in_data = jsonable_encoder(create_schema)
            stmt: Executable = insert(self.Model).values(**obj_in_data)
            await session.execute(stmt)
            await session.commit()

    async def delete_by_id(self, *, identity: Any) -> NoReturn:
        async with self.session_factory() as session:
            stmt: Executable = delete(self.Model).where(self.Model.id == identity)
            await session.execute(stmt)
            await session.commit()
