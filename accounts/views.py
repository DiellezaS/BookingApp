from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required

from bookings.models import Property, Booking 


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # E identifikon automatikisht pas regjistrimit
            return redirect('profile')  
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})

# @login_required
# def profile(request):
#     return render(request, 'accounts/profile.html')


@login_required(login_url='login')
def profile(request):
    user = request.user
    
    # Gjeni rezervimet e këtij përdoruesi
    bookings = Booking.objects.filter(user=user)
    
    # Gjeni pronat e listuara nga ky përdorues (për përdoruesit që janë pronarë)
    listed_properties = Property.objects.filter(listed_by=user.profile)
    
    context = {
        'user': user,
        'bookings': bookings,
        'listed_properties': listed_properties,
    }
    
    return render(request, 'accounts/profile.html', context)