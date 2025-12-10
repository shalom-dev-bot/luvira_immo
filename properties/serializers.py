from rest_framework import serializers
from django.contrib.gis.geos import Point
from .models import Property

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Property
        fields = ['id', 'owner', 'category', 'title', 'description', 'price_per_night', 'price_per_month', 'status', 'address', 'location', 'city', 'neighborhood', 'bedrooms', 'bathrooms', 'surface', 'services', 'photos', 'videos', 'created_at', 'is_active']

    def validate_location(self, value):
        if isinstance(value, dict):
            return Point(value['longitude'], value['latitude'])
        return value