# coding: utf8

import asyncio
from typing import Optional, Dict, Any, Union

import aiomysql
from aiogram import types

import config

connection_pool = None
mainloop = asyncio.get_event_loop()


async def main(loop):
    global connection_pool
    connection_pool = await aiomysql.create_pool(**config.mysql_info, loop=loop)


class RawConnection:
    @staticmethod
    async def _make_request(
            sql: str,
            params: tuple = None,
            fetch: bool = False,
            mult: bool = False,
            retries_count: int = 5
    ) -> Optional[Dict[str, Any]]:
        global connection_pool
        async with connection_pool.acquire() as conn:
            conn: aiomysql.Connection = conn
            async with conn.cursor(aiomysql.DictCursor) as cur:
                cur: aiomysql.DictCursor = cur
                for i in range(retries_count):
                    try:
                        await cur.execute(sql, params)
                    except aiomysql.OperationalError as e:
                        if 'Deadlock found' in str(e):
                            await asyncio.sleep(1)
                    except aiomysql.InternalError as e:
                        print(f'found error [{e}]  [{sql}] [{params}] retrying [{i}]')
                        if 'Deadlock found' in str(e):
                            await asyncio.sleep(1)
                    else:
                        break
                if fetch:
                    if mult:
                        r = await cur.fetchall()
                    else:
                        r = await cur.fetchone()
                    return r
                else:
                    await conn.commit()


class Chats(RawConnection):
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
        if res:
            return int(res['message_id'])
        else:
            return None


loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
