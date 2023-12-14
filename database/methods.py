import datetime
import json
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.models import User, Notification
from aiogram.types import Message


async def get_user_by_message(session: AsyncSession, message: Message) -> Optional[User]:
    telegram_id = message.from_user.id
    chat_id = message.chat.id

    task = select(User).where(User.telegram_id == telegram_id and User.chat_id == chat_id)
    result = await session.execute(task)

    return result.scalars().first()


async def create_user_by_message(session: AsyncSession, message: Message) -> Optional[User]:
    telegram_id = message.from_user.id
    chat_id = message.chat.id

    user = User(telegram_id=telegram_id, chat_id=chat_id, meta=json.dumps({}))
    session.add(user)
    result = await session.commit()

    return result


async def clean_user_meta(session: AsyncSession, user: User):
    user.meta = json.dumps({})
    return await session.commit()


async def get_notifications_by_user(session: AsyncSession, user: User):
    task = select(Notification).where(Notification.user_id == user.id)
    result = await session.execute(task)

    return result.scalars().all()


async def get_current_notifications(session: AsyncSession):
    now_datetime = datetime.datetime.now()
    task = select(Notification).where(
        Notification.end_date >= now_datetime
    ).where(
        Notification.start_date <= now_datetime
    ).where(
        Notification.notification_hour == now_datetime.hour
    ).where(
        Notification.notification_minute == now_datetime.minute
    )

    result = await session.execute(task)

    return result.scalars().all()


async def get_user_by_id(session: AsyncSession, user_id: int) -> User:
    task = select(User).where(User.id == user_id)

    result = await session.execute(task)

    return result.scalars().first()
