from django.shortcuts import render, redirect
from django.http import HttpResponse

# Kullanıcının sepetini görüntüleme
def view_cart(request):
    cart_items = [
        {'product': {'id': 2, 'name': 'Telefon', 'price': 15000}, 'quantity': 1},
        {'product': {'id': 2, 'name': 'Laptop', 'price': 25000}, 'quantity': 2},
    ]

    for item in cart_items:
        item['total'] = item['product']['price'] * item['quantity']

    total_price = sum(item['total'] for item in cart_items)
    return render(request, 'cart/cart.html', {'cart_items': cart_items, 'total_price': total_price})

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



