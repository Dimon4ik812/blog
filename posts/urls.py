from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, PostViewSet

router = DefaultRouter()
router.register("posts", PostViewSet)
router.register("comments", CommentViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
