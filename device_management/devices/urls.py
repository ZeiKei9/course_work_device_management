from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, BrandViewSet, LocationViewSet

router = DefaultRouter()
router.register("categories", CategoryViewSet)
router.register("brands", BrandViewSet)
router.register("locations", LocationViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
