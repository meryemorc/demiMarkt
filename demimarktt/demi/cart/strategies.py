from abc import ABC, abstractmethod  # ABC ve soyut sınıflar için gerekli modül

# PaymentStrategy: Soyut sınıf (Abstract Base Class)
class PaymentStrategy(ABC):
    @abstractmethod
    def process_payment(self, amount, **kwargs):
        """
        Ödemeyi işlemek için gerekli olan işlemleri tanımlayın.
        :param amount: Ödeme miktarı
        :param kwargs: Ek bilgiler (ör. kart bilgileri)
        """
        pass  # Alt sınıflarda uygulanmak üzere boş bırakılır


class CardPaymentStrategy(PaymentStrategy):
    def process_payment(self, amount, card_number, expiry_date, cvv):
        """
        Kartla ödeme işlemini simüle eder.
        :param amount: Ödeme miktarı
        :param card_number: Kart numarası
        :param expiry_date: Kartın son kullanma tarihi
        :param cvv: Kartın güvenlik kodu
        """
        print(f"Kartla ödeme alınıyor: {amount} $")
        print(f"Kart Bilgileri - Numara: {card_number}, Son Kullanma Tarihi: {expiry_date}")

        # Kart bilgilerini doğrulama simülasyonu
        if len(card_number) == 16 and len(cvv) == 3:
            print("Kart bilgileri doğrulandı.")
            print("Ödeme başarıyla alındı!")
        else:
            print("Kart bilgileri geçersiz!")

class EFTPaymentStrategy(PaymentStrategy):
    def process_payment(self, amount, bank_account):
        print(f"EFT ile ödeme alınıyor: {amount} $")
        print(f"Alıcı Hesap: {bank_account}")
        print("EFT işlemi tamamlandı.")

class CODPaymentStrategy(PaymentStrategy):
    def process_payment(self, amount, **kwargs):
        print(f"Kapıda ödeme alınıyor: {amount} $")
        print("Kapıda ödeme yöntemi seçildi.")
