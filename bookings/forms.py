
from django import forms
from .models import Property, Booking, PropertyImage
from django.utils import timezone

# Formë për krijimin e pronave
class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['image', 'name', 'description', 'price_per_night', 'is_available', 'location', 'property_type', 'square_meters', 'max_guests', 'start_date', 'end_date']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }
        
        
class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image']

# Formë për krijimin e rezervimeve
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date', 'end_date', 'guests', 'property']

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        property = cleaned_data.get('property')

        if start_date and end_date and property:
            if end_date <= start_date:
                raise forms.ValidationError('End date must be after start date.')

            # Kontrollo nëse prona është e disponueshme gjatë periudhës e kërkuar
            if not property.is_available_for_dates(start_date, end_date):
                raise forms.ValidationError('This property is not available for the selected dates.')

        return cleaned_data

# Formë për kërkimin e disponueshmërisë së pronave
class SearchAvailabilityForm(forms.Form):
    location = forms.CharField(required=True, label="Location")
    start_date = forms.DateField(required=True, widget=forms.SelectDateWidget)
    end_date = forms.DateField(required=True, widget=forms.SelectDateWidget)
