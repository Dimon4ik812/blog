from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from posts.models import Post
from users.models import CustomsUser


class UserModelTest(TestCase):
    def test_user_validation(self):
        # Невалидный пароль
        user = CustomsUser(username="test", email="test@mail.ru", password="123")
        user.phone = ""  # Добавляем phone, чтобы избежать ошибки
        user.birth_date = date(2000, 1, 1)  # Добавляем birth_date
        with self.assertRaises(ValidationError) as cm:
            user.full_clean()
        self.assertIn("Пароль должен быть >=8 символов", str(cm.exception))

        # Невалидный email
        user = CustomsUser(username="test", email="test@gmail.com", password="Pass1234")
        user.phone = "123456789"
        user.birth_date = date(2000, 1, 1)
        with self.assertRaises(ValidationError) as cm:
            user.full_clean()
        self.assertIn("Разрешены только домены", str(cm.exception))


class PostModelTest(TestCase):
    def setUp(self):
        self.user = CustomsUser.objects.create_user(
            username="adult",
            email="adult@mail.ru",
            password="Pass1234",
            phone="123456789",
            birth_date=date(2000, 1, 1),
        )

    def test_age_validation(self):
        # Пользователь младше 18
        young_user = CustomsUser.objects.create_user(
            username="young",
            email="young@mail.ru",
            password="Pass1234",
            phone="987654321",
            birth_date=date(2020, 1, 1),
        )

        post = Post(title="Test", text="Content", author=young_user)
        with self.assertRaises(ValidationError) as cm:
            post.full_clean()
        self.assertIn("Пользователю должно быть минимум 18 лет", str(cm.exception))

    def test_forbidden_words(self):
        post = Post(title="Это ерунда", text="Content", author=self.user)
        with self.assertRaises(ValidationError) as cm:
            post.full_clean()
        self.assertIn("Недопустимые слова: ерунда", str(cm.exception))


class PostAPITest(APITestCase):
    def setUp(self):
        self.user = CustomsUser.objects.create_user(
            username="user",
            email="user@mail.ru",
            password="Pass1234",
            birth_date=date(2020, 1, 1),
        )
        self.admin = CustomsUser.objects.create_superuser(
            username="admin",
            email="admin@mail.ru",
            password="Admin1234",
            birth_date=date(1990, 1, 1),
        )

    def test_create_post(self):
        # Неавторизованный доступ
        response = self.client.post(
            "/api/posts/posts/", {"title": "Test", "text": "Content"}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Авторизованный пользователь (взрослый)
        adult_user = CustomsUser.objects.create_user(
            username="adult",
            email="adult@mail.ru",
            password="Pass1234",
            birth_date=date(2000, 1, 1),  # Пользователь старше 18 лет
        )
        self.client.force_authenticate(user=adult_user)
        response = self.client.post(
            "/api/posts/posts/", {"title": "Valid Post", "text": "Content"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)

        # Запрещенные слова
        response = self.client.post(
            "/api/posts/posts/", {"title": "Это глупость", "text": "Content"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Недопустимые слова", response.data["title"][0])
