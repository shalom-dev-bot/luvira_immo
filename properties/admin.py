from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Property, Review


@admin.register(Property)
class PropertyAdmin(OSMGeoAdmin):
    list_display = ('title', 'owner', 'category', 'city', 'price_per_month', 'status', 'is_active')
    list_filter = ('category', 'city', 'status', 'is_active')
    search_fields = ('title', 'description', 'owner')
    readonly_fields = ('created_at',)
    # Carte interactive dans l’admin
    default_lon = 11.5021 * 1000000  # Yaoundé (longitude × 1 000 000)
    default_lat = 3.8480 * 1000000   # Yaoundé (latitude × 1 000 000)
    default_zoom = 10


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('property', 'user', 'rating', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'rating')
    search_fields = ('property__title', 'user__username', 'comment')
    actions = ['approve_reviews', 'reject_reviews']

    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
    approve_reviews.short_description = "Approuver les avis"

    def reject_reviews(self, request, queryset):
        queryset.update(is_approved=False)
    reject_reviews.short_description = "Rejeter les avis"