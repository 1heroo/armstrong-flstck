from django.contrib import admin
from django.utils.safestring import mark_safe
from urllib3 import fields

from .models import (Product, ContactInquiry, ProductImage, ProductTranslation, ProductType, ProductTypeTranslation,
 ProductCharacteristic, ProductCharacteristicTranslation, ProductCategory, ProductCategoryTranslation)
from django import forms

import requests
import time
from ceiling_solutions import settings
import os
import nested_admin
import re 


class ProductCategoryTranslationInline(nested_admin.NestedStackedInline):
    model = ProductCategoryTranslation
    extra = 1
    fields = ('language', 'name', 'description')


class CategoryForm(forms.ModelForm):
    upload = forms.ImageField(required=False, help_text="Выберите изображение для загрузки.")
    image_url = forms.CharField(max_length=255, required=False, help_text="Вставьте ссылку на изображение или загрузите файл.")

    class Meta:
        model = ProductCategory
        fields = ['image_url', 'upload']

    def save(self, commit=True):
        instance = super().save(commit=False)

        uploaded_file = self.cleaned_data.get('upload')
        url = self.cleaned_data.get('image_url')

        prefix = str(int(time.time()))
        if uploaded_file:
            # нормализуем имя файла: пробелы -> _, удаляем опасные символы
            original_name = uploaded_file.name
        elif url:
            original_name = url.split('/')[-1]
        else:
            original_name = 'image.jpg'

        safe_name = re.sub(r'\s+', '_', original_name)
        safe_name = re.sub(r'[^\w.\-]', '', safe_name)
        filename = f"{prefix}_{safe_name}"

        if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            raise forms.ValidationError("Файл должен быть изображением (PNG, JPG, JPEG, GIF).")

        path = f'uploads/{filename}'
        full_path = f'media/{path}'
        
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        print(full_path)

        if uploaded_file:
            with open(full_path, 'wb+') as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)
        elif url:
            response = requests.get(url.strip())
            if response.status_code == 200:
                with open(full_path, 'wb') as f:
                    f.write(response.content)

        instance.image_url = settings.HOST + '/' + full_path

        if commit:
            instance.save()
        return instance

class ProductCategoryAdmin(nested_admin.NestedModelAdmin):
    list_display = ('id', 'get_name')
    list_display_links = ('id', 'get_name')
    
    form = CategoryForm
    readonly_fields = ['preview']

    def preview(self, obj):
        if obj.image_url:
            return mark_safe(f'<img src="{obj.image_url}" width="100" />')
        return "-"
    
    def get_name(self, obj):
        translation = obj.translations.first()
        return translation.name if translation else '(Нет перевода)'
    get_name.short_description = 'Name'
    
    inlines = [ProductCategoryTranslationInline]


# --- Переводы характеристик ---
class ProductCharacteristicTranslationInline(nested_admin.NestedTabularInline):
    model = ProductCharacteristicTranslation
    extra = 1


# --- Характеристики ---
class ProductCharacteristicInline(nested_admin.NestedStackedInline):
    model = ProductCharacteristic
    extra = 1
    show_change_link = True
    inlines = [ProductCharacteristicTranslationInline]


class ProductTypeTranslationInline(nested_admin.NestedTabularInline):
    model = ProductTypeTranslation
    fields = ('language', 'name')
    extra = 1
    

class ProductTypeAdmin(nested_admin.NestedModelAdmin):
    inlines = [ProductTypeTranslationInline]



class ProductTranslationInline(nested_admin.NestedTabularInline):
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

        prefix = str(int(time.time()))
        if uploaded_file:
            # нормализуем имя файла: пробелы -> _, удаляем опасные символы
            original_name = uploaded_file.name
        elif url:
            original_name = url.split('/')[-1]
        else:
            original_name = 'image.jpg'

        safe_name = re.sub(r'\s+', '_', original_name)
        safe_name = re.sub(r'[^\w.\-]', '', safe_name)
        filename = f"{prefix}_{safe_name}"

        if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            raise forms.ValidationError("Файл должен быть изображением (PNG, JPG, JPEG, GIF).")

        path = f'uploads/{filename}'
        full_path = f'media/{path}'
        
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        print(full_path)

        if uploaded_file:
            with open(full_path, 'wb+') as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)
        elif url:
            response = requests.get(url.strip())
            if response.status_code == 200:
                with open(full_path, 'wb') as f:
                    f.write(response.content)

        instance.image_url = settings.HOST + '/' + full_path

        if commit:
            instance.save()
        return instance



class ProductImageInline(nested_admin.NestedTabularInline):
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
        fields = ['product_type', 'price_per_sqm', 'in_stock']


class ProductAdmin(nested_admin.NestedModelAdmin):
    list_display = ('id', 'get_name', 'price_per_sqm', 'created_at')
    list_display_links = ('id', 'get_name', 'price_per_sqm', 'created_at')

    search_fields = ('translations__name', 'tags')
    list_filter = ('translations__language',)
    inlines = [ProductImageInline, ProductCharacteristicInline, ProductTranslationInline]
    form = ProductForm

    def get_name(self, obj):
        translation = obj.translations.first()
        return translation.name if translation else '(Нет перевода)'
    get_name.short_description = 'Name'

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ['-created_at']


class ContactInquiryAdmin(nested_admin.NestedModelAdmin):
    list_display = ['name', 'email', 'phone', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'email', 'phone']
    readonly_fields = ['created_at']


admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ContactInquiry, ContactInquiryAdmin)
############################


def get_app_list(self, request):
    app_dict = self._build_app_dict(request)

    # Не сортируем модели по verbose_name, а оставляем в порядке регистрации
    return list(app_dict.values())

admin.AdminSite.get_app_list = get_app_list


###########################33
from django.contrib.auth.models import Group, User as DjangoUser
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

admin.site.unregister(Group)
admin.site.unregister(DjangoUser)

DjangoUser._meta.verbose_name = "Админ"
DjangoUser._meta.verbose_name_plural = "Админы"


admin.site.register(DjangoUser, DjangoUserAdmin)

