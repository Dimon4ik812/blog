from django.utils import timezone
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import CustomsUser
from .permissions import IsAdminOrSelf
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomsUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrSelf]

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return super().get_permissions()


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if request.user.is_authenticated:
            request.user.last_login = (
                timezone.now()
            )  # Обновление времени последнего входа
            request.user.save()
        return response
