from rest_framework import serializers

from users.models import CustomsUser
from users.validators import (
    validate_adult_birth_date,
    validate_email_domain,
    validate_password_strength,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomsUser
        fields = ["id", "username", "email", "phone", "birth_date", "password"]
        extra_kwargs = {
            "password": {
                "write_only": True,
                "validators": [validate_password_strength],
            },
            "email": {"validators": [validate_email_domain]},
            "birth_date": {"validators": [validate_adult_birth_date]},
        }

    def create(self, validated_data):
        user = CustomsUser.objects.create_user(**validated_data)
        return user
