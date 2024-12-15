from djongo import models # type: ignore

class Product(models.Model):
    ID = models.IntegerField()
    product_name = models.CharField(max_length=255)
    product_link = models.URLField()
    image_link = models.URLField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_percentage = models.FloatField(null=True, blank=True)
    price_before_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rating_out_of_5 = models.FloatField(null=True, blank=True)
    number_of_ratings = models.IntegerField(null=True, blank=True)
    brand = models.CharField(max_length=50, null=True, blank=True)  # Brand alanı doğru tanımlanmış
    
    class Meta:
        db_table = "demiMarktBirlesik"  # MongoDB koleksiyon adı doğru tanımlı

    def __str__(self):
        return self.product_name
