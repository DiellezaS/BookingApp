
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Booking

@receiver(post_save, sender=Booking)
def update_property_status(sender, instance, created, **kwargs):
    if created:  # Kjo është kur krijohet një rezervim i ri
        property = instance.property
        property.is_available = False  # Bëhet i paarritshëm për rezervime të tjera
        property.save()



@receiver(post_save, sender=Booking)
def send_booking_notification(sender, instance, created, **kwargs):
    if created:
        property = instance.property
        user = instance.user
        owner = property.listed_by.user  # Pronari i pronës

        # Dërgo njoftim për pronarin që prona u rezervua
        message = f"Pronën tuaj '{property.name}' e ka rezervuar {user.username} nga {instance.start_date} deri në {instance.end_date}. Çmimi total: {instance.total_price()} EUR"
        from .models import Notification 
        Notification.objects.create(user=owner, message=message)

        # Dërgo njoftim edhe për përdoruesin që ka bërë rezervimin
        message_for_user = f"Ju keni rezervuar pronën '{property.name}' nga {instance.start_date} deri në {instance.end_date}. Çmimi total: {instance.total_price()} EUR"
        from .models import Notification 
        Notification.objects.create(user=user, message=message_for_user)
