$(document).ready(function(){
	
	if($("#id_start_date").length){
		$("#id_start_date").datepicker({ dateFormat: "yy-mm-dd" , minDate: new Date()});
	}
	if($("#id_end_date").length){
		$("#id_end_date").datepicker({ dateFormat: "yy-mm-dd" , minDate: new Date()});
	}
	if ($("#id_newtag").length) {
		$("#id_newtag").autocomplete("/events/autosuggesttag/");
	}
	
	if ($("#id_venue").length){
		$("#id_venue").autocomplete("/events/autosugges_venue/");
		
	}
	
	$('#id_free_Event').click(function(){
		if ($(this).attr('checked')) {
			
			$("#id_tkt_prize").attr('disabled','disabled');
			$("#id_tkt_prize").val('');
			$("#id_tkt_prize").css('background-color','#D8D8D8');
		}else{
			$("#id_tkt_prize").removeAttr('disabled');
			$("#id_tkt_prize").removeAttr('style');
		}
	});
	
	$('#id_summary').keypress(function(){
		var a=$(this).val().length;
		
		if (a>300)
			{
			 $('#descounter').css('color','red');
			}
		else 
			{
				$('#descounter').css('color','');
			};
		update_lengthcounter(a,300,'descounter');
	});
	
	$('#id_title').keypress(function(){
		var a=$(this).val().length;
		var rem = 150-a
		
		if (a>120)
			{
			 $('#title_messge').css('color','red');
			 var rem = 150-a
			 $('#title_messge').html('Remaining:'+rem+' characters')
			 
			}
		else
			{		
				$('#title_messge').html('Remaining:'+rem+' characters')
				$('#title_messge').css('color','');
			}
		
	});
	
	scheduler_load();
	$(".day_names").click(function(){
		show_hide_day_timings();
	});
	
	//form validation Add Step 1
	$("#mform").validate({
		errorLabelContainer: "#validation_error",
   		wrapper: "span",
	   	rules: {
	    	title:"required",
			summary:"required",
			category:"required",
			start_date:"required",
			end_date:"required",
			venue_url:{
				url:"true"	
			     },
			     ticket_site:{
				url:"true"	
			     },
	   	},
	   	messages: {
	    	title: "Please enter the Title",
	    	summary: "Please enter the event summary",
	    	category: "Select the event type",
	    	start_date: "Pick the start date of the event",
	    	end_date:"Pick the end date of the event",
	    	venue_url:"Enter a valid event website, eg: http://www.example.com",
	    	ticket_site:"Enter a valid ticket site address, eg: http://www.buytickets.com"
	   	},
	   	invalidHandler: function(form, validator) {
	      var errors = validator.numberOfInvalids();
	      if (errors) {
	        $("div#validation_error").show();
	      } else {
	        $("div#validation_error").hide();
	      }
	    }
	});	
		//form validation Add Step 2 : Venue Details
	
	$("#mform1").validate({
		errorLabelContainer: "#validation_error",
   		wrapper: "span",
	   	rules: {
	    	venue:"required",
			address1:"required",
			contact_email:{
				email:"true"	
			     }
	   	},
	   	messages: {
	    	venue: "Please enter the venue name",
	    	address1: "Please enter the venue address",
	    	contact_email: "Please enter a valid email address",
	   	},
	   	invalidHandler: function(form, validator) {
	      var errors = validator.numberOfInvalids();
	      if (errors) {
	        $("div#validation_error").show();
	      } else {
	        $("div#validation_error").hide();
	      }
	    },
	    submitHandler: function(form) {
      		var lat_long = String(marker.getPoint());
			var lat_long_ready = lat_long.replace('(', '').replace(')', '');
			$('#id_lat').val(lat_long_ready.split(',')[0]);
			$('#id_lon').val(lat_long_ready.split(',')[1]);
			$('#id_zoom').val(map.getZoom());
     		form.submit();
  		 }
	});	
	
	

});
	
// -------------  ready document eneded, event based functions started from here. -------------

function as_autocomplete(){
		var ven = $("#id_venue").val();
		if (ven){
			$.ajax({
				url:"/events/auto_venue_details/",
				type : "GET",
				dataType : 'json',
				data :"eid="+ven,
				success : function(data){
					var add = data.venue_add;
					var add2 = data.venue_add2;
					var postal_code = data.postal_code;
					var loc_name = data.locality_id;
					var land_phone = data.land_phone;
					var mobile_phone = data.mobile_phone;
					var lat = data.lat;
					var longi = data.longi;
					var zoom = data.zoom
					
					$("#id_address1").val(add);
					$("#id_address2").val(add2);
					$("#id_zip").val(postal_code);
					
					if (loc_name){
						$("#id_locality option[value = "+ loc_name +"]").attr('selected','selected');
						$("#id_loader").show();
						load(lat, longi, zoom, loc_name, "");
						$("#id_loader").hide();		
						$("#id_lat").val(lat);	$("#id_lon").val(longi); $("#id_zoom").val(zoom)
					}
 }})}}


