
var icon='http://bm.static.s3.amazonaws.com/images/map/marker_green.png';
var mapTypeIds = [];
var map;
var marker;
$(document).ready(function(){
	for(var type in google.maps.MapTypeId) { mapTypeIds.push(google.maps.MapTypeId[type]);}
	mapTypeIds.push("OSM");
});

function load(map_id,lat,lng,zoom,name,address){
	var element = document.getElementById(map_id);
	var latlng = new google.maps.LatLng(lat,lng);
	
	map = new google.maps.Map(element, {
	    center: latlng,
	    zoom: zoom,
	    mapTypeId:google.maps.MapTypeId.ROADMAP,
	    mapTypeControlOptions: {mapTypeIds: mapTypeIds}
	});
	map.mapTypes.set("OSM", new google.maps.ImageMapType({
	    getTileUrl: function(coord, zoom) {return "http://tile.openstreetmap.org/" + zoom + "/" + coord.x + "/" + coord.y + ".png";},
	    tileSize: new google.maps.Size(256, 256),
	    name:"StreetView",
	    maxZoom:18
	}));
	
	var html = "<b>" + name + "</b> <br/>" + address;
	var infowindow = new google.maps.InfoWindow({
        content: html,
        maxWidth: 100
    });
	marker = new google.maps.Marker({
	    position:latlng, 
	    map: map,
	    title:name,
		icon:icon
	});
	google.maps.event.addListener(marker, 'click', function(){
		infowindow.open(map, marker);
	});
}	
function config_load(map_id,lat,lng,zoom,name){
	var element = document.getElementById(map_id);
	var latlng = new google.maps.LatLng(lat,lng);
	
	map = new google.maps.Map(element, {
	    center: latlng,
	    zoom: zoom,
	    mapTypeId:google.maps.MapTypeId.ROADMAP,
	    mapTypeControlOptions: {mapTypeIds: mapTypeIds}
	});
	map.mapTypes.set("OSM", new google.maps.ImageMapType({
	    getTileUrl: function(coord, zoom) {return "http://tile.openstreetmap.org/" + zoom + "/" + coord.x + "/" + coord.y + ".png";},
	    tileSize: new google.maps.Size(256, 256),
	    name:"StreetView",
	    maxZoom:18
	}));
	
	var html = "<b>" + name +'</b>';
	var infowindow = new google.maps.InfoWindow({
        content: html,
        maxWidth: 100
    });
	marker = new google.maps.Marker({
	    position:latlng, 
	    map: map,
	    title:name,
		icon:icon,
		draggable: true
	});
	google.maps.event.addListener(marker, 'click', function(){
		infowindow.open(map, marker);
	});
	google.maps.event.addListener(marker, 'dragend', function(evt){
		$('#id_google_map_lat').val(parseFloat(evt.latLng.lat()));
		$('#id_google_map_lon').val(parseFloat(evt.latLng.lng()));
	});
	google.maps.event.addListener (map, 'zoom_changed', function() { 
		$('#id_google_map_zoom').val(parseInt(map.getZoom()));
	 });

}	
function load_for_add(map_id,lat,lng,zoom,name,address){
	var element = document.getElementById(map_id);
	var latlng = new google.maps.LatLng(lat,lng);
	
	map = new google.maps.Map(element, {
	    center: latlng,
	    zoom: zoom,
	    mapTypeId:google.maps.MapTypeId.ROADMAP,
	    mapTypeControlOptions: {mapTypeIds: mapTypeIds}
	});
	map.mapTypes.set("OSM", new google.maps.ImageMapType({
	    getTileUrl: function(coord, zoom) {return "http://tile.openstreetmap.org/" + zoom + "/" + coord.x + "/" + coord.y + ".png";},
	    tileSize: new google.maps.Size(256, 256),
	    name:"StreetView",
	    maxZoom:18
	}));
	
	var html = "<b>" + name +'</b><br>'+address;
	var infowindow = new google.maps.InfoWindow({
        content: html,
        maxWidth: 100
    });
	marker = new google.maps.Marker({
	    position:latlng, 
	    map: map,
	    title:name,
		icon:icon,
		draggable: true
	});
	google.maps.event.addListener(marker, 'click', function(){
		infowindow.open(map, marker);
	});
}	
function load_multi_marker(map_id,lat,lng,zoom,markers){
	var markerBounds = [];  
	var myOptions = {
	    zoom: 13,
	    mapTypeId: google.maps.MapTypeId.ROADMAP
	}   
	map = new google.maps.Map(document.getElementById(map_id), myOptions);
	map.mapTypes.set("OSM", new google.maps.ImageMapType({
    getTileUrl: function(coord, zoom) {return "http://tile.openstreetmap.org/" + zoom + "/" + coord.x + "/" + coord.y + ".png";},
    tileSize: new google.maps.Size(256, 256),
    name:"StreetView",
    maxZoom:18
	}));
	for(i=0;i<markers.length;i++){
		var html = "<b>" + markers[i].name + "</b> <br/>" + markers[i].address;
		var infowindow = new google.maps.InfoWindow({content: html});
		var marker;
		if(markers[i].icon){
			marker = new google.maps.Marker({
			    position:new google.maps.LatLng(markers[i].lat,markers[i].lng), 
			    map: map,
			    title:markers[i].name,
				icon:markers[i].icon
			});
		}
		else{
			marker = new google.maps.Marker({
			    position:new google.maps.LatLng(markers[i].lat,markers[i].lng), 
			    map: map,
			    title:markers[i].name,
				icon:icon
			});
		}
		markerBounds.push(new google.maps.LatLng(markers[i].lat,markers[i].lng));
		google.maps.event.addListener(marker, 'click', (function(marker, i,html) {
	        return function() {
	          infowindow.setContent(html);
	          infowindow.open(map, marker);
	        }
	      })(marker, i,html));
		
	}
    if (markerBounds.length == 1){
    	map.setCenter(markerBounds[0]);
    }
    else{
    	var latlngbounds = new google.maps.LatLngBounds();
	    for ( var i = 0; i < markerBounds.length; i++ ) {
	        latlngbounds.extend(markerBounds[i]);
	    }
    	map.setCenter(latlngbounds.getCenter());
    	map.fitBounds(latlngbounds);
    }
}

