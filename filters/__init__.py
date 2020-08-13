from aiogram import Dispatcher

from .is_admin import SuperAdminFilter
from .is_chat_admin import AdminFilter


def setup(dp: Dispatcher):
    dp.filters_factory.bind(SuperAdminFilter)
    dp.filters_factory.bind(AdminFilter)
