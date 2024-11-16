import logging
from typing import Callable, Dict, Awaitable, Any

from aiogram import BaseMiddleware

from . import database
from . import config

from aiogram.filters import BaseFilter
from aiogram.types import Message




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
            event: Message,
            data: Dict[str, Any],
    ) -> Any:
        logging.info(data['event_from_user'].first_name + ' ' + event['message'].text)
        return await handler(event, data)

