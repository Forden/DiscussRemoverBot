from aiogram import types

from utils.db_api import Chats


async def forget(msg: types.Message):
    await Chats.remove_pinned(msg.chat)
    await msg.reply('Отлично, теперь я не буду мешать Telegram закреплять сообщения с канала')
