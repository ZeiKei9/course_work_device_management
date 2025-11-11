from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoleViewSet, UserProfileViewSet, UserViewSet

router = DefaultRouter()
router.register("roles", RoleViewSet)
router.register("profiles", UserProfileViewSet)
router.register("users", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
