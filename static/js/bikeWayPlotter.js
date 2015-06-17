/**
 * Created by Sharon on 15/06/2015.
 */

//var allBikeWays = {{}};
//var allBikeWays = [[[49.2327,-123.1207], [49.2827,-123.1907], [49.2227,-123.1207]],
//                    [[49.3827,-123.1207], [49.1827,-123.1207]]];

function plotBikeWay(map) {
    var allBikeWays = [[49.2327,-123.1207], [49.2827,-123.1907], [49.2227,-123.1207]];
    var bikeWayCoords = [];
    for (var i = 0; i < allBikeWays.length; i++) {

        //for (var j = 0; j < allBikeWays[i].coordinates.length; j++){
        var latLong = new google.maps.LatLng(allBikeWays[i][0], allBikeWays[i][1]);
        console.log(allBikeWays[i][0], allBikeWays[i][1]);
        bikeWayCoords.push(latLong);


        console.log("got here");
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
