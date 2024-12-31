from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib import admin
from core.views import CustomTokenObtainPairView, UserViewSet, UserRoleViewSet, UserProfileView, BannerView, MenuView, \
    FooterView, ManageUsersView
from django.conf import settings
from django.conf.urls.static import static

# Initialize the DefaultRouter for automatic URL routing
router = DefaultRouter()

# Register the User and UserRole viewsets
router.register(r'users', UserViewSet, basename='user')
router.register(r'user-roles', UserRoleViewSet, basename='user-role')

urlpatterns = [
    # Django admin panel
    path('admin/', admin.site.urls),

    # Include core app URLs
    path('api/', include('core.urls')),
]

    # path('auth/profile/', UserProfileView.as_view(), name='user_profile'),

    # # Publiczne API
    # path('banners/', BannerView.as_view(), name='banners'),
    # path('menu-items/', MenuView.as_view(), name='menu_items'),
    # path('footer/', FooterView.as_view(), name='footer'),
    #
    # # Admin API
    # path('admin/users/', ManageUsersView.as_view(), name='manage_users'),

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)