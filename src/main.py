import asyncio
from typing import Callable, Awaitable, Annotated
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response, Body, Depends

from src.conf.database import session_context, Base
from src.conf.settings import async_session, DEBUG, engine
from src.conf.producer import send_message, producer
from src.schemas import ApplicationCreateSchema, ApplicationDisplaySchema
from src.depends import pagination_params

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
    await producer.close()


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


@app.post('/api/applications/', status_code=201)
async def create_application(
    application: Annotated[
        ApplicationCreateSchema, 
        Body(embed=False)
    ] 
):
    return {
        'message': "Заявка создана",
        'data': {
            'id': 1,
            'user_name': 'testUser1',
            'description': 'testDescription1'
        }
    }

@app.get('/api/applications')
async def get_applications(
    pagination_params: Annotated[pagination_params, Depends()] = None
):
    return {
        'message': "Заявки получены",
        'data': [{
            'id': 1,
            'user_name': 'testUser1',
            'description': 'testDescription1'
        }]
    }