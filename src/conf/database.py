from __future__ import annotations

from collections.abc import Sequence
from contextvars import ContextVar
from typing import Any, Self

from sqlalchemy import MetaData, Row, Select, func, select
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession
from sqlalchemy.orm import DeclarativeBase

session_context: ContextVar[AsyncSession | None] = ContextVar("session", default=None)

class DBController:
    @property
    def session(self) -> AsyncSession:
        """Получение сессии из контекстных переменных"""
        session = session_context.get()
        if session is None:
            raise ValueError("Сессия не запущена")
        return session

    async def get_all(self, stmt: Select[Any]) -> Sequence[Any]:
        """Получение всех объектов"""
        return (await self.session.execute(stmt)).scalars().all()

    async def get_paginated(
        self, stmt: Select[Any], offset: int, limit: int
    ) -> Sequence[Any]:
        return await self.get_all(stmt.offset(offset).limit(limit))

db: DBController = DBController()

class MappingBase:
    @classmethod
    def select_by_kwargs(cls, *order_by: Any, **kwargs: Any) -> Select[tuple[Self]]:
        if len(order_by) == 0:
            return select(cls).filter_by(**kwargs)
        return select(cls).filter_by(**kwargs).order_by(*order_by)

    @classmethod
    async def find_paginated_by_kwargs(
        cls, offset: int, limit: int, *order_by: Any, **kwargs: Any
    ) -> Sequence[Self]:
        return await db.get_paginated(
            cls.select_by_kwargs(*order_by, **kwargs), offset, limit
        )

    async def update(self, **kwargs: Any) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)
        await db.session.flush()

    async def delete(self):
        await db.session.delete(self)
        await db.session.flush()

convention = {
    "ix": "ix_%(column_0_label)s",  
    "uq": "uq_%(table_name)s_%(column_0_name)s", 
    "ck": "ck_%(table_name)s_%(constraint_name)s", 
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",  # noqa: WPS323
    "pk": "pk_%(table_name)s", 
}

db_meta = MetaData(naming_convention=convention)


class Base(DeclarativeBase, DBController, MappingBase):
    __tablename__: str
    __abstract__: bool

    metadata = db_meta