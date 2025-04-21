from django.db import models

from posts.validators import validate_forbidden_words
from users.models import CustomsUser
from users.validators import validate_adult_birth_date


class Post(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    image = models.ImageField(upload_to="posts/", null=True, blank=True)
    author = models.ForeignKey(CustomsUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        # Проверка возраста автора
        validate_adult_birth_date(self.author.birth_date)

        # Валидация запрещенных слов
        validate_forbidden_words(self.title)


class Comment(models.Model):
    author = models.ForeignKey(CustomsUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
