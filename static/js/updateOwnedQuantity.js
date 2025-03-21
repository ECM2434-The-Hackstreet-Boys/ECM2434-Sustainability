// updateOwnedQuantity.js
export function updateOwnedQuantity() {
    fetch("/api/get_store_items/")  // Fetch updated owned quantities
        .then(response => response.json())
        .then(data => {
            let ownedItems = data.items;  // Array of owned items

            // Loop through all the items in the shop
            ownedItems.forEach(item => {
                // Get the owned count for the current item
                let ownedCount = item.owned || 0;

                // Get the element displaying the owned quantity for this item
                let ownedElement = document.getElementById(`owned-count-${item.name}`);
                if (ownedElement) {
                    ownedElement.textContent = ownedCount;
                }
            });
        })
        .catch(error => console.error("Error fetching owned quantities:", error));
}