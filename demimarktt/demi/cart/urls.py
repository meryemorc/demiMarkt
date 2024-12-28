from django.urls import path  # type: ignore # Django'nun URL yönlendirme modülü
from . import views  # Görünüm fonksiyonlarını içe aktarıyoruz

urlpatterns = [
    # Kullanıcı işlemleri
    path('login/', views.login_view, name='login'),  # Kullanıcı giriş sayfası
    path('register/', views.register_view, name='register'),  # Kullanıcı kayıt sayfası
    path('logout/', views.logout_view, name='logout'),  # Kullanıcı çıkış işlemi
    path('profile/', views.profile_view, name='profile'),  # Kullanıcı profili görüntüleme

    # Sepet işlemleri
    path('view-cart/', views.view_cart, name='view_cart'),  # Kullanıcının sepetini görüntüleme
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  # Sepete ürün ekleme
    path('remove-from-cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),  # Sepetten ürün çıkarma
    path('increase-quantity/<int:cart_item_id>/', views.increase_quantity, name='increase_quantity'),  # Ürün miktarını artırma
    path('decrease-quantity/<int:cart_item_id>/', views.decrease_quantity, name='decrease_quantity'),  # Ürün miktarını azaltma

    # Ödeme işlemleri
    path('checkout/', views.checkout_view, name='checkout'),  # Ödeme sayfasını görüntüleme
    path('process-payment/', views.process_payment, name='process_payment'),  # Ödeme bilgilerini işleme
    path('order-confirmation/', views.order_confirmation, name='order_confirmation'),#ödeme tamamlandı sayfası

]
