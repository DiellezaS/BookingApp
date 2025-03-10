
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Property, Booking, PropertyImage
from .forms import PropertyForm, BookingForm
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail
from .forms import SearchAvailabilityForm
from django.db.models import Q





# 1. Funksionaliteti për shfaqjen e pronave
def property_list(request):
    """List all available properties"""
    properties = Property.objects.filter(is_available=True)
    return render(request, 'bookings/property_list.html', {'properties': properties})

def property_detail(request, property_id):
    """Display details of a specific property"""
    property = get_object_or_404(Property, id=property_id)
    
    can_edit = request.user.is_authenticated and request.user == property.listed_by.user

    return render(request, 'bookings/property_detail.html', {'property': property, 'can_edit': can_edit})


# @login_required(login_url='login')
# def property_create(request):
#     """Create a new property"""
#     form = PropertyForm(request.POST, request.FILES)
#     if request.method == 'POST' and form.is_valid():
        
#         property_obj = form.save(commit=False)
#         property_obj.listed_by = request.user.profile  # Përdorni request.user.profile, jo request.user
#         property_obj.save()
#         messages.success(request, "Property created successfully!")
#         return redirect('property_list')

#     return render(request, 'bookings/property_form.html', {'form': form})

@login_required(login_url='login')
def property_create(request):
    """Create a new property"""
    if request.method == 'POST':
        property_form = PropertyForm(request.POST, request.FILES)

        # Validate the property form
        if property_form.is_valid():
            # Save the property object but don't commit it to the database yet
            property_obj = property_form.save(commit=False)
            property_obj.listed_by = request.user.profile  # Assign the user as the property owner
            property_obj.save()  # Save the property first to get an ID
            
            # Handle multiple image uploads
            images = request.FILES.getlist('image')  # Get the list of uploaded images
            
            if images:
                for image in images:
                    PropertyImage.objects.create(property=property_obj, image=image)
            else:
                messages.warning(request, "No images uploaded for this property.")

            # Inform the user that the property was created successfully
            messages.success(request, "Property created successfully!")

            # Redirect to the property list page
            return redirect('property_list')

    else:
        property_form = PropertyForm()

    return render(request, 'bookings/property_form.html', {'form': property_form})


@login_required
def property_update(request, property_id):
    """Update an existing property"""
    property_obj = get_object_or_404(Property, id=property_id)

    # Verifikoni nëse përdoruesi është pronar i pronës
    if property_obj.listed_by != request.user.profile:
        messages.error(request, "You are not authorized to edit this property.")
        return redirect('property_list')

    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Property updated successfully!")
            return redirect('property_detail', property_id=property_obj.id)
    else:
        form = PropertyForm(instance=property_obj)

    return render(request, 'bookings/property_form.html', {'form': form})


@login_required(login_url='login')
def property_delete(request, property_id):  
    """Delete a property"""
    property_obj = get_object_or_404(Property, id=property_id)

    if property_obj.listed_by != request.user.profile:
        messages.error(request, "You do not have permission to delete this property.")
        return redirect('property_list')

    if request.method == 'POST':
        property_obj.delete()
        messages.success(request, "Property deleted successfully!")
        return redirect('property_list')

    return render(request, 'bookings/property_confirm_delete.html', {'property': property_obj})



@login_required(login_url='login')
def booking_create(request, property_id):
    """Create a new booking for a property"""
    property_obj = get_object_or_404(Property, id=property_id)

    # Kontrolloni nëse prona është e disponueshme
    if not property_obj.is_available:
        return HttpResponse("Na vjen keq, kjo pronë nuk është më e disponueshme.")

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Krijoni rezervimin por mos e ruani ende
            booking = form.save(commit=False)
            booking.property = property_obj  # Lidhni pronën
            booking.user = request.user  # Lidhni përdoruesin që është loguar

            # Ruani rezervimin
            booking.save()

            # Ndryshoni statusin e pronës në 'reserved'
            property_obj.is_available = False  # Mund ta lini këtu të jetë i papranueshëm për rezervime të tjera
            property_obj.status = 'reserved'  # Vendosim një status të ri për pronën
            property_obj.save()

            # Dërgo njoftim për pronarin që prona është rezervuar
            send_booking_notification(
                property_obj.listed_by.user,
                request.user,
                property_obj.name,
                booking.start_date,
                booking.end_date
            )

            # Kthehu përdoruesin në faqen e suksesit të rezervimit
            return redirect('booking_success', booking_id=booking.id)


    else:
        form = BookingForm()

    return render(request, 'bookings/booking_form.html', {'form': form, 'property': property_obj})


def send_booking_notification(property_owner, booking_user, property_name, start_date, end_date):
    """Funksioni për të dërguar njoftimin tek pronari i pronës kur rezervimi është krijuar"""
    from .models import Notification  # Import dynamic, only when the function is called
    message = f"Prona {property_name} është rezervuar nga {booking_user.username} për periudhën nga {start_date} deri në {end_date}."
    
    # Krijo njoftimin për pronarin
    Notification.objects.create(user=property_owner, message=message)


