from djongo import models  # type: ignore

class Product(models.Model):
    ID = models.IntegerField(primary_key=True)  # Ürün ID'si primary key
    product_name = models.CharField(max_length=255)
    product_link = models.URLField()
    image_link = models.URLField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_percentage = models.FloatField(null=True, blank=True)
    price_before_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rating_out_of_5 = models.FloatField(null=True, blank=True)
    number_of_ratings = models.IntegerField(null=True, blank=True)
    brand = models.CharField(max_length=50, null=True, blank=True)
    model_name = models.CharField(max_length=100, null=True, blank=True)  # Yeni model_name alanı

    class Meta:
        db_table = "demiMarktBirlesik"

    def __str__(self):
        return self.product_name

    @property
    def full_name(self):
        """
        Ürün için brand + model_name kombinasyonu döner.
        Eğer model_name yoksa sadece brand döner.
        """
        if self.brand and self.model_name:
            return f"{self.brand} {self.model_name}"
        elif self.brand:
            return self.brand
        else:
            return self.product_name
