document.addEventListener("DOMContentLoaded", () => {
    // Sepet işlemleri için gerekli elemanları seç
    const totalPriceElement = document.getElementById("total-price");

    // Miktarı artırma
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

    // Miktarı azaltma
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

    // Ürünü silme
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
});
