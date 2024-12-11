from django.shortcuts import render
from django.http import HttpResponse

# Kullanıcı giriş sayfası
def login_view(request):
    return HttpResponse("Giriş sayfası!")  # Geçici çıktı

# Kullanıcı kayıt sayfası
def register_view(request):
    return HttpResponse("Kayıt sayfası!")  # Geçici çıktı

# Kullanıcı çıkış işlemi
def logout_view(request):
    return HttpResponse("Çıkış yapıldı!")  # Geçici çıktı

# Kullanıcı profil sayfası
def profile_view(request):
    return HttpResponse("Profil sayfası!")  # Geçici çıktı
