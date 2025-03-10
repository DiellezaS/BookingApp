from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import IntegrityError

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
 
    def __str__(self):
        return f'{self.user.username} Profile'



@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        try:
            Profile.objects.create(user=instance)
        except IntegrityError:
            # Nëse ekziston tashmë një profil për këtë përdorues, thjesht anashkalojmë.
            pass


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
    
