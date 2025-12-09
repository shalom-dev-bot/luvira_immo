import stripe
from django.conf import settings
from django.http import HttpResponse
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Payment
from .serializers import PaymentSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Payment.objects.all()
        return Payment.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'], url_path='create-checkout-session')
    def create_checkout_session(self, request):
        # Crée session Stripe pour paiement (ex: réservation)
        amount = request.data.get('amount')  # En FCFA ou EUR
        method = request.data.get('method')
        if method == 'card' or method == 'paypal':
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],  # Ajoute 'paypal' si intégré
                line_items=[{
                    'price_data': {
                        'currency': 'xaf',  # FCFA pour Cameroun
                        'product_data': {'name': 'Réservation LUVIRA'},
                        'unit_amount': int(amount * 100),  # En centimes
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='https://ton-site/success',  # Redirect après succès
                cancel_url='https://ton-site/cancel',
            )
            # Sauvegarde paiement pending
            payment = Payment.objects.create(
                user=request.user,
                amount=amount,
                method=method,
                transaction_id=session.id
            )
            return Response({'id': session.id})
        # Placeholder pour MTN/Orange : Utilise requests.post à leur API
        return Response({'error': 'Méthode non supportée'}, status=400)

    @action(detail=False, methods=['post'], url_path='webhook')
    def webhook(self, request):
        # Gère webhook Stripe pour update status
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET  # Ajoute dans .env
            )
        except ValueError:
            return HttpResponse(status=400)
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            payment = Payment.objects.get(transaction_id=session.id)
            payment.status = 'completed'
            payment.save()
            # Envoie notification, update booking, etc.
        return HttpResponse(status=200)