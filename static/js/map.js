function initializeMap(iconUrl) {
    document.addEventListener("DOMContentLoaded", function () {
        var map = L.map('map').setView([50.73694, -3.53301], 15);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; OpenStreetMap contributors'
        }).addTo(map);

        // Custom icon for quizzes (Blue)
        var userIcon = L.icon({
            iconUrl: iconUrl, // Update the path to your icon
            iconSize: [38, 38], // Size of the icon
            iconAnchor: [19, 19], // Point of the icon which will correspond to marker's location
            popupAnchor: [0, -19] // Point from which the popup should open relative to the iconAnchor
        });

        // Custom icon for bins (Red)
        var binIcon = L.icon({
            iconUrl: '/path/to/bin-icon.png', // Replace with your bin icon path
            iconSize: [38, 38], // Size of the icon
            iconAnchor: [19, 19], // Point of the icon which will correspond to marker's location
            popupAnchor: [0, -19] // Point from which the popup should open relative to the iconAnchor
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
                        var quizButton = "<button onclick='triggerQuizEvent()'>Take the quiz</button>"; // Replace with your quiz page link
                        var DistantPopup = location.locationName;
                        var closePopup = location.locationName + ". " + quizButton;

                        var marker = L.marker(location.coordinates).addTo(map).bindPopup(DistantPopup);

                        markers.push({ marker: marker, closePopup: closePopup, DistantPopup: DistantPopup });
                    });

                    // Add bin locations to the map
                    data.bin_data.forEach(function(location) {
                        var marker = L.marker(location.coordinates).addTo(map).bindPopup("Bin");
                    });
                });
        }

        // Call the function to load locations from the database
        loadLocations();

        // Variables to store user location and marker
        let userMarker = null;
        let userLocation = null;
        
        // Function that runs when the user location is found
        map.on('locationfound', function(e) {
            userLocation = e.latlng;

            // Remove previous user marker if it exists
            if (userMarker) {
                map.removeLayer(userMarker);
            } else {
                map.setView(userLocation, 16);
            }

            // Add new user marker
            userMarker = L.marker(userLocation, { icon: userIcon, opacity: 0.5 }).addTo(map)
                .bindPopup("You are here").openPopup();

            // Check distance to each marker and update popup content accordingly
            markers.forEach(function(item) {
                var distance = userLocation.distanceTo(item.marker.getLatLng());

                if (distance <= 500000) {
                    item.marker.setPopupContent(item.closePopup).openPopup();
                } else {
                    item.marker.setPopupContent(item.DistantPopup).openPopup();
                }
            });
        });

        // Start locating user
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

// Function to handle when the quiz button is clicked
function triggerQuizEvent() {
    console.log("Quiz link clicked");
    var quizEvent = new CustomEvent('quizLinkClicked', {
        detail: { message: 'Quiz link clicked' }
    });
    window.parent.quizClicked(quizEvent);
}
