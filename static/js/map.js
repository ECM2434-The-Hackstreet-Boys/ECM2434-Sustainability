function initializeMap(iconUrl) {
    document.addEventListener("DOMContentLoaded", function () {
        var map = L.map('map').setView([50.73694, -3.53301], 15);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; OpenStreetMap contributors'
        }).addTo(map);

        // Custom icon
        var customIcon = L.icon({
            iconUrl: iconUrl, // Update the path to your icon
            iconSize: [38, 38], // Size of the icon
            iconAnchor: [19, 19], // Point of the icon which will correspond to marker's location
            popupAnchor: [0, -19] // Point from which the popup should open relative to the iconAnchor
        });

        // Variable to store the user's location marker
        let userMarker = null;
        let userLocation = null;

        map.on('locationfound', function(e) {
            userLocation = e.latlng;
            console.log(userLocation);

            // Remove previous user marker if it exists
            if (userMarker) {
                map.removeLayer(userMarker);
            } else {
                map.setView(userLocation);
            }

            // Add new user marker with 50% opacity and custom icon
            userMarker = L.marker(userLocation, {icon: customIcon, opacity: 0.5}).addTo(map)
                .bindPopup("You are within " + Math.round(e.accuracy) + " meters from this point").openPopup();
        });

        // Fix issue where map does not render fully
        setTimeout(function () {
            map.invalidateSize();
        }, 500);

        map.locate({ maxZoom: 16, watch: true, enableHighAccuracy: true });

        function onLocationError() {
            alert("Location access denied. Please enable location services.");
        }

        map.on('locationerror', onLocationError);

        // Add event listener for recenter button
        document.getElementById('recenter-button').addEventListener('click', function() {
            if (userLocation) {
                map.setView(userLocation, 16);
                console.log("Map recentered on user's location");
            } else {
                alert("User location not found. Please enable location services.");
            }
        });
    });
}