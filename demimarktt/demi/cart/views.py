from django.shortcuts import render, redirect, get_object_or_404  # type: ignore
from django.contrib import messages  # type: ignore
from django.contrib.auth.hashers import make_password, check_password  # type: ignore
from cart.models import User, Cart  # Sepet ve kullanıcı modelleri
from products.models import Product
from django.utils.crypto import get_random_string  # type: ignore


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, ID=product_id)

    if request.method == 'POST':
        selected_color = request.POST.get('selected_color')

        # Renk kontrolü
        if selected_color not in product.color_list:
            messages.error(request, "Seçilen renk bu ürün için mevcut değil.")
            return redirect('product_detail', product_id=product_id)

        # Sepeti kontrol et
        user_id = request.session.get('user_id')
        session_id = request.session.session_key or get_random_string(32)

        cart, _ = Cart.objects.get_or_create(
            user_id=user_id,
            session_id=session_id if not user_id else None
        )

        # Ürünü sepete ekle
        cart.add_item(product, selected_color=selected_color)

        # Başarılı mesajı
        messages.success(request, f"{product.product_name} ({selected_color}) sepete eklendi.")

        # Sepet sayfasına yönlendirme
        return redirect('view_cart')

    return redirect('product_detail', product_id=product_id)


# Kullanıcı Girişi
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                request.session['user_id'] = str(user.id)  # `user_id` oturumda tutulur
                messages.success(request, 'Giriş başarılı!')
                return redirect('homepage')
            else:
                messages.error(request, 'Hatalı şifre!')
        except User.DoesNotExist:
            messages.error(request, 'Bu e-posta adresine sahip kullanıcı bulunamadı.')

    return render(request, 'login.html')


# Kullanıcı Kaydı
def register(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Bu e-posta adresi zaten kayıtlı. Giriş yapabilirsiniz.')
            return render(request, 'register.html', {'show_login_button': True})

        user = User(
            full_name=full_name,
            email=email,
            password=make_password(password)
        )
        user.save()

        messages.success(request, 'Kayıt başarılı! Şimdi giriş yapabilirsiniz.')
        return redirect('login')

    return render(request, 'register.html', {'show_login_button': False})


# Çıkış Yapma
def logout(request):
    request.session.flush()
    messages.success(request, 'Başarıyla çıkış yaptınız.')
    return redirect('login')


# Sepeti Görüntüleme
def view_cart(request):
    user_id = request.session.get('user_id')
    session_id = request.session.session_key or get_random_string(32)

    cart, _ = Cart.objects.get_or_create(
        user_id=user_id,
        session_id=session_id if not user_id else None
    )

    return render(request, 'cart/cart.html', {
        'cart_items': cart.items or [],
        'total_price': cart.total_price,
    })




# Sepetten Ürün Çıkarma
def remove_from_cart(request, product_id):
    user_id = request.session.get('user_id')
    session_id = request.session.session_key

    cart = Cart.objects.filter(
        user_id=user_id,
        session_id=session_id if not user_id else None
    ).first()

    if cart:
        cart.remove_item(product_id)
        messages.success(request, "Ürün sepetten kaldırıldı.")
    else:
        messages.error(request, "Sepet bulunamadı.")
    return redirect('view_cart')


# Sipariş Tamamlama
def checkout(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "Sipariş tamamlamak için lütfen giriş yapınız.")
        return redirect('login')

    if request.method == 'POST':
        address = request.POST.get('address')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')
        card_number = request.POST.get('card_number')
        expiry_date = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')

        if not all([address, city, postal_code, card_number, expiry_date, cvv]):
            return render(request, 'cart/checkout.html', {'error': 'Lütfen tüm alanları doldurun!'})

        user = get_object_or_404(User, id=user_id)
        try:
            # Adres ve ödeme bilgisi ekle
            user.addresses.append({
                "address": address,
                "city": city,
                "postal_code": postal_code
            })
            user.payment_methods.append({
                "card_number": card_number,
                "expiry_date": expiry_date,
                "cvv": cvv
            })
            user.save()

            # Sepeti temizle
            Cart.objects.filter(user_id=user_id).delete()
            messages.success(request, 'Sipariş başarıyla tamamlandı!')
            return redirect('homepage')
        except Exception as e:
            return render(request, 'cart/checkout.html', {'error': f"Hata: {str(e)}"})

    return render(request, 'cart/checkout.html')
