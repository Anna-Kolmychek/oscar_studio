from celery import shared_task


@shared_task
def send_notification(recipient, recipient_type, message):
    """Задача Celery для отправки уведомления"""
    pass