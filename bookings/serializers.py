from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Booking
        fields = ['id', 'tenant', 'property', 'start_date', 'end_date', 'status', 'created_at']