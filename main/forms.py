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
                'pattern': r'^(?:\+996|0)\s?\d{2,3}(?:\s?\d{2}){3,4}$'
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

        # Убираем пробелы, скобки, тире и т.д.
        cleaned_phone = re.sub(r'[^\d+]', '', phone)

        # Проверяем международный формат (+996XXXYYYZZZ...)
        if cleaned_phone.startswith('+'):
            if not re.match(r'^\+996\d{9}$', cleaned_phone):
                raise ValidationError(
                    'Введите номер в формате +996XXXXXXXXX'
                )
        else:
            # Локальный формат: 0XXXXXXXXX или XXXXXXXXX
            if re.match(r'^0\d{9}$', cleaned_phone):
                # конвертируем 0XXXXXXXXX → +996XXXXXXXXX
                cleaned_phone = '+996' + cleaned_phone[1:]
            elif re.match(r'^\d{9}$', cleaned_phone):
                # конвертируем XXXXXXXXX → +996XXXXXXXXX
                cleaned_phone = '+996' + cleaned_phone
            else:
                raise ValidationError(
                    'Введите номер в формате +996XXXXXXXXX или 0XXXXXXXXX'
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
