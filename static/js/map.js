function initializeMap(iconUrl) {
    document.addEventListener("DOMContentLoaded", function () {
        var map = L.map('map').setView([50.73694, -3.53301], 15);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; OpenStreetMap contributors'
        }).addTo(map);

        // Custom icon for quizzes (Blue)
        var userIcon = L.icon({
            iconUrl: iconUrl,
            iconSize: [38, 38],
            iconAnchor: [19, 19],
            popupAnchor: [0, -19]
        });

        // Custom icon for bins (Pink)
        var binIcon = L.icon({
            iconUrl: '/static/resources/bin-marker.png',
            iconSize: [38, 38],
            iconAnchor: [19, 19],
            popupAnchor: [0, -19] 
        });

        // Array to store marker instances
        var markers = [];

        // Function to load locations from the database
        function loadLocations() {
            fetch('/play_screen/get-locations')
                .then(response => response.json())
                .then(data => {
                    // Add quiz locations to the map
                    data.quiz_data.forEach(function(location) {
                        var quizButton = `<button onclick='triggerQuizEvent(${location.locationID})'>Take the quiz</button>`; // Replace with your quiz page link
                        var DistantPopup = location.locationName;
                        var closePopup = location.locationName + ". " + quizButton;

                        var marker = L.marker(location.coordinates).addTo(map).bindPopup(DistantPopup);

                        markers.push({ marker: marker, closePopup: closePopup, DistantPopup: DistantPopup });
                    });

                    // Add bin locations to the map
                    data.bin_data.forEach(function(location) {
                        var popupContent = location.binIdentifier;
                        var marker = L.marker(location.coordinates, {icon: binIcon}).addTo(map).bindPopup(popupContent);
                    });
                });
        }

        loadLocations();

        let userMarker = null;
        let userLocation = null;

        map.on('locationfound', function(e) {
            userLocation = e.latlng;

            if (userMarker) {
                map.removeLayer(userMarker);
            } else {
                map.setView(userLocation, 16);
            }

            userMarker = L.marker(userLocation, { icon: userIcon, opacity: 0.5 }).addTo(map)
                .bindPopup("You are here").openPopup();

            // Check distance to each marker and update popup content accordingly
            markers.forEach(function(item) {
                var distance = userLocation.distanceTo(item.marker.getLatLng());

                if (distance <= 100) {
                    item.marker.setPopupContent(item.closePopup).openPopup();
                } else {
                    item.marker.setPopupContent(item.DistantPopup).openPopup();
                }
            });
        });

        // Locate the user
        map.locate({ maxZoom: 16, enableHighAccuracy: true });

        function onLocationError() {
            alert("Location access denied. Please enable location services.");
        }

        map.on('locationerror', onLocationError);

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

// Function to handle when the quiz button is clicked
function triggerQuizEvent(locationID) {
    console.log("Redirecting to: /quiz/" + locationID);
    window.top.location.href = `/quiz/${locationID}`;
}