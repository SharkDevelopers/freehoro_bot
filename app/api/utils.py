from aiogram.client.bot import Bot
from fastapi import Request, WebSocket
from shared.storage import Database

from stream.core import StreamManager


def get_bot(request: Request) -> Bot:
    return request.app.state.bot


def get_stream_manager(request: Request) -> StreamManager:
    return request.app.state.stream_manager


def get_stream_manager_websocket(request: WebSocket) -> StreamManager:
    return request.app.state.stream_manager


def get_db(request: Request) -> Database:
    return request.app.state.db