function recurring_events(){
	var reapeating = $("#reapeating").attr("checked");
	if(reapeating){
		$(".recurring_input").show(300);
		$("#time_hide").hide();
	}else{
		$(".recurring_input").hide(300);
		$("#time_hide").show();
	}
}

function scheduler_load(){
	if($("#area_repeat_on").val()){
		$("#reapeating").click();
	}
	if($("#area_repeat_on_days").val() > 0){
		$("#different").attr("checked",true);
		event_multiple_timings($("#event_id").val());
	}
}

function event_multiple_timings(id){
	
	if(!id){
		id = 0  
	}
	var radio = $("input:radio[name=custom_timing]:checked").val();
	if(radio == "same"){
		$("#time_hide").show(300);
		$("#multiple_time_hide").hide(300);
	}else{
		$("#time_hide").hide(300);
		
		if($("#multiple_time_hide").children().length > 0){
			$("#multiple_time_hide").show(300);
			show_hide_day_timings();
		}else{
			
			$("#id_loading").show();
			$.get("/events/seven-days/",{id:id},function(data){
				$("#multiple_time_hide").html(data).show(300);
				show_hide_day_timings();
				$("#id_loading").hide();
				//Below code executes if Returned ajax is loaded for first time with pre filled database values from ajax template
				if($(".times_days").length){
					$(".times_days").each(function(){
						var values_composite = $(this).val();
						values_composite = values_composite.split("_");
						$("#"+values_composite[0]+"_start_time").val(values_composite[1]);
						$("#"+values_composite[0]+"_end_time").val(values_composite[2]);
					});
				}
			});
		}
	}
}

function show_hide_day_timings(){
	var radio = $("input:radio[name=custom_timing]:checked").val();
	if(radio == "different"){
		$('.day_names').each(function(){
			if($(this).attr("checked")){
				class_ele = $(this).val()+"_time";
				$("."+class_ele).show();
			}else{
				class_ele = $(this).val()+"_time";
				$("."+class_ele).hide();
			}
		});
		}
}
// updates the # chars left
		function update_lengthcounter(a,len,counter){
			var the_len = a;
			var left = (len-the_len);
			if (a<300)
			{
				$('#'+counter).html(left+" characters left");
				//document.getElementById(counter).innerHTML = left+" characters left";
			}
			
			else
			{
			document.getElementById(counter).innerHTML = "Exceeded Characters"+left ;
			}
		}
		

