from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib import admin
from .views import user_profile, UserProfileView, BannerView, MenuView, FooterView, ManageUsersView, StaticTextView

from .views import (
    UserViewSet, UserRoleViewSet, UserPermissionViewSet, UserSessionViewSet, LocationViewSet, RegionStatisticViewSet,
    AirlineViewSet, AirportViewSet, FlightViewSet, FlightClassViewSet, FlightRouteViewSet, FlightBookingViewSet,
    PassengerDetailsViewSet, HotelViewSet, HotelRoomViewSet, HotelAmenityViewSet, HotelAmenityMappingViewSet,
    HotelBookingViewSet, HotelReviewViewSet, PriceHistoryViewSet, PriceAlertViewSet, PricePredictionViewSet,
    PaymentViewSet, PaymentMethodViewSet, RefundViewSet, PromotionViewSet, LoyaltyProgramViewSet, SystemLogViewSet,
    NotificationViewSet, AuditLogViewSet, SubscriptionViewSet, NewsletterViewSet, NewsViewSet,
    MenuViewSet, MenuItemViewSet, FooterViewSet, StaticTextViewSet, FAQViewSet, ContactViewSet, BannerViewSet,
    CustomTokenObtainPairView
)

# Initialize the DefaultRouter
router = DefaultRouter()

# Register ViewSets to the router
router.register(r'users', UserViewSet, basename='users')
router.register(r'user-roles', UserRoleViewSet, basename='user-roles')
router.register(r'user-profile', UserRoleViewSet, basename='user-profile')
router.register(r'user-permissions', UserPermissionViewSet, basename='user-permissions')
router.register(r'user-sessions', UserSessionViewSet, basename='user-sessions')
router.register(r'locations', LocationViewSet, basename='locations')
router.register(r'region-statistics', RegionStatisticViewSet, basename='region-statistics')
router.register(r'airlines', AirlineViewSet, basename='airlines')
router.register(r'airports', AirportViewSet, basename='airports')
router.register(r'flights', FlightViewSet, basename='flights')
router.register(r'flight-classes', FlightClassViewSet, basename='flight-classes')
router.register(r'flight-routes', FlightRouteViewSet, basename='flight-routes')
router.register(r'flight-bookings', FlightBookingViewSet, basename='flight-bookings')
router.register(r'passenger-details', PassengerDetailsViewSet, basename='passenger-details')
router.register(r'hotels', HotelViewSet, basename='hotels')
router.register(r'hotel-rooms', HotelRoomViewSet, basename='hotel-rooms')
router.register(r'hotel-amenities', HotelAmenityViewSet, basename='hotel-amenities')
router.register(r'hotel-amenity-mappings', HotelAmenityMappingViewSet, basename='hotel-amenity-mappings')
router.register(r'hotel-bookings', HotelBookingViewSet, basename='hotel-bookings')
router.register(r'hotel-reviews', HotelReviewViewSet, basename='hotel-reviews')
router.register(r'price-history', PriceHistoryViewSet, basename='price-history')
router.register(r'price-alerts', PriceAlertViewSet, basename='price-alerts')
router.register(r'price-predictions', PricePredictionViewSet, basename='price-predictions')
router.register(r'payments', PaymentViewSet, basename='payments')
router.register(r'payment-methods', PaymentMethodViewSet, basename='payment-methods')
router.register(r'refunds', RefundViewSet, basename='refunds')
router.register(r'promotions', PromotionViewSet, basename='promotions')
router.register(r'loyalty-programs', LoyaltyProgramViewSet, basename='loyalty-programs')
router.register(r'system-logs', SystemLogViewSet, basename='system-logs')
router.register(r'notifications', NotificationViewSet, basename='notifications')
router.register(r'audit-logs', AuditLogViewSet, basename='audit-logs')
router.register(r'subscriptions', SubscriptionViewSet, basename='subscriptions')
router.register(r'newsletters', NewsletterViewSet, basename='newsletters')
router.register(r'news', NewsViewSet, basename='news')
router.register(r'menus', MenuViewSet, basename='menus')
router.register(r'menu-items', MenuItemViewSet, basename='menu-item')
router.register(r'footers', FooterViewSet, basename='footers')
router.register(r'faqs', FAQViewSet, basename='faqs')
router.register(r'contacts', ContactViewSet, basename='contacts')
router.register(r'banners', BannerViewSet, basename='banners')
router.register(r'static-texts', StaticTextViewSet, basename='static-texts')

# Schema view for Swagger documentation
schema_view = get_schema_view(
    openapi.Info(
        title="AirHub API",
        default_version='v1',
        description="API documentation for AirHub",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@airhub.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Define urlpatterns
urlpatterns = [
    # JWT Authentication Endpoints
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/profile/', UserProfileView.as_view(), name='user_profile'),

    # Public API endpoints
    # path('banners/', BannerView.as_view(), name='banners'),
    # path('menu-items/', MenuView.as_view(), name='menu_item'),
    path('footer/', FooterView.as_view(), name='footer'),
    # path('static-texts/', StaticTextView.as_view(), name='static-text'),

    # Admin API
    path('admin/users/', ManageUsersView.as_view(), name='manage_users'),

    # Include router-generated endpoints
    path('', include(router.urls)),


]


# Add static files serving in development
# if settings.DEBUG: