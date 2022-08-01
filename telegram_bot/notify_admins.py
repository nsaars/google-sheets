import logging

from aiogram import Dispatcher

from data.config import ADMINS


async def notify_admins(dp: Dispatcher, message: str):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, message)
        except Exception as err:
            logging.exception(err)
