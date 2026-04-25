from django import forms
from .models import Store

class StoreApplicationForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'owner_name', 'phone_number', 'contact_email', 'address', 'city', 'category', 'description', 'quantity_total']
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. FlashBite Bakery'}),
            'owner_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Ali Khan'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. +92 300 1234567'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'vendor@email.com'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'e.g. 123 Main St, Johar Town'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Lahore'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Bakery, Restaurant'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Tell customers about your amazing food...'}),
        }