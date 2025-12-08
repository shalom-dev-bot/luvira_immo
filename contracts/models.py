from django.db import models
from accounts.models import User
from properties.models import Property

class ContractTemplate(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'admin'})
    title = models.CharField(max_length=200)
    content = models.TextField()  # Modèle de contrat

class Contract(models.Model):
    template = models.ForeignKey(ContractTemplate, on_delete=models.SET_NULL, null=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, related_name='owner_contracts', on_delete=models.CASCADE)
    tenant = models.ForeignKey(User, related_name='tenant_contracts', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    signed_by_owner = models.BooleanField(default=False)
    signed_by_tenant = models.BooleanField(default=False)
    pdf_file = models.FileField(upload_to='contracts/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)