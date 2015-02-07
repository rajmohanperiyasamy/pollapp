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
				url:'/classifieds/dashboard/galleryupload/?id='+id,
				secureuri:false,
				fileElementId:'id_photo',
				dataType: 'json',
				success: function (data, status)
				{
						var now = new Date();
						var imgdiv = window.document.getElementById("id_listGallery");
						var imagetag = "<span class='thumb-container' id='id_span"+data.pid+"'>";
						imagetag +="<a href='' target='_blank' 'title='' style='background:transparent url("+data.classified_photo+") no-repeat scroll center center;'></a>";
						imagetag +="<em><a href='javascript:void(0)' onclick='sureToRemove("+data.pid+","+data.cid+")' title='Remove'><img src='{{ STATIC_URL }}images/design/icons/over_cross.png'/></a></em>";
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
	function galleryUrlUpload(id)
		{
			var urlvalue=window.document.getElementById('photo_gal_url').value;
			$("#loading")
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
				url:'/classifieds/dashboard/galleryurlupload/',
				data: {'id':id,'url':urlvalue},
				dataType: 'json',
				success: function (data)
				{
					  	var now = new Date();
						var imgdiv = window.document.getElementById("id_listGallery");
						var imagetag = "<span class='thumb-container' id='id_span"+data.pid+"'>";
						imagetag +="<a href='' target='_blank' 'title='' style='background:transparent url("+data.classified_photo+") no-repeat scroll center center;'></a>";
						imagetag +="<em><a href='javascript:void(0)' onclick='sureToRemove("+data.pid+","+data.cid+")' title='Remove'><img src='{{ STATIC_URL }}images/design/icons/over_cross.png'/></a></em>";
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
	
	function sureToRemove(pid,cid){
		if(confirm("Are you sure to delete?")){
			$.get("/classifieds/dashboard/deleteimage/",{cid:cid,id:pid},function(data){
				if(data==1){$('#id_span'+pid).remove();}
				else{alert('Oops!!! Not able to process your request.');}
			});
		}
		else{
			return false;
		}
	}



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
	
	




