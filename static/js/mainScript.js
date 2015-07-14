    var loggedIn = false;
    var times = 0;
    var inputLocations = [];

    function greyOut(inputLocations, i) {
        console.log("Executing input change callback");
        var place = inputLocations[i].searchBox.getPlace();
        console.log(inputLocations[i].searchBox.getPlace());
        var locationString = document.getElementById("locationInput" + (i+1).toString()).value;
                          
        if (place == null && locationString === "") {
            if (i < 4) {
                document.getElementById("locationInput"+(i+2).toString()).disabled = true;
                document.getElementById("delete"+(i+2).toString()).disabled = true;
                document.getElementById("locationInput"+(i+2).toString()).style.backgroundColor = '#CCCCCC';
            }
            return false;
        } else {
            if (i < 4) {
                document.getElementById("locationInput"+(i+2).toString()).disabled = false;
                document.getElementById("delete"+(i+2).toString()).disabled = false;
                document.getElementById("locationInput"+(i+2).toString()).style.backgroundColor = '#FFFFFF';
            }
        }
        return true;
    }
    
    function initialize() {
        
        // map setup
        var mapProp = {
            center:new google.maps.LatLng(49.2827,-123.1207),
            zoom:12,
            mapTypeId:google.maps.MapTypeId.ROADMAP
        };
        
        var map = new google.maps.Map(document.getElementById("googleMap"),mapProp);
        
        var allBikeWays = {{ allBikeWays }};
        for (var i = 0; i < allBikeWays.length; i++) {
            plotBikeWay(allBikeWays[i], map);
        }
        
        // setting up the search boxes
        var inputBoxes = document.querySelectorAll("input[type=text]");
        console.log(inputBoxes.length);
        
        for (var i = 0; i < inputBoxes.length; i++) {
            
            console.log("Found " + inputBoxes[i].id);
            
            // make a struct of related data for each input box
            // save all the information in an array of structs
            inputLocations[i] = { 
                element: inputBoxes[i], 
            
                marker: new google.maps.Marker({
                    map: map,
                    anchorPoint: new google.maps.Point(0, -29)
                }),

                searchBox: new google.maps.places.Autocomplete(/** @type {HTMLInputElement} */(inputBoxes[i])),

                markerIcon: "{{ STATIC_URL }}images/marker" + (i+1).toString() + ".png"
            };
        
            console.log(inputLocations[i].markerIcon);
            inputLocations[i].marker.setVisible(false);
            
            // document.getElementById("locationInput"+(i+1).toString()).value = "";

            // create the listener for when the text box is updated
            google.maps.event.addListener(inputLocations[i].searchBox, 'place_changed', function() {
                                          
                var bounds = new google.maps.LatLngBounds();
                var invalidLocations = [];
                var numMarkers = 0;
                // disabling and enabling input text boxes
                for (var i = 0; i < inputLocations.length; i++) {
                    var place = inputLocations[i].searchBox.getPlace();
                    
                    if (!greyOut(inputLocations, i)) {
                        continue;
                    }
                    inputLocations[i].marker.setVisible(false);

                    // Create a marker if the location can be found
                    if (place.geometry == null) {
                        invalidLocations.push(place.name); 
                        console.log("invalid location: " + place.name);
                        continue;
                    }
                
                inputLocations[i].marker = new google.maps.Marker({
                    map: map,
                    //icon: 'http://maps.google.com/mapfiles/marker.png',
                    icon: inputLocations[i].markerIcon,
                    title: place.name,
                    position: place.geometry.location
                });

                inputLocations[i].marker.setVisible(true);
                numMarkers++;
                bounds.extend(place.geometry.location);
            }

            if (invalidLocations.length > 0) {
                var errMsg = invalidLocations.length > 1 ? "Locations ":"Location ";
                errMsg += "not recognized:\n";
                for (j = 0; j < invalidLocations.length; j++) {
                    errMsg += invalidLocations[j] + "\n";
                }
                window.alert(errMsg);
            }
                                      
            if (numMarkers != 0) {
                map.fitBounds(bounds);
            } else  {
                map.setCenter(new google.maps.LatLng(49.2827,-123.1207));
                map.setZoom(12);
            }
        });
    };

    // Bias the SearchBox results towards places that are within the bounds of the
    // current map's viewport.
    google.maps.event.addListener(map, 'bounds_changed', function() {
        var bounds = map.getBounds();

        for (var i = 0; i < inputLocations.length; i++) {
            inputLocations[i].searchBox.setBounds(bounds);

        }
    });
}

google.maps.event.addDomListener(window, 'load', initialize);

function deleteClicked(e, number) {
    if (document.getElementById("delete"+number.toString()).disabled) {
        e.preventDefault();
        return;
    }
    
    if (confirm('Are you sure you want to delete this marker from the map?'))
        deleteMarker(number);
    else {
        e.preventDefault();
        console.log("cancelled deleting marker # " + number.toString());
    }
}

function deleteMarker(number) {
    console.log("removing marker # " + number.toString());
    inputLocations[number-1].marker.setMap(null);
    document.getElementById("locationInput"+number.toString()).value = "";
    shiftLocations(number-1);
}

function shiftLocations(index) {
    for (var j = index; j < inputLocations.length-1; j++) {
        inputLocations[j].searchBox.set('place', inputLocations[j+1].searchBox.getPlace());
        document.getElementById("locationInput"+(j+1).toString()).value = document.getElementById("locationInput"+(j+2).toString()).value;
    }
    inputLocations[inputLocations.length-1].searchBox.set('place', void(0));
    document.getElementById("locationInput"+inputLocations.length.toString()).value = "";
}

function resetClicked(e) {
    if (confirm('Are you sure you want to remove all markers from the map?'))
    removeAllMarkers();
    else {
        e.preventDefault();
        console.log("cancelled deleting all markers");
    }
}

function removeAllMarkers() {
    console.log("removing all markers");
    for (var i = 0, ip; ip = inputLocations[i]; i++) {
        ip.marker.setMap(null);
        document.getElementById("locationInput"+(i+1).toString()).value = "";
        ip.searchBox.set('place',void(0));
    }
}

function calcRoute(startIndex, finIndex) {
    var startID = "locationInput" + (startIndex + 1).toString();
    var endID = "locationInput" + (finIndex + 1).toString();
      var start = document.getElementById(startID).value;
      var end = document.getElementById(endID).value;
      var request = {
          origin:start,
          destination:end,
          travelMode: google.maps.TravelMode.DRIVING
      };
      directionsService.route(request, function(response, status) {
        if (status == google.maps.DirectionsStatus.OK) {
          directionsDisplay.setDirections(response);
          var plannedRoutes = response.routes;
          var singleRoute = plannedRoutes[0];
          var leg = singleRoute.legs[0];
          var steps = leg.steps;
          var length = steps.length;
          alert("There are " + length + " steps in these direction instructions.");
        }
      });
 }

 function plotCalcRoute() {

 }
