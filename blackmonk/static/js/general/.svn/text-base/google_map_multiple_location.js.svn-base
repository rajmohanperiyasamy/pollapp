//<![CDATA[
    var iconGreen = new GIcon(); 
    iconGreen.image = '/site_media/images/map/marker_green.png';
    iconGreen.shadow = '/site_media/images/map/shadow.png';
    iconGreen.iconSize = new GSize(20, 34);
    iconGreen.shadowSize = new GSize(37, 34);
    iconGreen.iconAnchor = new GPoint(9, 34);
    iconGreen.infoWindowAnchor = new GPoint(5, 1);
    var opt  
	opt = {}
	opt.draggable = false  
	opt.clickable = true  
	opt.dragCrossMove = true 
	var marker;
	var map;
	function moreaddress(lat,lng,name,address,type){
		var point = new GLatLng(lat, lng);
		marker = createMarker(point, name, address, type);
		map.addOverlay(marker);
	}
	function createMarker(point, name, address, type) {
    	opt.icon = iconGreen
		var marker = new GMarker(point, opt);
		var html = "<b>" + name + "</b> <br/>" + address;
		GEvent.addListener(marker, 'click', function() {
			marker.openInfoWindowHtml(html);
		});
		return marker;
    }
	
	
	
	
	
	var side_bar_html = "";
		var gmarkers = [];
		var htmls = [];
		// arrays to hold variants of the info window html with get direction forms open
		var to_htmls = [];
		var from_htmls = [];
		var gdir;

		// === Array for decoding the failure codes ===
		var reasons=[];
		reasons[G_GEO_SUCCESS]            = "Success";
		reasons[G_GEO_MISSING_ADDRESS]    = "Missing Address: The address was either missing or had no value.";
		reasons[G_GEO_UNKNOWN_ADDRESS]    = "Unknown Address:  No corresponding geographic location could be found for the specified address.";
		reasons[G_GEO_UNAVAILABLE_ADDRESS]= "Unavailable Address:  The geocode for the given address cannot be returned due to legal or contractual reasons.";
		reasons[G_GEO_BAD_KEY]            = "Bad Key: The API key is either invalid or does not match the domain for which it was given";
		reasons[G_GEO_TOO_MANY_QUERIES]   = "Too Many Queries: The daily geocoding quota for this site has been exceeded.";
		reasons[G_GEO_SERVER_ERROR]       = "Server error: The geocoding request could not be successfully processed.";
		reasons[G_GEO_BAD_REQUEST]        = "A directions request could not be successfully parsed.";
		reasons[G_GEO_MISSING_QUERY]      = "No query was specified in the input.";
		reasons[G_GEO_UNKNOWN_DIRECTIONS] = "The GDirections object could not compute directions between the points.";
		
		

		// A function to create the marker and set up the event window
		function createMarkerDirection(point,name,html) {
			var marker = new GMarker(point);
			
			var i = gmarkers.length;
			/*
			// The info window version with the "to here" form open
			to_htmls[i] = html + '<br>Directions: <b>To here<\/b> - <a href="javascript:fromhere(' + i + ')">From here<\/a>' +
			   '<br>Start address:<form action="javascript:getDirections()">' +
			   '<input type="text" SIZE=40 MAXLENGTH=40 name="saddr" id="saddr" value="" /><br>' +
			   '<INPUT value="Get Directions" TYPE="SUBMIT"><br>' +
			   'Walk <input type="checkbox" name="walk" id="walk" /> &nbsp; Avoid Highways <input type="checkbox" name="highways" id="highways" />' +
			   '<input type="hidden" id="daddr" value="'+name+"@"+ point.lat() + ',' + point.lng() + 
			   '"/>';
			// The info window version with the "from here" form open
			from_htmls[i] = html + '<br>Directions: <a href="javascript:tohere(' + i + ')">To here<\/a> - <b>From here<\/b>' +
			   '<br>End address:<form action="javascript:getDirections()">' +
			   '<input type="text" SIZE=40 MAXLENGTH=40 name="daddr" id="daddr" value="" /><br>' +
			   '<INPUT value="Get Directions" TYPE="SUBMIT"><br>' +
			   'Walk <input type="checkbox" name="walk" id="walk" /> &nbsp; Avoid Highways <input type="checkbox" name="highways" id="highways" />' +
			   '<input type="hidden" id="saddr" value="'+name+"@"+ point.lat() + ',' + point.lng() +
			   '"/>';
			// The inactive version of the direction info
			html = html + '<br>Directions: <a href="javascript:tohere('+i+')">To here<\/a> - <a href="javascript:fromhere('+i+')">From here<\/a>';
			*/
			GEvent.addListener(marker, "click", function() {
			  marker.openInfoWindowHtml(html);
			});
			// save the info we need to use later for the side_bar
			gmarkers.push(marker);
			htmls[i] = html;
			// add a line to the side_bar html
			side_bar_html += '<a href="javascript:myclick(' + i + ')">' + name + '<\/a><br>';
			return marker;
		}
		
		// ===== request the directions =====
		function getDirections() {
			// ==== Set up the walk and avoid highways options ====
			var opts = {};
			if (document.getElementById("walk").checked) {
			   opts.travelMode = G_TRAVEL_MODE_WALKING;
			}
			if (document.getElementById("highways").checked) {
			   opts.avoidHighways = true;
			}
			// ==== set the start and end locations ====
			var saddr = document.getElementById("saddr").value
			var daddr = document.getElementById("daddr").value
			gdir.load("from: "+saddr+" to: "+daddr, opts);
		}
		
		
		// This function picks up the click and opens the corresponding info window
		function myclick(i) {
			gmarkers[i].openInfoWindowHtml(htmls[i]);
		}
		
		// functions that open the directions forms
		function tohere(i) {
			gmarkers[i].openInfoWindowHtml(to_htmls[i]);
		}
		function fromhere(i) {
			gmarkers[i].openInfoWindowHtml(from_htmls[i]);
		}
	
	
	
	
	
	
    //]]>