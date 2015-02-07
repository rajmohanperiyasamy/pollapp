
var map;
var infowindow;
var pyrmont;	
var markersArray = [];	
var mapTypeIds = [];	
var infowindow = new google.maps.InfoWindow();	

var directionDisplay;
var directionsService = new google.maps.DirectionsService();


$(document).ready(function(){
	for(var type in google.maps.MapTypeId) { mapTypeIds.push(google.maps.MapTypeId[type]);}
	mapTypeIds.push("OSM");
	
	$('#id_travel_mode_ul li a').click(function(){
		$('#id_travel_mode_ul li a').removeClass('active');
		$(this).addClass('active');
		$('#gmap_travel_mode').val($(this).attr('name'));
		calcRoute();
	});

});

function initialize() {
    pyrmont = new google.maps.LatLng(lat,lng);

	// Directions Code
	directionsDisplay = new google.maps.DirectionsRenderer();
	var defaultBounds = new google.maps.LatLngBounds(
  		new google.maps.LatLng(lat, lng),
  		new google.maps.LatLng(lat, lng)
	);

	var options = {
  	bounds: defaultBounds,
	types: ['geocode'],
	componentRestrictions: {country: "ca"}
	};

	var input_one = document.getElementById('id_from_text');
	var input_two = document.getElementById('id_to_text');
	var autocomplete_one = new google.maps.places.Autocomplete(input_one,options);
	var autocomplete_two = new google.maps.places.Autocomplete(input_two,options);
	// Directions Code end

    map = new google.maps.Map(document.getElementById('map'), {
      mapTypeId: google.maps.MapTypeId.ROADMAP,
	  mapTypeControlOptions: {mapTypeIds: mapTypeIds},
      center: pyrmont,
      zoom: 15
    });

	map.mapTypes.set("OSM", new google.maps.ImageMapType({
	    getTileUrl: function(coord, zoom) {return "http://tile.openstreetmap.org/" + zoom + "/" + coord.x + "/" + coord.y + ".png";},
	    tileSize: new google.maps.Size(256, 256),
	    name:"StreetView",
	    maxZoom:18
	}));
	

}

function find_places(){
	request = null;
	var selected_places=[];
	clear();
	$('#bm_places_option :checked').each(function() {
       selected_places.push($(this).val());
     });
	/*selected_places.forEach(function(item){ 
		initialize();
		var request = {
          location: pyrmont,
          radius: 20000,
          types: [item]
        };
        var service = new google.maps.places.PlacesService(map);
        service.search(request, callback);
	 });*/

	for (var i = 0; i < selected_places.length; i++) {
    //alert(selected_places[i]);
   		initialize();
		var request = {
          location: pyrmont,
          radius: 20000,
          types: [selected_places[i]]
        };
        var service = new google.maps.places.PlacesService(map);
        service.search(request, callback);
	}



}

function callback(results, status) {
    if (status == google.maps.places.PlacesServiceStatus.OK) {
      for (var i = 0; i < results.length; i++) {
        createMarker(results[i]);
      }
    }
}

function createMarker(place) {
        var placeLoc = place.geometry.location;
		var icon = new google.maps.MarkerImage(place.icon, null, null, null, new google.maps.Size(20, 20));
        var marker = new google.maps.Marker({
          map: map,
		  icon:icon,	
		  animation: google.maps.Animation.DROP,	
          position: place.geometry.location
        });
		markersArray.push(marker);
		var title = place.name;
		var address = place.vicinity;

        google.maps.event.addListener(marker, 'click', function() {
		  infowindow.setContent('<strong>'+place.name + '</strong><br />' + place.vicinity);
          infowindow.open(map, marker);
        });

}
		
function clear(){
	if (markersArray) {
	   for (i in markersArray) {
                markersArray[i].setMap(null);
        }
    }
}

function calcRoute() {
	
	var selectedMode = document.getElementById("gmap_travel_mode").value;
	directionsDisplay.setMap(map);
	directionsDisplay.setPanel(document.getElementById('directions-panel'));

    var start = $('#id_from_text').val();
    var end = $('#id_to_text').val();

    var request = {
        origin:start, 
        destination:end,
        //travelMode: google.maps.DirectionsTravelMode.DRIVING
		travelMode: google.maps.DirectionsTravelMode[selectedMode]
    };
    directionsService.route(request, function(response, status) {
      if (status == google.maps.DirectionsStatus.OK) {
		$('#directions-panel').empty();
        directionsDisplay.setDirections(response);
      }
    });
  }