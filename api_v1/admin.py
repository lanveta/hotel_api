from django.contrib import admin
from .models import RoomCategory, Room, Booking, Amenity 

@admin.register(RoomCategory)
class RoomCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price_per_night']
    search_fields = ['name']

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'room_number', 'category', 'is_cleaned', 'created_at']
    list_filter = ['category', 'is_cleaned']
    search_fields = ['room_number']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'room', 'guest_name', 'check_in_date', 'check_out_date', 'created_at']
    list_filter = ['check_in_date', 'room']
    search_fields = ['guest_name']

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)