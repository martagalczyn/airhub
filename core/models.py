from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

# Add more comments here

# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, role="user", **extra_fields):
        if not email:
            raise ValueError("Email jest wymagany")
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)  # Domyślna rola "user"
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, role="admin", **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError("Superuser musi mieć is_staff=True.")
        if not extra_fields.get('is_superuser'):
            raise ValueError("Superuser musi mieć is_superuser=True.")

        return self.create_user(email, password, role=role, **extra_fields)

# Custom User Model
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name="Email Address")
    role = models.CharField(max_length=50, blank=True, null=True, verbose_name="Role")
    date_registered = models.DateTimeField(auto_now_add=True, verbose_name="Date Registered")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    is_staff = models.BooleanField(default=False, verbose_name="Is Staff")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # No additional required fields other than email

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

# User Role
class UserRole(models.Model):
    name = models.CharField(max_length=50, verbose_name="Role Name")
    description = models.TextField(verbose_name="Role Description")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "User Role"
        verbose_name_plural = "User Roles"

# User Permission
class UserPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="permissions")
    role = models.ForeignKey(UserRole, on_delete=models.CASCADE, null=True, blank=True, related_name="permissions")

    def __str__(self):
        return f"{self.user} - {self.role}"

    class Meta:
        verbose_name = "User Permission"
        verbose_name_plural = "User Permissions"

# User Session
class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="sessions")
    session_start = models.DateTimeField(auto_now_add=True, verbose_name="Session Start")
    session_end = models.DateTimeField(null=True, blank=True, verbose_name="Session End")
    ip_address = models.GenericIPAddressField(verbose_name="IP Address")

    def __str__(self):
        return f"Session for {self.user} ({self.ip_address})"

    class Meta:
        verbose_name = "User Session"
        verbose_name_plural = "User Sessions"

# Location
class Location(models.Model):
    city = models.CharField(max_length=100, verbose_name="City")
    country = models.CharField(max_length=100, verbose_name="Country")

    def __str__(self):
        return f"{self.city}, {self.country}"

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"

# Region Statistic
class RegionStatistic(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True, related_name="statistics")
    flight_bookings_count = models.PositiveIntegerField(default=0, verbose_name="Flight Bookings Count")
    hotel_bookings_count = models.PositiveIntegerField(default=0, verbose_name="Hotel Bookings Count")
    last_updated = models.DateTimeField(auto_now=True, verbose_name="Last Updated")

    def __str__(self):
        return f"Stats for {self.location}"

    class Meta:
        verbose_name = "Region Statistic"
        verbose_name_plural = "Region Statistics"

# Airline
class Airline(models.Model):
    name = models.CharField(max_length=100, verbose_name="Airline Name")
    iata_code = models.CharField(max_length=3, verbose_name="IATA Code")
    image = models.ImageField(upload_to="airlines/", null=True, blank=True, verbose_name="Logo")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Airline"
        verbose_name_plural = "Airlines"

# Airport
class Airport(models.Model):
    name = models.CharField(max_length=100, verbose_name="Airport Name")
    iata_code = models.CharField(max_length=3, verbose_name="IATA Code")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True, related_name="airports")
    image = models.ImageField(upload_to="airports/", null=True, blank=True, verbose_name="Image")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Airport"
        verbose_name_plural = "Airports"

# Flight
class Flight(models.Model):
    flight_number = models.CharField(max_length=10, verbose_name="Flight Number")
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE, null=True, blank=True, related_name="flights")
    departure_airport = models.ForeignKey(Airport, related_name="departure_flights", on_delete=models.CASCADE, null=True, blank=True)
    arrival_airport = models.ForeignKey(Airport, related_name="arrival_flights", on_delete=models.CASCADE, null=True, blank=True)
    departure_time = models.DateTimeField(verbose_name="Departure Time")
    arrival_time = models.DateTimeField(verbose_name="Arrival Time")
    base_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Base Price")

    def __str__(self):
        return self.flight_number

    class Meta:
        verbose_name = "Flight"
        verbose_name_plural = "Flights"

# Continue similar structure for remaining models...


class FlightClass(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, null=True, blank=True)
    class_type = models.CharField(max_length=50, choices=[
        ('economy', 'Economy'),
        ('business', 'Business'),
        ('first_class', 'First Class'),
    ])
    additional_cost_percentage = models.DecimalField(max_digits=5, decimal_places=2)

class FlightRoute(models.Model):
    departure_airport = models.ForeignKey(Airport, related_name='routes_from', on_delete=models.CASCADE, null=True, blank=True)
    arrival_airport = models.ForeignKey(Airport, related_name='routes_to', on_delete=models.CASCADE, null=True, blank=True)
    distance_km = models.PositiveIntegerField()

# Flights reservations
class FlightBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, null=True, blank=True)
    passengers = models.PositiveIntegerField()
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ])

