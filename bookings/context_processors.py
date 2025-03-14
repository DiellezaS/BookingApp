# bookings/context_processors.py

from .models import Notification

def notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')
    else:
        notifications = []
    return {'notifications': notifications}
