from rest_framework import serializers

from posts.models import Comment, Post
from posts.validators import validate_forbidden_words


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["author"]


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ["author"]
        extra_kwargs = {"title": {"validators": [validate_forbidden_words]}}

    def validate(self, data):
        # Проверка прав доступа при обновлении
        if self.instance:
            # Разрешить редактирование только автору или администратору
            if (
                self.instance.author != self.context["request"].user
                and not self.context["request"].user.is_staff
            ):
                raise serializers.ValidationError(
                    "Вы не можете редактировать этот пост"
                )
        return data
