from django.urls import path  # type: ignore
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),  # Kayıt Ol Sayfası
    path('login/', views.login, name='login'),  # Giriş Yap Sayfası
    path('logout/', views.logout, name='logout'),  # Çıkış Yap
    path('', views.view_cart, name='view_cart'),  # Sepeti Görüntüle
    path('add/<str:product_id>/', views.add_to_cart, name='add_to_cart'),  # Ürün Ekle
    path('remove/<str:product_id>/', views.remove_from_cart, name='remove_from_cart'),  # Ürün Çıkar
    path('checkout/', views.checkout, name='checkout'),  # Ödeme Sayfası
]
