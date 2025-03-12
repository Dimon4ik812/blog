import re

from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def validate_email_domain(value):
    allowed_domains = ["mail.ru", "yandex.ru"]
    domain = value.split("@")[-1]
    if domain not in allowed_domains:
        raise ValidationError(
            _("Разрешены только домены: %(domains)s"),
            params={"domains": ", ".join(allowed_domains)},
        )


def validate_password_strength(value):
    if len(value) < 8:
        raise ValidationError(_("Пароль должен содержать минимум 8 символов"))
    if not re.search(r"\d", value):
        raise ValidationError(_("Пароль должен содержать хотя бы одну цифру"))


def validate_adult_birth_date(value):
    if value.year > (timezone.now().year - 18):
        raise ValidationError(_("Пользователю должно быть минимум 18 лет"))
