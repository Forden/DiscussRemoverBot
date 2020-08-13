from aiogram import types

from utils.db_api import Chats


async def remember(msg: types.Message):
    if msg.reply_to_message:
        await Chats.set_pinned(msg.chat, msg.reply_to_message)
        m = [
            'Отлично, я запомнил это сообщение и буду закреплять его каждый раз, '
            'когда сервисный аккаунт Telegram репостнет запись с канала'
        ]
    else:
        m = ['Эту команду можно использовать только в ответ на какое-то сообщение, иначе ничего не сработает']
    await msg.reply('\n'.join(m))
