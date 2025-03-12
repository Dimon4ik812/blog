from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Comment, Post
from .permissions import IsAuthorOrAdmin
from .serializers import CommentSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrAdmin]

    # Добавьте метод для получения объекта с проверкой прав
    def get_queryset(self):
        # Администратор видит все объекты
        if self.request.user.is_staff:
            return Post.objects.all()
        # Обычные пользователи видят только свои объекты
        return Post.objects.filter(author=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def perform_create(self, serializer):
        # Устанавливаем автора из текущего пользователя
        serializer.save(author=self.request.user)
        # Вызываем полную валидацию модели
        serializer.instance.full_clean()


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrAdmin]

    def get_queryset(self):
        # Администратор видит все объекты
        if self.request.user.is_staff:
            return Comment.objects.all()
        # Обычные пользователи видят только свои объекты
        return Comment.objects.filter(author=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def perform_create(self, serializer):
        # Устанавливаем автора из текущего пользователя
        serializer.save(author=self.request.user)
        # Вызываем полную валидацию модели
        serializer.instance.full_clean()
