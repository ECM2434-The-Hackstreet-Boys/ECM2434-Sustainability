function initializeMap(iconUrl) {
    document.addEventListener("DOMContentLoaded", function () {
        var map = L.map('map').setView([50.73694, -3.53301], 15);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; OpenStreetMap contributors'
        }).addTo(map);

        // Custom icon
        var customIcon = L.icon({
            iconUrl: "/static/resources/blue-circle-noBg.png", // Update the path to your icon
            iconSize: [38, 38], // Size of the icon
            iconAnchor: [19, 19], // Point of the icon which will correspond to marker's location
            popupAnchor: [0, -19] // Point from which the popup should open relative to the iconAnchor
        });

        // Initial markers with custom icon
        const forumMarker = L.marker([50.73554, -3.534], {icon: customIcon, opacity: 0.5}).addTo(map).bindPopup("The Forum");
        const resilienceMarker = L.marker([50.73694, -3.53301], {icon: customIcon, opacity: 0.5}).addTo(map).bindPopup("Centre for Resilience");

        // Variable to store the user's location marker
        let userMarker = null;

        map.on('locationfound', function(e) {
            const userLocation = e.latlng;

            // Remove previous user marker if it exists
            if (userMarker) {
                map.removeLayer(userMarker);
            }

            // Add new user marker with 50% opacity and custom icon
            userMarker = L.marker(userLocation, {icon: customIcon, opacity: 0.5}).addTo(map)
                .bindPopup("You are within " + Math.round(e.accuracy) + " meters from this point").openPopup();

            // Calculate the distance to the forum marker
            const forumDistance = userLocation.distanceTo(forumMarker.getLatLng());

            // Change the opacity and popup content based on distance to the forum marker
            if (forumDistance < 50) {
                forumMarker.setOpacity(1);
                forumMarker.bindPopup("You are nearby the Forum").openPopup();
            } else {
                forumMarker.setOpacity(0.5);
                forumMarker.bindPopup("The Forum").openPopup();
            }

            // Calculate the distance to the resilience marker
            const resilienceDistance = userLocation.distanceTo(resilienceMarker.getLatLng());

            // Change the opacity and popup content based on distance to the resilience marker
            if (resilienceDistance < 50) {
                resilienceMarker.setOpacity(1);
                resilienceMarker.bindPopup("You are nearby the Centre for Resilience").openPopup();
            } else {
                resilienceMarker.setOpacity(0.5);
                resilienceMarker.bindPopup("Centre for Resilience").openPopup();
            }
        });

        // Fix issue where map does not render fully
        setTimeout(function () {
            map.invalidateSize();
        }, 500);

        map.locate({setView: true, maxZoom: 16, watch: true, enableHighAccuracy: true});

        function onLocationError() {
            alert("Location access denied. Please enable location services.");
        }

        map.on('locationerror', onLocationError);
    });
}