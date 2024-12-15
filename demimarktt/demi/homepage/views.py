from django.shortcuts import render, redirect  # type: ignore
from django.http import HttpResponse  # type: ignore
from cart.models import User  # type: ignore
from products.models import Product  # type: ignore
from django.core.paginator import Paginator # type: ignore

from django.db.models import Count # type: ignore


def homepage(request):
    # Marka filtresi için GET parametresini al
    brand_filter = request.GET.get('brand')
    
    # Ürünleri filtrele
    products = Product.objects.all()
    if brand_filter:  # Belirli bir marka seçilmişse ürünleri filtrele
        products = products.filter(brand=brand_filter)

    # Markaları ürün sayısına göre sıralayarak al
    brands = Product.objects.values('brand').annotate(brand_count=Count('brand')).order_by('-brand_count')
    
    # Sayfalama: Her sayfada 20 ürün
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)

    return render(request, 'homepage/homepage.html', {
        'products': products_page,
        'brands': brands,
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
