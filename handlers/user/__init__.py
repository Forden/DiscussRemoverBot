from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import CommandHelp, CommandStart

from .help import bot_help
from .start import bot_start


def setup(dp: Dispatcher):
    dp.register_message_handler(bot_start, types.ChatType.is_private, CommandStart())
    dp.register_message_handler(bot_help, CommandHelp())
