from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PaymentViewSet, ServiceOrderViewSet

router = DefaultRouter()
router.register("service-orders", ServiceOrderViewSet)
router.register("payments", PaymentViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
