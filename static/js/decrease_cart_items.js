document.addEventListener('DOMContentLoaded', () => {
    // Attach event listeners to all decrease buttons
    document.querySelectorAll('.ref-decrease, .ref-increase').forEach((button) => {
        button.addEventListener('click', async (event) => {
            const itemSlug = button.getAttribute('data-item-slug'); // Get item slug from data attribute
            const action = button.classList.contains('ref-decrease') ? 'remove' : 'add'; // Determine action
            if (!itemSlug) return;

            const cartActionUrl = `/cart/${action}/${itemSlug}/`;
            try {
                const response = await fetch(`${cartActionUrl}`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCSRFToken(), // Ensure CSRF token is included
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ action }), // Optional: include additional data
                });

                if (!response.ok) {
                    console.log(error);
                    throw new Error('Failed to  item quantity');
                }

                const data = await response.json(); // Assuming the view returns a JSON response
                console.log(`Item ${action}d:`, data);
                
                if (data.success){
                // Optionally update the UI (e.g., decrement quantity, update subtotal)
                updateCartUI(itemSlug, data.new_quantity, data.subtotal);
                }
            } catch (error) {
                console.error(`Error during ${action} action:`, error);
            }
        });
    });

    // Helper function to get CSRF token from the cookie
    function getCSRFToken() {
        const name = 'csrftoken';
        const cookies = document.cookie.split(';');
        for (const cookie of cookies) {
            const trimmed = cookie.trim();
            if (trimmed.startsWith(`${name}=`)) {
                return trimmed.substring(name.length + 1);
            }
        }
        return '';
    }

    // Function to update the cart UI after a successful request
    function updateCartUI(itemSlug, newQuantity, subtotal) {
        const quantityInput = document.querySelector(`.ref-quantity-container[data-item-id="${itemSlug}"] input`);
        const subtotalElement = document.getElementById('subtotal');

        if (quantityInput) {
            if (newQuantity > 0) {
                quantityInput.value = newQuantity;
            } 
            else {
                // Remove the item's row if quantity is now 0
                const productRow = quantityInput.closest('.ref-product');
                if (productRow) productRow.remove();
            }
        }

        // Update the subtotal
        if (subtotalElement) {
            subtotalElement.textContent = `Subtotal: Rs. ${subtotal.toFixed(2)}`;
        }
    }
}); 