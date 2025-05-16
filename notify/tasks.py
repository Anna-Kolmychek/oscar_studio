from smtplib import SMTPException

import requests
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from notify.models import RecipientTG, RecipientEmail, NotificationLog, \
    Notification, STATUS


@shared_task
def send_notification(
        recipient_pk: int, recipient_type: str, notification_pk: int
) -> None:
    """
    Задача Celery для отправки уведомления
    """

    # Получаем объект получателя и объект уведомления
    recipient_class = (
        RecipientTG if recipient_type == 'RecipientTG' else RecipientEmail
    )
    recipient = recipient_class.objects.filter(pk=recipient_pk).first()
    notification = Notification.objects.filter(pk=notification_pk).first()

    # Определяем что нужно отправить (письмо или сообщение в ТГ),
    # вызываем соответствующую функцию
    send_msg_handler = (
        send_tg_message
        if recipient_type == 'RecipientTG'
        else send_email
    )

    result = send_msg_handler(
        recipient=recipient.recipient,
        message=notification.message
    )

    # Пишем логи
    write_log(result, recipient, notification)


def send_tg_message(recipient: str, message: str) -> str | Exception:
    """
    Отправка сообщения в ТГ
    """

    url = f'https://api.telegram.org/bot{settings.TG_BOT_TOKEN}/sendMessage'

    data = {
        'chat_id': recipient,
        'text': message,
        'parse_mode': 'HTML',
    }

    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        return 'success'
    except Exception as e:
        return e


def send_email(recipient: str, message: str) -> str | Exception:
    """
    Отправка сообщения на почту
    """
    try:
        send_mail(
            subject='Oscar Studio Notificaion',
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[recipient],
        )
        return 'success'
    except Exception as e:
        return e


def write_log(
        result: str | Exception,
        recipient: RecipientTG | RecipientEmail,
        notification: Notification,
) -> None:
    """
    Запись лога
    """

    field_recipient_name = (
        'recipient_tg'
        if isinstance(recipient, RecipientTG)
        else 'recipient_email'
    )

    if result == 'success':
        status = STATUS.SUCCESS
        error_message = None
    else:
        status = STATUS.FAILED
        error_message = result

    NotificationLog.objects.create(
        notification=notification,
        **{field_recipient_name: recipient},
        status=status,
        error_message=error_message,
    )
