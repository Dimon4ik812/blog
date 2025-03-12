from django.contrib import admin

from users.models import CustomsUser


@admin.register(CustomsUser)
class CustomsUserAdmin(admin.ModelAdmin):
    list_display = ("id", "username")
    list_filter = ("id", "email")
