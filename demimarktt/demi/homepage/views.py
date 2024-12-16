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
        if product.price is None or (isinstance(product.price, float) and math.isnan(product.price)):
            product.temp_price = "500 $"  # Fiyat bilinmiyorsa 500 $ olarak ayarla
        else:
            product.temp_price = f"{product.price} $"

    # Markaları çek ve popüler/diğer brand'ları ayır
    all_brands = (
        Product.objects
        .values('brand')
        .annotate(brand_count=Count('brand'))
        .filter(brand__isnull=False)
        .exclude(brand="nan")
        .order_by('-brand_count')
    )
    # Popüler brand'lar ve diğer brand'ların sayısını hesapla
    popular_brands = [brand for brand in all_brands if brand['brand_count'] >= 200]
    other_brands = [brand['brand'] for brand in all_brands if brand['brand_count'] < 200]

    # Brand filtresi
    if brand_filter == 'other':
        products = products.filter(brand__in=other_brands)  # "Diğer" brand'ları filtrele
    elif brand_filter:
        products = products.filter(brand=brand_filter)  # Seçilen brand'ı filtrele

    # Sayfalama
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)

    return render(request, 'homepage/homepage.html', {
        'products': products_page,
        'popular_brands': popular_brands,
        'other_brands_count': sum(brand['brand_count'] for brand in all_brands if brand['brand_count'] < 200),
    })


def about(request):
    return HttpResponse("Hakkımızda")


def contact(request):
    return HttpResponse("İletişim")


def profile_view(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = User.objects.get(id=user_id)  # Kullanıcı bilgilerini al
        return render(request, 'profile.html', {'user': user})
    else:
        return redirect('login')  # Oturum yoksa login sayfasına yönlendir
