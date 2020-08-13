from aiogram import Dispatcher

from .forget import forget
from .remember import remember


def setup(dp: Dispatcher):
    dp.register_message_handler(remember, commands=['remember'], is_admin=True)
    dp.register_message_handler(forget, commands=['forget'], is_admin=True)
