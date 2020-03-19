from aiogram import Bot, Dispatcher, exceptions, executor, types
from aiogram.utils import markdown as md

import config
import filters
from api import Chats

bot = Bot(token=config.token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

dp.filters_factory.bind(filters.AdminFilter)

MEDIA_TYPES = [
    types.ContentType.PHOTO, types.ContentType.DOCUMENT, types.ContentType.AUDIO,
    types.ContentType.STICKER, types.ContentType.VIDEO, types.ContentType.VIDEO_NOTE,
    types.ContentType.VOICE, types.ContentType.LOCATION, types.ContentType.CONTACT,
    types.ContentType.ANIMATION, types.ContentType.TEXT
]


@dp.message_handler(lambda message: message.chat.type == 'private', commands=['start'])
async def start(msg: types.Message):
    botinfo = await bot.get_me()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Добавить бота в чат',
                                            url=f'https://telegram.me/{botinfo.username}?startgroup=true'))
    txt = [
        f'Привет, <b>{md.quote_html(msg.from_user.full_name)}</b>! '
        'Я помогу тебе удерживать конкретнее сообщение закрепленным, исправляя недостаток Telegram.\n',
        'Просто добавь меня в нужный чат и выдай права на закрепление сообщений. Об остальном я сразу расскажу.',
        'Если ты хочешь увидеть справку - используй команду /help'
    ]
    await msg.reply('\n'.join(txt), reply_markup=keyboard)


@dp.message_handler(commands=['help'])
async def cmd_help(msg: types.Message):
    botinfo = await bot.get_me()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Добавить бота в чат',
                                            url=f'https://telegram.me/{botinfo.username}?startgroup=true'))
    txt = [
        'Чтобы увидеть это сообщение - используй команду /help',
        'Чтобы добавить меня в чат - используй кнопку ниже',
        'Чтобы я запомнил нужное сообщение - ответь на него командой /remember <b>в группе</b>',
        'Чтобы я забыл сообщение и позволял закреплять любые сообщения - используй команду /forget <b>в группе</b>'
    ]
    await msg.reply('\n'.join(txt), reply_markup=keyboard)


@dp.message_handler(content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
async def new_member(msg: types.Message):
    botinfo = await bot.get_me()
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
            await bot.send_message(
                chat_id=msg.chat.id,
                text='\n'.join(txt),
            )


@dp.message_handler(commands=['remember'], is_admin=True)
async def remember(msg: types.Message):
    if msg.reply_to_message:
        await Chats.set_pinned(msg.chat, msg.reply_to_message)
        m = [
            'Отлично, я запомнил это сообщение и буду закреплять его каждый раз, '
            'когда сервисный аккаунт Telegram репостнет запись с канала'
        ]
        await bot.send_message(
            msg.chat.id,
            '\n'.join(m),
            reply_to_message_id=msg.reply_to_message.message_id
        )
    else:
        m = ['Эту команду можно использовать только в ответ на какое-то сообщение, иначе ничего не сработает']
        await msg.reply('\n'.join(m))


@dp.message_handler(commands=['forget'], is_admin=True)
async def forget(msg: types.Message):
    await Chats.remove_pinned(msg.chat)
    await msg.reply('Отлично, теперь я не буду мешать Telegram закреплять сообщения с канала')


@dp.message_handler(lambda message: message.from_user.id == 777000, content_types=MEDIA_TYPES)
async def unpin(msg: types.Message):
    try:
        to_be_pinned = await Chats.get_pinned(msg.chat)
        if to_be_pinned is None:
            return True
        await msg.chat.unpin_message()
        await bot.pin_chat_message(msg.chat.id, to_be_pinned, disable_notification=True)
    except exceptions.NotEnoughRightsToPinMessage:
        await bot.send_message(msg.chat.id, 'У меня недостаточно прав чтобы закреплять/откреплять сообщения')
    except exceptions.TelegramAPIError as e:
        await bot.send_message(msg.chat.id, f'Произошла ошибка: {e}')
    except Exception as e:
        print(e)


@dp.errors_handler(exception=exceptions.BotBlocked)
async def blocked_by_user(upd: types.Update, err: exceptions.BotBlocked):
    print(str(err))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
