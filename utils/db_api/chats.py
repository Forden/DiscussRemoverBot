from typing import Union

from aiogram import types

from .storages import MysqlConnection


class Chats(MysqlConnection):
    @staticmethod
    async def is_new(chat: types.Chat) -> bool:
        sql = 'SELECT * FROM `admins` WHERE `chat_id` = %s'
        params = (chat.id,)
        r = await Chats._make_request(sql, params, fetch=True)
        return not bool(r)

    @staticmethod
    async def register(chat: types.Chat):
        sql = 'INSERT INTO `admins` (`chat_id`, `admins`) VALUES (%s, %s)'
        params = (chat.id, '')
        await Chats._make_request(sql, params)

    @staticmethod
    async def set_pinned(chat: types.Chat, msg: types.Message):
        if (await Chats.get_pinned(chat)) is not None:
            sql = 'UPDATE `pinned` SET `message_id` = %s WHERE `chat_id`= %s'
            params = (msg.message_id, chat.id)
        else:
            sql = 'INSERT INTO `pinned` (`chat_id`, `message_id`) VALUES (%s, %s)'
            params = (chat.id, msg.message_id)
        await Chats._make_request(sql, params)

    @staticmethod
    async def remove_pinned(chat: types.Chat):
        sql = 'DELETE FROM `pinned` WHERE `chat_id` = %s'
        params = (chat.id,)
        await Chats._make_request(sql, params)

    @staticmethod
    async def get_pinned(chat: types.Chat) -> Union[int, None]:
        sql = 'SELECT `message_id` FROM `pinned` WHERE `chat_id` = %s'
        params = (chat.id,)
        res = await Chats._make_request(sql, params, fetch=True)
        return int(res['message_id']) if res else None
