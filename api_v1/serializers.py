from rest_framework import serializers
from .models import RoomCategory, Room, Booking, Amenity


class RoomCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomCategory
        fields = ['id', 'name', 'description', 'price_per_night']

class RoomSerializer(serializers.ModelSerializer):
    category = RoomCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=RoomCategory.objects.all(), source='category', write_only=True
    )

    class Meta:
        model = Room
        fields = [
            'id', 'room_number', 'category', 'category_id', 
            'amenities', 'is_cleaned', 'created_at'
        ]

class BookingSerializer(serializers.ModelSerializer):
    room = serializers.StringRelatedField(read_only=True)
    room_id = serializers.PrimaryKeyRelatedField(
        queryset=Room.objects.all(), source='room', write_only=True
    )

    class Meta:
        model = Booking
        fields = ['id', 'room', 'room_id', 'guest_name', 'check_in_date', 'check_out_date', 'created_at']


class AmenitySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Amenity
        fields = ['id', 'name']
        read_only_fields = ['id']