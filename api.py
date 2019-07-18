# coding: utf8

import sqlite3
import typing

from aiogram import types


class DataConn:
    def __init__(self, db_name):
        self.db_name = db_name

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
        if exc_val:
            raise


class Chats:
    @staticmethod
    def is_new(chat: types.Chat) -> bool:
        with DataConn('db.db') as conn:
            curs = conn.cursor()
            sql = 'SELECT * FROM `admins` WHERE `chat_id` = ?'
            curs.execute(sql, (chat.id,))
            return not bool(curs.fetchone())

    @staticmethod
    def register(chat: types.Chat):
        with DataConn('db.db') as conn:
            curs = conn.cursor()
            sql = 'INSERT INTO `admins` (`chat_id`) VALUES (?)'
            curs.execute(sql, (chat.id,))
            conn.commit()

    @staticmethod
    def set_pinned(chat: types.Chat, msg: types.Message):
        if Chats.get_pinned(chat) is not None:
            with DataConn('db.db') as conn:
                curs = conn.cursor()
                sql = 'UPDATE `pinned` SET `message_id` = ? WHERE `chat_id`= ?'
                curs.execute(sql, (msg.message_id, chat.id))
                conn.commit()
        else:
            with DataConn('db.db') as conn:
                curs = conn.cursor()
                sql = 'INSERT INTO `pinned` (`chat_id`, `message_id`) VALUES (?, ?)'
                curs.execute(sql, (chat.id, msg.message_id))
                conn.commit()

    @staticmethod
    def remove_pinned(chat: types.Chat):
        with DataConn('db.db') as conn:
            curs = conn.cursor()
            sql = 'DELETE FROM `pinned` WHERE `chat_id` = ?'
            curs.execute(sql, (chat.id,))
            conn.commit()

    @staticmethod
    def get_pinned(chat: types.Chat) -> typing.Union[int, None]:
        with DataConn('db.db') as conn:
            curs = conn.cursor()
            sql = 'SELECT `message_id` FROM `pinned` WHERE `chat_id` = ?'
            curs.execute(sql, (chat.id,))
            res = curs.fetchone()
            if res:
                return int(res[0])
            else:
                return None
