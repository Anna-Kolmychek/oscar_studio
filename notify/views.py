from drf_spectacular.utils import extend_schema
from rest_framework import generics

from notify.models import Notification
from notify.serializers import NotifySerializer


@extend_schema(
    summary='Отправка уведомления'
)
class NotifyCreateAPIView(generics.CreateAPIView):
    """
    Отправка уведомления. \n
    В поле recipient может содержаться как список строк, так ио дна строка. \n
    Но в строках должен быть либо TG ID, либо адрес почты. \n

    Для поля delay предусмотрены только значения: \n
    0 - моментальная отправка \n
    1 - отправка с задержкой в один час \n
    2 - отправка с задержкой в один день \n
    """

    queryset = Notification.objects.all()
    serializer_class = NotifySerializer
    authentication_classes = []