function load_multi_marker_with_numeric_overlay(map_id,lat,lng,zoom,markers){
	var markerBounds = [];  
	var myOptions = {
	    zoom: 13,
	    mapTypeId: google.maps.MapTypeId.ROADMAP
	}   
	map = new google.maps.Map(document.getElementById(map_id), myOptions);
	map.mapTypes.set("OSM", new google.maps.ImageMapType({
    getTileUrl: function(coord, zoom) {return "http://tile.openstreetmap.org/" + zoom + "/" + coord.x + "/" + coord.y + ".png";},
    tileSize: new google.maps.Size(256, 256),
    name:"StreetView",
    maxZoom:18
	}));
	for(i=0;i<markers.length;i++){
		var html = "<b>" + markers[i].name + "</b> <br/>" + markers[i].address;
		var infowindow = new google.maps.InfoWindow({content: html});
		var marker;
		if(markers[i].icon){
				var marker = new MarkerWithLabel({
	            map: map,
	            position: new google.maps.LatLng(markers[i].lat,markers[i].lng),
	            icon: markers[i].icon,
	            labelContent:  markers[i].label,
	            labelAnchor: new google.maps.Point(6, 40),
	            labelClass: "counter-labels"
        	});
		}
		else{
				var marker = new MarkerWithLabel({
	            map: map,
	            position: new google.maps.LatLng(markers[i].lat,markers[i].lng),
	            icon: markers[i].icon,
	            labelContent:  markers[i].label,
	            labelAnchor: new google.maps.Point(6, 40),
	            labelClass: "counter-labels"
	        });
		}
		markerBounds.push(new google.maps.LatLng(markers[i].lat,markers[i].lng));
		google.maps.event.addListener(marker, 'click', (function(marker, i,html) {
	        return function() {
	          infowindow.setContent(html);
	          infowindow.open(map, marker);
	        }
	      })(marker, i,html));
		
	}
    if (markerBounds.length == 1){
    	map.setCenter(markerBounds[0]);
    }
    else{
    	var latlngbounds = new google.maps.LatLngBounds();
	    for ( var i = 0; i < markerBounds.length; i++ ) {
	        latlngbounds.extend(markerBounds[i]);
	    }
    	map.setCenter(latlngbounds.getCenter());
    	map.fitBounds(latlngbounds);  
    }
}


var directionDisplay;
var directionsService = new google.maps.DirectionsService();

