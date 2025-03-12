import re

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class CustomsUser(AbstractUser):
    phone = models.CharField(max_length=20)
    birth_date = models.DateField()

    def clean(self):
        # Валидация пароля
        if len(self.password) < 8 or not re.search(r"\d", self.password):
            raise ValidationError("Пароль должен быть >=8 символов и содержать цифры")

        # Валидация email
        allowed_domains = ["mail.ru", "yandex.ru"]
        domain = self.email.split("@")[-1]
        if domain not in allowed_domains:
            raise ValidationError(
                f"Разрешены только домены: {', '.join(allowed_domains)}"
            )
