from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    BrandViewSet,
    CategoryViewSet,
    DeviceViewSet,
    LocationViewSet,
    ReservationViewSet,
)

router = DefaultRouter()
router.register("categories", CategoryViewSet)
router.register("brands", BrandViewSet)
router.register("locations", LocationViewSet)
router.register("devices", DeviceViewSet)
router.register("reservations", ReservationViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
