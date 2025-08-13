from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('calculator/', views.calculator, name='calculator'),
    path('contact/', views.contact, name='contact'),
    path('ajax/calculate/', views.ajax_calculate_cost, name='ajax_calculate_cost'),
]