class PassengerDetails(models.Model):
    flight_booking = models.ForeignKey(FlightBooking, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    passport_number = models.CharField(max_length=50)
    nationality = models.CharField(max_length=50)

# Hotels, rooms and amenities
class Hotel(models.Model):
    name = models.CharField(max_length=100)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    stars = models.IntegerField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='hotels/', null=True, blank=True)

class HotelRoom(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True, blank=True)
    room_type = models.CharField(max_length=50)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    max_occupancy = models.PositiveIntegerField()

class HotelAmenity(models.Model):
    name = models.CharField(max_length=100)

class HotelAmenityMapping(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True, blank=True)
    amenity = models.ForeignKey(HotelAmenity, on_delete=models.CASCADE, null=True, blank=True)

class HotelBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True, blank=True)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    num_people = models.PositiveIntegerField()
    status = models.CharField(max_length=50, choices=[
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ])

class HotelReview(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.IntegerField()
    comment = models.TextField()
    review_date = models.DateTimeField(auto_now_add=True)

# Prices, alerts and predictions
class PriceHistory(models.Model):
    item_type = models.CharField(max_length=50, choices=[
        ('flight', 'Flight'),
        ('hotel', 'Hotel'),
    ])
    item_id = models.PositiveIntegerField()
    previous_price = models.DecimalField(max_digits=10, decimal_places=2)
    new_price = models.DecimalField(max_digits=10, decimal_places=2)
    change_date = models.DateTimeField(auto_now_add=True)

class PriceAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    item_type = models.CharField(max_length=50, choices=[
        ('flight', 'Flight'),
        ('hotel', 'Hotel'),
    ])
    item_id = models.PositiveIntegerField()
    desired_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=[
        ('active', 'Active'),
        ('fulfilled', 'Fulfilled'),
    ])

class PricePrediction(models.Model):
    item_type = models.CharField(max_length=50, choices=[
        ('flight', 'Flight'),
        ('hotel', 'Hotel'),
    ])
    item_id = models.PositiveIntegerField()
    predicted_price = models.DecimalField(max_digits=10, decimal_places=2)
    prediction_date = models.DateTimeField(auto_now_add=True)

# Payments and refunds
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.ForeignKey('PaymentMethod', on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('pending', 'Pending'),
    ])

class PaymentMethod(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='payment_method/', null=True, blank=True)

class Refund(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True, blank=True)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2)
    refund_date = models.DateTimeField(auto_now_add=True)

# Promotions and loyalty program
class Promotion(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='promotions/', null=True, blank=True)

class LoyaltyProgram(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    points = models.PositiveIntegerField(default=0)
    tier = models.CharField(max_length=50, choices=[
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
    ], default='silver')

# Logs and Notifications
class SystemLog(models.Model):
    event_type = models.CharField(max_length=50, choices=[
        ('user_login', 'User Login'),
        ('booking_created', 'Booking Created'),
        ('price_alert_triggered', 'Price Alert Triggered'),
    ])
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    event_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    notification_type = models.CharField(max_length=50, choices=[
        ('price_alert', 'Price Alert'),
        ('promotion', 'Promotion'),
        ('booking_update', 'Booking Update'),
    ])
    message = models.TextField()
    status = models.CharField(max_length=50, choices=[
        ('sent', 'Sent'),
        ('pending', 'Pending'),
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action_type = models.CharField(max_length=50, choices=[
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
    ])
    table_name = models.CharField(max_length=100)
    record_id = models.PositiveIntegerField()
    action_timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

# Subscriptions and newsletters
class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    subscription_type = models.CharField(max_length=50, choices=[
        ('newsletter', 'Newsletter'),
        ('price_alerts', 'Price Alerts'),
        ('promotions', 'Promotions'),
    ])
    start_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

class Newsletter(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    sent_date = models.DateTimeField(null=True, blank=True)
    recipients = models.ManyToManyField(User, blank=True)

class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='news/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Menu(models.Model):
    name = models.CharField(max_length=100, help_text="Name of the menu, e.g., 'Main Menu'")
    is_active = models.BooleanField(default=True, help_text="Whether this menu is active")

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=100, help_text="Text displayed on the menu")
    url = models.CharField(max_length=255, help_text="URL or path for this menu item")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', help_text="Parent menu item for submenus")
    display_order = models.PositiveIntegerField(default=0, help_text="Order of this menu item in the menu")
    is_active = models.BooleanField(default=True, help_text="Whether this menu item is active")

    def __str__(self):
        return self.title


class Footer(models.Model):
    name = models.CharField(max_length=100, help_text="Section name, e.g., 'About Us'")
    content = models.TextField(help_text="Content for the footer section")
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class StaticText(models.Model):
    key = models.CharField(max_length=100, unique=True, help_text="Identifier for the text, e.g., 'home_about_us'")
    content = models.TextField(help_text="Text content to display")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.key

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.question

class Contact(models.Model):
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Contact: {self.email}"

class Banner(models.Model):
    title = models.CharField(max_length=200, help_text="Banner title or heading")
    image = models.ImageField(upload_to='banners/', null=True, blank=True)
    link = models.URLField(null=True, blank=True, help_text="Optional URL the banner links to")
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title