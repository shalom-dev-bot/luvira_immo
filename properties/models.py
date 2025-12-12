from django.db import models
from django.contrib.gis.db import models as gis_models
from accounts.models import User

class Property(gis_models.Model):
    CATEGORY_CHOICES = (
        ('house', 'Maison'),
        ('apartment', 'Appartement'),
        ('studio', 'Studio'),
        ('room', 'Chambre'),
        ('hotel', 'Hôtel'),
        ('residence', 'Résidence meublée'),
        ('land', 'Terrain'),
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'owner'},
        verbose_name="Propriétaire"
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        verbose_name="Catégorie"
    )
    title = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(verbose_name="Description")
    price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Prix par nuit"
    )
    price_per_month = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Prix par mois"
    )
    status = models.CharField(
        max_length=20,
        default='available',
        choices=(
            ('available', 'Disponible'),
            ('reserved', 'Réservée'),
            ('unavailable', 'Indisponible')
        ),
        verbose_name="Statut"
    )
    address = models.TextField(verbose_name="Adresse")
    location = gis_models.PointField(srid=4326, verbose_name="Localisation GPS")  # longitude, latitude (WGS84)
    city = models.CharField(max_length=100, verbose_name="Ville")
    neighborhood = models.CharField(max_length=100, verbose_name="Quartier")
    bedrooms = models.IntegerField(default=1, verbose_name="Chambres")
    bathrooms = models.IntegerField(default=1, verbose_name="Salles de bain")
    surface = models.FloatField(null=True, blank=True, verbose_name="Surface (m²)")
    services = models.JSONField(default=list, verbose_name="Services")  # e.g., ['wifi', 'parking', 'eau_24h']
    photos = models.JSONField(default=list, verbose_name="Photos URLs")
    videos = models.JSONField(default=list, verbose_name="Vidéos URLs")
    favorites = models.ManyToManyField(
        User,
        related_name='favorite_properties',
        blank=True,
        verbose_name="Favoris"
    )  # Pour favoris clients
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    is_active = models.BooleanField(default=True, verbose_name="Actif")

    class Meta:
        ordering = ['-created_at']  # Tri par date récente
        verbose_name = "Bien immobilier"
        verbose_name_plural = "Biens immobiliers"

    def __str__(self):
        return self.title

class Review(models.Model):
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="Bien"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Utilisateur"
    )
    rating = models.IntegerField(
        default=0,
        choices=[(i, str(i)) for i in range(1, 6)],  # 1-5 étoiles
        verbose_name="Note"
    )
    comment = models.TextField(blank=True, verbose_name="Commentaire")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    is_approved = models.BooleanField(default=False, verbose_name="Approuvé")  # Admin approuve pour éviter spam

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Avis"
        verbose_name_plural = "Avis"

    def __str__(self):
        return f"Avis {self.rating} pour {self.property.title} par {self.user.username}"