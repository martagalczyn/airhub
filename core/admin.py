from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from .models import (
    User, UserRole, UserPermission, UserSession, Location, RegionStatistic,
    Airline, Airport, Flight, FlightClass, FlightRoute, FlightBooking, PassengerDetails,
    Hotel, HotelRoom, HotelAmenity, HotelAmenityMapping, HotelBooking, HotelReview,
    PriceHistory, PriceAlert, PricePrediction, Payment, PaymentMethod, Refund,
    Promotion, LoyaltyProgram, SystemLog, Notification, AuditLog, Subscription, Newsletter, News,
    MenuItem, Menu, Footer, StaticText, FAQ, Contact, Banner
)

# Custom User Admin
@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    list_display = ('email', 'is_staff', 'is_superuser', 'role', 'date_registered')
    list_filter = ('is_staff', 'is_superuser', 'role', 'date_registered')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Personal Info', {'fields': ('role', 'date_registered')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role'),
        }),
    )
    ordering = ('email',)
    search_fields = ('email',)


# Custom UserRole Admin
@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


# Remaining model admin registrations
@admin.register(UserPermission)
class UserPermissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    search_fields = ('user__email', 'role__name')


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_start', 'session_end', 'ip_address')
    list_filter = ('session_start', 'session_end')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('city', 'country')
    search_fields = ('city', 'country')


@admin.register(RegionStatistic)
class RegionStatisticAdmin(admin.ModelAdmin):
    list_display = ('location', 'flight_bookings_count', 'hotel_bookings_count', 'last_updated')
    list_filter = ('last_updated',)


@admin.register(Airline)
class AirlineAdmin(admin.ModelAdmin):
    list_display = ('name', 'iata_code')
    search_fields = ('name', 'iata_code')


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ('name', 'iata_code', 'location')
    search_fields = ('name', 'iata_code')
    list_filter = ('location',)


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_number', 'airline', 'departure_airport', 'arrival_airport', 'departure_time', 'arrival_time', 'base_price')
    list_filter = ('departure_time', 'arrival_time', 'airline')
    search_fields = ('flight_number',)


@admin.register(FlightClass)
class FlightClassAdmin(admin.ModelAdmin):
    list_display = ('flight', 'class_type', 'additional_cost_percentage')
    list_filter = ('class_type',)


@admin.register(FlightRoute)
class FlightRouteAdmin(admin.ModelAdmin):
    list_display = ('departure_airport', 'arrival_airport', 'distance_km')
    search_fields = ('departure_airport__name', 'arrival_airport__name')


@admin.register(FlightBooking)
class FlightBookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'flight', 'passengers', 'booking_date', 'status')
    list_filter = ('booking_date', 'status')
    search_fields = ('user__email', 'flight__flight_number')


@admin.register(PassengerDetails)
class PassengerDetailsAdmin(admin.ModelAdmin):
    list_display = ('flight_booking', 'name', 'surname', 'passport_number', 'nationality')
    search_fields = ('name', 'surname', 'passport_number')


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'stars', 'price_per_night')
    search_fields = ('name', 'location__city', 'location__country')
    list_filter = ('stars',)


@admin.register(HotelRoom)
class HotelRoomAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'room_type', 'base_price', 'max_occupancy')
    list_filter = ('room_type', 'max_occupancy')


@admin.register(HotelAmenity)
class HotelAmenityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(HotelAmenityMapping)
class HotelAmenityMappingAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'amenity')


@admin.register(HotelBooking)
class HotelBookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'hotel', 'check_in_date', 'check_out_date', 'num_people', 'status')
    list_filter = ('status', 'check_in_date', 'check_out_date')
    search_fields = ('user__email', 'hotel__name')


@admin.register(HotelReview)
class HotelReviewAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'user', 'rating', 'review_date')
    list_filter = ('rating', 'review_date')
    search_fields = ('hotel__name', 'user__email')


@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ('item_type', 'item_id', 'previous_price', 'new_price', 'change_date')
    list_filter = ('item_type', 'change_date')


@admin.register(PriceAlert)
class PriceAlertAdmin(admin.ModelAdmin):
    list_display = ('user', 'item_type', 'item_id', 'desired_price', 'status')
    list_filter = ('status', 'item_type')


@admin.register(PricePrediction)
class PricePredictionAdmin(admin.ModelAdmin):
    list_display = ('item_type', 'item_id', 'predicted_price', 'prediction_date')
    list_filter = ('item_type', 'prediction_date')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'method', 'date', 'status')
    list_filter = ('status', 'date')


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ('payment', 'refund_amount', 'refund_date')
    list_filter = ('refund_date',)


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('name', 'discount_percentage', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('name',)


@admin.register(LoyaltyProgram)
class LoyaltyProgramAdmin(admin.ModelAdmin):
    list_display = ('user', 'points', 'tier')
    list_filter = ('tier',)


@admin.register(SystemLog)
class SystemLogAdmin(admin.ModelAdmin):
    list_display = ('event_type', 'user', 'created_at')
    list_filter = ('event_type', 'created_at')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'created_at')
    list_filter = ('notification_type', 'created_at')


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action_type', 'action_timestamp', 'table_name')
    list_filter = ('action_type', 'action_timestamp')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscription_type', 'start_date', 'is_active')
    list_filter = ('subscription_type', 'is_active')


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('title', 'sent_date')
    search_fields = ('title',)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'content')


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    search_fields = ('name',)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'menu', 'parent', 'display_order', 'is_active')
    list_filter = ('menu', 'is_active')
    ordering = ('menu', 'display_order')
    search_fields = ('title', 'url')


@admin.register(Footer)
class FooterAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'display_order')
    ordering = ('display_order',)
    search_fields = ('name',)


@admin.register(StaticText)
class StaticTextAdmin(admin.ModelAdmin):
    list_display = ('key', 'content', 'is_active')
    search_fields = ('key',)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'is_active', 'display_order')
    ordering = ('display_order',)
    search_fields = ('question', 'answer')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'email', 'is_active')
    search_fields = ('address', 'email', 'phone_number')


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'display_order')
    ordering = ('display_order',)
    search_fields = ('title',)
