$(document).ready(function() {
	
	if ($("#id_newtag").length) {
		$("#id_newtag").autocomplete("/events/autosuggesttag/");
	};
	//Classifed add2.html validation and Classifed add3.html validation
	$('#website').click(function(){
	if ($('#website').val().length < 8){
		$('#website').val('http://');				
	}
	});
	
	$('#website').blur(function(){
		if($('#website').val() == 'http://'){
			$('#website').val('');
		};	
	});
	
});

//classified add-3.html



function largemap(){
		$('#map').height(280);
		$('#id_large').hide();
}

//Tag S


function addtag(){
var tagcount = 0;
	var tags=$('#id_newtag').val();
	var taglist = tags.split(",")
	var tag='';
	var len_tag = taglist.length;
	for(var i=0; i<len_tag; i++){
		tag=$.trim(taglist[i]);
		if(tag!=''){
			var newtag="<li id='id_stag_"+tagcount+"'><span onclick='deletetag("+tagcount+")'>&nbsp;</span>";
			newtag += tag;
			newtag += "<input type='hidden' name='tagselected' value='"+tag+"'/>";
			newtag += "</li>";
			$('#id_alltags').append(newtag);
			tagcount +=1;
			$('#id_newtag').val('');
		}
	}
}


function deletetag(id)
	{
	var id = "id_stag_"+id
	var el = document.getElementById(id);
	el.parentNode.removeChild(el);
	}
	
	


function load_locality_map(loc_id){
	
	if(!loc_id){
		$("#id_pin").val("");
		return false;
	}

			$("#id_loader").show();
			$.get("/events/getlocality-lat-long/",{ server_loc_id: loc_id }, function(lat_long){
				var lat  = 		String(lat_long.split("$")[0]);
				var longi = 		String(lat_long.split("$")[1]);
				var loc_name = 	String(lat_long.split("$")[2]);
				var zip_code = 	String(lat_long.split("$")[3]);
				load(lat, longi, 11, loc_name, "Longisland");
				$("#id_lat").val(lat);
				$("#id_lon").val(longi);
				$("#id_zoom").val(11)
				$("#id_pin").val(zip_code);
				$("#id_loader").hide(lat);
			});
} 



function validate_address_form(){
	noerror = true;
	
	if (noerror) {
			var lat_long = String(marker.getPoint());
			var lat_long_ready = lat_long.replace('(', '').replace(')', '');
			$('#id_pointer_lat').val(lat_long_ready.split(',')[0]);
			$('#id_pointer_lng').val(lat_long_ready.split(',')[1]);
			$('#id_map_zoom').val(map.getZoom());
			
		}
	return noerror;
}




