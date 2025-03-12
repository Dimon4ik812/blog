from django.contrib import admin
from django.utils.html import mark_safe

from .models import Comment, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author_link")
    raw_id_fields = ("author",)
    search_fields = ("title", "author__username", "author__email")
    list_filter = ("created_at",)

    def author_link(self, obj):
        if obj.author:
            url = f"/admin/users/CustomsUser/{obj.author.id}/change/"
            return mark_safe(f'<a href="{url}">{obj.author}</a>')
        return "-"

    author_link.short_description = "Автор"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "post", "text", "created_at", "updated_at")
    list_filter = ("author",)
