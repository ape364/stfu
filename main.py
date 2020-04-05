import logging
import re
from datetime import datetime
from datetime import timedelta

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ChatPermissions

import settings

logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="[%(asctime)s] %(levelname)-8s [%(name)-s.%(funcName)-s:%(lineno)d] %(message)s",
)
logger = logging.getLogger(__name__)

bot = Bot(token=settings.API_TOKEN)
dp = Dispatcher(bot)

REGEX_MUTE = re.compile(r'!m\s(\d+)([mhd])')


@dp.message_handler(regexp=REGEX_MUTE)
async def mute_user(message: types.Message):
    if not message.reply_to_message:
        return

    now = datetime.now()
    duration = parse_duration(message.text)

    restrict_until = now + timedelta(seconds=duration)

    try:
        permissions = ChatPermissions(
            can_send_media_messages=False,
            can_send_polls=False,
            can_send_other_messages=False,
            can_add_web_page_previews=False,
            can_change_info=False,
            can_invite_users=False,
            can_pin_messages=False
        )

        reply = message.reply_to_message
        await message.bot.restrict_chat_member(
            chat_id=reply.chat.id,
            user_id=reply.from_user.id,
            until_date=restrict_until,
            permissions=permissions
        )
    except Exception as e:
        logger.exception('Unable to restrict')
        await message.reply(f'Unable to restrict ({type(e).__name__}): {e}')
    else:
        logger.info(f'Restricted {reply.from_user.to_python()} until {restrict_until}')
        await message.reply(f'User restricted until {restrict_until.ctime()}')


def parse_duration(duration: str) -> int:
    number, duration_type = REGEX_MUTE.match(duration).groups()
    return {
               'm': 60,
               'h': 60 * 60,
               'd': 60 * 60 * 24
           }[duration_type] * int(number)


if __name__ == '__main__':
    dp.middleware.setup(LoggingMiddleware())
    executor.start_polling(dp, skip_updates=True)
