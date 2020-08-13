from aiogram import Dispatcher

from .leave_chat import leave_chat


def setup(dp: Dispatcher):
    dp.register_message_handler(leave_chat, commands=['leave'], is_super_admin=True)
