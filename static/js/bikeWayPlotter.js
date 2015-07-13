function plotBikeWay(BikeWay, map) {
    var completeBikeWay = BikeWay;
    var bikeWayCoords = [];
    for (var i = 0; i < completeBikeWay.length; i++) {

        var latLong = new google.maps.LatLng(completeBikeWay[i][0], completeBikeWay[i][1]);
        bikeWayCoords.push(latLong);


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
