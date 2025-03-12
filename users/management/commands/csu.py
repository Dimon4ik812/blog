from django.core.management import BaseCommand

from users.models import CustomsUser


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        user = CustomsUser.objects.create(
            username="admin", email="admin@mail.ru", birth_date="2025-03-11"
        )
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.set_password("852123654")
        user.save()
