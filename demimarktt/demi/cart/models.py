from djongo import models # type: ignore

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

class User(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    addresses = models.ArrayField(
        model_container=Address
    )
    payment_methods = models.ArrayField(
        model_container=PaymentMethod
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
