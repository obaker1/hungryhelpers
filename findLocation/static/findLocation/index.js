function initMap() {
  const bounds = new google.maps.LatLngBounds();
  const markersArray = [];
    // origin hard coded for now
    const origin = "1000 Hilltop Circle Catonsville, Maryland";
    const destinationA = "Towson, Maryland";
    const destinationB = "Columbia, Maryland";

  const map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 55.53, lng: 9.4 },
    zoom: 10,
  });
  const geocoder = new google.maps.Geocoder();
  const service = new google.maps.DistanceMatrixService();
  // creates distance matrix
  service.getDistanceMatrix(
    {
      origins: [origin],
      destinations: [destinationA, destinationB],
      travelMode: google.maps.TravelMode.DRIVING,
      unitSystem: google.maps.UnitSystem.METRIC,
      avoidHighways: false,
      avoidTolls: false,
    },
    (response, status) => { // makes sure that the google maps distance matrix loaded correctly
      if (status !== "OK") {
        alert("Error was: " + status);
      } else {
        const originList = response.originAddresses;
        const destinationList = response.destinationAddresses;
        const outputDiv = document.getElementById("output");
        outputDiv.innerHTML = "";
        deleteMarkers(markersArray);

        const showGeocodedAddressOnMap = function (asDestination) { //add markers on map
          const icon = asDestination ? "D" : "O";
          const popup = asDestination ? "Destination" : "Origin";
          return function (results, status) {
            if (status === "OK") { // makes sure that the google maps geoencoder loaded correctly
              map.fitBounds(bounds.extend(results[0].geometry.location));
              const marker = new google.maps.Marker({
                  map,
                  position: results[0].geometry.location,
                  label: icon,
              })
              markersArray.push(marker);
              attachSecretMessage(marker, popup);
              /*map.addListener("center_changed", () => { //testing map center change
                // 3 seconds after the center of the map has changed, pan back to the marker.
                window.setTimeout(() => {
                map.panTo(marker.getPosition());
                }, 3000);
              });
              marker.addListener("click", () => { //testing map zoom on click
                map.setZoom(13);
                map.setCenter(marker.getPosition());
              });*/
            } else {
              alert("Geocode was not successful due to: " + status);
            }
          };
        };

        for (let i = 0; i < originList.length; i++) {
          const results = response.rows[i].elements;
          geocoder.geocode(
            { address: originList[i] },
            showGeocodedAddressOnMap(false)
          );

          for (let j = 0; j < results.length; j++) {
            geocoder.geocode(
              { address: destinationList[j] },
              showGeocodedAddressOnMap(true)
            );
            outputDiv.innerHTML +=
              originList[i] +
              " to " +
              destinationList[j] +
              ": " +
              results[j].distance.text +
              " in " +
              results[j].duration.text +
              "<br>";
          }
        }
      }
    }
  );
}
function attachSecretMessage(marker, secretMessage) { //add popups when marker is clicked
   const infowindow = new google.maps.InfoWindow({
     content: secretMessage,
   });
   marker.addListener("click", () => {
     infowindow.open(marker.get("map"), marker);
   });
}
function deleteMarkers(markersArray) {
  for (let i = 0; i < markersArray.length; i++) {
    markersArray[i].setMap(null);
  }
  markersArray = [];
}