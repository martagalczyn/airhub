from datetime import datetime, timedelta
from django.utils.timezone import now
from .models import (
    User, UserRole, UserPermission, UserSession, Location, RegionStatistic,
    Airline, Airport, Flight, FlightClass, FlightRoute, FlightBooking, PassengerDetails,
    Hotel, HotelRoom, HotelAmenity, HotelAmenityMapping, HotelBooking, HotelReview,
    PriceHistory, PriceAlert, PricePrediction, Payment, PaymentMethod, Refund,
    Promotion, LoyaltyProgram, SystemLog, Notification, AuditLog, Subscription, Newsletter, News, MenuItem, Menu,
    Footer, StaticText, FAQ, Contact, Banner
)

# Random data to populate tables, will be changed

def populate_data():
    # Users
    user1 = User.objects.create_user(email="user1@example.com", password="password1", role="user")
    user2 = User.objects.create_user(email="user2@example.com", password="password2", role="admin")

    # User Roles
    role1 = UserRole.objects.create(name="User", description="Regular user role")
    role2 = UserRole.objects.create(name="Admin", description="Administrator role")

    # User Permissions
    UserPermission.objects.create(user=user1, role=role1)
    UserPermission.objects.create(user=user2, role=role2)

    # User Sessions
    UserSession.objects.create(user=user1, ip_address="192.168.1.1")
    UserSession.objects.create(user=user2, ip_address="192.168.1.2")

    # Locations
    location1 = Location.objects.create(city="New York", country="USA")
    location2 = Location.objects.create(city="Paris", country="France")

    # Region Statistics
    RegionStatistic.objects.create(location=location1, flight_bookings_count=10, hotel_bookings_count=5)
    RegionStatistic.objects.create(location=location2, flight_bookings_count=15, hotel_bookings_count=8)

    # Airlines
    airline1 = Airline.objects.create(name="Airline 1", iata_code="A1")
    airline2 = Airline.objects.create(name="Airline 2", iata_code="A2")

    # Airports
    airport1 = Airport.objects.create(name="Airport 1", iata_code="AP1", location=location1)
    airport2 = Airport.objects.create(name="Airport 2", iata_code="AP2", location=location2)

    # Flights
    flight1 = Flight.objects.create(
        flight_number="F1001", airline=airline1, departure_airport=airport1, arrival_airport=airport2,
        departure_time=now(), arrival_time=now() + timedelta(hours=2), base_price=100.00
    )
    flight2 = Flight.objects.create(
        flight_number="F1002", airline=airline2, departure_airport=airport2, arrival_airport=airport1,
        departure_time=now(), arrival_time=now() + timedelta(hours=3), base_price=150.00
    )

    # Flight Classes
    FlightClass.objects.create(flight=flight1, class_type="economy", additional_cost_percentage=10.00)
    FlightClass.objects.create(flight=flight2, class_type="business", additional_cost_percentage=20.00)

    # Flight Routes
    FlightRoute.objects.create(departure_airport=airport1, arrival_airport=airport2, distance_km=500)
    FlightRoute.objects.create(departure_airport=airport2, arrival_airport=airport1, distance_km=500)

    # Flight Bookings
    booking1 = FlightBooking.objects.create(user=user1, flight=flight1, passengers=1, status="confirmed")
    booking2 = FlightBooking.objects.create(user=user2, flight=flight2, passengers=2, status="cancelled")

    # Passenger Details
    PassengerDetails.objects.create(flight_booking=booking1, name="John", surname="Doe", passport_number="P123", nationality="USA")
    PassengerDetails.objects.create(flight_booking=booking2, name="Jane", surname="Doe", passport_number="P124", nationality="FRA")

    # Hotels
    hotel1 = Hotel.objects.create(name="Hotel 1", location=location1, stars=5, price_per_night=200.00)
    hotel2 = Hotel.objects.create(name="Hotel 2", location=location2, stars=4, price_per_night=150.00)

    # Hotel Rooms
    HotelRoom.objects.create(hotel=hotel1, room_type="Suite", base_price=300.00, max_occupancy=2)
    HotelRoom.objects.create(hotel=hotel2, room_type="Deluxe", base_price=200.00, max_occupancy=3)

    # Hotel Amenities
    amenity1 = HotelAmenity.objects.create(name="WiFi")
    amenity2 = HotelAmenity.objects.create(name="Pool")

    # Hotel Amenity Mappings
    HotelAmenityMapping.objects.create(hotel=hotel1, amenity=amenity1)
    HotelAmenityMapping.objects.create(hotel=hotel2, amenity=amenity2)

    # Hotel Bookings
    HotelBooking.objects.create(user=user1, hotel=hotel1, check_in_date=datetime.today(), check_out_date=datetime.today() + timedelta(days=2), num_people=1, status="confirmed")
    HotelBooking.objects.create(user=user2, hotel=hotel2, check_in_date=datetime.today(), check_out_date=datetime.today() + timedelta(days=3), num_people=2, status="cancelled")

    # Hotel Reviews
    HotelReview.objects.create(hotel=hotel1, user=user1, rating=5, comment="Excellent")
    HotelReview.objects.create(hotel=hotel2, user=user2, rating=4, comment="Very good")

    # Prices
    PriceHistory.objects.create(item_type="flight", item_id=flight1.id, previous_price=120.00, new_price=100.00)
    PriceAlert.objects.create(user=user1, item_type="hotel", item_id=hotel1.id, desired_price=180.00, status="active")
    PricePrediction.objects.create(item_type="flight", item_id=flight2.id, predicted_price=140.00)

    # Payments
    method1 = PaymentMethod.objects.create(name="Credit Card", description="Visa/Mastercard")
    method2 = PaymentMethod.objects.create(name="PayPal", description="Online payment system")
    payment1 = Payment.objects.create(user=user1, amount=300.00, method=method1, status="completed")
    Payment.objects.create(user=user2, amount=450.00, method=method2, status="pending")

    # Refunds
    Refund.objects.create(payment=payment1, refund_amount=100.00)

    # Promotions
    Promotion.objects.create(name="Promo 1", discount_percentage=10.00)
    Promotion.objects.create(name="Promo 2", discount_percentage=15.00)

    # Loyalty Programs
    LoyaltyProgram.objects.create(user=user1, points=100, tier="silver")
    LoyaltyProgram.objects.create(user=user2, points=200, tier="gold")

    # Logs and Notifications
    SystemLog.objects.create(event_type="user_login", user=user1, event_description="User logged in")
    SystemLog.objects.create(event_type="booking_created", user=user2, event_description="Booking created")

    Notification.objects.create(user=user1, notification_type="promotion", message="Promo message", status="sent")
    Notification.objects.create(user=user2, notification_type="price_alert", message="Price Alert message", status="pending")

    AuditLog.objects.create(user=user1, action_type="create", table_name="Flight", record_id=flight1.id, description="Created flight")
    AuditLog.objects.create(user=user2, action_type="update", table_name="Hotel", record_id=hotel1.id, description="Updated hotel")

    # Subscriptions and Newsletters
    Subscription.objects.create(user=user1, subscription_type="newsletter", is_active=True)
    Subscription.objects.create(user=user2, subscription_type="price_alerts", is_active=False)

    Newsletter.objects.create(title="Newsletter 1", content="Content for newsletter 1")
    Newsletter.objects.create(title="Newsletter 2", content="Content for newsletter 2")

    News.objects.create(title="News 1", content="Breaking news 1")
    News.objects.create(title="News 2", content="Breaking news 2")

    # Menus and Footer
    menu1 = Menu.objects.create(name="Main Menu", is_active=True)
    MenuItem.objects.create(menu=menu1, title="Home", url="/", display_order=1)
    MenuItem.objects.create(menu=menu1, title="About", url="/about", display_order=2)

    footer1 = Footer.objects.create(name="Footer Section 1", content="Footer content 1", is_active=True)
    footer2 = Footer.objects.create(name="Footer Section 2", content="Footer content 2", is_active=False)

    StaticText.objects.create(key="home_about", content="About us static text")
    StaticText.objects.create(key="contact_info", content="Contact information static text")

    FAQ.objects.create(question="What is this?", answer="This is a test FAQ.")
    FAQ.objects.create(question="How does it work?", answer="It works perfectly.")

    Contact.objects.create(address="123 Main St", phone_number="123-456-7890", email="contact@example.com")
    Contact.objects.create(address="456 Another Rd", phone_number="987-654-3210", email="info@example.com")

    Banner.objects.create(title="Banner 1", link="http://example.com", is_active=True)
    Banner.objects.create(title="Banner 2", link="http://example.com", is_active=False)

    print("Database populated with all models.")

# Run this function
if __name__ == "__main__":
    populate_data()


# How to run this script in shell (py manage.py shell???)"
#from core.populate_data import populate_data
#populate_data()
