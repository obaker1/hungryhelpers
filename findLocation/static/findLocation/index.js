var ORIGIN_LIST;
var ADDRESS_LIST;
var LOCATION_FILTER;
var map;
var markersArray = [];
var filters = {school:false, bus:false}; // start out with filter features set to false, so no filtering happens by default

function initMap() {
  const bounds = new google.maps.LatLngBounds();
  const origin = ORIGIN_LIST;
  const destination = ADDRESS_LIST;

  // creates instaces for the map that is to be displayed
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 55.53, lng: 9.4 },
    zoom: 10,
  });
  // calls geocoder to get the exact location and uses it to pin the correct location on the map
  const geocoder = new google.maps.Geocoder();
  deleteMarkers(markersArray);
  const showGeocodedAddressOnMap = function (asDestination, school, bus, location, j) { //add markers on map
    return function (results, status) {
        if (asDestination) {
            icon = j.toString();
        }
        else {
            icon = "O";
        }
        if (status === "OK") { // makes sure that the google maps geoencoder loaded correctly
            map.fitBounds(bounds.extend(results[0].geometry.location));
            var marker;
            if (!asDestination) { // creates marker for origin
                location = results[0].formatted_address;
                marker = new google.maps.Marker({
                    map,
                    position: results[0].geometry.location,
                    label: icon,
                })
            }
           else { // creates marker for destination
                var prop = {school: school, bus:bus, title: results[0].formatted_address};
                marker = new google.maps.Marker({
                    map,
                    position: results[0].geometry.location,
                    properties: prop,
                    label: icon,
                })
            }
            markersArray.push(marker);
            const popup = results[0].formatted_address;
            attachSecretMessage(marker, location);
        } else {
            alert("Geocode was not successful due to: " + status);
        }
        };
    };
    if (origin != 0) { // if origin exists in database
      geocoder.geocode(
        { address: origin[j] },
        showGeocodedAddressOnMap(false, false, false, [], 0));
    }
    for (let j = 0; j < destination.length; j++) {
      school = false;
      bus = false;
      if (LOCATION_FILTER[j*2] == "T") {
        school = true;
      }
      if (LOCATION_FILTER[j*2+1] == "T") {
        bus = true;
      }
      geocoder.geocode(
        { address: destination[j] },
        showGeocodedAddressOnMap(true, school, bus, LOCATION_LIST[j], j+1));
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

// sets global variables for the origin and destinations
function setParameters(origin, address, filter, location){
    ORIGIN_LIST = origin;
    if (address[0] == "") { //if no destinations in database
        ADDRESS_LIST = 0;
    }
    else {
        ADDRESS_LIST = address;
    }
    LOCATION_FILTER = filter;
    LOCATION_LIST = location;
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