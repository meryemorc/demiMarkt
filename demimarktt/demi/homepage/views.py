from django.shortcuts import render, redirect  # type: ignore
from django.http import HttpResponse  # type: ignore
from cart.models import User  # type: ignore
from products.models import Product  # type: ignore
from django.core.paginator import Paginator  # type: ignore
from django.db.models import Count  # type: ignore
import math  # nan kontrolü için

def homepage(request):
    # Ürünleri çek
    products = Product.objects.all()
    brand_filter = request.GET.get('brand')

    # Ürünlerin fiyatlarını kontrol et ve düzelt
    for product in products:
        try:
            # Virgülleri noktaya çevirip float'a dönüştür
            price = float(str(product.price).replace(',', '').replace(' ', ''))
            if math.isnan(price):  # Eğer fiyat NaN ise
                product.temp_price = "500 $"
            else:
                product.temp_price = f"{price:.2f} $"  # Formatlı fiyat
        except (ValueError, TypeError):  # Geçersiz veya boş fiyat durumunda
            product.temp_price = "500 $"

    # Markaları çek ve filtrele
    all_brands = (
        Product.objects
        .values('brand')
        .annotate(brand_count=Count('brand'))
        .filter(brand__isnull=False, brand__gt='')  # Boş olmayanları filtrele
        .exclude(brand="nan")
        .order_by('-brand_count')
    )
    popular_brands = all_brands[:10]  # İlk 10 markayı al

    # Debug: Terminale markaları yazdır
    print("Popular brands:", popular_brands)

    other_brands_count = sum(brand['brand_count'] for brand in all_brands[10:])

    # Brand filtresi
    if brand_filter == 'other':
        other_brands = [brand['brand'] for brand in all_brands[10:]]
        products = products.filter(brand__in=other_brands)
    elif brand_filter:
        products = products.filter(brand=brand_filter)

    # Sayfalama
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)

    return render(request, 'homepage/homepage.html', {
        'products': products_page,
        'popular_brands': popular_brands,
        'other_brands_count': other_brands_count,
    })

def about(request):
    return HttpResponse("Hakkımızda")

def contact(request):
    return HttpResponse("İletişim")

def profile_view(request):
    user_id = request.session.get('user_id')
    if user_id:
        try:
            user = User.objects.get(id=user_id)  # Kullanıcı bilgilerini al
            return render(request, 'profile.html', {'user': user})
        except User.DoesNotExist:
            return redirect('login')  # Kullanıcı bulunamazsa login sayfasına yönlendir
    else:
        return redirect('login')  # Oturum yoksa login sayfasına yönlendir
