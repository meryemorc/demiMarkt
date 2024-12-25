from djongo import models  # type: ignore
from products.models import Product  # Ürün modelini içe aktar
from bson import ObjectId # type: ignore

# Adres ve ödeme bilgisi için soyut modeller
class Address(models.Model):
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20)

    class Meta:
        abstract = True


class PaymentMethod(models.Model):
    card_number = models.CharField(max_length=16)
    expiry_date = models.CharField(max_length=7)
    cvv = models.CharField(max_length=3)

    class Meta:
        abstract = True


# Kullanıcı modeli
class User(models.Model):
    id = models.ObjectIdField(primary_key=True, default=ObjectId, editable=False)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    password = models.CharField(max_length=128)  # Şifre alanı
    addresses = models.ArrayField(
        model_container=Address,
        null=True,
        blank=True
    )
    payment_methods = models.ArrayField(
        model_container=PaymentMethod,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


# Cart ve CartItem modelleri
class Cart(models.Model):
    id = models.ObjectIdField(primary_key=True, default=ObjectId, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,  # Anonim kullanıcılar için
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart (User: {self.user})"

    @property
    def total_price(self):
        return sum(item.subtotal for item in self.items.all())


class CartItem(models.Model):
    id = models.ObjectIdField(primary_key=True, default=ObjectId, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.product.price
        super().save(*args, **kwargs)
