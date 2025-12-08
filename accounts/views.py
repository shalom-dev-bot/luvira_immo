from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import OwnerRequest
from .serializers import UserSerializer, OwnerRequestSerializer

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.AllowAny()]
        if self.action in ['list', 'retrieve', 'update', 'partial_update', 'destroy']:
            if self.request.user.is_staff or self.request.user.role == 'admin':
                return [permissions.IsAuthenticated()]
            return [permissions.IsAuthenticated(), permissions.IsOwnerOrReadOnly()]  # Custom permission si besoin

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class OwnerRequestViewSet(viewsets.ModelViewSet):
    queryset = OwnerRequest.objects.all()
    serializer_class = OwnerRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]