from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),  # Kullanıcı giriş sayfası
    path('register/', views.register_view, name='register'),  # Kullanıcı kayıt sayfası
    path('logout/', views.logout_view, name='logout'),  # Kullanıcı çıkış işlemi
    path('profile/', views.profile_view, name='profile'),  # Kullanıcı profil sayfası
]
