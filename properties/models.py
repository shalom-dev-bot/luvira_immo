from django.db import models
from django.contrib.gis.db import models as gis_models
from accounts.models import User

class Property(models.Model):
    CATEGORY_CHOICES = (
        ('house', 'Maison'),
        ('apartment', 'Appartement'),
        ('studio', 'Studio'),
        ('room', 'Chambre'),
        ('hotel', 'Hôtel'),
        ('residence', 'Résidence meublée'),
        ('land', 'Terrain'),
    )
    owner           = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'owner'})
    category        = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    title           = models.CharField(max_length=200)
    description     = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    status          = models.CharField(max_length=20, default='available', choices=(('available', 'Disponible'), ('reserved', 'Réservée'), ('unavailable', 'Indisponible')))
    address         = models.TextField()
    location        = gis_models.PointField()  # GPS : latitude, longitude
    city            = models.CharField(max_length=100)
    neighborhood    = models.CharField(max_length=100)
    bedrooms        = models.IntegerField(default=1)
    bathrooms       = models.IntegerField(default=1)
    surface         = models.FloatField(null=True)  # m²
    services        = models.JSONField(default=list)  # e.g., ['wifi', 'parking', 'eau_24h']
    photos          = models.JSONField(default=list)  # Liste URLs photos
    videos          = models.JSONField(default=list)  # URLs vidéos/360
    created_at      = models.DateTimeField(auto_now_add=True)
    is_active       = models.BooleanField(default=True)