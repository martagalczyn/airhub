from rest_framework import viewsets
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser, FormParser


from .models import (
    User, UserRole, UserPermission, UserSession, Location, RegionStatistic,
    Airline, Airport, Flight, FlightClass, FlightRoute, FlightBooking, PassengerDetails,
    Hotel, HotelRoom, HotelAmenity, HotelAmenityMapping, HotelBooking, HotelReview,
    PriceHistory, PriceAlert, PricePrediction, Payment, PaymentMethod, Refund,
    Promotion, LoyaltyProgram, SystemLog, Notification, AuditLog, Subscription, Newsletter, News, MenuItem, Menu,
    Footer, StaticText, FAQ, Contact, Banner
)
from .serializers import (
    UserSerializer, UserRoleSerializer, UserPermissionSerializer, UserSessionSerializer, LocationSerializer,
    RegionStatisticSerializer,
    AirlineSerializer, AirportSerializer, FlightSerializer, FlightClassSerializer, FlightRouteSerializer,
    FlightBookingSerializer, PassengerDetailsSerializer,
    HotelSerializer, HotelRoomSerializer, HotelAmenitySerializer, HotelAmenityMappingSerializer, HotelBookingSerializer,
    HotelReviewSerializer,
    PriceHistorySerializer, PriceAlertSerializer, PricePredictionSerializer, PaymentSerializer, PaymentMethodSerializer,
    RefundSerializer,
    PromotionSerializer, LoyaltyProgramSerializer, SystemLogSerializer, NotificationSerializer, AuditLogSerializer,
    SubscriptionSerializer, NewsletterSerializer, NewsSerializer, MenuItemSerializer, MenuSerializer, FooterSerializer,
    StaticTextSerializer, FAQSerializer, ContactSerializer, BannerSerializer, CustomTokenObtainPairSerializer
)
from rest_framework_simplejwt.views import TokenObtainPairView


from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class StaticTextView(APIView):
    def get(self, request):
        texts = StaticText.objects.filter(is_active=True)
        serializer = StaticTextSerializer(texts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BannerView(APIView):
    def get(self, request):
        banners = Banner.objects.filter(is_active=True)
        serializer = BannerSerializer(banners, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MenuView(APIView):
    def get(self, request):
        menu_items = MenuItem.objects.filter(is_active=True).order_by("display_order")
        serializer = MenuItemSerializer(menu_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FooterView(APIView):
    def get(self, request):
        footer_sections = Footer.objects.filter(is_active=True).order_by("display_order")
        serializer = FooterSerializer(footer_sections, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ManageUsersView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRoleViewSet(viewsets.ModelViewSet):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer


class UserPermissionViewSet(viewsets.ModelViewSet):
    queryset = UserPermission.objects.all()
    serializer_class = UserPermissionSerializer


# Twórz podobne ViewSety dla wszystkich modeli:
class UserSessionViewSet(viewsets.ModelViewSet):
    queryset = UserSession.objects.all()
    serializer_class = UserSessionSerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class RegionStatisticViewSet(viewsets.ModelViewSet):
    queryset = RegionStatistic.objects.all()
    serializer_class = RegionStatisticSerializer


class AirlineViewSet(viewsets.ModelViewSet):
    queryset = Airline.objects.all()
    serializer_class = AirlineSerializer


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer


class FlightClassViewSet(viewsets.ModelViewSet):
    queryset = FlightClass.objects.all()
    serializer_class = FlightClassSerializer


class FlightRouteViewSet(viewsets.ModelViewSet):
    queryset = FlightRoute.objects.all()
    serializer_class = FlightRouteSerializer


class FlightBookingViewSet(viewsets.ModelViewSet):
    queryset = FlightBooking.objects.all()
    serializer_class = FlightBookingSerializer


class PassengerDetailsViewSet(viewsets.ModelViewSet):
    queryset = PassengerDetails.objects.all()
    serializer_class = PassengerDetailsSerializer


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer


class HotelRoomViewSet(viewsets.ModelViewSet):
    queryset = HotelRoom.objects.all()
    serializer_class = HotelRoomSerializer


class HotelAmenityViewSet(viewsets.ModelViewSet):
    queryset = HotelAmenity.objects.all()
    serializer_class = HotelAmenitySerializer


class HotelAmenityMappingViewSet(viewsets.ModelViewSet):
    queryset = HotelAmenityMapping.objects.all()
    serializer_class = HotelAmenityMappingSerializer


class HotelBookingViewSet(viewsets.ModelViewSet):
    queryset = HotelBooking.objects.all()
    serializer_class = HotelBookingSerializer


class HotelReviewViewSet(viewsets.ModelViewSet):
    queryset = HotelReview.objects.all()
    serializer_class = HotelReviewSerializer


class PriceHistoryViewSet(viewsets.ModelViewSet):
    queryset = PriceHistory.objects.all()
    serializer_class = PriceHistorySerializer


class PriceAlertViewSet(viewsets.ModelViewSet):
    queryset = PriceAlert.objects.all()
    serializer_class = PriceAlertSerializer


class PricePredictionViewSet(viewsets.ModelViewSet):
    queryset = PricePrediction.objects.all()
    serializer_class = PricePredictionSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentMethodViewSet(viewsets.ModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer


class RefundViewSet(viewsets.ModelViewSet):
    queryset = Refund.objects.all()
    serializer_class = RefundSerializer


class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.filter(is_active=True)
    serializer_class = PromotionSerializer


class LoyaltyProgramViewSet(viewsets.ModelViewSet):
    queryset = LoyaltyProgram.objects.all()
    serializer_class = LoyaltyProgramSerializer


class SystemLogViewSet(viewsets.ModelViewSet):
    queryset = SystemLog.objects.all()
    serializer_class = SystemLogSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


class AuditLogViewSet(viewsets.ModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


class NewsletterViewSet(viewsets.ModelViewSet):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.filter(is_active=True)
    serializer_class = NewsSerializer

class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.filter(is_active=True)
    serializer_class = MenuSerializer

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.filter(is_active=True).order_by('display_order')
    serializer_class = MenuItemSerializer

class FooterViewSet(viewsets.ModelViewSet):
    queryset = Footer.objects.filter(is_active=True).order_by('display_order')
    serializer_class = FooterSerializer

class StaticTextViewSet(viewsets.ModelViewSet):
    queryset = StaticText.objects.filter(is_active=True)  # Pobieraj tylko aktywne teksty
    serializer_class = StaticTextSerializer

class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.filter(is_active=True).order_by('display_order')
    serializer_class = FAQSerializer

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.filter(is_active=True)
    serializer_class = ContactSerializer

class BannerViewSet(viewsets.ModelViewSet):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_context(self):
        return {'request': self.request}
    #
    # def create(self, request, *args, **kwargs):
    #     print("Request data:", request.data)  # Debugowanie danych wejściowych
    #     return super().create(request, *args, **kwargs)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """
    Zwraca dane zalogowanego użytkownika.
    """
    user = request.user  # Pobierz zalogowanego użytkownika
    serializer = UserSerializer(user)  # Serializuj dane użytkownika
    return Response(serializer.data)

@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(username=email, password=password)  # Authenticate user

    if user is not None:
        refresh = RefreshToken.for_user(user)  # Generate tokens
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })
    return Response({"detail": "Invalid email or password"}, status=401)