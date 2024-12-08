from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')),  # Anasayfa uygulaması için
    # Aşağıdaki satırları geçici olarak yorum satırına alın
    # path('products/', include('products.urls')),
    # path('cart/', include('cart.urls')),
    # path('search/', include('search.urls')),
    # path('account/', include('userAccount.urls')),
]
