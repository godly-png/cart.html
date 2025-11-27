# forms.py
from django import forms
from .models import BillingDetails

class BillingDetailsForm(forms.ModelForm):
    class Meta:
        model = BillingDetails
        fields = ['full_name', 'email', 'phone_number', 'address', 'city', 'state', 'pincode']



