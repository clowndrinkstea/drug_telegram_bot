from typing import List

from database.models import Notification
from messages_text import head_notification_text


def serialize(notifications: List[Notification]) -> str:
    head_text = head_notification_text

    for notification in notifications:
        additional_text = '\n{}: {} {} с {}.{} по {}.{}\nв {}:{}'.format(
            notification.drug_name,
            notification.amount,
            notification.drug_type,
            notification.start_date.day,
            notification.start_date.month,
            notification.end_date.day,
            notification.end_date.month,
            notification.notification_hour,
            notification.notification_minute
        )

        if notification.period > 0:
            additional_text += '\nповторять курс каждые {} дней'.format(notification.period)

        head_text += additional_text

    return head_text
