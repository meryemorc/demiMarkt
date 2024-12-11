from django.http import HttpResponse

# Ürün listesi
def product_list(request):
    return HttpResponse("Ürün listesi görüntülendi!")  # Geçici çıktı

# Ürün detayları
def product_detail(request, product_id):
    return HttpResponse(f"Ürün detayları görüntülendi! Ürün ID: {product_id}")  # Geçici çıktı

# Kategoriye göre ürünler
def product_by_category(request, category_name):
    return HttpResponse(f"Kategori: {category_name} için ürünler listelendi!")  # Geçici çıktı

# Ürün arama
def search_products(request):
    query = request.GET.get('q', '')
    return HttpResponse(f"Arama yapıldı! Aranan kelime: {query}")  # Geçici çıktı
