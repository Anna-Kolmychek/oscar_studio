import os

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand


User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):

        username = os.getenv('ADMIN_USERNAME', default='admin')
        password = os.getenv('ADMIN_PASS', default='admin')
        email = f'{username}@example.com'

        if User.objects.filter(username=username).exists():
            return

        User.objects.create_superuser(
            username=username, email=email, password=password
        )
