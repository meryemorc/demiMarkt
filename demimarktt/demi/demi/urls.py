from django.contrib import admin # type: ignore
from django.urls import path, include # type: ignore

urlpatterns = [
    path('admin/', admin.site.urls),
    path('search/', include('search.urls')),
    path('products/', include('products.urls')),
    path('', include('homepage.urls')), 
]
