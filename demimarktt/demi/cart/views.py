from django.shortcuts import render, redirect # type: ignore
from django.http import HttpResponse # type: ignore

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
    from django.shortcuts import render # type: ignore

# Ödeme ve adres bilgileri için checkout işlemi
def checkout(request):
    if request.method == 'POST':
        # Formdan gelen verileri al
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')
        phone = request.POST.get('phone')
        card_number = request.POST.get('card_number')
        expiry_date = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')

        # Basit doğrulama
        if not full_name or not address or not city or not postal_code or not phone or not card_number or not expiry_date or not cvv:
            return HttpResponse("Lütfen tüm alanları doldurun.", status=400)

        # Ödeme işlemini simüle et (gerçek bir ödeme API'si entegre edilebilir)
        if card_number == "1234567812345678":  # Örnek geçerli kart numarası
            # Ödeme başarılı, siparişi kaydedin (örneğin bir veritabanına)
            print(f"Ödeme alındı: {full_name}, {address}, {card_number}")
            return HttpResponse("Ödeme başarıyla tamamlandı!")
        else:
            return HttpResponse("Ödeme başarısız. Lütfen bilgilerinizi kontrol edin.", status=400)

    # GET isteği için checkout sayfasını render et
    cart_items = [
        {'product': {'id': 2, 'name': 'Telefon', 'price': 15000}, 'quantity': 1},
        {'product': {'id': 3, 'name': 'Laptop', 'price': 25000}, 'quantity': 2},
    ]

    for item in cart_items:
        item['total'] = item['product']['price'] * item['quantity']

    total_price = sum(item['total'] for item in cart_items)
    return render(request, 'cart/checkout.html', {'cart_items': cart_items, 'total_price': total_price})





