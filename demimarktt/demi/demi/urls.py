
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')),
    path('products/', include('products.urls')),
    path('search/', include('search.urls')),
    path('cart/', include('cart.urls')),
    path('account/', include('userAccount.urls')),

]
