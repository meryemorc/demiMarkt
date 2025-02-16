from django.db import models  # type: ignore
from products.models import Product  # Ürün modelini products uygulamasından alıyoruz
from django.conf import settings  # type: ignore # Django'nun ayarlarındaki kullanıcı modelini alıyoruz
from .state import Preparing  # type: ignore # Yeni durum sınıfını ekliyoruz
from .observers import Subject  # Observer mekanizmasını ekliyoruz


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.FloatField()  # Ürün fiyatı
    subtotal = models.FloatField()  # Ara toplam

    def save(self, *args, **kwargs):
        self.subtotal = self.price * self.quantity
        super().save(*args, **kwargs)



# Sepet Modeli
class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # Kullanıcı modeli
        on_delete=models.CASCADE,
        related_name='cart'
    )
    items = models.ManyToManyField(CartItem, blank=True)  # Sepet öğeleri

    def total_price(self):
    # Toplam fiyatı hesapla ve tüm subtotal değerlerini float'a dönüştür
     return sum(float(item.subtotal) for item in self.items.all())


    def __str__(self):
        return f"Cart of {self.user.username}"


class Order(models.Model, Subject):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    total_price = models.FloatField()  # DecimalField yerine FloatField kullanıldı
    current_state = None  # Varsayılan olarak durum yok


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Subject.__init__(self)  # Subject sınıfını başlat
        self.current_state = Preparing()  # Yeni siparişler 'Preparing' durumu ile başlar

    def set_state(self, state):
        """Siparişin durumunu güncelle."""
        self.current_state = state

    def proceed_state(self):
        """Bir sonraki duruma geçiş yap."""
        if self.current_state:
            self.current_state.proceed(self)

    def cancel_order(self):
        """Siparişi iptal et."""
        if self.current_state:
            self.current_state.cancel(self)
