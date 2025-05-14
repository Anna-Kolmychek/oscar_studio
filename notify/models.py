from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext as _


class Notification(models.Model):
    """Модель уведомления"""

    DELAY_CHOICES = [
        (0, 'отправка сразу'),
        (1, 'отправка с задержкой в 1 час'),
        (2, 'отправка с задержкой в 1 день'),
    ]

    message = models.CharField(
        max_length=1024,
        verbose_name=_('message'),
    )
    delay = models.PositiveSmallIntegerField(
        choices=DELAY_CHOICES,
        verbose_name=_('delay')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created_at')
    )

    class Meta:
        ordering = ('created_at', )
        verbose_name = _('notification')
        verbose_name_plural = _('notifications')

    def __str__(self):
        return f'{self.message}'


class RecipientTG(models.Model):
    """Модель для адресов получаетелей по tg"""

    recipient = models.CharField(
        max_length=150,
        verbose_name=_('recipient in tg'),
    )
    notification = models.ForeignKey(
        Notification,
        on_delete=models.CASCADE,
        related_name='recipients_tg',
        verbose_name=_('notification')
    )

    class Meta:
        verbose_name = _('recipient in TG')
        verbose_name_plural = _('recipients in TG')

    def __str__(self):
        return f'{self.recipient}'


class RecipientEmail(models.Model):
    """Модель для адресов получаетелей по email"""

    recipient = models.EmailField(
        max_length=150,
        null=True,
        blank=True,
        verbose_name=_('recipient in email'),
    )
    notification = models.ForeignKey(
        Notification,
        on_delete=models.CASCADE,
        related_name='recipients_email',
        verbose_name=_('notification')
    )

    class Meta:
        verbose_name = _('recipient in email')
        verbose_name_plural = _('recipients in email')

    def __str__(self):
        return f'{self.recipient}'


class NotificationLog(models.Model):
    """Модель для логов отправки"""

    STATUS_CHOICES = [
        ('success', 'Успешно'),
        ('failed', 'Ошибка'),
    ]

    notification = models.ForeignKey(
        Notification,
        on_delete=models.CASCADE,
        related_name='notification_logs',
        verbose_name=_('notification'),
    )
    recipient_tg = models.ForeignKey(
        RecipientTG,
        on_delete=models.CASCADE,
        related_name='notification_logs',
        verbose_name=_('recipient in tg'),
    )
    recipient_email = models.ForeignKey(
        RecipientEmail,
        on_delete=models.CASCADE,
        related_name='notification_logs',
        verbose_name=_('recipient in email'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created_at')
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        verbose_name=_('status'),
    )
    error_message = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('error message')
    )

    @property
    def recipient(self):
        return self.recipient_email or self.recipient_tg

    def clean(self):
        if not (self.recipient_email or self.recipient_tg):
            raise ValidationError("Должен быть указан получатель")
        if self.recipient_email and self.recipient_tg:
            raise ValidationError("Можно указать только одного получателя")

    class Meta:
        verbose_name = _('notification log')
        verbose_name_plural = _('notification logs')

    def __str__(self):
        return f'{self.notification} --- {self.recipient} --- {self.status}'
