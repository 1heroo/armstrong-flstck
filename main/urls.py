from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('calculator/', views.calculator, name='calculator'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search, name='search'),
    path('ajax/calculate/', views.ajax_calculate_cost, name='ajax_calculate_cost'),
]
