from django.shortcuts import render, get_object_or_404  # type: ignore
from .models import Product

def product_detail(request, product_id):
    # ID'ye göre ürünü bul, eğer bulunamazsa 404 döner
    product = get_object_or_404(Product, ID=product_id)
    
    # Renkleri listeye ayır
    available_colors = product.available_colors.split(", ") if product.available_colors else []
    
    # Mevcut depolama seçenekleri
    storage_options = [64, 128, 256, 512]  # Örnek depolama seçenekleri
    active_storage = product.storage_gb  # Güncel depolama alanı

    return render(request, 'products/product_detail.html', {
        'product': product,
        'available_colors': available_colors,  # Şablon için renkler
        'storage_options': storage_options,  # Şablon için depolama seçenekleri
        'active_storage': active_storage  # Aktif depolama seçeneği
    })
