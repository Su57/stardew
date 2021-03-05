# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 2021/2/1 14:39
# @Description   : 数据库增删改查
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Type, TypeVar, Union, Callable, AsyncContextManager, ContextManager

from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.engine.result import Result
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql import select, Select, insert, Insert, delete, Delete, update, Update, text, Executable

from stardew.core.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class AbstractCRUDService(ABC):
    __slots__ = ("Model", "session_factory")

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
        :param model: 需要跟新的对象
        :param update_schema: 更新所需schema
        :return: 更新后的对象
        """

    @abstractmethod
    def add(self, *, create_schema: CreateSchemaType) -> None:
        """
        创建对象
        :param create_schema: 创建对象所提供的数据(schema)
        :return: 创建的对象
        """

    @abstractmethod
    def delete_by_id(self, *, identity: str) -> None:
        """
        通过id进行删除操作
        :param identity: 对象id
        :return:
        """


class CRUDService(AbstractCRUDService):
    """ CRUD逻辑(同步) """

    def __init__(
            self,
            *,
            model_class: Type[ModelType],
            session_factory: Callable[..., ContextManager[Session]]
    ) -> None:
        self.Model = model_class
        self.session_factory = session_factory

    def filter(self, *, where_clause: Dict) -> List[ModelType]:
        with self.session_factory() as session:
            clauses: List = []
            for k, v in where_clause.items():
                clauses.append(f"{k} = '{v}'")
            stmt: str = " AND ".join(clauses)
            return session.query(self.Model).filter(text(stmt)).all()

    def get_by_id(self, *, identity: Any) -> Optional[ModelType]:
        with self.session_factory() as session:
            return session.query(self.Model).filter(self.Model.id == identity).first()

    def get_multi(self, *, page_no: int = 0, page_size: int = 100) -> List[ModelType]:
        offset: int = page_no * page_size
        with self.session_factory() as session:
            return session.query(self.Model).offset(offset).limit(page_size).all()

    def add(self, *, create_schema: Union[CreateSchemaType, Dict[str, Any]]) -> None:
        with self.session_factory() as session:
            if isinstance(create_schema, dict):
                input_data = create_schema
            else:
                input_data = create_schema.dict(exclude_unset=True)
            model = self.Model(**input_data)
            session.add(model)
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
            # stmt: Update = update(self.Model).where(self.Model.id == identity).values(**update_data)
            session.add(model)
            session.commit()
            session.refresh(model)
            return model

    def delete_by_id(self, *, identity: str) -> None:
        with self.session_factory() as session:
            obj = session.query(self.Model).get(ident=identity)
            session.delete(obj)
            session.commit()


class AsyncCRUDService(AbstractCRUDService):
    """ CRUD逻辑(异步) """

    def __init__(
            self,
            *,
            model_class: Type[ModelType],
            session_factory: Callable[..., AsyncContextManager[AsyncSession]]
    ) -> None:
        self.Model = model_class
        self.session_factory = session_factory

    async def get_by_id(self, *, identify: Any) -> Optional[ModelType]:
        async with self.session_factory() as session:
            return await session.get(entity=self.Model, ident=identify)

    async def filter(self, *, where_clause: Dict) -> List[ModelType]:
        async with self.session_factory() as session:
            clauses_stmt: List = []
            for k, v in where_clause.items():
                clauses_stmt.append(f"{k} = '{v}'")
            where_stmt: str = " AND ".join(clauses_stmt)
            stmt: Select = select(self.Model).where(text(where_stmt))
            result: Result = session.execute(stmt)
            return [x[0] for x in result.fetchall()]

    async def get_multi(self, *, page_no: int = 0, page_size: int = 100) -> List[ModelType]:
        async with self.session_factory() as session:
            offset: int = page_no * page_size
            stmt: Select = select(self.Model).offset(offset).limit(page_size)
            result: Result = await session.execute(stmt)
            # ORM模式下的select，其返回结果与Core模式不同
            # 具体信息，参考 https://docs.sqlalchemy.org/en/14/tutorial/data.html#selecting-orm-entities-and-columns
            return [x[0] for x in result.fetchall()]

    async def update(self, *, identity: Any, update_schema: Union[UpdateSchemaType, Dict[str, Any]]) -> None:
        async with self.session_factory() as session:
            update_data: Dict = update_schema if isinstance(update_schema, dict) else update_schema.dict(
                exclude_unset=True)
            stmt: Update = update(self.Model).where(self.Model.id == identity).values(**update_data)
            await session.execute(stmt)
            await session.commit()

    async def add(self, *, create_schema: CreateSchemaType) -> None:
        async with self.session_factory() as session:
            obj_in_data = jsonable_encoder(create_schema)
            stmt: Insert = insert(self.Model).values(**obj_in_data)
            await session.execute(stmt)
            await session.commit()

    async def delete_by_id(self, *, identity: Any) -> None:
        async with self.session_factory() as session:
            stmt: Delete = delete(self.Model).where(self.Model.id == identity)
            await session.execute(stmt)
            await session.commit()
