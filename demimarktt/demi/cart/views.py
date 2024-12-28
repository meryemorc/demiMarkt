from django.shortcuts import render, redirect,get_object_or_404  # type: ignore
from django.contrib.auth import authenticate, login, logout  # type: ignore
from django.contrib.auth.decorators import login_required  # type: ignore
from django.contrib.auth.models import User  # type: ignore
from django.contrib import messages  # type: ignore # Mesaj modülünü ekliyoruz
from django.template.loader import render_to_string # type: ignore
from django.http import JsonResponse # type: ignore
from .models import Cart, CartItem, Product
from .strategies import CardPaymentStrategy, EFTPaymentStrategy, CODPaymentStrategy
from .observers import PaymentPublisher, StockUpdateObserver, MailNotificationObserver


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, ID=product_id)
 # Ürünü al
    cart, created = Cart.objects.get_or_create(user=request.user)  # Kullanıcıya ait sepeti al veya oluştur

    # Sepette aynı üründen var mı kontrol et
    cart_item, item_created = CartItem.objects.get_or_create(
        product=product,
        defaults={'price': product.price, 'quantity': 1, 'subtotal': product.price}
    )

    if not item_created:
        # Eğer ürün zaten varsa miktarını artır
        cart_item.quantity += 1
        cart_item.subtotal = cart_item.quantity * cart_item.price
        cart_item.save()

    cart.items.add(cart_item)  # Sepete ekle
    return redirect('view_cart')  # Sepet sayfasına yönlendir


  # Sepet detay sayfasına yönlendirme (uygun bir rota ekleyin)
@login_required
def view_cart(request):
    cart = Cart.objects.filter(user=request.user).first()
    return render(request, 'cart/cart.html', {'cart': cart})

# Kullanıcı Girişi
def login_view(request):
    if request.user.is_authenticated:  # Kullanıcı zaten giriş yapmışsa
        return redirect('homepage')  # Doğrudan homepage'e yönlendir
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Giriş başarılı! Hoş geldiniz.')  # Başarı mesajı
            return redirect('homepage')  # Giriş başarılı, homepage'e yönlendir
        else:
            messages.error(request, 'Geçersiz kullanıcı adı veya şifre!')
    return render(request, 'login.html')


# Kullanıcı Kaydı
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not User.objects.filter(email=email).exists():
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)  # Kullanıcıyı otomatik giriş yap
            return redirect('homepage')
        else:
            return render(request, 'register.html', {'error': 'Bu email zaten kullanılıyor!'})
    return render(request, 'register.html')

# Kullanıcı Çıkışı
def logout_view(request):
    logout(request)
    return redirect('homepage')

@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})

@login_required
def increase_quantity(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')

@login_required
def decrease_quantity(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('view_cart')

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    return redirect('view_cart')

@login_required
def checkout_view(request):
    return render(request, 'cart/checkout.html')


@login_required
def process_payment(request):
    if request.method == 'POST':
        # Kullanıcıdan gelen ödeme bilgilerini al
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method')

        # Sepeti al
        cart = Cart.objects.filter(user=request.user).first()
        if not cart or not cart.items.exists():
            messages.error(request, 'Sepetiniz boş! Lütfen ürün ekleyin.')
            return redirect('view_cart')

        # Sepetin ilk ürünü örnek olarak alınıyor (tüm ürünler için genişletilebilir)
        first_item = cart.items.first()

        # Ödeme bilgilerini hazırlayın
        payment_data = {
            'user_email': request.user.email,
            'product': first_item.product.product_name,  # Burada 'name' yerine 'product_name' kullanıldı
            'quantity': first_item.quantity,
            'amount': first_item.subtotal,  # Toplam tutar
            'unit_price': first_item.price,  # Birim fiyat
        }

        # Observer Pattern: Publisher ve Observer'ları oluştur
        publisher = PaymentPublisher()
        stock_observer = StockUpdateObserver()
        mail_observer = MailNotificationObserver()

        # Observer'ları Publisher'a bağla
        publisher.attach(stock_observer)
        publisher.attach(mail_observer)

        # Ödeme yöntemi kontrolü ve işlem (Strategy Pattern ile)
        if payment_method == 'credit_card':
            card_number = request.POST.get('card_number')
            expiry_date = request.POST.get('expiry_date')
            cvv = request.POST.get('cvv')

            if not card_number or not expiry_date or not cvv:
                messages.error(request, 'Kredi kartı bilgileri eksik! Lütfen kontrol edin.')
                return redirect('checkout')

            strategy = CardPaymentStrategy()
            strategy.process_payment(payment_data['amount'], card_number=card_number, expiry_date=expiry_date, cvv=cvv)

        elif payment_method == 'eft':
            bank_account = request.POST.get('bank_account')

            if not bank_account:
                messages.error(request, 'EFT bilgileri eksik! Lütfen kontrol edin.')
                return redirect('checkout')

            strategy = EFTPaymentStrategy()
            strategy.process_payment(payment_data['amount'], bank_account=bank_account)

        elif payment_method == 'cash_on_delivery':
            strategy = CODPaymentStrategy()
            strategy.process_payment(payment_data['amount'])

        else:
            messages.error(request, 'Geçersiz ödeme yöntemi seçildi.')
            return redirect('checkout')

        # Observer'ları bilgilendir (Ödeme sonrası süreçler)
        publisher.process_payment(payment_data)

        # Ödeme sonrası başarı sayfasına yönlendir
        messages.success(request, 'Ödemeniz başarıyla alındı!')
        return redirect('order_confirmation')

    # GET isteği gelirse ödeme sayfasına yönlendirin
    return redirect('checkout')



@login_required
def order_confirmation(request):
    return render(request, 'cart/order_confirmation.html')
