// Author: Ethan Clapham

document.addEventListener("DOMContentLoaded", function() {
    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(checkUserDistance, showError);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
});

// Check the users distance from the bin location
function checkUserDistance(position) {
    const userLatitude = position.coords.latitude;
    const userLongitude = position.coords.longitude;

    // Calculate distance between user and bin location
    const distance = getDistanceFromLatLonInMeters(userLatitude, userLongitude, BIN_LAT, BIN_LON);

    // If the user is within 100 meters of the bin location, display the recycling form
    if (distance <= 100) {
        document.getElementById("recycling-form").style.display = "block";
    } else {
        alert("You are too far from the bin location.")
    }
}

// Display an error message if the user's location cannot be retrieved
function showError(error) {
    alert("Unable to retrieve your location. Please enable location services and refresh the page.");
}

// Haversine formula to calculate the distance between two points
function getDistanceFromLatLonInMeters(lat1, lon1, lat2, lon2) {
    const R = 6371000 // Radius of the earth in meters
    const dLat = (lat2 - lat1) * (Math.PI / 180);
    const dLon = (lon2 - lon1) * (Math.PI / 180);
    const a =
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(lat1 * (Math.PI / 180)) *
        Math.cos(lat2 * (Math.PI / 180)) *
        Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

    return R * c;
}

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