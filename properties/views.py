from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Property, Review
from .serializers import PropertySerializer, ReviewSerializer

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.filter(is_active=True)
    serializer_class = PropertySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['city', 'neighborhood', 'category', 'price_per_month', 'bedrooms', 'status']
    search_fields = ['title', 'description']
    ordering_fields = ['price_per_month', 'created_at']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]  # Visiteurs peuvent voir liste/détails
        return [permissions.IsAuthenticated()]  # Pour create/update/delete, logué (et owner via custom perm si besoin)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'], url_path='favorite')
    def favorite(self, request, pk=None):
        property = self.get_object()
        if request.user in property.favorites.all():
            property.favorites.remove(request.user)
            return Response({'status': 'removed from favorites'})
        property.favorites.add(request.user)
        return Response({'status': 'added to favorites'})

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.filter(is_approved=True)  # Seul approuvés visibles
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Review.objects.all()
        return Review.objects.filter(is_approved=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)