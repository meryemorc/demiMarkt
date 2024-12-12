document.querySelectorAll('.btn').forEach(button => {
    button.addEventListener('click', function () {
        let action = this.innerText.trim();
        let quantityElement = this.parentElement.querySelector('span');
        let quantity = parseInt(quantityElement.innerText);

        if (action === '+' && quantity < 99) {
            quantity++;
        } else if (action === '-' && quantity > 1) {
            quantity--;
        }

        quantityElement.innerText = quantity;

        // Fiyatı güncellemek için bir AJAX çağrısı yapabilirsin.
        console.log(`Action: ${action}, Quantity: ${quantity}`);
    });
});
