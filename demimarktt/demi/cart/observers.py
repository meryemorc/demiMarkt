from abc import ABC, abstractmethod
from django.core.mail import send_mail # type: ignore
from products.models import Product


# Observer Base Class
class Observer(ABC):
    @abstractmethod
    def update(self, event_data):
        """
        Olay gerçekleştiğinde tetiklenecek metot.
        :param event_data: Publisher'dan gelen veri
        """
        pass

# Subject (Publisher) Class
class Subject:
    def __init__(self):
        self._observers = []  # Kayıtlı Observer'lar

    def attach(self, observer):
        """Observer'ı ekle."""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        """Observer'ı çıkar."""
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, event_data):
        """Tüm Observer'ları bilgilendir."""
        for observer in self._observers:
            observer.update(event_data)

    # notify_observers için alias
    def notify_observers(self, event_data):
        self.notify(event_data)



# Stock Update Observer (Stok Güncelleme)
class StockUpdateObserver(Observer):
    def update(self, event_data):
        """
        Stokları güncelle.
        :param event_data: Ödeme sonrası ürün bilgileri
        """
        try:
            product_name = event_data.get("product")  # Ürünün adı
            quantity = event_data.get("quantity")  # Satılan miktar

            # Veritabanında ürünü bul
            product = Product.objects.filter(product_name=product_name).first()
            if product:
                if product.stock >= quantity:  # Yeterli stok varsa
                    product.stock -= quantity
                    product.save()  # Stok değerini güncelle
                    print(f"Stok Güncellendi: {product_name} için {quantity} adet düşüldü. Yeni stok: {product.stock}")
                else:
                    print(f"Stok Yetersiz: {product_name} için {quantity} adet bulunamadı.")
            else:
                print(f"Ürün Bulunamadı: {product_name}")
        except Exception as e:
            print(f"Stok güncelleme sırasında hata: {e}")



class MailNotificationObserver(Observer):
    def update(self, event_data):
        """
        Gerçek bir e-posta gönderir.
        :param event_data: Ödeme sonrası müşteri bilgileri
        """
        subject = "Sipariş Onayınız"
        message = (
            f"Sayın {event_data['user_email']},\n\n"
            f"Başarılı bir şekilde sipariş verdiniz.\n"
            f"Ürün: {event_data['product']}\n"
            f"Adet: {event_data['quantity']}\n"
            f"Birim Fiyat: ${event_data['unit_price']}\n"
            f"Toplam Tutar: ${event_data['amount']}\n\n"
            f"Teşekkür ederiz."
        )
        from_email = 'your-email@gmail.com'
        recipient_list = [event_data['user_email']]

        try:
            send_mail(subject, message, from_email, recipient_list)
            print("E-posta başarıyla gönderildi.")
        except Exception as e:
            print(f"E-posta gönderilemedi: {e}")




# Payment Publisher (Ödeme İşleminden Sorumlu Publisher)
class PaymentPublisher(Subject):
    def process_payment(self, payment_data):
        """
        Ödeme işlemini gerçekleştir ve Observer'ları bilgilendir.
        :param payment_data: Ödeme bilgileri
        """
        print(f"Ödeme Alındı: {payment_data['amount']} $")
        self.notify(payment_data)  # Observer'ları bilgilendir
