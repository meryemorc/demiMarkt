from djongo import models  # type: ignore # MongoDB için Djongo kullanımı

class Product(models.Model):
    # Temel Ürün Bilgileri
    ID = models.IntegerField(primary_key=True)  # Ürün ID'si primary key
    product_name = models.CharField(max_length=255)  # Ürün adı
    product_link = models.URLField()  # Ürün bağlantısı
    image_link = models.URLField()  # Ürün görseli bağlantısı

    # Fiyat ve İndirim Bilgileri
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, db_column="Price (Dollar)")
    discount_percentage = models.FloatField(null=True, blank=True)  # İndirim yüzdesi
    price_before_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # İndirim öncesi fiyat

    # Puan ve Değerlendirme Bilgileri
    rating_out_of_5 = models.FloatField(null=True, blank=True)  # 5 üzerinden puan
    number_of_ratings = models.IntegerField(null=True, blank=True)  # Değerlendirme sayısı

    # Marka ve Model Bilgileri
    brand = models.CharField(max_length=50, null=True, blank=True)  # Marka
    model_name = models.CharField(max_length=100, null=True, blank=True)  # Model adı

    # Renk Bilgileri
    available_colors = models.TextField(null=True, blank=True)  # Mevcut renkler (virgülle ayrılmış)

    # Depolama Bilgileri
    storage_gb = models.IntegerField(null=True, blank=True)  # Depolama kapasitesi (örneğin 64, 128)

    # Yeni Eklenen Alan: Stok Bilgisi
    stock = models.PositiveIntegerField(default=5)  # Varsayılan stok miktarı

    class Meta:
        db_table = "demiMarktBirlesik"  # MongoDB'deki koleksiyon adı

    def __str__(self):
        return self.product_name

    @property
    def full_name(self):
        """
        Ürün için `brand + model_name` kombinasyonu döner.
        Eğer `model_name` yoksa sadece `brand` döner.
        """
        if self.brand and self.model_name:
            return f"{self.brand} {self.model_name}"
        elif self.brand:
            return self.brand
        return self.product_name

    @property
    def color_list(self):
        """
        `available_colors` alanındaki renkleri liste olarak döner.
        """
        if self.available_colors:
            return [color.strip() for color in self.available_colors.split(",")]
        return []
