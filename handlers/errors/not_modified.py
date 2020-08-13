from aiogram import types
from aiogram.utils import exceptions


# noinspection PyUnusedLocal
async def message_not_modified(update: types.Update, error: exceptions.MessageNotModified):
    return True


# noinspection PyUnusedLocal
async def message_to_delete_not_found(update: types.Update, error: exceptions.MessageToDeleteNotFound):
    return True
