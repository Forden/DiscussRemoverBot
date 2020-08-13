from aiogram import Bot, types
from aiogram.utils import markdown as md

import keyboards


async def bot_start(msg: types.Message):
    txt = [
        f'Привет, <b>{md.quote_html(msg.from_user.full_name)}</b>! '
        'Я помогу тебе удерживать конкретнее сообщение закрепленным, исправляя недостаток Telegram.\n',
        'Просто добавь меня в нужный чат и выдай права на закрепление сообщений. Об остальном я сразу расскажу.',
        'Если ты хочешь увидеть справку - используй команду /help'
    ]
    kb = keyboards.inline.Users.main_menu(await Bot.get_current().get_me())
    await msg.answer('\n'.join(txt), reply_markup=kb)
