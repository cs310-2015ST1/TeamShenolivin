function plotBikeWay(BikeWay, map) {
    var completeBikeWay = BikeWay;
    var bikeWayCoords = [];
    for (var i = 0; i < completeBikeWay.length; i++) {
        //for (var j = 0; j < allBikeWays[i].coordinates.length; j++){
        var latLong = new google.maps.LatLng(completeBikeWay[i][0], completeBikeWay[i][1]);
        //console.log(allBikeWays[i][0], allBikeWays[i][1]);
        bikeWayCoords.push(latLong);


        //console.log("got here");
        //};
    }
        var bikeWayLine = new google.maps.Polyline({
            path: bikeWayCoords,
            geodesic: true,
            strokeColor: '#FF0000',
            strokeOpacity: 1.0,
            strokeWeight: 2
        });

        bikeWayLine.setMap(map);


}
