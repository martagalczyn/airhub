from rest_framework.test import APITestCase
from rest_framework import status
from core.models import (
    User, UserRole, UserPermission, UserSession, Location, RegionStatistic,
    Airline, Airport, Flight, FlightClass, FlightRoute, FlightBooking, PassengerDetails,
    Hotel, HotelRoom, HotelAmenity, HotelAmenityMapping, HotelBooking, HotelReview,
    PriceHistory, PriceAlert, PricePrediction, Payment, PaymentMethod, Refund,
    Promotion, LoyaltyProgram, SystemLog, Notification, AuditLog, Subscription, Newsletter
)

#Add more tests, here


class APITests(APITestCase):

    # -------------------- CRUD Test Template --------------------
    def create_and_list_test(self, url, create_data):
        # Create an object
        response = self.client.post(url, create_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # List all objects
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    # -------------------- User and Roles --------------------
    def test_user_crud(self):
        self.create_and_list_test("/api/users/", {"username": "testuser", "email": "test@example.com"})

    def test_user_role_crud(self):
        self.create_and_list_test("/api/user-roles/", {"name": "Admin", "description": "Admin role"})

    def test_user_permission_crud(self):
        role = UserRole.objects.create(name="Admin", description="Administrator role")
        user = User.objects.create(username="testuser", email="test@example.com")
        self.create_and_list_test("/api/user-permissions/", {"user": user.id, "role": role.id})

    def test_user_session_crud(self):
        user = User.objects.create(username="testuser", email="test@example.com")
        self.create_and_list_test("/api/user-sessions/", {"user": user.id, "ip_address": "192.168.1.1"})

    # -------------------- Locations and Statistics --------------------
    def test_location_crud(self):
        self.create_and_list_test("/api/locations/", {"city": "Warsaw", "country": "Poland"})

    def test_region_statistic_crud(self):
        location = Location.objects.create(city="Warsaw", country="Poland")
        self.create_and_list_test("/api/region-statistics/", {"location": location.id, "flight_bookings_count": 10})

    # -------------------- Airlines, Airports, and Flights --------------------
    def test_airline_crud(self):
        self.create_and_list_test("/api/airlines/", {"name": "LOT Polish Airlines", "iata_code": "LO"})

    def test_airport_crud(self):
        location = Location.objects.create(city="Warsaw", country="Poland")
        self.create_and_list_test("/api/airports/",
                                  {"name": "Chopin Airport", "iata_code": "WAW", "location": location.id})

    def test_flight_crud(self):
        airline = Airline.objects.create(name="LOT Polish Airlines", iata_code="LO")
        location = Location.objects.create(city="Warsaw", country="Poland")
        airport = Airport.objects.create(name="Chopin Airport", iata_code="WAW", location=location)
        self.create_and_list_test("/api/flights/", {
            "flight_number": "LO123",
            "airline": airline.id,
            "departure_airport": airport.id,
            "arrival_airport": airport.id,
            "departure_time": "2024-12-01T10:00:00Z",
            "arrival_time": "2024-12-01T12:00:00Z",
            "base_price": 300.00
        })

    def test_flight_class_crud(self):
        flight = Flight.objects.create(flight_number="LO123",
                                       airline=Airline.objects.create(name="LOT", iata_code="LO"),
                                       departure_airport=Airport.objects.create(name="WAW", iata_code="WAW",
                                                                                location=Location.objects.create(
                                                                                    city="Warsaw", country="Poland")),
                                       arrival_airport=Airport.objects.create(name="KRK", iata_code="KRK",
                                                                              location=Location.objects.create(
                                                                                  city="Krakow", country="Poland")),
                                       departure_time="2024-12-01T10:00:00Z", arrival_time="2024-12-01T12:00:00Z",
                                       base_price=300.00)
        self.create_and_list_test("/api/flight-classes/",
                                  {"flight": flight.id, "class_type": "economy", "additional_cost_percentage": 10.00})

    def test_flight_route_crud(self):
        airport1 = Airport.objects.create(name="WAW", iata_code="WAW",
                                          location=Location.objects.create(city="Warsaw", country="Poland"))
        airport2 = Airport.objects.create(name="KRK", iata_code="KRK",
                                          location=Location.objects.create(city="Krakow", country="Poland"))
        self.create_and_list_test("/api/flight-routes/",
                                  {"departure_airport": airport1.id, "arrival_airport": airport2.id,
                                   "distance_km": 300})

    # -------------------- Flight Booking and Passenger Details --------------------
    def test_flight_booking_crud(self):
        user = User.objects.create(username="testuser", email="test@example.com")
        flight = Flight.objects.create(flight_number="LO123",
                                       airline=Airline.objects.create(name="LOT", iata_code="LO"),
                                       departure_airport=Airport.objects.create(name="WAW", iata_code="WAW",
                                                                                location=Location.objects.create(
                                                                                    city="Warsaw", country="Poland")),
                                       arrival_airport=Airport.objects.create(name="KRK", iata_code="KRK",
                                                                              location=Location.objects.create(
                                                                                  city="Krakow", country="Poland")),
                                       departure_time="2024-12-01T10:00:00Z", arrival_time="2024-12-01T12:00:00Z",
                                       base_price=300.00)
        self.create_and_list_test("/api/flight-bookings/",
                                  {"user": user.id, "flight": flight.id, "passengers": 2, "status": "confirmed"})

    def test_passenger_details_crud(self):
        booking = FlightBooking.objects.create(user=User.objects.create(username="testuser", email="test@example.com"),
                                               flight=Flight.objects.create(flight_number="LO123",
                                                                            airline=Airline.objects.create(name="LOT",
                                                                                                           iata_code="LO"),
                                                                            departure_airport=Airport.objects.create(
                                                                                name="WAW", iata_code="WAW",
                                                                                location=Location.objects.create(
                                                                                    city="Warsaw",
                                                                                    country="Poland")),
                                                                            arrival_airport=Airport.objects.create(
                                                                                name="KRK", iata_code="KRK",
                                                                                location=Location.objects.create(
                                                                                    city="Krakow",
                                                                                    country="Poland")),
                                                                            departure_time="2024-12-01T10:00:00Z",
                                                                            arrival_time="2024-12-01T12:00:00Z",
                                                                            base_price=300.00), passengers=2,
                                               status="confirmed")
        self.create_and_list_test("/api/passenger-details/",
                                  {"flight_booking": booking.id, "name": "John", "surname": "Doe",
                                   "passport_number": "123456", "nationality": "Polish"})

    # -------------------- Price Alert --------------------
    def test_price_alert_crud(self):
        user = User.objects.create(username="testuser", email="test@example.com")
        self.create_and_list_test("/api/price-alerts/",
                                  {"user": user.id, "item_type": "flight", "item_id": 1, "desired_price": 150.00,
                                   "status": "active"})

    # -------------------- Hotel, Room, and Booking --------------------
    def test_hotel_crud(self):
        location = Location.objects.create(city="Warsaw", country="Poland")
        self.create_and_list_test("/api/hotels/",
                                  {"name": "Marriott", "location": location.id, "stars": 5, "price_per_night": 500.00})

    def test_hotel_room_crud(self):
        hotel = Hotel.objects.create(name="Marriott", location=Location.objects.create(city="Warsaw", country="Poland"),
                                     stars=5, price_per_night=500.00)
        self.create_and_list_test("/api/hotel-rooms/",
                                  {"hotel": hotel.id, "room_type": "Deluxe", "base_price": 300.00, "max_occupancy": 2})

    def test_hotel_booking_crud(self):
        user = User.objects.create(username="testuser", email="test@example.com")
        hotel = Hotel.objects.create(name="Marriott", location=Location.objects.create(city="Warsaw", country="Poland"),
                                     stars=5, price_per_night=500.00)
        self.create_and_list_test("/api/hotel-bookings/", {
            "user": user.id,
            "hotel": hotel.id,
            "check_in_date": "2024-12-01",
            "check_out_date": "2024-12-05",
            "num_people": 2,
            "status": "confirmed"
        })

    def test_hotel_review_crud(self):
        user = User.objects.create(username="testuser", email="test@example.com")
        hotel = Hotel.objects.create(name="Marriott", location=Location.objects.create(city="Warsaw", country="Poland"),
                                     stars=5, price_per_night=500.00)
        self.create_and_list_test("/api/hotel-reviews/",
                                  {"hotel": hotel.id, "user": user.id, "rating": 5, "comment": "Great stay!"})

    # -------------------- Hotel Amenities --------------------
    def test_hotel_amenity_crud(self):
        self.create_and_list_test("/api/hotel-amenities/", {"name": "Free WiFi"})

    def test_hotel_amenity_mapping_crud(self):
        hotel = Hotel.objects.create(name="Marriott", location=Location.objects.create(city="Warsaw", country="Poland"),
                                     stars=5, price_per_night=500.00)
        amenity = HotelAmenity.objects.create(name="Free WiFi")
        self.create_and_list_test("/api/hotel-amenity-mappings/", {"hotel": hotel.id, "amenity": amenity.id})

    # -------------------- Price Management --------------------
    def test_price_history_crud(self):
        self.create_and_list_test("/api/price-history/",
                                  {"item_type": "flight", "item_id": 1, "previous_price": 200.00, "new_price": 180.00})

    def test_price_prediction_crud(self):
        self.create_and_list_test("/api/price-predictions/",
                                  {"item_type": "hotel", "item_id": 1, "predicted_price": 150.00})

    # -------------------- Refunds --------------------
    def test_refund_crud(self):
        user = User.objects.create(username="testuser", email="test@example.com")
        method = PaymentMethod.objects.create(name="Credit Card", description="Visa or Mastercard")
        payment = Payment.objects.create(user=user, amount=500.00, method=method, status="completed")
        self.create_and_list_test("/api/refunds/", {"payment": payment.id, "refund_amount": 100.00})

    # -------------------- Loyalty Programs --------------------
    def test_loyalty_program_crud(self):
        user = User.objects.create(username="testuser", email="test@example.com")
        self.create_and_list_test("/api/loyalty-programs/", {"user": user.id, "points": 1000, "tier": "gold"})

    # -------------------- System Logs --------------------
    def test_system_log_crud(self):
        user = User.objects.create(username="testuser", email="test@example.com")
        self.create_and_list_test("/api/system-logs/",
                                  {"event_type": "user_login", "user": user.id, "event_description": "User logged in"})

    # -------------------- Notifications --------------------
    def test_notification_crud(self):
        user = User.objects.create(username="testuser", email="test@example.com")
        self.create_and_list_test("/api/notifications/",
                                  {"user": user.id, "notification_type": "price_alert", "message": "Price dropped!"})

    # -------------------- Audit Logs --------------------
    def test_audit_log_crud(self):
        user = User.objects.create(username="testuser", email="test@example.com")
        self.create_and_list_test("/api/audit-logs/", {
            "user": user.id,
            "action_type": "create",
            "table_name": "flight",
            "record_id": 1,
            "description": "Created a flight."
        })

    # -------------------- Subscriptions --------------------
    def test_subscription_crud(self):
        user = User.objects.create(username="testuser", email="test@example.com")
        self.create_and_list_test("/api/subscriptions/",
                                  {"user": user.id, "subscription_type": "newsletter", "is_active": True})

    # -------------------- Newsletters --------------------
    def test_newsletter_crud(self):
        self.create_and_list_test("/api/newsletters/",
                                  {"title": "Travel Deals", "content": "Amazing discounts on flights and hotels"})
