from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Product, ContactInquiry, ProductImage, ProductTranslation, ProductType, ProductTypeTranslation
from django import forms

import requests
import time
from ceiling_solutions import settings
import os


class ProductTypeTranslationInline(admin.TabularInline):
    model = ProductTypeTranslation
    fields = ('language', 'name')
    extra = 1
    

@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [ProductTypeTranslationInline]



class ProductTranslationInline(admin.TabularInline):
    model = ProductTranslation
    extra = 1  # сколько пустых форм для новых переводов показывать
    fields = ('language', 'name', 'description')


class ImageForm(forms.ModelForm):
    upload = forms.ImageField(required=False, help_text="Выберите изображение для загрузки.")
    image_url = forms.CharField(max_length=255, required=False, help_text="Вставьте ссылку на изображение или загрузите файл.")

    class Meta:
        model = ProductImage
        fields = ['image_url', 'upload']

    def save(self, commit=True):
        instance = super().save(commit=False)

        uploaded_file = self.cleaned_data.get('upload')
        url = self.cleaned_data.get('image_url')

        prefix = str(time.time())
        filename = f"{prefix}_{uploaded_file.name}" if uploaded_file else f"{prefix}_{url.split('/')[-1]}"
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            raise forms.ValidationError("Файл должен быть изображением (PNG, JPG, JPEG, GIF).")

        if uploaded_file:
            path = os.path.join('uploads', filename)
            full_path = os.path.join(settings.MEDIA_ROOT, path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            with open(full_path, 'wb+') as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)
            instance.image_url = settings.HOST + '/' + full_path

        elif url:
            response = requests.get(url.strip())
            if response.status_code == 200:
                path = os.path.join('uploads', filename)
                full_path = os.path.join(settings.MEDIA_ROOT, path)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)

                with open(full_path, 'wb') as f:
                    f.write(response.content)
                instance.image_url = settings.HOST + '/' + full_path

        if commit:
            instance.save()
        return instance


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    form = ImageForm
    exclude = []
    # fields = ('alt_text', 'order')
    readonly_fields = ['preview']

    def preview(self, obj):
        if obj.image_url:
            return mark_safe(f'<img src="{obj.image_url}" width="100" />')
        return "-"


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['product_type', 'price_per_sqm', 'tags']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_name', 'price_per_sqm', 'created_at')
    list_display_links = ('id', 'get_name', 'price_per_sqm', 'created_at')

    search_fields = ('translations__name', 'tags')
    list_filter = ('translations__language',)
    inlines = [ProductImageInline, ProductTranslationInline]
    form = ProductForm

    def get_name(self, obj):
        translation = obj.translations.first()
        return translation.name if translation else '(Нет перевода)'
    get_name.short_description = 'Name'

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ['-created_at']


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'email', 'phone']
    readonly_fields = ['created_at']



###########################33
from django.contrib.auth.models import Group, User as DjangoUser
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

admin.site.unregister(Group)
admin.site.unregister(DjangoUser)

DjangoUser._meta.verbose_name = "Админ"
DjangoUser._meta.verbose_name_plural = "Админы"


admin.site.register(DjangoUser, DjangoUserAdmin)

