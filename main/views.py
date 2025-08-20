from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from decimal import Decimal

from django.utils import translation

from .models import Product, ContactInquiry, ProductType, ProductCategory
from .forms import ContactForm, CalculatorForm


def home(request):
    language = translation.get_language()
    
    # Получаем все категории с их переводами
    categories = ProductCategory.objects.prefetch_related('translations').all()
    
    # Формируем данные для шаблона
    categories_data = []
    for category in categories:
        category_data = category.get_translation_json(language)
        category_data['image_url'] = category.image_url
        categories_data.append(category_data)
    
    return render(request, 'main/home.html', {
        'categories': categories_data
    })


def category_detail(request, category_id):
    language = translation.get_language()
    category = get_object_or_404(ProductCategory, id=category_id)
    
    # Получаем все типы продуктов для этой категории с их продуктами
    product_types = ProductType.objects.filter(category=category).prefetch_related(
        'products__translations', 
        'products__images',
        'products__characteristics__translations'
    ).all()
    
    # Собираем все уникальные характеристики для фильтрации
    unique_characteristics = {}
    all_products = []
    
    # Формируем данные для шаблона
    product_sections = []
    for product_type in product_types:
        if product_type.products.exists():  # Показываем только типы с продуктами
            products_data = []
            for product in product_type.products.all():
                product_data = product.get_translation_json(language)
                products_data.append(product_data)
                all_products.append(product_data)
                
                # Собираем уникальные характеристики
                for char in product_data.get('characteristics', []):
                    char_name = char['name']
                    char_value = char['value']
                    if char_name not in unique_characteristics:
                        unique_characteristics[char_name] = set()
                    unique_characteristics[char_name].add(char_value)
            
            section_data = {
                'type_name': product_type.get_name(language),
                'products': products_data
            }
            product_sections.append(section_data)
    
    # Преобразуем sets в списки для JSON сериализации
    characteristics_filter = {}
    for name, values in unique_characteristics.items():
        characteristics_filter[name] = sorted(list(values))
    
    # Получаем минимальную и максимальную цены для слайдера
    prices = []
    for product in all_products:
        price = product.get('price_per_sqm', 0)
        if price and price > 0:
            prices.append(float(price))
    
    if prices:
        min_price = min(prices)
        max_price = max(prices)
        # Добавляем небольшой буфер для удобства использования слайдера
        price_range = max_price - min_price
        if price_range > 0:
            buffer = price_range * 0.1  # 10% буфер
            min_price = max(0, min_price - buffer)
            max_price = max_price + buffer
    else:
        min_price = 0
        max_price = 100

    print(f"Prices found: {prices}")
    print(f"Min price: {min_price}")
    print(f"Max price: {max_price}")
    print(f"All products data: {[{'name': p.get('name'), 'price': p.get('price_per_sqm')} for p in all_products]}")
    print(f"Product sections: {len(product_sections)}")
    return render(request, 'main/category_detail.html', {
        'category': category.get_translation_json(language),
        'product_sections': product_sections,
        'unique_characteristics': characteristics_filter,
        'all_products': all_products,
        'min_price': min_price,
        'max_price': max_price
    })
    

def product_detail(request, product_id):
    language = translation.get_language()
    product = get_object_or_404(Product, id=product_id)

    return render(request, 'main/product_detail.html', {
        'product': product.get_translation_json(language),
        'category': product.product_type.category.get_translation_json(language)
    })


def calculator(request):
    """Cost calculator page"""
    language = translation.get_language()

    print(request.method)
    form = CalculatorForm()
    estimated_cost = None
    
    if request.method == 'POST':
        form = CalculatorForm(request.POST)
        if form.is_valid():
            width = form.cleaned_data['width']
            length = form.cleaned_data['length']
            ceiling_type = form.cleaned_data['ceiling_type']
            
            # Calculate area and cost
            area = width * length
            estimated_cost = area * ceiling_type.price_per_sqm
            
            # Return JSON response for AJAX requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'area': float(area),
                    'cost': float(estimated_cost),
                    'product_name': ceiling_type.get_name(language),
                    'price_per_sqm': float(ceiling_type.price_per_sqm)
                })
    
    products = Product.objects.all()
    return render(request, 'main/calculator.html', {
        'form': form,
        'products': [p.get_translation_json(language) for p in products],
        'estimated_cost': estimated_cost
    })


def contact(request):
    """Contact page with form"""
    language = translation.get_language()

    success_text = {
        'ru': 'Спасибо за вашу заявку! Мы свяжемся с вами в ближайшее время.',
        'en': 'Thank you for your inquiry! We will contact you soon.',
        'ky': 'Сураныч, сиздин кайрылууңуз үчүн рахмат! Биз сиз менен жакын арада байланышабыз.'
    }.get(language, 'Thank you for your inquiry! We will contact you soon.')

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, success_text)
            return redirect('contact')
    else:
        form = ContactForm()
    
    return render(request, 'main/contact.html', {'form': form})


def ajax_calculate_cost(request):
    """AJAX endpoint for cost calculation"""
    print(request, 'ajax_calculate_cost')
    if request.method == 'POST':
        try:
            width = Decimal(request.POST.get('width', '0'))
            length = Decimal(request.POST.get('length', '0'))
            product_id = request.POST.get('product_id')
            
            if width > 0 and length > 0 and product_id:
                product = get_object_or_404(Product, id=product_id)
                area = width * length
                cost = area * product.price_per_sqm
                
                return JsonResponse({
                    'success': True,
                    'area': float(area),
                    'cost': float(cost),
                    'product_name': product.name,
                    'price_per_sqm': float(product.price_per_sqm)
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid input values'
                })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def search(request):
    """Search products by name, characteristics, and description in all languages"""
    language = translation.get_language()
    query = request.GET.get('q', '').strip()
    
    products = Product.objects.none()
    
    if query:
        language = translation.get_language()
        search_query = (
            Q(translations__language=language, translations__name__icontains=query) |
            Q(translations__language=language, translations__description__icontains=query) |
            Q(characteristics__translations__value__icontains=query)
        )

        products = (
            Product.objects.filter(search_query)
            .prefetch_related("images", "translations", "characteristics__translations")
            .distinct()
            .order_by("id")  # или created_at, т.к. name нет
        )
    
    # Pagination
    paginator = Paginator(products, 12)  # Show 12 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Convert products to translation JSON
    products_data = []
    for product in page_obj:
        products_data.append(product.get_translation_json(language))
    
    context = {
        'query': query,
        'products': products_data,
        'qnt': products.count(),
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    }
    
    return render(request, 'main/search_results.html', context)

