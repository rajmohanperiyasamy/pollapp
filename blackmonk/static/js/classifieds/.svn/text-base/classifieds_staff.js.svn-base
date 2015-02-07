	function load_locality_map(){
		var loc_id = $("#id_locality").val();
		$.ajax({
			type: "GET",
			url: "/locality/getxmllocation/",
			data: "locality=" +$('#id_locality').val(),
			success: function(xml){
				var markers = xml.documentElement.getElementsByTagName("marker");
				for (var i = 0; i < markers.length; i++) {
					var lat = parseFloat(markers[i].getAttribute("lat"));
					var lng = parseFloat(markers[i].getAttribute("lng"));
					var zoom = parseInt(markers[i].getAttribute("zoom"));
					var name = $('#id_name').val();
					var address = $('#id_address1').val();
					load(lat, lng, zoom, 'green', name, address, '');
					$("#id_lat").val(lat);
					$("#id_lon").val(lng);
					$("#id_zoom").val(zoom)
					$("#id_loader").hide(lat);
				}
			}
		});
	}
	
	
		
	function validate(){
		
		$(".error").removeClass("error");
		var category = $("#id_category");
		var title = $("#id_title");
		var description = $("#id_description");
		var name = $("#id_name");
		var address = $("#id_address1");
		var locality = $("#id_locality");
		var zip = $("#id_pin");
		var website = $("#id_website");
		var email = $("#id_email");
		var validity_test = true;
		
	
		if (website.val() == 'http://' || website.val() == 'https://' ){
			website.val('');
		}else{
			website.removeClass("error");
		}
	
		if(title.val().length < 1){
			validity_test = false;
			title.addClass("error");
			title.focus();
		}
		
		if(category.val().length < 1){
			validity_test = false;
			category.addClass("error");
			category.focus();
		}
		
		if(description.val().length < 1){
			validity_test = false;
			description.addClass("error");
			description.focus();
		}
		if(name.val().length < 1){
			validity_test = false;
			name.addClass("error");
			name.focus();
		}
		if(address.val().length < 1){
			validity_test = false;
			address.addClass("error");
			address.focus();
		}
		
		if(locality.val().length < 1){
			validity_test = false;
			locality.addClass("error");
			locality.focus();
		}
		if(zip.val().length < 1){
			validity_test = false;
			zip.addClass("error");
			zip.focus();
		}
	
		
		if(website.val() !=''){
	    	if(!/^(http|https):\/\/[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(([0-9]{1,5})?\/.*)?$/.test(website.val())){
				validity_test = false;
				website.addClass("error").focus();		
			}
		}
		
		if(email.val() !=''){
	    	if(!/^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/.test(email.val())){
	    		validity_test = false;
				email.addClass("error").focus();		
			}
		}
	
		if (!validity_test){
			$(".messageerror").show();
		}else{
			$(".messageerror").hide();
		}
	return validity_test;
	}



