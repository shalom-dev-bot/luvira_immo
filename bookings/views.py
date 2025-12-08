from rest_framework import viewsets, permissions
from .models import Booking
from .serializers import BookingSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Booking.objects.all()
        elif user.role == 'owner':
            return Booking.objects.filter(property__owner=user)
        elif user.role == 'client':
            return Booking.objects.filter(tenant=user)
        return Booking.objects.none()

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user)