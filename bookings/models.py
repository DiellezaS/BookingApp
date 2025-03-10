
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from accounts.models import Profile  # Importojmë modelin Profile nga aplikacioni accounts


class Property(models.Model):
    PROPERTY_TYPES = [
        ('apartamente', 'Apartamente'),
        ('villa', 'Villa'),
        ('suita', 'Suita'),
    ]

    STATUS_CHOICES = [
    ('available', 'Available'),
    ('reserved', 'Reserved'),
    ('unavailable', 'Unavailable'),
]

    name = models.CharField(max_length=255)
    description = models.TextField()
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    price_per_night = models.DecimalField(max_digits=12, decimal_places=2)
    location = models.CharField(max_length=255)
    square_meters = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    max_guests = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_available = models.BooleanField(default=True)
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default='available')  # Statusi i pronës
    listed_by = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    image = models.ImageField(upload_to='property_photos/', default='property_photos/default_image.jpg')

    
    def __str__(self):
        return f"{self.name} - {self.location} ({self.square_meters}m², {self.max_guests} guests)"

    # def is_available_for_dates(self, start_date, end_date):
    #     """Kontrollon nëse prona është e disponueshme për datat e kërkuara."""
    #     return not Booking.objects.filter(property=self, status='reserved') \
    #         .filter(start_date__lt=end_date, end_date__gt=start_date).exists()
    def is_available_for_dates(self, start_date, end_date):
            """Kontrollon nëse prona është e disponueshme për datat e kërkuara."""
            return not Booking.objects.filter(property=self).filter(status__in=['reserved', 'pending']).filter(start_date__lt=end_date, end_date__gt=start_date).exists()
                       



class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    guests = models.PositiveIntegerField()
    status = models.CharField(max_length=50, choices=[ 
        ('reserved', 'Reserved'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('pending', 'Pending')  
    ], default='reserved')
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        start_date = self.start_date
        end_date = self.end_date

        # Kontrollo nëse start_date dhe end_date janë të plota
        if not start_date or not end_date:
            raise ValidationError("Both start date and end date are required.")

        # Kontrollo nëse datat janë të vlefshme
        if start_date < timezone.now().date():
            raise ValidationError("The start date cannot be in the past.")
        
        if end_date <= start_date:
            raise ValidationError("The end date must be later than the start date.")

        # Kontrollo disponueshmërinë e pronës
        if not self.property.is_available_for_dates(start_date, end_date):
            raise ValidationError(f"The property is already booked for the selected dates from {start_date} to {end_date}.")

    def total_price(self):
        """Llogarit çmimin total të rezervimit"""
        nights = (self.end_date - self.start_date).days
        return nights * self.property.price_per_night

    def __str__(self):
        return f"Booking for {self.property.name} by {self.user.username} from {self.start_date} to {self.end_date}"

    def create_notification(self):
        from .models import Notification  # Importimi i Notification brenda funksionit për të shmangur ciklin e importimit

        message = f"Prona {self.property.name} është rezervuar nga {self.user.username} për periudhën nga {self.start_date} deri në {self.end_date}."
        Notification.objects.create(user=self.property.listed_by.user, message=message)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings_notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Njoftim për {self.user.username}: {self.message[:50]}"
    



class PropertyImage(models.Model):
    property = models.ForeignKey(Property, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_images/')
    
    def __str__(self):
        return f"Image for {self.property.name}"
