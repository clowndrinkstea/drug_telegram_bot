import datetime
import json

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete

from database.models import Notification
from view import notifications_view
from database.base import async_session
from database.methods import get_user_by_message, create_user_by_message, clean_user_meta, get_notifications_by_user, \
    get_current_notifications, get_user_by_id, get_drug_by_message, get_notifications_to_delete
from menu.menu_templates import drug_type_menu, only_to_main_menu, main_menu
from messages_text import hi_text, add_new_drug_text, notification_list_text, hi_again_text, to_main_page_text, \
    drug_name_text, course_days_text, done_text, drug_type_text, drug_amount_input_text, \
    date_input_text, date_format_error_text, int_format_error_text, delete_drug_text, choose_drug_text, \
    nothing_to_delete_text, deleted_text, name_too_long_text
import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters.command import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup

logging.basicConfig(level=logging.INFO)
bot = Bot(token='6596678022:AAGTOIpq4YO2CxSA0n4bz0jHb19deh4ebK0')
dp = Dispatcher()


@dp.message(F.text == to_main_page_text)
@dp.message(Command("start"))
async def cmd_start(message: Message, session: AsyncSession):
    answer = f'{hi_text}, {message.from_user.first_name}!'

    user = await get_user_by_message(session, message)
    if user:
        answer = hi_again_text
        await clean_user_meta(session, user)
    else:
        await create_user_by_message(session, message)

    await message.answer(answer, reply_markup=main_menu)


@dp.message(F.text == add_new_drug_text)
async def cmd_add_new_drug(message: Message, session: AsyncSession):
    user = await get_user_by_message(session, message)
    meta = json.loads(user.meta)

    meta['stage_passed'] = 'add_new_drug'

    user.meta = json.dumps(meta)
    await session.commit()
    await message.answer(drug_name_text, reply_markup=only_to_main_menu)


@dp.message(F.text == notification_list_text)
async def cmd_notification_list_text(message: Message, session: AsyncSession):
    user = await get_user_by_message(session, message)
    notifications = await get_notifications_by_user(session, user)

    await message.answer(notifications_view.get_view(notifications), reply_markup=only_to_main_menu)


@dp.message(F.text == delete_drug_text)
async def cmd_select_drug(message: Message, session: AsyncSession):
    user = await get_user_by_message(session, message)
    meta = json.loads(user.meta)

    meta['stage_passed'] = 'delete_drug'

    user.meta = json.dumps(meta)
    await session.commit()

    info = await get_drug_by_message(session, message)

    drug_names = [str(drug.drug_name) for drug in info]
    if drug_names:
        answer = choose_drug_text
        delete_drug_menu = []
        for name in drug_names:
            delete_drug_menu.append([KeyboardButton(text=name)])

        delete_drug_menu = ReplyKeyboardMarkup(keyboard=delete_drug_menu)

        await message.answer(answer, reply_markup=delete_drug_menu)
    else:
        answer = nothing_to_delete_text
        await message.answer(answer, reply_markup=main_menu)


@dp.message()
async def cmd_msg(message: Message, session: AsyncSession):
    user = await get_user_by_message(session, message)
    meta = json.loads(user.meta)
    reply_markup = only_to_main_menu
    msg = ''

    if meta['stage_passed'] == 'add_new_drug':
        if len(message.text) < 256:
            meta['drug_name'] = message.text
            meta['stage_passed'] = 'drug_name'

            msg = drug_type_text
            reply_markup = drug_type_menu
        else:
            msg = name_too_long_text


    elif meta['stage_passed'] == 'drug_name':
        meta['drug_type'] = message.text
        meta['stage_passed'] = 'drug_type'

        msg = drug_amount_input_text

    elif meta['stage_passed'] == 'drug_type':
        try:
            meta['amount'] = int(message.text)
            meta['stage_passed'] = 'amount'

            msg = date_input_text
        except Exception as e:
            msg = int_format_error_text

    elif meta['stage_passed'] == 'amount':
        try:
            inp = message.text.split(' ')
            if not (len(inp) == 2 and -1 < int(inp[0]) < 25 and -1 < int(inp[1]) < 61):
                raise Exception

            hours = int(inp[0])
            minutes = int(inp[1])

            meta['stage_passed'] = 'notification_time'
            meta['notification_hour'] = hours
            meta['notification_minute'] = minutes

            msg = course_days_text
        except Exception as e:
            msg = date_format_error_text

    elif meta['stage_passed'] == 'notification_time':
        try:
            course = int(message.text)
            if not (course > 0):
                raise Exception
            meta['stage_passed'] = 'course'
            meta['course'] = course

        except Exception as e:
            msg = int_format_error_text
        else:
            notification = Notification(
                drug_name=meta['drug_name'],
                start_date=datetime.datetime.now(),
                amount=meta['amount'],
                drug_type=meta['drug_type'],
                notification_hour=meta['notification_hour'],
                notification_minute=meta['notification_minute'],
                end_date=datetime.datetime.now() + datetime.timedelta(days=meta['course']),
                user_id=user.id,
            )

            session.add(notification)
            await session.commit()

            msg = done_text

    elif meta['stage_passed'] == 'delete_drug':
        name_to_delete = message.text

        task = delete(Notification).where(Notification.drug_name == name_to_delete and Notification.user_id == user.id)
        await session.execute(task)

        msg = deleted_text

    user.meta = json.dumps(meta)
    await session.commit()
    await message.answer(msg, reply_markup=reply_markup)


async def send_notifications():
    session = async_session()
    while True:
        current_notifications = await get_current_notifications(session)

        for notification in current_notifications:
            user = await get_user_by_id(session, notification.user_id)
            await bot.send_message(user.chat_id, notifications_view.get_view([notification]))

        await get_notifications_to_delete(session)

        await asyncio.sleep(60 - datetime.datetime.now().second)


async def run_bot():
    session = async_session()
    await dp.start_polling(bot, session=session)


async def main():
    loop_task_notifications = asyncio.create_task(send_notifications())

    bot_task = asyncio.create_task(run_bot())

    await asyncio.gather(loop_task_notifications, bot_task)


if __name__ == "__main__":
    asyncio.run(main())
