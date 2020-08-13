from aiogram import Bot, types

import keyboards


async def bot_help(msg: types.Message):
    txt = [
        'Чтобы увидеть это сообщение - используй команду /help',
        'Чтобы добавить меня в чат - используй кнопку ниже',
        'Чтобы я запомнил нужное сообщение - ответь на него командой /remember <b>в группе</b>',
        'Чтобы я забыл сообщение и позволял закреплять любые сообщения - используй команду /forget <b>в группе</b>'
    ]
    kb = keyboards.inline.Users.main_menu(await Bot.get_current().get_me())
    await msg.answer('\n'.join(txt), reply_markup=kb, reply=not msg.chat.type == 'private')
