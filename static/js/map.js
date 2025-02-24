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

        // Array of locations to be replaced with loading of loactions from a databse later on
        var locations = [
            { coords: [50.7381145, -3.5311094], name: "Location 1" },
            { coords: [50.7371145, -3.5321094], name: "Location 2" },
            { coords: [50.7361145, -3.5331094], name: "Location 3" }
        ];

        // Array to store marker instances
        var markers = [];

        // adding each location to the map as well as a marker array
        locations.forEach(function(location) {
            var quizButton = "<button onclick='triggerQuizEvent()'>Take the quiz</button>"; // Replace with your quiz page link
            var DistantPopup = location.name;
            var closePopup = location.name + ". " + quizButton;

            var marker = L.marker(location.coords).addTo(map).bindPopup(DistantPopup);
            markers.push({ marker: marker, closePopup: closePopup, DistantPopup: DistantPopup });
        });

        // variables to store user location and marker
        let userMarker = null;
        let userLocation = null;
        //function that runs when the user location is found
        map.on('locationfound', function(e) {
            userLocation = e.latlng;
            console.log(userLocation);
            //to be removed, location on the user location to show off functionality
            var quizButton = "<button onclick='triggerQuizEvent()'>Take the quiz</button>"; // Replace with your quiz page link
            var DistantPopup = "Test location";
            var closePopup = "Test location" + ". " + quizButton;
            var marker = L.marker(userLocation).addTo(map).bindPopup(DistantPopup);
            markers.push({ marker: marker, closePopup: closePopup, DistantPopup: DistantPopup });

            // checks if a user marker is already on the map when the location is found again, prevents stacked location markers
            if (userMarker) {
                map.removeLayer(userMarker);
            } else {
                map.setView(userLocation, 16);
            }

            // puts the user marker onto the map
            userMarker = L.marker(userLocation, {icon: customIcon, opacity: 0.5}).addTo(map)
                .bindPopup("You are within " + Math.round(e.accuracy) + " meters from this point").openPopup();

            // Check distance to each marker and update popup content accordingly
            markers.forEach(function(item) {
                var distance = userLocation.distanceTo(item.marker.getLatLng());

                if (distance <= 50) {
                    item.marker.setPopupContent(item.closePopup).openPopup();
                } else {
                    item.marker.setPopupContent(item.DistantPopup).openPopup();
                }
            });
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

// Function handle when the quiz button is pressed
function triggerQuizEvent() {
    console.log("Quiz link clicked");
    var quizEvent = new CustomEvent('quizLinkClicked', {
        detail: { message: 'Quiz link clicked' }
    });
    window.parent.quizClicked(quizEvent);
}