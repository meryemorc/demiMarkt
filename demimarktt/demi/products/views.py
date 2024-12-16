from django.shortcuts import render, get_object_or_404 # type: ignore
from .models import Product

def product_detail(request, product_id):
    # ID'ye göre ürünü bul, eğer bulunamazsa 404 döner
    product = get_object_or_404(Product, ID=product_id)
    return render(request, 'products/product_detail.html', {'product': product})
