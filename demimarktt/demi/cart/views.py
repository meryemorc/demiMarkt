from django.shortcuts import render, redirect
from django.http import HttpResponse

# Kullanıcının sepetini görüntüleme
def view_cart(request):
    return HttpResponse("Sepet içeriği burada listelenecek.")

# Sepete ürün ekleme
def add_to_cart(request, product_id):
    return HttpResponse(f"Ürün {product_id} sepete eklendi.")

# Sepetten ürün kaldırma
def remove_from_cart(request, product_id):
    return HttpResponse(f"Ürün {product_id} sepetten kaldırıldı.")

# Sepetteki ürün miktarını güncelleme
def update_cart(request, product_id):
    return HttpResponse(f"Ürün {product_id} miktarı güncellendi.")

# Sepeti tamamen temizleme
def clear_cart(request):
    return HttpResponse("Sepet temizlendi.")

# Ödeme sayfası
def checkout(request):
    return HttpResponse("Ödeme sayfası.")



