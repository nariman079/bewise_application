import asyncio
from typing import Callable, Awaitable, Annotated
from contextlib import asynccontextmanager


from fastapi import FastAPI, Request, Response, Body, status, Query

from src.conf.database import session_context, Base
from src.conf.settings import async_session, DEBUG, engine
from src.conf.producer import send_message, producer
from src.models import Application
from src.schemas import ApplicationCreateSchema, ApplicationDisplaySchema


@asynccontextmanager
async def lifespan(_: FastAPI):
    """ЖЦ приложения"""
    if DEBUG:
        # reinit database
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    for attempt in range(5):
        try:
            await producer.start()
            break
        except Exception as e:
            print(f"Ошибка при запуске продюсера: {e}")
            await asyncio.sleep(3)
    yield
    try:
        await producer.close()
    except AttributeError:
        pass


app = FastAPI(lifespan=lifespan)


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


@app.post("/api/applications/", status_code=status.HTTP_201_CREATED)
async def create_application(
    application: Annotated[ApplicationCreateSchema, Body(embed=False)],
):
    """Создание заявки"""
    try:
        new_application = await Application.create(**application.model_dump())
        result = {"id": new_application.id, 'create_at':str(new_application.created_at), **application.model_dump()}
        await send_message("applications", result)
    except:
        await send_message("logs", {
            'level': "ERROR",
            'messge': "Ошибка при создании заявки",
            'data': application
        })
    return {
        "message": "Заявка создана",
        "data": result,
    }


@app.get("/api/applications")
async def get_applications(
    user_name: str | None = Query(None, description="Фильтр по имени пользователя"),
    page: int = Query(1, ge=1, description="Номер страницы"),
    size: int = Query(10, ge=1, le=100, description="Количество элементов на странице"),
):
    """Получение заявок"""
    filter_by_user_name = {"user_name": user_name} if user_name else {}
    applications = await Application.find_all_by_kwargs(**filter_by_user_name)

    offset = (page - 1) * size
    limit = size

    return {
        "message": "Заявки получены",
        "data": [
            ApplicationDisplaySchema(
                id=application.id,
                user_name=application.user_name,
                description=application.description,
            )
            for application in applications[offset:limit]
        ],
    }
