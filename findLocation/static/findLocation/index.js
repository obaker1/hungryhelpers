var map;
var markersArray = [];
var filters = {school:false, bus:false}; // start out with filter features set to false, so no filtering happens by default

// constantly update filter markers
$(function () {
    $('input[name=filter]').change(function (e) {
        map_filter(this.id);
        filter_markers();
    });
})
var map_filter = function(id_val) {
   if (filters[id_val])
      filters[id_val] = false;
   else
      filters[id_val] = true;
}

// get a subset of the filters that are set to true
var get_set_options = function() {
  ret_array = [];
  for (option in filters) {
    if (filters[option]) {
      ret_array.push(option);
    }
  }
  return ret_array;
}

var filter_markers = function() {
  set_filters = get_set_options();
  // for each marker, check to see if all required options are set
  for (i = 0; i < markersArray.length; i++) {
    marker = markersArray[i];
    keep=true; // start the filter check assuming the marker will be displayed
    for (opt=0; opt<set_filters.length; opt++) {
      if (!marker.properties[set_filters[opt]]) {
        keep = false; // if missing required feature
      }
    }
    marker.setVisible(keep);
  }
}

// loads the markers onto the map
function loadMarkers() {
  var infoWindow = new google.maps.InfoWindow();
  geojson_url = 'https://raw.githubusercontent.com/obaker1/hungryhelpers/feature/filterMap/map.geojson';
  // load the geoJSON file
  $.getJSON(geojson_url, function(result) {
      // Post select to url
      data = result['features'];
      // iterate through the map data to create markers
      $.each(data, function(key, val) {
        var point = new google.maps.LatLng(
            parseFloat(val['geometry']['coordinates'][0]),
            parseFloat(val['geometry']['coordinates'][1]));
        var titleText = val['properties']['title'];
        var descriptionText = val['properties']['description'];
        var marker = new google.maps.Marker({
          position: point,
          title: titleText,
          map: map,
          properties: val['properties'],
          label: "D"
        });
        //attachSecretMessage(marker, "Destination");
        var markerInfo = "<div><h3>" + titleText + "</h3>Amenities: " + descriptionText + "</div>";

        // show info windows when a marker is clicked
        marker.addListener('click', function() {
           $('#places_info').html(markerInfo);
        });
        markersArray.push(marker);
      });
  });
}

function initMap() {
  const bounds = new google.maps.LatLngBounds();
    // locations and distances, hard coded for now
    const origin = "1000 Hilltop Circle Catonsville, Maryland";
    const destinationA = new google.maps.LatLng(39.401794462959664, -76.60364082158517);
    const destinationB = new google.maps.LatLng(39.20393322969507, -76.85615843748513);
    const destinationC = new google.maps.LatLng(39.321837620538545, -76.65404104179306);

  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 39.332857, lng: -76.681437 },
    zoom: 10,
  });
  loadMarkers(); // loads the markers onto the map
  const geocoder = new google.maps.Geocoder();
  const service = new google.maps.DistanceMatrixService();
  // creates distance matrix
  service.getDistanceMatrix(
    {
      origins: [origin],
      destinations: [destinationA, destinationB, destinationC],
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

        const showGeocodedAddressOnMap = function (asDestination) { //add markers on map
          const icon = asDestination ? "D" : "O";
          const popup = asDestination ? "Destination" : "Origin";
          return function (results, status) {
            if (status === "OK") { // makes sure that the google maps geoencoder loaded correctly
              map.fitBounds(bounds.extend(results[0].geometry.location));
                if (!asDestination) {
                  const marker = new google.maps.Marker({
                      map,
                      position: results[0].geometry.location,
                      label: icon,
                  })
                  markersArray.push(marker);
                  attachSecretMessage(marker, popup);
                }
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