from django.urls import path, include  # type: ignore
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),  # Ana sayfa
    path('about/', views.about, name='about'),  # Hakkında
    path('contact/', views.contact, name='contact'),  # İletişim
    path('cart/', include('cart.urls')),  # Kullanıcı ve sepet işlemleri
]
