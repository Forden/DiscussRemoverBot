from aiogram import types

from .consts import InlineConstructor


class Users(InlineConstructor):
    @staticmethod
    def main_menu(bot: types.User):
        schema = [1]
        actions = [
            {'text': 'Добавить бота в чат', 'url': f'https://telegram.me/{bot.username}?startgroup=true'}
        ]
        return Users._create_kb(actions, schema)
