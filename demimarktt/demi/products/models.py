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

    class Meta:
        db_table = "demiMarktBirlesik"  # Koleksiyon adı MongoDB'deki gibi olmalı

    def __str__(self):
        return self.product_name
