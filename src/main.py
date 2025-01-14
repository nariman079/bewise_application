import asyncio
from typing import Callable, Awaitable
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response

from src.conf.database import session_context
from src.conf.settings import async_session, DEBUG
from src.conf.producer import send_message, producer


@asynccontextmanager
async def lifespan():
    """ЖЦ приложения""" 
    if DEBUG:
        # reinit database
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    """Событие при старте приложении"""
    try:
        await producer.start()
    except Exception as e:
        print(f"Ошибка при запуске продюсера: {e}")

        # Попытка переподключения
        await asyncio.sleep(5)
        await startup_event()


@app.on_event("shutdown")
async def shotdown_event():
    """Событие при завершении приложения"""
    await producer.close()


@app.middleware("http")
async def database_session_context_middleware(
    request: Request, call_next: Awaitable[Callable]
) -> Response:
    """Установка сессии в контекстную переменную"""
    async with async_session.begin() as session:
        session_context.set(session)
        return await call_next(request)


@app.get("/")
async def main():
    await send_message("test", b"test message")
    return {"message": "testKafka"}


@app.get('/api/applications')
async def get_applications():
    pass