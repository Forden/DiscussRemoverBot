import config
from aiogram import Bot, types
from aiogram.dispatcher.filters import BoundFilter

bot = Bot(token=config.token, parse_mode=types.ParseMode.HTML)


class AdminFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message: types.Message):
        if message.chat.type in ['supergroup', 'group']:
            member = await bot.get_chat_member(message.chat.id, message.from_user.id)
            return member.is_chat_admin()
        else:
            return False
