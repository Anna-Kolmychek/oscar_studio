from django.urls import path

from notify.apps import NotifyConfig
from notify.views import NotifyCreateAPIView

app_name = NotifyConfig.name

urlpatterns = [
    path('', NotifyCreateAPIView.as_view()),
]
