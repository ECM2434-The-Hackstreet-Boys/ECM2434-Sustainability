// Author: Ethan Clapham

// Function to increment the count of a recycling item
function increment(id) {
    let displayElement = document.getElementById(id);
    let inputElement = document.getElementById(id + "-value");
    let newCount = parseInt(displayElement.innerHTML) + 1;
    
    displayElement.innerHTML = newCount;
    inputElement.value = newCount;
}

// Function to decrement the count of a recycling item
function decrement(id) {
    let displayElement = document.getElementById(id);
    let inputElement = document.getElementById(id + "-value");
    let count = parseInt(displayElement.innerHTML);

    // Ensure the count is not negative
    if (count > 0) {
        let newCount = count - 1;
        displayElement.innerHTML = newCount;
        inputElement.value = newCount;
    }
}