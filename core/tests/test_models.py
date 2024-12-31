from django.test import TestCase
from django.utils.timezone import now
from datetime import timedelta
from core.models import (
    User, UserRole, UserPermission, UserSession, Location, RegionStatistic,
    Airline, Airport, Flight, FlightClass, FlightRoute, FlightBooking, PassengerDetails,
    Hotel, HotelRoom, HotelAmenity, HotelAmenityMapping, HotelBooking, HotelReview,
    PriceHistory, PriceAlert, PricePrediction, Payment, PaymentMethod, Refund,
    Promotion, LoyaltyProgram, SystemLog, Notification, AuditLog, Subscription, Newsletter
)

#Add more tests here and to test_api.py, create ne tests files, do it at the end


class ModelTests(TestCase):

    def test_user_creation(self):
        role = UserRole.objects.create(name="Admin", description="Administrator role")
        user = User.objects.create(username="testuser", email="test@example.com", role=role)
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.role.name, "Admin")

    def test_user_role_creation(self):
        role = UserRole.objects.create(name="Customer", description="Customer role")
        self.assertEqual(role.name, "Customer")

    def test_user_permission_creation(self):
        role = UserRole.objects.create(name="Customer", description="Customer role")
        user = User.objects.create(username="testuser", email="test@example.com", role=role)
        permission = UserPermission.objects.create(user=user, role=role)
        self.assertEqual(permission.user.username, "testuser")

    def test_user_session_creation(self):
        user = User.objects.create(username="testuser", email="test@example.com")
        session = UserSession.objects.create(user=user, ip_address="192.168.1.1")
        self.assertEqual(session.user.username, "testuser")

    def test_location_creation(self):
        location = Location.objects.create(city="Warsaw", country="Poland")
        self.assertEqual(location.city, "Warsaw")

    def test_region_statistic_creation(self):
        location = Location.objects.create(city="Warsaw", country="Poland")
        stat = RegionStatistic.objects.create(location=location, flight_bookings_count=10, hotel_bookings_count=5)
        self.assertEqual(stat.flight_bookings_count, 10)

    def test_airline_creation(self):
        airline = Airline.objects.create(name="LOT Polish Airlines", iata_code="LO")
        self.assertEqual(airline.name, "LOT Polish Airlines")

    def test_airport_creation(self):
        location = Location.objects.create(city="Warsaw", country="Poland")
        airport = Airport.objects.create(name="Chopin Airport", iata_code="WAW", location=location)
        self.assertEqual(airport.name, "Chopin Airport")

    def test_flight_creation(self):
        airline = Airline.objects.create(name="LOT Polish Airlines", iata_code="LO")
        location = Location.objects.create(city="Warsaw", country="Poland")
        airport = Airport.objects.create(name="Chopin Airport", iata_code="WAW", location=location)
        flight = Flight.objects.create(
            flight_number="LO123",
            airline=airline,
            departure_airport=airport,
            arrival_airport=airport,
            departure_time=now(),
            arrival_time=now() + timedelta(hours=2),
            base_price=300.00
        )
        self.assertEqual(flight.flight_number, "LO123")

    def test_flight_class_creation(self):
        airline = Airline.objects.create(name="LOT Polish Airlines", iata_code="LO")
        location = Location.objects.create(city="Warsaw", country="Poland")
        airport = Airport.objects.create(name="Chopin Airport", iata_code="WAW", location=location)
        flight = Flight.objects.create(
            flight_number="LO123",
            airline=airline,
            departure_airport=airport,
            arrival_airport=airport,
            departure_time=now(),
            arrival_time=now() + timedelta(hours=2),
            base_price=300.00
        )
        flight_class = FlightClass.objects.create(flight=flight, class_type="economy", additional_cost_percentage=10.0)
        self.assertEqual(flight_class.class_type, "economy")

    def test_flight_route_creation(self):
        location = Location.objects.create(city="Warsaw", country="Poland")
        airport1 = Airport.objects.create(name="Chopin Airport", iata_code="WAW", location=location)
        airport2 = Airport.objects.create(name="Modlin Airport", iata_code="MOD", location=location)
        route = FlightRoute.objects.create(departure_airport=airport1, arrival_airport=airport2, distance_km=50)
        self.assertEqual(route.distance_km, 50)

    def test_flight_booking_creation(self):
        airline = Airline.objects.create(name="LOT Polish Airlines", iata_code="LO")
        location = Location.objects.create(city="Warsaw", country="Poland")
        airport = Airport.objects.create(name="Chopin Airport", iata_code="WAW", location=location)
        flight = Flight.objects.create(
            flight_number="LO123",
            airline=airline,
            departure_airport=airport,
            arrival_airport=airport,
            departure_time=now(),
            arrival_time=now() + timedelta(hours=2),
            base_price=300.00
        )
        user = User.objects.create(username="testuser", email="test@example.com")
        booking = FlightBooking.objects.create(user=user, flight=flight, passengers=2, status="confirmed")
        self.assertEqual(booking.passengers, 2)

    def test_passenger_details_creation(self):
        user = User.objects.create(username="testuser", email="test@example.com")
        flight = Flight.objects.create(
            flight_number="LO123",
            airline=Airline.objects.create(name="LOT", iata_code="LO"),
            departure_airport=Airport.objects.create(name="WAW", iata_code="WAW",
                                                     location=Location.objects.create(city="Warsaw", country="Poland")),
            arrival_airport=Airport.objects.create(name="KRK", iata_code="KRK",
                                                   location=Location.objects.create(city="Krakow", country="Poland")),
            departure_time=now(),
            arrival_time=now() + timedelta(hours=2),
            base_price=300.00
        )
        booking = FlightBooking.objects.create(user=user, flight=flight, passengers=1, status="confirmed")
        passenger = PassengerDetails.objects.create(flight_booking=booking, name="John", surname="Doe",
                                                    passport_number="123456", nationality="Polish")
        self.assertEqual(passenger.name, "John")

    def test_hotel_creation(self):
        location = Location.objects.create(city="Warsaw", country="Poland")
        hotel = Hotel.objects.create(name="Hotel Warsaw", location=location, stars=5, price_per_night=100.00)
        self.assertEqual(hotel.name, "Hotel Warsaw")

    def test_hotel_booking_creation(self):
        location = Location.objects.create(city="Warsaw", country="Poland")
        hotel = Hotel.objects.create(name="Hotel Warsaw", location=location, stars=5, price_per_night=100.00)
        user = User.objects.create(username="testuser", email="test@example.com")
        booking = HotelBooking.objects.create(
            user=user, hotel=hotel, check_in_date="2024-12-01", check_out_date="2024-12-05", num_people=2,
            status="confirmed"
        )
        self.assertEqual(booking.num_people, 2)

    def test_hotel_room_creation(self):
        hotel = Hotel.objects.create(name="Hotel Warsaw", location=None, stars=5, price_per_night=100.00)
        room = HotelRoom.objects.create(hotel=hotel, room_type="Single", base_price=120.00, max_occupancy=1)
        self.assertEqual(room.room_type, "Single")
        self.assertEqual(room.max_occupancy, 1)

    def test_hotel_amenity_creation(self):
        amenity = HotelAmenity.objects.create(name="Free WiFi")
        self.assertEqual(amenity.name, "Free WiFi")

    def test_hotel_amenity_mapping_creation(self):
        hotel = Hotel.objects.create(name="Hotel Warsaw", location=None, stars=5, price_per_night=100.00)
        amenity = HotelAmenity.objects.create(name="Free WiFi")
        mapping = HotelAmenityMapping.objects.create(hotel=hotel, amenity=amenity)
        self.assertEqual(mapping.hotel.name, "Hotel Warsaw")
        self.assertEqual(mapping.amenity.name, "Free WiFi")

    def test_hotel_review_creation(self):
        hotel = Hotel.objects.create(name="Hotel Warsaw", location=None, stars=5, price_per_night=100.00)
        user = User.objects.create(username="testuser", email="test@example.com")
        review = HotelReview.objects.create(hotel=hotel, user=user, rating=4, comment="Great stay!")
        self.assertEqual(review.rating, 4)
        self.assertEqual(review.comment, "Great stay!")

    def test_price_history_creation(self):
        history = PriceHistory.objects.create(
            item_type="flight", item_id=1, previous_price=200.00, new_price=180.00
        )
        self.assertEqual(history.item_type, "flight")
        self.assertEqual(history.previous_price, 200.00)

    def test_price_alert_creation(self):
        user = User.objects.create(username="testuser", email="test@example.com")
        alert = PriceAlert.objects.create(
            user=user, item_type="hotel", item_id=1, desired_price=150.00, status="active"
        )
        self.assertEqual(alert.status, "active")
        self.assertEqual(alert.desired_price, 150.00)

    def test_price_prediction_creation(self):
        prediction = PricePrediction.objects.create(
            item_type="flight", item_id=1, predicted_price=190.00
        )
        self.assertEqual(prediction.item_type, "flight")
        self.assertEqual(prediction.predicted_price, 190.00)

    def test_payment_creation(self):
        user = User.objects.create(username="testuser", email="test@example.com")
        method = PaymentMethod.objects.create(name="Credit Card", description="Visa or Mastercard")
        payment = Payment.objects.create(user=user, amount=300.00, method=method, status="completed")
        self.assertEqual(payment.amount, 300.00)
        self.assertEqual(payment.status, "completed")

    def test_payment_method_creation(self):
        method = PaymentMethod.objects.create(name="PayPal", description="Online payment")
        self.assertEqual(method.name, "PayPal")

    def test_refund_creation(self):
        user = User.objects.create(username="testuser", email="test@example.com")
        method = PaymentMethod.objects.create(name="Credit Card", description="Visa or Mastercard")
        payment = Payment.objects.create(user=user, amount=300.00, method=method, status="completed")
        refund = Refund.objects.create(payment=payment, refund_amount=100.00)
        self.assertEqual(refund.refund_amount, 100.00)

    def test_promotion_creation(self):
        promotion = Promotion.objects.create(
            name="Summer Discount", description="20% off on flights", discount_percentage=20.0, is_active=True
        )
        self.assertEqual(promotion.name, "Summer Discount")
        self.assertTrue(promotion.is_active)

    def test_loyalty_program_creation(self):
        user = User.objects.create(username="testuser", email="test@example.com")
        loyalty = LoyaltyProgram.objects.create(user=user, points=500, tier="gold")
        self.assertEqual(loyalty.points, 500)
        self.assertEqual(loyalty.tier, "gold")

    def test_system_log_creation(self):
        user = User.objects.create(username="testuser", email="test@example.com")
        log = SystemLog.objects.create(
            event_type="user_login", user=user, event_description="User logged in"
        )
        self.assertEqual(log.event_type, "user_login")
        self.assertEqual(log.event_description, "User logged in")

    def test_notification_creation(self):
        user = User.objects.create(username="testuser", email="test@example.com")
        notification = Notification.objects.create(
            user=user, notification_type="price_alert", message="Price dropped!"
        )
        self.assertEqual(notification.message, "Price dropped!")

    def test_audit_log_creation(self):
        user = User.objects.create(username="testuser", email="test@example.com")
        audit = AuditLog.objects.create(
            user=user, action_type="create", table_name="Flight", record_id=1
        )
        self.assertEqual(audit.action_type, "create")
        self.assertEqual(audit.table_name, "Flight")

    def test_subscription_creation(self):
        user = User.objects.create(username="testuser", email="test@example.com")
        subscription = Subscription.objects.create(user=user, subscription_type="newsletter", is_active=True)
        self.assertTrue(subscription.is_active)

    def test_newsletter_creation(self):
        newsletter = Newsletter.objects.create(title="Travel Deals", content="Amazing offers await!")
        self.assertEqual(newsletter.title, "Travel Deals")
