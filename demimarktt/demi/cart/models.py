from django.db import models  # type: ignore
from products.models import Product  # Ürün modelini products uygulamasından alıyoruz
from django.conf import settings  # type: ignore # Django'nun ayarlarındaki kullanıcı modelini alıyoruz

# Sepet Öğesi Modeli

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
