from django.db import models
from accounts.models import User
from properties.models import Property

class Payment(models.Model):
    METHOD_CHOICES = (
        ('mtn', 'MTN Mobile Money'),
        ('orange', 'Orange Money'),
        ('paypal', 'PayPal'),
        ('card', 'Carte bancaire'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    status = models.CharField(max_length=20, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)