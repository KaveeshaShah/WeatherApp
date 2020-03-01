from django import forms
from weather.models import Location
from weather.models import User

class SubscribeForm(forms.ModelForm):
    email_id = forms.EmailField(required=True)
    City = forms.ModelChoiceField(queryset= Location.objects.values_list('city', flat=True).order_by('city'),to_field_name="city")
    
    class Meta:
        model = User
        fields = ['email_id','City']