from conf import config

from contextlib import asynccontextmanager

from fastapi import FastAPI
from aiogram import Bot
from loguru import logger

from stream import StreamManager
from shared.storage import Database
from api import chat_routes, message_routes, websocket_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = Database(db_name=config.db_name, uri=config.mongo_uri, logger=logger)  # type: ignore
    stream_manager = StreamManager()
    app.state.db = db
    app.state.stream_manager = stream_manager
    app.state.bot = Bot(config.bot_token)
    yield
    db.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(chat_routes.router)
app.include_router(message_routes.router)
app.include_router(websocket_routes.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=config.app_port)
