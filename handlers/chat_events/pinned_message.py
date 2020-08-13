from aiogram import types
from aiogram.utils import exceptions, markdown as md
from loguru import logger

from utils.db_api import Chats


async def new_pinned_message(msg: types.Message):
    try:
        to_be_pinned = await Chats.get_pinned(msg.chat)
        if to_be_pinned is None:
            return True
        await msg.chat.pin_message(to_be_pinned, disable_notification=True)
    except exceptions.NotEnoughRightsToPinMessage:
        await msg.answer('У меня недостаточно прав чтобы закреплять/откреплять сообщения')
    except exceptions.TelegramAPIError as e:
        await msg.answer(f'Произошла ошибка: {md.quote_html(str(e))}')
        logger.error(f'Telegram API error: [{e}] [{e.__class__}]. Caused by [{msg}]')
    except Exception as e:
        logger.error(f'Unexpected error: [{e}] [{e.__class__}]. Caused by [{msg}]')
