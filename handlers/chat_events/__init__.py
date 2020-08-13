from aiogram import Dispatcher, types

from .new_members import new_members
from .pinned_message import new_pinned_message

MEDIA_TYPES = [
    types.ContentType.PHOTO, types.ContentType.DOCUMENT, types.ContentType.AUDIO,
    types.ContentType.STICKER, types.ContentType.VIDEO, types.ContentType.VIDEO_NOTE,
    types.ContentType.VOICE, types.ContentType.LOCATION, types.ContentType.CONTACT,
    types.ContentType.ANIMATION, types.ContentType.TEXT, types.ContentType.DICE
]


def setup(dp: Dispatcher):
    dp.register_message_handler(new_members, content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
    dp.register_message_handler(new_pinned_message, user_id=[777000], content_types=MEDIA_TYPES)
