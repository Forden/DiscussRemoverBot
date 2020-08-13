from typing import List

import aiojobs
from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode
from aiohttp import web
from loguru import logger

from data import config


# noinspection PyUnusedLocal
async def on_startup(app: web.Application):
    import middlewares
    import filters
    import handlers

    middlewares.setup(dp)
    filters.setup(dp)

    handlers.errors.setup(dp)
    handlers.super_admin_commands.setup(dp)
    handlers.admin_commands.setup(dp)
    handlers.user.setup(dp)
    handlers.chat_events.setup(dp)

    logger.info(f'Configure Webhook URL to: {config.WEBHOOK_URL}')
    await dp.bot.set_webhook(config.WEBHOOK_URL)


async def on_shutdown(app: web.Application):
    app_bot: Bot = app['bot']
    await app_bot.close()


async def init() -> web.Application:
    from utils.misc import logging
    import web_handlers
    logging.setup()
    scheduler = await aiojobs.create_scheduler()
    app = web.Application()
    subapps: List[str, web.Application] = [
        ('/health', web_handlers.health_app),
        ('/tg/webhooks', web_handlers.tg_updates_app),
    ]
    for prefix, subapp in subapps:
        subapp['bot'] = bot
        subapp['dp'] = dp
        subapp['scheduler'] = scheduler
        app.add_subapp(prefix, subapp)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    return app


if __name__ == '__main__':
    bot = Bot(config.BOT_TOKEN, parse_mode=ParseMode.HTML, validate_token=True)
    dp = Dispatcher(bot)

    web.run_app(init(), port=5153, host='localhost')
