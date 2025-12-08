from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Sum, Q
from django.contrib.auth import get_user_model
from properties.models import Property
from bookings.models import Booking
from payments.models import Payment
from subscriptions.models import Subscription
from .serializers import StatsSerializer  # Optionnel, pour formater

User = get_user_model()

class DashboardViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='admin')
    def admin_stats(self, request):
        if request.user.role != 'admin':
            return Response({'error': 'Accès refusé : réservé aux admins'}, status=403)
        
        stats = {
            'total_users': User.objects.count(),
            'total_properties': Property.objects.count(),
            'total_bookings': Booking.objects.count(),
            'total_payments': Payment.objects.aggregate(total=Sum('amount'))['total'] or 0,
            'active_owners': User.objects.filter(role='owner', subscription__is_active=True).count(),  # Assume lien avec Subscription
            'properties_by_city': Property.objects.values('city').annotate(count=Count('id')),
            # Ajoute plus : e.g., revenus mensuels avec filters date
        }
        serializer = StatsSerializer(stats)  # Optionnel
        return Response(serializer.data if serializer else stats)

    @action(detail=False, methods=['get'], url_path='owner')
    def owner_stats(self, request):
        if request.user.role != 'owner':
            return Response({'error': 'Accès refusé : réservé aux propriétaires'}, status=403)
        
        stats = {
            'my_properties': Property.objects.filter(owner=request.user).count(),
            'my_bookings': Booking.objects.filter(property__owner=request.user).count(),
            'my_revenues': Payment.objects.filter(property__owner=request.user).aggregate(total=Sum('amount'))['total'] or 0,
            'subscription_status': Subscription.objects.filter(user=request.user, is_active=True).exists(),
            'visits': Property.objects.filter(owner=request.user).aggregate(total_views=Sum('views'))['total_views'] or 0,  # Assume un champ 'views' dans Property si tu l'ajoutes
            # Ajoute graphs : e.g., bookings par mois
        }
        serializer = StatsSerializer(stats)
        return Response(serializer.data if serializer else stats)

    @action(detail=False, methods=['get'], url_path='client')
    def client_stats(self, request):
        if request.user.role != 'client':
            return Response({'error': 'Accès refusé : réservé aux clients'}, status=403)
        
        stats = {
            'my_bookings': Booking.objects.filter(tenant=request.user).count(),
            'my_payments': Payment.objects.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or 0,
            'active_bookings': Booking.objects.filter(tenant=request.user, status='confirmed').count(),
            'saved_properties': Property.objects.filter(favorites=request.user).count(),  # Assume un ManyToMany 'favorites' dans Property si tu l'ajoutes
            # Historique : e.g., liste récente
        }
        serializer = StatsSerializer(stats)
        return Response(serializer.data if serializer else stats)