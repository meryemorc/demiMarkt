from django.shortcuts import render, redirect  # type: ignore
from django.http import HttpResponse  # type: ignore
from cart.models import User  # type: ignore
from products.models import Product  # type: ignore


def homepage(request):
    # MongoDB'den tüm ürünleri çek
    products = Product.objects.all()

    # Ürünleri template'e gönder
    return render(request, 'homepage/homepage.html', {'products': products})


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
