from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from decimal import Decimal

from django.utils import translation

from .models import Product, ContactInquiry, ProductType
from .forms import ContactForm, CalculatorForm


def home(request):
    langauge = translation.get_language()
    
    # Получаем все типы продуктов с их продуктами
    product_types = ProductType.objects.prefetch_related('products__translations', 'products__images').all()
    
    # Формируем данные для шаблона
    product_sections = []
    for product_type in product_types:
        if product_type.products.exists():  # Показываем только типы с продуктами
            section_data = {
                'type_name': product_type.get_name(langauge),
                'products': [p.get_translation_json(langauge) for p in product_type.products.all()]
            }
            product_sections.append(section_data)
    return render(request, 'main/home.html', {
        'product_sections': product_sections
    })


def product_detail(request, product_id):
    langauge = translation.get_language()
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'main/product_detail.html', {'product': product.get_translation_json(langauge)})


def calculator(request):
    """Cost calculator page"""
    langauge = translation.get_language()

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
                    'product_name': ceiling_type.get_name(langauge),
                    'price_per_sqm': float(ceiling_type.price_per_sqm)
                })
    
    products = Product.objects.all()
    return render(request, 'main/calculator.html', {
        'form': form,
        'products': [p.get_translation_json(langauge) for p in products],
        'estimated_cost': estimated_cost
    })


def contact(request):
    """Contact page with form"""
    langauge = translation.get_language()

    success_text = {
        'ru': 'Спасибо за вашу заявку! Мы свяжемся с вами в ближайшее время.',
        'en': 'Thank you for your inquiry! We will contact you soon.',
        'ky': 'Сураныч, сиздин кайрылууңуз үчүн рахмат! Биз сиз менен жакын арада байланышабыз.'
    }.get(langauge, 'Thank you for your inquiry! We will contact you soon.')

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

