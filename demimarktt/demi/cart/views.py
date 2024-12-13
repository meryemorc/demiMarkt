from django.shortcuts import render, redirect  # type: ignore
from django.http import HttpResponse  # type: ignore
from .models import User, Address, PaymentMethod  # Modellerinizi kontrol edin
from django.contrib.auth.decorators import login_required  # type: ignore # Kullanıcı oturumu kontrolü için
from django.contrib.auth.forms import UserCreationForm  # type: ignore  # Django'nun hazır formu
from django.contrib import messages  # type: ignore # Kullanıcıya mesajlar göstermek için


@login_required  # Kullanıcı giriş yapmamışsa login sayfasına yönlendirir
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kayıt başarılı! Şimdi giriş yapabilirsiniz.')
            return redirect('login')  # Kayıttan sonra giriş sayfasına yönlendir
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# Kullanıcının sepetini görüntüleme
def view_cart(request):
    cart_items = [
        {'product': {'id': 2, 'name': 'Telefon', 'price': 15000}, 'quantity': 1},
        {'product': {'id': 3, 'name': 'Laptop', 'price': 25000}, 'quantity': 2},
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

def checkout(request):
    user_saved = False  # Kullanıcı bilgisi kaydedildi mi kontrolü

    if request.method == 'POST':
        # Formdan gelen verileri al
        address = request.POST.get('address')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')
        card_number = request.POST.get('card_number')
        expiry_date = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')

        # Doğrulama
        if not address or not city or not postal_code or not card_number or not expiry_date or not cvv:
            return render(request, 'cart/checkout.html', {'error': 'Lütfen tüm alanları doldurun!'})

        # Giriş yapmış kullanıcıyı al
        user = request.user

        # Kullanıcıya adres ve ödeme bilgisi ekle
        try:
            user_profile = User.objects.get(id=user.id)  # Giriş yapmış kullanıcıyı al
            user_profile.addresses.append(Address(address=address, city=city, postal_code=postal_code))
            user_profile.payment_methods.append(PaymentMethod(card_number=card_number, expiry_date=expiry_date, cvv=cvv))
            user_profile.save()
            user_saved = True  # Kayıt başarılı
        except Exception as e:
            # Kayıt başarısız olursa hata göster
            return render(request, 'cart/checkout.html', {'error': f"Kayıt sırasında bir hata oluştu: {str(e)}"})

    # GET isteği veya POST işlemi sonrası durumu render et
    return render(request, 'cart/checkout.html', {'user_saved': user_saved})
