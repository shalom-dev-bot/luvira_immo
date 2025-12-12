from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from africastalking.AfricasTalkingGateway import AfricasTalkingGateway
from .models import Subscription
from datetime import timedelta, date

@shared_task
def send_subscription_alerts():
    today = date.today()
    expiring_soon = Subscription.objects.filter(is_active=True, end_date__lte=today + timedelta(days=7))
    for sub in expiring_soon:
        days_left = (sub.end_date - today).days
        if days_left in [7, 3, 1, 0]:
            # Email
            send_mail(
                'Alerte Abonnement LUVIRA',
                f"Votre abonnement expire dans {days_left} jours. Renouvelez sur le site.",
                settings.EMAIL_HOST_USER,
                [sub.user.email],
            )
            # SMS via AfricasTalking
            gateway = AfricasTalkingGateway(settings.AFRICASTALKING_USERNAME, settings.AFRICASTALKING_API_KEY)
            gateway.sendMessage([sub.user.phone], f"Alerte LUVIRA: Abonnement expire dans {days_left} jours.")
            if days_left == 0:
                sub.is_active = False
                sub.save()