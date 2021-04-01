var ORIGIN_LIST;
var DESTINATION_LIST;

function initMap() {
  const bounds = new google.maps.LatLngBounds();
  const markersArray = [];
    const origin = ORIGIN_LIST;
    const destination = DESTINATION_LIST;

   // creates instaces for the map that is to be displayed
  const map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 55.53, lng: 9.4 },
    zoom: 10,
  });

  // calls geocoder to get the exact location and uses it to pin the correct location
 // on the map
  const geocoder = new google.maps.Geocoder();
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
        } else {
          alert("Geocode was not successful due to: " + status);
        }
      };
    };

    // creates a marker for the origin and destinations
    for( let j = 0; j< origin.length;j++){
      geocoder.geocode(
        { address: origin[j] },
        showGeocodedAddressOnMap(false));
        }
      for (let j = 0; j < destination.length; j++) {
        geocoder.geocode(
          { address: destination[j] },
          showGeocodedAddressOnMap(true)
        );

      }

}

// sets global variables for the origin and destinations
function setParameters(origin, destinations){
    ORIGIN_LIST = [origin];
    DESTINATION_LIST = destinations;
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