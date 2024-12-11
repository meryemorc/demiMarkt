from django.shortcuts import render
from django.http import HttpResponse

# Ana arama sayfası
def search_page(request):
    return HttpResponse("Arama sayfası!")  # Geçici çıktı

# Arama sonuçları sayfası
def search_results(request):
    query = request.GET.get('q', '')  # Kullanıcının arama yaptığı kelime
    return HttpResponse(f"Arama sonuçları görüntülendi! Aranan kelime: {query}")  # Geçici çıktı
