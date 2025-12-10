from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Property
from .serializers import PropertySerializer

class PropertyViewSet(viewsets.ModelViewSet):
    queryset          = Property.objects.filter(is_active=True)
    serializer_class  = PropertySerializer
    filter_backends   = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields  = ['city', 'neighborhood', 'category', 'price_per_month', 'bedrooms', 'status']
    search_fields     = ['title', 'description']
    ordering_fields   = ['price_per_month', 'created_at']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]  # Visiteurs peuvent voir
        return [permissions.IsAuthenticated()]  # Pour create/update, logué (et owner)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)