from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),  # Tüm ürünlerin listelendiği sayfa
    path('<int:product_id>/', views.product_detail, name='product_detail'),  # Tek bir ürünün detay sayfası
    path('category/<str:category_name>/', views.product_by_category, name='product_by_category'),  # Kategoriye göre ürün listesi
    path('search/', views.search_products, name='search_products'),  # Ürün arama sayfası
]
