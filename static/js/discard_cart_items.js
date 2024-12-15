document.addEventListener('DOMContentLoaded', () => {
    // Attach event listeners to all remove buttons
    document.querySelectorAll('.ref-product-remove').forEach((button) => {
        button.addEventListener('click', async (event) => {
            const itemSlug = button.getAttribute('data-item-slug'); // Get slug dynamically
            if (!itemSlug) {
                console.error('No item slug found for this button');
                return;
            }

            // Construct the URL dynamically using the slug
            const removeItemUrl = `/cart/discard/${itemSlug}/`; 

            try {
                const response = await fetch(removeItemUrl, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCSRFToken(), // Ensure CSRF token is included
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ slug: itemSlug }), // Optional: send slug or other data
                });

                if (!response.ok) {
                    throw new Error('Failed to remove item from cart');
                }

                const data = await response.json();
                console.log('Item removed:', data);

                if (data.success) {
                    // Optionally update the UI (e.g., remove the row from the DOM)
                    updateCartUI(itemSlug);
                }
            } catch (error) {
                console.error('Error:', error);
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
    function updateCartUI(itemSlug) {
        // Find the row corresponding to the slug and remove it from the DOM
        const productRow = document.querySelector(`.ref-product[data-item-slug="${itemSlug}"]`);
        if (productRow) {
            productRow.remove();
        }

        // Optionally, update the subtotal
        const subtotalElement = document.getElementById('subtotal');
        if (subtotalElement) {
            const newSubtotal = calculateNewSubtotal();
            subtotalElement.textContent = `Subtotal: Rs. ${newSubtotal.toFixed(2)}`;
        }
    }

    // Calculate the new subtotal after removing an item
    function calculateNewSubtotal() {
        let subtotal = 0;
        document.querySelectorAll('.ref-product .ref-product-total-sum').forEach((totalElement) => {
            subtotal += parseFloat(totalElement.textContent.replace('Rs. ', ''));
        });
        return subtotal;
    }
});
