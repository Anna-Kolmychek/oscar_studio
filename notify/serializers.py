from datetime import timedelta

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from notify.models import Notification, RecipientTG, RecipientEmail
from notify.tasks import send_notification


class RecipientField(serializers.Field):
    """
    Сериализатор для поля recipient. Включает валидацию данных.
    """

    def to_internal_value(self, data):
        if isinstance(data, str):
            data = [data]
        elif not isinstance(data, list):
            raise serializers.ValidationError(
                'В поле должна быть строка или список строк'
            )

        for recipient in data:
            if not self.is_valid_recipient(recipient):
                raise serializers.ValidationError(
                    f'Невалидный формат получателя для {recipient}'
                )

        return data

    def is_valid_recipient(self, recipient):
        """
        Проверка, является ли recipient tg ID или Email
        """

        if recipient.isdigit():
            return True

        try:
            validate_email(recipient)
            return True
        except ValidationError:
            return False


class NotifySerializer(serializers.ModelSerializer):
    """
    Основной сериализатор - создание напоминания и получаетелей в базе
    """
    recipient = RecipientField(write_only=True,)

    class Meta:
        model = Notification
        fields = ('message', 'delay', 'recipient',)

    def create(self, validated_data):
        recipients = validated_data.pop('recipient')
        notification = super().create(validated_data)

        eta = None
        if notification.delay == 1:
            eta = timezone.now() + timedelta(minutes=1)
        elif notification.delay == 2:
            eta = timezone.now() + timedelta(days=1)

        for recipient in recipients:
            if recipient.isdigit():
                recipient_class = RecipientTG
            else:
                recipient_class = RecipientEmail

            new_recipient = recipient_class.objects.create(
                recipient=recipient,
                notification=notification,
            )

            transaction.on_commit(
                lambda: send_notification.apply_async(
                    args=[
                        new_recipient.pk,
                        recipient_class.__name__,
                        notification.pk,
                    ],
                    eta=eta,
                )
            )

        return notification
