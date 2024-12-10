from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls')),
    path('search/', include('search.urls')),
    path('user/', include('userAccount.urls')),
    path('products/', include('product.urls')),
    path('', include('homepage.urls')), 
]
