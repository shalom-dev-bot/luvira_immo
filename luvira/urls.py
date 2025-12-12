"""
URL configuration for luvira project.
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import: from my_app import views
    2. Add a URL to urlpatterns: path('', views.home, name='home')
Class-based views
    1. Add an import: from other_app.views import Home
    2. Add a URL to urlpatterns: path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns: path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static  # Pour servir media en dev
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Imports des views de chaque app
from accounts.views import UserViewSet, OwnerRequestViewSet
from properties.views import PropertyViewSet, ReviewViewSet  # Ajout pour reviews
from contracts.views import ContractViewSet, ContractTemplateViewSet
from payments.views import PaymentViewSet
from subscriptions.views import SubscriptionViewSet
from bookings.views import BookingViewSet
from dashboard.views import DashboardViewSet

# Router pour API REST
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'owner-requests', OwnerRequestViewSet)
router.register(r'properties', PropertyViewSet)
router.register(r'contracts', ContractViewSet)
router.register(r'contract-templates', ContractTemplateViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'subscriptions', SubscriptionViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'dashboard', DashboardViewSet, basename='dashboard')
router.register(r'reviews', ReviewViewSet, basename='reviews')  # Ajout pour avis

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),  # Pour login DRF browser
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login JWT
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh JWT
    path('api/payments/webhook/', PaymentViewSet.as_view({'post': 'webhook'}), name='payment-webhook'),
]

# Servir media files en dev mode (photos, docs, etc.)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)