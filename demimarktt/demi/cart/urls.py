from django.urls import path # type: ignore
from . import views
from django.contrib.auth import views as auth_views # type: ignore


urlpatterns = [
    path('', views.view_cart, name='view_cart'),
    path('register/', views.register, name='register'),  # Kayıt Sayfası
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),  # Giriş Sayfası
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),  # Çıkış
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
]
