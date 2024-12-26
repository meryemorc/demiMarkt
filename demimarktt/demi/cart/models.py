from djongo import models  # type: ignore # Djongo ile MongoDB bağlantısı için
from products.models import Product  # Ürün modelini içe aktar
from bson import ObjectId  # type: ignore # ObjectId kullanımı için
from django.db.models import DecimalField  # type: ignore # Django'nun DecimalField'ı

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


# Sepet öğesi modeli
class CartItem(models.Model):
    product_id = models.CharField(max_length=255)  # ObjectId yerine string kullanıyoruz
    product_name = models.CharField(max_length=255)
    selected_color = models.CharField(max_length=50, null=True, blank=True)  # Seçilen renk
    price = DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = DecimalField(max_digits=10, decimal_places=2, editable=False)

    class Meta:
        abstract = True


# Sepet modeli
class Cart(models.Model):
    id = models.ObjectIdField(primary_key=True, default=ObjectId, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,  # Kullanıcı giriş yapmamışsa None olabilir
        blank=True
    )
    session_id = models.CharField(max_length=255, null=True, blank=True)  # Anonim kullanıcılar için oturum ID
    items = models.ArrayField(
        model_container=CartItem,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart (User: {self.user or 'Anonymous'}, Session: {self.session_id})"

    @property
    def total_price(self):
        # Sepetteki ürünlerin toplam fiyatını hesaplar
        if not self.items:
            return 0
        return sum(item['subtotal'] for item in self.items)

    def add_item(self, product, selected_color, quantity=1):
        if not self.items:
            self.items = []

        price = product.price or 0  # Fiyat kontrolü, eğer None ise 0 atayın

        for item in self.items:
            if item['product_id'] == str(product.ID) and item['selected_color'] == selected_color:
                item['quantity'] += quantity
                item['subtotal'] = item['quantity'] * price
                break
        else:
            self.items.append({
                'product_id': str(product.ID),
                'product_name': product.product_name,
                'selected_color': selected_color,
                'price': price,
                'quantity': quantity,
                'subtotal': price * quantity,
            })
        self.save()

    def remove_item(self, product_id):
        # Sepetten ürün çıkarma
        if not self.items:
            return
        self.items = [item for item in self.items if item['product_id'] != str(product_id)]
        self.save()
