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

