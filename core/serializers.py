from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import (
    User, UserRole, UserPermission, UserSession, Location, RegionStatistic,
    Airline, Airport, Flight, FlightClass, FlightRoute, FlightBooking, PassengerDetails,
    Hotel, HotelRoom, HotelAmenity, HotelAmenityMapping, HotelBooking, HotelReview,
    PriceHistory, PriceAlert, PricePrediction, Payment, PaymentMethod, Refund,
    Promotion, LoyaltyProgram, SystemLog, Notification, AuditLog, Subscription, Newsletter, News,
    MenuItem, Menu, Banner, FAQ, StaticText, Footer, Contact
)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email = attrs.get('email')
        if not email:
            raise serializers.ValidationError({"email": "This field is required."})
        attrs['username'] = email  # Zamiana email na username
        return super().validate(attrs)


#User serializer
class UserSerializer(serializers.ModelSerializer):
    is_admin = serializers.SerializerMethodField()  # Add an explicit field for admin detection

    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'date_registered', 'is_active', 'is_staff', 'is_admin']  # Include is_admin
        read_only_fields = ['date_registered', 'is_staff', 'is_admin']  # Prevent modification of these fields

    def get_is_admin(self, obj):
        return obj.role == 'admin'  # Logic to determine if a user is an admin


# UserRole Serializer
class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = '__all__'

# UserPermission Serializer
class UserPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPermission
        fields = '__all__'

# UserSession Serializer
class UserSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSession
        fields = '__all__'

# Location Serializer
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

# RegionStatistic Serializer
class RegionStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegionStatistic
        fields = '__all__'

# Airline Serializer
class AirlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airline
        fields = '__all__'

# Airport Serializer
class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = '__all__'

# Flight Serializer
class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = '__all__'

# FlightClass Serializer
class FlightClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightClass
        fields = '__all__'

# FlightRoute Serializer
class FlightRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightRoute
        fields = '__all__'

# FlightBooking Serializer
class FlightBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightBooking
        fields = '__all__'

# PassengerDetails Serializer
class PassengerDetailsSerializer(serializers.ModelSerializer):
    flight_booking = serializers.PrimaryKeyRelatedField(queryset=FlightBooking.objects.all(), allow_null=True)
    class Meta:
        model = PassengerDetails
        fields = '__all__'


# Hotel Serializer
class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'

# HotelRoom Serializer
class HotelRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelRoom
        fields = '__all__'

# HotelAmenity Serializer
class HotelAmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelAmenity
        fields = '__all__'

# HotelAmenityMapping Serializer
class HotelAmenityMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelAmenityMapping
        fields = '__all__'

# HotelBooking Serializer
class HotelBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelBooking
        fields = '__all__'

# HotelReview Serializer
class HotelReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelReview
        fields = '__all__'

# PriceHistory Serializer
class PriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceHistory
        fields = '__all__'

# PriceAlert Serializer
class PriceAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceAlert
        fields = '__all__'

# PricePrediction Serializer
class PricePredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricePrediction
        fields = '__all__'

# Payment Serializer
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

# PaymentMethod Serializer
class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'

# Refund Serializer
class RefundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refund
        fields = '__all__'

# Promotion Serializer
class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = '__all__'

# LoyaltyProgram Serializer
class LoyaltyProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoyaltyProgram
        fields = '__all__'

# SystemLog Serializer
class SystemLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemLog
        fields = '__all__'

# Notification Serializer
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

# AuditLog Serializer
class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'

# Subscription Serializer
class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

# Newsletter Serializer
class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = '__all__'

# News Serializer
class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'

# MenuItem Serializer
class MenuItemSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = MenuItem
        fields = ['id', 'menu', 'title', 'url', 'parent', 'display_order', 'is_active', 'children']

    def get_children(self, obj):
        children = obj.children.filter(is_active=True).order_by('display_order')
        return MenuItemSerializer(children, many=True).data



# Menu Serializer
class MenuSerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True, read_only=True)

    class Meta:
        model = Menu
        fields = ['id', 'name', 'is_active', 'items']

# Footer Serializer
class FooterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Footer
        fields = '__all__'

# StaticText Serializer
class StaticTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticText
        fields = '__all__'  # Wymień pola, które mają być dostępne

# FAQ Serializer
class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'

# Contact Serializer
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

# Banner Serializer
class BannerSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)  # Generuje pełny URL do pliku

    class Meta:
        model = Banner
        fields = '__all__'

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None
