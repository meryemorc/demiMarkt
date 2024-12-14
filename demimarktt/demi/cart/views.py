from django.http import HttpResponse  # type: ignore
from django.shortcuts import render, redirect # type: ignore
from .models import User, Address, PaymentMethod  # Modellerinizi kontrol edin
from django.contrib import messages # type: ignore
from django.contrib.auth import login, logout  # type: ignore # Django'nun oturum kontrolü
from django.contrib.auth.hashers import make_password  # type: ignore
from django.contrib.auth.hashers import check_password # type: ignore


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Kullanıcıyı e-posta ile bul
            user = User.objects.get(email=email)

            # Şifreyi kontrol et
            if check_password(password, user.password):
                # Giriş başarılı
                request.session['user_id'] = user.id  # Oturumu başlat
                messages.success(request, 'Giriş başarılı!')
                return redirect('homepage')  # Anasayfa veya başka bir sayfaya yönlendir
            else:
                # Şifre hatalı
                messages.error(request, 'Hatalı şifre. Lütfen tekrar deneyin.')
        except User.DoesNotExist:
            # Kullanıcı bulunamadı
            messages.error(request, 'Bu e-posta ile kayıtlı bir kullanıcı yok.')

    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Veritabanında aynı e-posta adresi varsa hata döndür
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Bu e-posta adresiyle kayıt yapılmış. Giriş yapabilirsiniz.')
            return render(request, 'register.html', {'show_login_button': True})  # Login butonunu göstermek için değişken ekledik
        
        # Kullanıcıyı oluştur ve şifreyi hashle
        user = User(
            full_name=full_name,
            email=email,
            password=make_password(password)  # Şifreyi hashle
        )
        user.save()  # Kullanıcıyı veritabanına kaydet
        
        messages.success(request, 'Kayıt başarılı! Şimdi giriş yapabilirsiniz.')
        return redirect('login')

    return render(request, 'register.html', {'show_login_button': False})



def logout(request):
    request.session.flush()  # Tüm oturum verilerini siler
    messages.success(request, 'Başarıyla çıkış yaptınız.')
    return redirect('login')  # Giriş sayfasına yönlendirme


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
