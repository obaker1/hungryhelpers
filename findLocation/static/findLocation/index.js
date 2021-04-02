var ORIGIN_LIST;
var DESTINATION_LIST;
var map;
var markersArray = [];
var filters = {school:false, bus:false}; // start out with filter features set to false, so no filtering happens by default


function initMap() {
  const bounds = new google.maps.LatLngBounds();
  const origin = ORIGIN_LIST;
  const destination = DESTINATION_LIST;

  // creates instaces for the map that is to be displayed
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 55.53, lng: 9.4 },
    zoom: 10,
  });
  loadMarkers(); // loads the markers onto the map
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
        if (!asDestination) {
          const marker = new google.maps.Marker({
              map,
              position: results[0].geometry.location,
              label: icon,
          })
          markersArray.push(marker);
          attachSecretMessage(marker, popup);
        }
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
        showGeocodedAddressOnMap(true));
    }
}
        
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
    if (marker.label == 'D') { // if the marker is a destination
        keep=true; // start the filter check assuming the marker will be displayed
        for (opt=0; opt<set_filters.length; opt++) {
          if (!marker.properties[set_filters[opt]]) { // if a property is not selected
            keep = false;
          }
        }
        marker.setVisible(keep);
    }
  }
}

// loads the markers onto the map
function loadMarkers() {
  var infoWindow = new google.maps.InfoWindow();
  geojson_url = 'https://raw.githubusercontent.com/obaker1/hungryhelpers/main/map.geojson';
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
        var markerInfo = "<div><h3>" + titleText + "</h3>Amenities: " + descriptionText + "</div>";

        // show info windows when a marker is clicked
        marker.addListener('click', function() {
           $('#places_info').html(markerInfo);
        });
        markersArray.push(marker);
      });
  });
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