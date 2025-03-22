function initializeMap(iconUrl) {
    document.addEventListener("DOMContentLoaded", function () {
        var map = L.map('map').setView([50.73694, -3.53301], 15);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; OpenStreetMap contributors'
        }).addTo(map);

        var userIcon = L.icon({
            iconUrl: iconUrl,
            iconSize: [38, 38],
            iconAnchor: [19, 19],
            popupAnchor: [0, -19]
        });

        var binIcon = L.icon({
            iconUrl: '/static/resources/bin-marker.png',
            iconSize: [38, 38],
            iconAnchor: [19, 19],
            popupAnchor: [0, -19] 
        });

        var markers = [];

        function loadLocations() {
            fetch('/play_screen/get-locations')
                .then(response => response.json())
                .then(data => {

                    data.quiz_data.forEach(function(location) {
                        var quizButton = `<button onclick='triggerQuizEvent(${location.locationID})'>Start Quiz</button>`; 

                        var popupContent = `
                            <div>
                                <h3>${location.locationName}</h3>
                                ${quizButton}
                            </div>
                        `;

                        var marker = L.marker(location.coordinates).addTo(map).bindPopup(popupContent);

                        markers.push({ marker: marker });
                    });

                    data.bin_data.forEach(function(location) {
                        var binButton = `<button onclick='triggerBinEvent(${location.binID})'>Track Recycling</button>`; 

                        var popupContent = `
                            <div>
                                <h3>Bin: ${location.binIdentifier}</h3>
                                ${binButton}
                            </div>
                        `;
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
        });

        // Locate the user
        map.locate({ maxZoom: 16, watch: true, enableHighAccuracy: true });

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

// Function to handle when the bin button is clicked
function triggerBinEvent(binID) {
    window.top.location.href = `/recycling/${binID}`
}

// Function to handle when the quiz button is clicked
function triggerQuizEvent(locationID) {
    console.log("Redirecting to: /quiz/" + locationID);
    window.top.location.href = `/quiz/${locationID}`;
}
