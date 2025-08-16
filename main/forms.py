from django import forms
from django.core.exceptions import ValidationError
import re
from .models import ContactInquiry, Product

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactInquiry
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+996 XXX XXX XXX',
                'required': True,
                'pattern': r'^\+?[1-9]\d{1,14}$'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Your Message',
                'rows': 5,
                'required': True
            })
        }
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone:
            raise ValidationError('Phone number is required.')
        
        # Remove all non-digit characters except +
        cleaned_phone = re.sub(r'[^\d+]', '', phone)
        
        # Check if phone starts with + and has country code
        if cleaned_phone.startswith('+'):
            # International format validation
            if not re.match(r'^\+[1-9]\d{6,14}$', cleaned_phone):
                raise ValidationError(
                    'Please enter a valid international phone number (e.g., +996707123456)'
                )
        else:
            # Local format validation for Kyrgyzstan
            if re.match(r'^0[0-9]{9}$', cleaned_phone):
                # Convert local format to international
                cleaned_phone = '+996' + cleaned_phone[1:]
            elif re.match(r'^[0-9]{9}$', cleaned_phone):
                # Add country code if missing
                cleaned_phone = '+996' + cleaned_phone
            elif not re.match(r'^[1-9]\d{6,14}$', cleaned_phone):
                raise ValidationError(
                    'Please enter a valid phone number (e.g., +996707123456 or 0707123456)'
                )
        
        # Additional length validation
        if len(cleaned_phone) < 7 or len(cleaned_phone) > 16:
            raise ValidationError(
                'Phone number must be between 7 and 16 digits long.'
            )
        
        return cleaned_phone

class CalculatorForm(forms.Form):
    width = forms.DecimalField(
        max_digits=5, 
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Room Width (meters)',
            'step': '0.01',
            'min': '0.1'
        })
    )
    length = forms.DecimalField(
        max_digits=5, 
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Room Length (meters)',
            'step': '0.01',
            'min': '0.1'
        })
    )
    ceiling_type = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        empty_label="Choose a ceiling type..."
    )
