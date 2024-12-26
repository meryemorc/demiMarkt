from djongo import models  # type: ignore
from products.models import Product  # Ürün modelini içe aktar
from bson import ObjectId  # type: ignore


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
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

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
    
def add_item(self, product, quantity=1):
    if not self.items:
        self.items = []

    for item in self.items:
        if item['product_id'] == str(product.ID):  # ObjectId yerine str karşılaştırması
            item['quantity'] += quantity
            item['subtotal'] = item['quantity'] * (product.price or 0)  # Varsayılan değer
            break
    else:
        self.items.append({
            'product_id': str(product.ID),  # ObjectId yerine string ID
            'product_name': product.product_name,
            'price': product.price or 0,  # Varsayılan değer
            'quantity': quantity,
            'subtotal': (product.price or 0) * quantity,  # Varsayılan değer
        })
    self.save()


    def remove_item(self, product_id):
        # Sepetten ürün çıkarma
        if not self.items:
            return
        self.items = [item for item in self.items if item['product_id'] != str(product_id)]
        self.save()
