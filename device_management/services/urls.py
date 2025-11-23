from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ServiceOrderViewSet

router = DefaultRouter()
router.register("service-orders", ServiceOrderViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
