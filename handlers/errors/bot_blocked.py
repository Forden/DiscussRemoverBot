from aiogram import types
from aiogram.utils import exceptions
from loguru import logger


async def blocked_by_user(upd: types.Update, err: exceptions.BotBlocked):
    logger.error(f'Bot blocked by user: {upd} [{err}]')
