from aiogram import Bot, types
from aiogram.dispatcher.filters import BoundFilter

from data import config


class AdminFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, upd: types.Message, *args):
        if upd.chat.type in ['supergroup', 'group']:
            if upd.from_user.id in config.admins:
                return True
            member = await Bot.get_current().get_chat_member(upd.chat.id, upd.from_user.id)
            return member.is_chat_admin()
        else:
            return False
