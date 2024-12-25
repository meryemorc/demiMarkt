from django.shortcuts import render, redirect  # type: ignore
from django.http import HttpResponse  # type: ignore
from cart.models import User  # type: ignore
from products.models import Product  # type: ignore
from django.core.paginator import Paginator  # type: ignore
from django.db.models import Count  # type: ignore

# Geçerli renklerin listesi
VALID_COLORS = [
    "Black", "Blue", "Red", "Green", "White", "Yellow", "Orange", "Purple",
    "Pink", "Gray", "Silver", "Gold", "Brown", "Lavender",
    "Navy", "Turquoise"
]

def homepage(request):
    # Ürünleri çek (artık ID ve fiyatlar temizlendiği için ekstra kontrole gerek yok)
    products = Product.objects.all()

    # Marka filtresi
    brand_filter = request.GET.get('brand')

    # Markaları çek ve filtrele
    all_brands = (
        Product.objects
        .values('brand')
        .annotate(brand_count=Count('brand'))
        .filter(brand__isnull=False, brand__gt='')  # Boş olmayan markaları filtrele
        .order_by('-brand_count')
    )
    popular_brands = all_brands[:10]  # İlk 10 markayı al
    other_brands_count = sum(brand['brand_count'] for brand in all_brands[10:])

    # Marka filtresine göre ürünleri filtrele
    if brand_filter == 'other':
        other_brands = [brand['brand'] for brand in all_brands[10:]]
        products = products.filter(brand__in=other_brands)
    elif brand_filter:
        products = products.filter(brand=brand_filter)

    # Renk filtresi
    all_colors = (
        Product.objects
        .values_list("available_colors", flat=True)
        .filter(available_colors__isnull=False)
    )

    # Renkleri ayır ve eşsiz bir liste oluştur
    color_set = set()
    for color_list in all_colors:
        if color_list:
            colors = [color.strip() for color in color_list.split(",")]
            valid_colors = [color for color in colors if color in VALID_COLORS]
            color_set.update(valid_colors)

    color_filter = request.GET.get('color')  # Renk filtresini al
    if color_filter and color_filter in VALID_COLORS:
        products = products.filter(available_colors__icontains=color_filter)

    # Sayfalama
    paginator = Paginator(products, 20)  # Her sayfada 20 ürün göster
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)

    return render(request, 'homepage/homepage.html', {
        'products': products_page,
        'popular_brands': popular_brands,
        'other_brands_count': other_brands_count,
        'colors': sorted(color_set),  # Renklere göre filtre
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