var tagcount = 0;
function addtag(){
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

function largemap(){
		$('#map').height(280);
		$('#id_large').hide();
}


// Third Step(template) , Gallery

<!---- GALLERY	-->
function imageExtension(picField) {
		var imagePath = picField;
		var pathLength = imagePath.length;
		var lastDot = imagePath.lastIndexOf(".");
		var fileType = imagePath.substring(lastDot,pathLength);
		fileType=fileType.toUpperCase()
		if((fileType == ".JPE") || (fileType == ".JPG") || (fileType == ".PNG") || (fileType == ".JPEG") || (fileType == ".BMP")) {
			return true;
		}else{
			alert("We supports .JPG, .PNG, and .BMP image formats.");
			return false;
		}
  }

  function showImageFromComputer() {
    $('#imageFromComputer').css('display', '');
    $('#imageFromUrl').css('display', 'none');
       
  }
  function showImageFromUrl() {
  	$('#imageFromComputer').css('display', 'none');
    $('#imageFromUrl').css('display', '');
  	
  }
 
function load_locality_map(loc_id){

			$("#id_loader").show();
			$.get("/events/getlocality-lat-long/",{ server_loc_id: loc_id }, function(lat_long){
				var lat  = 		String(lat_long.split("$")[0]);
				var longi = 	String(lat_long.split("$")[1]);
				var loc_name = 	String(lat_long.split("$")[2]);
				var zoom = 	parseInt(lat_long.split("$")[3]);
				load(lat, longi, zoom, loc_name, "");	
				//alert(load);
				$("#id_lat").val(lat);
				$("#id_lon").val(longi);
				$("#id_zoom").val(zoom);
				$("#id_loader").hide(lat);
				
			});
} 


function is_ext_supported(element){
	var extensions = new Array("jpg","jpeg","gif","png","bmp");
	var image_file = $(element).val();
	var image_length =  image_file.length;
	var pos = image_file.lastIndexOf('.') + 1;
	var ext = image_file.substring(pos, image_length);
	var final_ext = ext.toLowerCase();
	for (i = 0; i < extensions.length; i++)
	{
	    if(extensions[i] == final_ext)
	    {
			return true;
	    }
	}
	alert("We supports .JPG, .PNG, and .BMP image formats.");
	return false;
}
  
function galleryUpload(id)
		{
			if(!imageExtension(document.getElementById('id_photo').value)){
				return false;
			}
			$("#loading")
			.ajaxStart(function(){
				$("#error_message").empty();
				$("#error_message").hide();
				$(this).show();
			})
			.ajaxComplete(function(){
				$(this).hide();
			});
			$.ajaxFileUpload({
				url:'/events/eventgalleryupload/?eid='+id,
				secureuri:false,
				fileElementId:'id_photo',
				dataType: 'json',
				success: function (data, status)
				{
					
						var now = new Date();
						var imgdiv = window.document.getElementById("id_listGallery");
						var imagetag = "<span class='thumb-container' id='id_span"+data.pid+"'>";
						imagetag +="<a href='' target='_blank' 'title='' style='background:transparent url("+data.event_photo+") no-repeat scroll center center;'></a>";
						imagetag +="<em><a href='javascript:void(0)' onclick='sureToRemove("+data.pid+")' title='Remove'><img src='{{ STATIC_URL }}images/design/icons/over_cross.png'/></a></em>";
						imagetag +="</span>";
						imgdiv.innerHTML += imagetag;
						window.document.getElementById('id_photo').value='';
					
				},
				error: function (data, status, e)
				{
					$("#error_message").show();
					$("#error_message").html(data.responseText);
				}
			})
			//window.location.reload()= false;
			return false;
		}  
function sureToRemove(eid,pid){
	$('#notice_photo').html('');
	if(confirm("Are you sure to delete?")){
		$.get("/events/eventdeleteimage/",{ eid:eid, pid:pid }, function(x){
			if (x=='1'){
				$("#span_"+pid).remove();
				$('#notice_photo').html('Deleted Successfully');
				$('#notice_photo').delay(2000).slideUp(400,function(){
					$('#notice_photo').html('').show();	
				});
				
				}else{
				$('#notice_photo').html('Sorry Encountered an Erroe, Please try after some time');
				$('#notice_photo').delay(2000).slideUp(600);
			}
		});
	}
}

function galleryUrlUpload(id)
		{
			
			var urlvalue=window.document.getElementById('photo_gal_url').value;
			$("#url_loading")
			.ajaxStart(function(){
				$("#error_message").empty();
				$("#error_message").hide();
				$(this).show();
			})
			.ajaxComplete(function(){
				$(this).hide();
			});
			$.ajax({
				type: 'POST',
				url:'/events/eventgalleryurlupload/',
				data: {'vid':id,'url':urlvalue},
				dataType: 'json',
				success: function (data)
				{
					  	var now = new Date();
						var imgdiv = window.document.getElementById("id_listGallery");
						var imagetag = "<span class='thumb-container' id='id_span"+data.pid+"'>";
						imagetag +="<a href='' target='_blank' 'title='' style='background:transparent url("+data.event_photo+") no-repeat scroll center center;'></a>";
						imagetag +="<em><a href='javascript:void(0)' onclick='sureToRemove("+data.pid+")' title='Remove'><img src='{{ STATIC_URL }}images/design/icons/over_cross.png'/></a></em>";
						imagetag +="</span>";
						imgdiv.innerHTML += imagetag;
						//alert(imagetag);
						window.document.getElementById('photo_gal_url').value='';
					
				},
				error: function (data, status, e)
				{
					$("#error_message").show();
					$("#error_message").empty().html(data.responseText);
				}
			})
			//window.location.reload()= false;
			return false;
		}  

function is_ext_supported(element){
	var extensions = new Array("jpg","jpeg","gif","png","bmp");
	var image_file = $(element).val();
	var image_length =  image_file.length;
	var pos = image_file.lastIndexOf('.') + 1;
	var ext = image_file.substring(pos, image_length);
	var final_ext = ext.toLowerCase();
	for (i = 0; i < extensions.length; i++)
	{
	    if(extensions[i] == final_ext)
	    {
			return true;
	    }
	}
	alert("We supports .JPG, .PNG, and .BMP image formats.");
	return false;
}

