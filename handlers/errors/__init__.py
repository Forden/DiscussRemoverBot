from aiogram import Dispatcher
from aiogram.utils import exceptions

from .bot_blocked import blocked_by_user
from .not_modified import message_not_modified, message_to_delete_not_found


def setup(dp: Dispatcher):
    dp.register_errors_handler(message_not_modified, exception=exceptions.MessageNotModified)
    dp.register_errors_handler(message_to_delete_not_found, exception=exceptions.MessageToDeleteNotFound)
    dp.register_errors_handler(blocked_by_user, exception=exceptions.BotBlocked)
