from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from django.contrib.gis.geos import Point
from .models import Property, Review

class PropertySerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Property
        geo_field = 'location'
        fields = [
            'id', 'owner', 'category', 'title', 'description', 'price_per_night',
            'price_per_month', 'status', 'address', 'location', 'city', 'neighborhood',
            'bedrooms', 'bathrooms', 'surface', 'services', 'photos', 'videos',
            'created_at', 'is_active'
        ]

    def validate_location(self, value):
        if isinstance(value, dict):
            return Point(value.get('longitude', 0), value.get('latitude', 0))
        return value

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'property', 'user', 'rating', 'comment', 'created_at', 'is_approved']
        read_only_fields = ['user', 'created_at']