# def booking_success(request):
#     return render(request, 'bookings/booking_success.html')


@login_required
def booking_success(request, booking_id):
    # Merrni rezervimin dhe pronën lidhur me këtë rezervim
    booking = get_object_or_404(Booking, id=booking_id)
    property_obj = booking.property  # Marrim pronën lidhur me këtë rezervim

    # Dërgo detajet në shabllon
    return render(request, 'bookings/booking_success.html', {
        'booking': booking,
        'property': property_obj
    })
    
    
    
@login_required(login_url='login')
def booking_list(request):
    """List all bookings for the logged-in user"""
    bookings = Booking.objects.filter(user=request.user)  # Përdorni request.user dhe jo request.user.profile
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})


@login_required(login_url='login')
def booking_update(request, booking_id):
    """Update an existing booking"""
    booking = get_object_or_404(Booking, id=booking_id)

    # Vetëm pronari i rezervimit mund ta modifikojë atë
    if booking.user != request.user:
        messages.error(request, "You are not authorized to edit this booking.")
        return redirect('booking_list')

    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, "Booking updated successfully!")
            return redirect('booking_list')
    else:
        form = BookingForm(instance=booking)

    return render(request, 'bookings/booking_form.html', {'form': form, 'booking': booking})


class PropertyUpdateView(UpdateView):
    model = Property
    fields = ['name', 'description', 'price_per_night', 'location', 'square_meters', 'max_guests', 'is_available']
    template_name = 'bookings/property_update.html'
    success_url = reverse_lazy('property_list')


def update_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id)

    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            # Marrim datat e reja të rezervimit
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            # Kontrollojmë nëse ka ndonjë rezervim tjetër për ato data
            conflicting_booking = Booking.objects.filter(
                property=booking.property,
                start_date__lt=end_date,
                end_date__gt=start_date
            ).exclude(id=booking.id)  # Përshtatja me përjashtimin e vetë rezervimit që po editohet

            if conflicting_booking.exists():
                # Nëse ka një rezervim që mbulon këto data, e ndalim ruajtjen dhe e njoftojmë përdoruesin
                messages.error(request, "This property is not available for the selected dates.")
                return redirect('booking_form', booking_id=booking.id)

            # Nëse nuk ka konflikte, ruajmë rezervimin
            form.save()
            messages.success(request, "Booking updated successfully!")
            return redirect('booking_success')  # Ky është URL që përdoruesi do të drejtohet pas përditësimit

    else:
        form = BookingForm(instance=booking)

    return render(request, 'update_booking.html', {'form': form})


# Funksionaliteti për kërkimin e pronave
def search_properties(request):
    location = request.GET.get('location', '')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    properties = Property.objects.all()

    if location:
        properties = properties.filter(location__icontains=location)

    if start_date and end_date:
        properties = properties.filter(
            start_date__lte=end_date,
            end_date__gte=start_date,
            is_available=True
        )

    return render(request, 'bookings/search_results.html', {'properties': properties})


@login_required
def my_properties(request):
    properties = Property.objects.filter(listed_by=request.user.profile)
    bookings = {}

    # Përdor për të marrë rezervimet që janë bërë për çdo pronë
    for property in properties:
        bookings[property] = property.booking_set.all()  # Përdor lidhjen reverse për të marrë rezervimet

    return render(request, 'my_properties.html', {'properties': properties, 'bookings': bookings})


@login_required
def book_property(request, property_id):
    property = Property.objects.get(id=property_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.property = property

            # Kontrollo që rezervimi të mos përfshijë datat që janë tashmë të rezervuara
            conflicting_bookings = Booking.objects.filter(property=property).filter(
                start_date__lte=booking.end_date,
                end_date__gte=booking.start_date
            )

            if conflicting_bookings.exists():
                form.add_error(None, "This property is already booked for the selected dates.")
                return render(request, 'property_list.html', {'form': form, 'property': property})

            booking.save()

            # Dërgo një njoftim pronarit për rezervimin
            send_booking_notification(property.listed_by.user, booking)

            return redirect('booking_success')  # Kthehu përdoruesin në faqen e konfirmimit
    else:
        form = BookingForm()

    return render(request, 'property_list.html', {'form': form, 'property': property})


@login_required
def my_bookings(request):
    """Shfaq pronat që përdoruesi ka rezervuar"""
    user = request.user
    bookings = Booking.objects.filter(user=user, status='reserved')
    reserved_properties = [booking.property for booking in bookings]
    
    return render(request, 'bookings/my_bookings.html', {
        'reserved_properties': reserved_properties
    })



def user_notifications(request):
    """Shfaq njoftimet e përdoruesit të loguar"""
    from .models import Notification 
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'bookings/notifications.html', {'notifications': notifications})


def mark_notification_as_read(request, notification_id):
    from .models import Notification 
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('user_notifications')


