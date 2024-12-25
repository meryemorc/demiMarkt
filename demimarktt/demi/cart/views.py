from django.shortcuts import render, redirect, get_object_or_404  # type: ignore
from django.contrib import messages  # type: ignore
from django.contrib.auth.decorators import login_required  # type: ignore
from django.contrib.auth.hashers import make_password, check_password  # type: ignore
from cart.models import User, Cart, CartItem  # Modellerinizi kontrol edin
from products.models import Product


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)

            if check_password(password, user.password):
                request.session['user_id'] = user.id  # Burada user_id doğru şekilde kaydediliyor mu kontrol edin
                messages.success(request, 'Giriş başarılı!')
                return redirect('homepage')
            else:
                messages.error(request, 'Hatalı şifre!')
        except User.DoesNotExist:
            messages.error(request, 'Bu e-posta adresine sahip kullanıcı bulunamadı.')
    
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Bu e-posta adresiyle kayıt yapılmış. Giriş yapabilirsiniz.')
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


def logout(request):
    request.session.flush()
    messages.success(request, 'Başarıyla çıkış yaptınız.')
    return redirect('login')


def view_cart(request):
    user_id = request.session.get('user_id')
    if user_id:
        # Kullanıcı giriş yapmışsa, kullanıcıya ait sepeti getir
        user_cart, _ = Cart.objects.get_or_create(user_id=user_id)
    else:
        # Giriş yapılmamışsa anonim bir sepet oluştur
        user_cart, _ = Cart.objects.get_or_create(user_id=None)

    cart_items = user_cart.items.all()
    total_price = user_cart.total_price if user_cart.items.exists() else 0

    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })




@login_required(login_url='/login/')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user_id = request.session.get('user_id')
    user_cart, _ = Cart.objects.get_or_create(user_id=user_id)
    cart_item, created = CartItem.objects.get_or_create(cart=user_cart, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{product.product_name} sepete eklendi.")
    return redirect('view_cart')


@login_required(login_url='/login/')
def remove_from_cart(request, product_id):
    user_id = request.session.get('user_id')
    user_cart = get_object_or_404(Cart, user_id=user_id)
    cart_item = get_object_or_404(CartItem, cart=user_cart, product_id=product_id)
    cart_item.delete()

    messages.success(request, "Ürün sepetten kaldırıldı.")
    return redirect('view_cart')


@login_required(login_url='/login/')
def checkout(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')
        card_number = request.POST.get('card_number')
        expiry_date = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')

        if not address or not city or not postal_code or not card_number or not expiry_date or not cvv:
            return render(request, 'cart/checkout.html', {'error': 'Lütfen tüm alanları doldurun!'})

        user_id = request.session.get('user_id')
        user = get_object_or_404(User, id=user_id)

        try:
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

            Cart.objects.filter(user=user).delete()  # Sepeti boşalt
            messages.success(request, 'Sipariş başarıyla tamamlandı!')
            return redirect('homepage')
        except Exception as e:
            return render(request, 'cart/checkout.html', {'error': f"Hata: {str(e)}"})

    return render(request, 'cart/checkout.html')
