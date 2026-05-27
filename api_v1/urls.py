from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomCategoryViewSet, RoomViewSet, BookingViewSet, AmenityViewSet

router = DefaultRouter()
router.register(r'categories', RoomCategoryViewSet, basename='category')
router.register(r'rooms', RoomViewSet, basename='room')
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'amenities', AmenityViewSet, basename='amenity')

urlpatterns = [
    path('', include(router.urls)),
]