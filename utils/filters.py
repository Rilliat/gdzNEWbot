import logging
from typing import Callable, Dict, Awaitable, Any

from aiogram import BaseMiddleware

from . import database
from . import config

from aiogram.filters import BaseFilter
from aiogram.types import Message, Update

message_logger = logging.getLogger('message_logger')
message_logger.setLevel(logging.INFO)

message_handler = logging.FileHandler('message_logger.log', mode='w')
message_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
message_handler.setFormatter(message_formatter)

message_logger.addHandler(message_handler)


class IsAllowed(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        db = database.Database()
        if db.check_access(message.from_user.id):
            return True
        else:
            return False

class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.from_user.id in config.admins:
            return True
        else:
            return False


class LoggingMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Update | Any,
            data: Dict[str, Any],
    ) -> Any:
        message_logger.info(data['event_from_user'].first_name + ': ' + event.message.text if event.message else event.callback_query.data)
        return await handler(event, data)

