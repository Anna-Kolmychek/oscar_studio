from rest_framework import generics

from notify.models import Notification
from notify.serializers import NotifySerializer


class NotifyCreateAPIView(generics.CreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotifySerializer
    authentication_classes = []