function init_getdirection(lat,lng,zoom) {
	  directionsDisplay = new google.maps.DirectionsRenderer();
	  var myOptions = {
	    zoom:zoom,
	    mapTypeId: google.maps.MapTypeId.ROADMAP,
	    center: new google.maps.LatLng(lat,lng)
	  };
	  map = new google.maps.Map(document.getElementById('map_getdirection'),myOptions);
	  directionsDisplay.setMap(map);
	  directionsDisplay.setPanel(document.getElementById('directions'));
}

function getDirections() {
	  var start = document.getElementById('saddr').value;
	  var end=document.getElementById('daddr').value;
	  var request = {
	    origin: start,
	    destination: end,
	    travelMode: google.maps.DirectionsTravelMode.DRIVING
	  };
	  directionsService.route(request, function(response, status) {
	    if (status == google.maps.DirectionsStatus.OK) {directionsDisplay.setDirections(response);}
	    else{
	    	if(status==google.maps.DirectionsStatus.NOT_FOUND){try_getDirections();}
	    	else{alert(gettext('Sorry !!! Not able to get direction.'));}
	    }
	  });
}
function try_getDirections() {
	  var start = document.getElementById('saddr').value;
	  var lat_lng=document.getElementById('daddr').value;
	  lat_lng=lat_lng.split('@');
	  var end=lat_lng[1];
	  var request = {
	    origin: start,
	    destination: end,
	    travelMode: google.maps.DirectionsTravelMode.DRIVING
	  };
	  directionsService.route(request, function(response, status) {
	    if (status == google.maps.DirectionsStatus.OK) {directionsDisplay.setDirections(response);}
	    else{alert(gettext('Sorry !!! Not able to get direction.'));}
	  });
	}

function set_center(lat,lan,zoom){
	var loc=new google.maps.LatLng(lat,lan)
	map.setZoom(zoom)
	map.setCenter(loc);
}
function set_center(lat,lan,zoom){
	var loc=new google.maps.LatLng(lat,lan)
	map.setZoom(zoom)
	map.setCenter(loc);
}
function set_center_marker(lat,lan,zoom){
	var loc=new google.maps.LatLng(lat,lan)
	map.setZoom(zoom)
	map.setCenter(loc);
	marker.setPosition(loc);
}
function set_center_map(map_id,lat,lan,zoom,name,address){
	var element = document.getElementById(map_id);
	var latlng = new google.maps.LatLng(lat,lan);
	var myOptions = {
	    zoom:zoom,
	    mapTypeId: google.maps.MapTypeId.ROADMAP,
	    center: new google.maps.LatLng(lat,lan)
	};
	map = new google.maps.Map(document.getElementById(map_id),myOptions);
	var html = "<b>"+name+'</b><br>'+address;
	var infowindow = new google.maps.InfoWindow({
	    content: html,
	    maxWidth: 100
	});
	marker = new google.maps.Marker({
	    position:latlng, 
	    map: map,
	    title:name,
		icon:icon,
		draggable: true
	});
	google.maps.event.addListener(marker, 'click', function(){
		infowindow.open(map, marker);
	});
	map.setZoom(zoom)
}


function getPin(address,pin) {
    var formatted_address;                        
    var address=address+" "+pin;
    var geocoder = new google.maps.Geocoder();
    geocoder.geocode( { 'address': address}, function(results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
        try{formatted_address=results[0].formatted_address;}
        catch(e){}                                               
        map.setCenter(results[0].geometry.location);
        set_center_marker_pin(results[0].geometry.location,formatted_address,13);
      } else {trygetPin(pin)}
    });
}
function trygetPin(pin) {
    var formatted_address;                        
    var address=pin;
    var geocoder = new google.maps.Geocoder();
    geocoder.geocode( { 'address': address}, function(results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
        try{formatted_address=results[0].formatted_address;}
        catch(e){}                                           
        map.setCenter(results[0].geometry.location);
        set_center_marker_pin(results[0].geometry.location,formatted_address,13);
      }
    });
}
function set_center_marker_pin(loc,address,zoom){
    map.setZoom(zoom)
    map.setCenter(loc);
    marker.title=address;
    marker.setPosition(loc);
    google.maps.event.clearListeners(marker, 'click');
   
    /*var html = "<b>" + address +"</b>";
    var infowindow = new google.maps.InfoWindow({
        content: html,
        maxWidth: 100
    });
    var marker = new google.maps.Marker({
      position: loc,
      map: map,
      title: address,
      icon:icon,
      draggable: true
     });
     google.maps.event.addListener(marker, 'click', function() {
       infowindow.open(map,marker);
     });*/
                                               
}
