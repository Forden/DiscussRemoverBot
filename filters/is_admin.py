from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from data import config


class SuperAdminFilter(BoundFilter):
    key = 'is_super_admin'

    def __init__(self, is_super_admin):
        self.is_super_admin = is_super_admin

    async def check(self, message: types.Message, *args):
        return message.from_user.id in config.admins
