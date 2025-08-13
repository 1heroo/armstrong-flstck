from django import forms
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
                'placeholder': 'Phone Number',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Your Message',
                'rows': 5,
                'required': True
            })
        }

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
