from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models as gis_models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('owner', 'Propriétaire'),
        ('client', 'Client'),
    )
    role                  = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')
    phone                 = models.CharField(max_length=20, blank=True)
    address               = models.TextField(blank=True)
    cni                   = models.CharField(max_length=50, blank=True)  # Document ID
    birth_date            = models.DateField(null=True, blank=True)
    gender                = models.CharField(max_length=10, blank=True)
    profile_photo         = models.ImageField(upload_to='profiles/', blank=True)
    is_verified           = models.BooleanField(default=False)
    notifications_enabled = models.BooleanField(default=True)

class OwnerRequest(models.Model):
    user                  = models.OneToOneField(User, on_delete=models.CASCADE)
    documents             = models.FileField(upload_to='owner_docs/')  # CNI, titre foncier
    status                = models.CharField(max_length=10, default='pending', choices=(('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')))
    created_at            = models.DateTimeField(auto_now_add=True)