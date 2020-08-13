from aiogram import Bot, types
from aiogram.utils import markdown as md

from utils.db_api import Chats


async def new_members(msg: types.Message):
    botinfo = await Bot.get_current().get_me()
    for i in msg.new_chat_members:
        if i.id == botinfo.id:
            if await Chats.is_new(msg.chat):
                await Chats.register(msg.chat)
            txt = [
                f'Привет, <b>{md.quote_html(msg.chat.title)}</b>! '
                'Я помогу вам удерживать одно сообщение закрепленным, исправляя недостаток Telegram\n',
                'Чтобы я запомнил нужное сообщение - просто ответь на него командой /remember.',
                'Чтобы я забыл сообщение и позволял закреплять любые сообщения - используй команду /forget.'
            ]
            await msg.answer('\n'.join(txt))
