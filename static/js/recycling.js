// Author: Ethan Clapham

// Function to increment the count of a recycling item
function increment(id) {
    let item = document.getElementById(id);
    let newCount = parseInt(item.innerHTML) + 1;
    item.innerHTML = newCount;
}

// Function to decrement the count of a recycling item
function decrement(id) {
    let item = document.getElementById(id);
    let count = parseInt(item.innerHTML);

    // Ensure the count is not negative
    if (count > 0) {
        let newCount = count - 1;
        item.innerHTML = newCount;
    }
}