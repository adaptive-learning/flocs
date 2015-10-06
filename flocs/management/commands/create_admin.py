from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Creates superuser 'admin' with password 'admin' if not already exists."

    def handle(self, *args, **options):
        if User.objects.filter(username='admin').exists():
            self.stdout.write("User 'admin' already exists.")
        else:
            User.objects.create_superuser('admin', '', 'admin')
            self.stdout.write("Created superuser 'admin' with password 'admin'.")
