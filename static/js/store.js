import { updateOwnedQuantity } from "./updateOwnedQuantity.js";



let cart = {};

document.addEventListener("DOMContentLoaded", function () {
    fetch("/api/get_store_items/")
        .then(response => response.json())
        .then(data => {
            let items = data.items;
            if (!items || items.length === 0) {
                console.warn("No items found in API response.");
                return;
            }

            let storeGrid = document.getElementById("store-grid");
            storeGrid.innerHTML = "";  // Clear previous items

            const mediaUrl = window.MEDIA_URL;  // Get MEDIA_URL from Django

            items.forEach(item => {
                let itemDiv = document.createElement("div");
                itemDiv.classList.add("store-item");

                let imagePath = item.blockPath.startsWith("media/") ? item.blockPath.substring(6) : item.blockPath;

                itemDiv.innerHTML = `
                    <img src="${mediaUrl}${imagePath}" alt="${item.name}" width="50" height="50"/>
                    <h3>${item.name}</h3>
                    <p>Price: ${item.cost} Points</p>
                    <p><strong>Currently Owned:</strong> <span id="owned-count-${item.name}">${item.owned || 0}</span></p>
                    <div class="quantity-controls">
                        <button class="decrease" data-item="${item.name}">-</button>
                        <span id="cart-count-${item.name}">0</span>
                        <button class="increase" data-item="${item.name}">+</button>
                    </div>
                    <button class="buy" data-item-id="${item.blockID}" data-cost="${item.cost}" data-item-name="${item.name}">Buy</button>
                `;

                storeGrid.appendChild(itemDiv);
            });

            // Attach event listeners to the buttons after the DOM content is loaded
            document.querySelectorAll('.decrease').forEach(button => {
                button.addEventListener('click', function() {
                    const itemName = this.getAttribute('data-item');
                    updateCart(itemName, -1);
                });
            });

            document.querySelectorAll('.increase').forEach(button => {
                button.addEventListener('click', function() {
                    const itemName = this.getAttribute('data-item');
                    updateCart(itemName, 1);
                });
            });

            document.querySelectorAll('.buy').forEach(button => {
                button.addEventListener('click', function() {
                    const itemId = this.getAttribute('data-item-id');
                    const cost = parseInt(this.getAttribute('data-cost'));
                    const itemName = this.getAttribute('data-item-name');
                    buyItem(itemId, cost, itemName);
                });
            });

        })
        .catch(error => console.error("Error fetching store items:", error));
});

// Update cart quantity
function updateCart(itemId, change) {
    if (!cart[itemId]) cart[itemId] = 0;
    cart[itemId] = Math.max(0, cart[itemId] + change);
    document.getElementById(`cart-count-${itemId}`).textContent = cart[itemId];
}


// Function to retrieve the CSRF token from the page
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}


// Handle item purchase
function buyItem(itemId, cost, itemName) {
    const quantity = cart[itemName] || 0;  // Get the quantity from the cart

    console.log("Buying item:", itemId, cost, itemName, quantity);
    if (quantity === 0) {
        alert("You need to select at least one item to buy.");
        return;
    }

    // Calculate total cost
    const totalCost = cost * quantity;

    fetch("buy_item/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({ itemId: itemId, cost: totalCost, quantity: quantity }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("Purchase successful!");
                updateOwnedQuantity(itemName);
                cart[itemName] = 0;  // Reset the cart for the item after purchase
                document.getElementById(`cart-count-${itemName}`).textContent = 0;
            } else {
                alert(data.message || "Not enough currency!");
            }
        })
        .catch(error => console.error("Error buying item:", error));


}
