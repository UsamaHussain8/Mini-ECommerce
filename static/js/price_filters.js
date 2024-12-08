document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("priceRangesContainer");

    // Clear current price ranges
    container.innerHTML = "<p>Loading price ranges...</p>";

    // AJAX call to fetch price ranges
    fetch(`${apiUrl}?tag=${tag}`)
        .then(response => {
            if (!response.ok) {
                throw new Error("Failed to fetch price ranges");
            }
            return response.json();
        })
        .then(data => {
            // Populate price ranges
            if (data.price_ranges.length > 0) {
                let html = `<form method="GET" id="priceFilterForm">`;
                data.price_ranges.forEach((range, index) => {
                    const isChecked = range === selectedPriceRange ? "checked" : ""; // Check if this range is selected
                    html += `
                        <div class="form-check">
                            <input
                                class="form-check-input"
                                type="radio"
                                name="price_range"
                                id="price_${index}"
                                value="${range}"
                                ${isChecked}
                                onchange="document.getElementById('priceFilterForm').submit()"
                            />
                            <label class="form-check-label" for="price_${index}">
                                ${range}
                            </label>
                        </div>
                    `;
                });
                html += `</form>`;
                container.innerHTML = html;
            } else {
                container.innerHTML = "<p>No price ranges available for this category.</p>";
            }
        })
        .catch(error => {
            console.error(error);
            container.innerHTML = "<p>Error loading price ranges.</p>";
        });
});
