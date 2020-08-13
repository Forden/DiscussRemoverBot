from aiogram import types


async def leave_chat(msg: types.Message):
    if msg.chat.type != 'private':
        await msg.chat.leave()
    else:
        await msg.reply('Это личные сообщения, бот не может выйти отсюда')
