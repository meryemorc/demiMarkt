// Sayfa yüklendiğinde çalışan işlemler
// Hem sepet işlemleri hem de ödeme yöntemi alanlarını kontrol eder
document.addEventListener("DOMContentLoaded", () => {
    // Sepet işlemleri için gerekli elemanları seç
    const totalPriceElement = document.getElementById("total-price");

    // Miktarı artırma işlemi
    document.querySelectorAll(".increase-quantity").forEach(button => {
        button.addEventListener("click", () => {
            const row = button.closest(".cart-item");
            const quantityInput = row.querySelector(".quantity-input");
            let quantity = parseInt(quantityInput.value) || 0;

            quantity++;
            quantityInput.value = quantity;

            updateSubtotal(row);
            updateTotalPrice();
        });
    });

    // Miktarı azaltma işlemi
    document.querySelectorAll(".decrease-quantity").forEach(button => {
        button.addEventListener("click", () => {
            const row = button.closest(".cart-item");
            const quantityInput = row.querySelector(".quantity-input");
            let quantity = parseInt(quantityInput.value) || 0;

            if (quantity > 1) {
                quantity--;
                quantityInput.value = quantity;

                updateSubtotal(row);
                updateTotalPrice();
            }
        });
    });

    // Ürünü silme işlemi
    document.querySelectorAll(".delete-item").forEach(button => {
        button.addEventListener("click", () => {
            const row = button.closest(".cart-item");
            row.remove(); // Satırı kaldır
            updateTotalPrice(); // Toplam fiyatı güncelle
        });
    });

    // Ara toplamı güncelle
    function updateSubtotal(row) {
        const price = parseFloat(row.querySelector(".item-price").textContent);
        const quantity = parseInt(row.querySelector(".quantity-input").value) || 0;
        const subtotalElement = row.querySelector(".item-subtotal");

        const subtotal = price * quantity;
        subtotalElement.textContent = `$${subtotal.toFixed(2)}`;
    }

    // Toplam fiyatı güncelle
    function updateTotalPrice() {
        let totalPrice = 0;

        document.querySelectorAll(".cart-item").forEach(row => {
            const subtotal = parseFloat(row.querySelector(".item-subtotal").textContent.replace("$", "")) || 0;
            totalPrice += subtotal;
        });

        totalPriceElement.textContent = `$${totalPrice.toFixed(2)}`;
    }

    // Ödeme yöntemi alanlarının gösterilmesi/gizlenmesi
    const paymentMethodSelect = document.getElementById("payment_method");
    const creditCardFields = document.getElementById("credit_card_fields");
    const eftFields = document.getElementById("eft_fields");

    paymentMethodSelect.addEventListener("change", () => {
        const selectedMethod = paymentMethodSelect.value;

        // Alanları göster/gizle
        if (selectedMethod === "credit_card") {
            creditCardFields.style.display = "block";
            eftFields.style.display = "none";
        } else if (selectedMethod === "eft") {
            creditCardFields.style.display = "none";
            eftFields.style.display = "block";
        } else {
            creditCardFields.style.display = "none";
            eftFields.style.display = "none";
        }
    });

    // Sayfa yüklendiğinde varsayılan seçime göre alanları ayarla
    const initialPaymentMethod = paymentMethodSelect.value;
    if (initialPaymentMethod === "credit_card") {
        creditCardFields.style.display = "block";
        eftFields.style.display = "none";
    } else if (initialPaymentMethod === "eft") {
        creditCardFields.style.display = "none";
        eftFields.style.display = "block";
    } else {
        creditCardFields.style.display = "none";
        eftFields.style.display = "none";
    }
});
