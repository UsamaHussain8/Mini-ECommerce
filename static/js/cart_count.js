document.addEventListener('DOMContentLoaded', () => {
    const cartBadge = document.getElementById('cart-count');

    if(cartBadge){
        console.log('Cart badge found');
    }
    // Function to fetch cart count
    async function updateCartCount() {
        try {
            const response = await fetch(`${apiUrl}`); // Fetch cart count from the API
            if (!response.ok) {
                throw new Error('Failed to fetch cart count');
            }

            const data = await response.json();
            const count = data.num_items || 0;
            console.log(`Cart updated with count: ${count}`);
            // Update badge
            if (count > 0) {
                cartBadge.textContent = count;
                cartBadge.style.display = 'inline-block'; // Show badge if count > 0

            } else {
                cartBadge.style.display = 'none'; // Hide badge if count is 0
            }
        } catch (error) {
            console.error('Error updating cart count:', error);
        }
    }

    // Call the function on page load
    updateCartCount();

    // Optionally, set an interval to refresh the count periodically
    //setInterval(updateCartCount, 60000); // Update every 60 seconds
});