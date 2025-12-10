from django.db import models
from accounts.models import User

class Subscription(models.Model):
    PLAN_CHOICES = (
        ('monthly', 'Mensuel'),
        ('quarterly', 'Trimestriel'),
        ('annual', 'Annuel'),
    )
    user       = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'owner'})
    plan       = models.CharField(max_length=20, choices=PLAN_CHOICES)
    start_date = models.DateField()
    end_date   = models.DateField()
    is_active  = models.BooleanField(default=True)
    payment    = models.ForeignKey('payments.Payment', on_delete=models.SET_NULL, null=True)