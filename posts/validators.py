from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_forbidden_words(value):
    forbidden = ["ерунда", "глупость", "чепуха"]
    found = [word for word in forbidden if word in value.lower()]
    if found:
        raise ValidationError(
            _("Недопустимые слова: %(words)s"),
            params={"words": ", ".join(found)},
        )
