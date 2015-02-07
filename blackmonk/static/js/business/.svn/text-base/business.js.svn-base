$(document).ready(function(){
	
	//synopsis begin
	
	//Description expanding and contracting begin
	var str_len = $('#as_bs_synopsis').text().length;
	if(str_len<1140){
		$('#as_bs_synopsis').css('height','100%');
		$('.as_bs_toggle').remove();
	}
	//Expanding and Contracting "Synopsis" 
	$('a.as_bs_toggle').click(function(){
		var hgt=$('#as_bs_synopsis').css('height');		
		$('#as_bs_synopsis').css('overflow','hidden');
		$('#as_bs_synopsis').css('height','100%');
		var syp_hgt=$('#as_bs_synopsis').height();
		$('#as_bs_synopsis').css('height',hgt);
		$('#as_bs_synopsis').css('overflow','visible');		
		
		if(hgt=="301px"){
			$('#as_bs_synopsis').animate({
				'height': syp_hgt+'px'
			},300,function(){
				$('a.as_bs_toggle').empty().html('(see less)');
			});
		}
		else{
			$('#as_bs_synopsis').animate({
				'height':'301px'
			},300,function(){
				$('a.as_bs_toggle').empty().html('(see more)');
			});
			$('html, body').animate({scrollTop:$('#as_desc').offset().top-50}, 300);			
		}
		
	});

//Free listing Description expanding and contracting end

	//Description expanding and contracting begin
	var str_len = $('#as_bs_fl_synopsis').text().length;
	if(str_len<690){
		$('#as_bs_fl_synopsis').css('height','100%');
		$('.as_bs_fl_toggle').remove();
	}
	//Expanding and Contracting "Synopsis" 
	$('a.as_bs_fl_toggle').click(function(){
		var hgt=$('#as_bs_fl_synopsis').css('height');		
		$('#as_bs_fl_synopsis').css('overflow','hidden');
		$('#as_bs_fl_synopsis').css('height','100%');
		var syp_hgt=$('#as_bs_fl_synopsis').height();
		$('#as_bs_fl_synopsis').css('height',hgt);
		$('#as_bs_fl_synopsis').css('overflow','visible');		
		
		if(hgt=="110px"){
			$('#as_bs_fl_synopsis').animate({
				'height': syp_hgt+'px'
			},300,function(){
				$('a.as_bs_fl_toggle').empty().html('(see less)');
			});
		}
		else{
			$('#as_bs_fl_synopsis').animate({
				'height':'110px'
			},300,function(){
				$('a.as_bs_fl_toggle').empty().html('(see more)');
			});
		}
		
	});

//Description expanding and contracting end
	
	//synopsis end
	
	//Business photo Gallery begin
	
	//Loading the full image when clicking on any img on the thumbnail view
	$('#slider_thumb li a').click(function(event){
		event.preventDefault();
		$('#slider_thumb li a').removeClass('selected');			
		$(this).addClass('selected');
		$('li').removeClass('active_li');
		$(this).parent('li').addClass('active_li');
		var imsrc= $('li.active_li a img').attr('datasrc');		
		load_fullimg(imsrc);
	});
	
	//Loading the full image on clicking navigation button	
	$('#top_prev,#top_next').click(function(event){
			event.preventDefault();
			var id=$(this).attr('id');																
			move_img(id);
			var imsrc= $('li.active_li a img').attr('datasrc');
			load_fullimg(imsrc);	
	});
	
	//function to make the active thumbnail img to "selected" and li to "active_li"	
	function move_img(id_nav){
		$('li.active_li').addClass('p')				
		if (id_nav == "top_next") {
			if($("li.active_li").hasClass("last_li")){
					$('div.panel:first li:first').addClass('active_li')
					stepcarousel.stepBy('galleryc', 1)
			}
			
			else if ($("li.active_li").hasClass("div_lst_li")) {
				$("li.active_li").parent("div").next("div").children("li:first").addClass('active_li')
				stepcarousel.stepBy('galleryc', 1)	
			}
			
			else {
				$('li.active_li').next().addClass('active_li')
			}		
		}
		if (id_nav == "top_prev") {
			if($("li.active_li").hasClass("first_li")){
					$('div.panel:last li:last').addClass('active_li')
					stepcarousel.stepBy('galleryc', -1)
			}
			
			else if($("li.active_li").hasClass("div_fst_li") || $("li.active_li").attr('id')=="div_fst_li" ) {
				$("li.active_li").parent("div").prev("div").children("li:last").addClass('active_li')
				stepcarousel.stepBy('galleryc', -1)
				
			}
			else {
				$('li.active_li').prev().addClass('active_li')
			}
		}
		$('li.p').removeClass('active_li')
		$('li.p a').removeClass('selected')
		$('li.active_li a').addClass('selected');
		$('li').removeClass('p')
	}	
			
	//function which shows the downloading gif and loads the full size img
	function load_fullimg(imsrc){
		$('#as_load_hack').val('yes');
		$('.loader_32').show();
		$("#full_img").attr("src", imsrc).load(function(){
					load_callback();			
		});
	}
	
	//hack to prevent the load callback function not to execute more than once
	function load_callback(){
		var exec = $('#as_load_hack').val();
		if (exec == 'yes'){
			$('.loader_32').hide();
			$('#as_load_hack').val('no');
		}	
	}
		
	
	
	//Business photo Gallery end
	
	//sms begin
	$('.as_sms_submit').click(function(){
		var title = $('#as_business_name').text();
		var addr = $('#as_business_addr').text();
		var as_business_numbers = $('#as_business_numbers').text();
		var number = $('#to_number').val();
		var msg = "Business:"+title+"\nAddress:"+addr+"\nPhone/mob:"+as_business_numbers;
		var module_id  = $('#as_module_id').val();
		send_sms(msg,number,module_id);
	})
	//sms end
	
	//Respond email code begin
	
	//On calling the respond , making all the fields empty
	$('.contact_form_clr').click(function(){
		$('#contact_form [type="text"]').val('');
		$('#respond_msg').val('');
		$('.tellfriend input').css('border-color', '#069');
		$('.tellfriend textarea').css('border-color', '#069');
	});
	
	$('#contact_form [type="text"]').keyup(function(){
		$(this).css('border-color', '#069');
	});
	$('.tellfriend textarea').keyup(function(){
		$(this).css('border-color', '#069');
	});
	$('#respond_phone').keyup(function(){
		$('#respond_email').css('border-color', '#069');
	});
	$('#respond_email').keyup(function(){
		$('#respond_phone').css('border-color', '#069');
	});
	
	
	//Assigning the "#contact_hashkey" hidden input box with the comment hash key value only at the first loading of the page  
	$('#contact_hashkey').val($('#id_hashkey').val());
	
	$('.respond_submit').click(function(){
		$('.tellfriend input').css('border-color', 'green');
		$('.tellfriend textarea').css('border-color', 'green');
	});
	
	$("#contact_form").submit(function(event){
		event.preventDefault();
		var business_contact_form = true;
		
		//validate all the text boxes
		$("#contact_form [type = 'text']").each(function(i) {
		
			var val = $(this).val();
			var str = jQuery.trim(val);
			if (str.length == 0) {
				$(this).css('border-color','red').focus();
				business_contact_form = false;
			}
			else{
				$(this).css('border-color','green');
			}
			
			
			if($(this).attr('name') == 'respond_email'){
				if (!(/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test($(this).val()))) {
					$(this).css('border-color','red').focus();
					business_contact_form = false;
				}
				else{
					$(this).css('border-color','green');
				}
			}
		
		});
		
		//validate phone number
		var number = $("#respond_phone").val();
		var str = jQuery.trim(number);
		if (str.length == 0) {
			$("#respond_phone").css('border-color', 'red').focus();
		}
		else {
			if (isNaN($("#respond_phone").val()) || number.search(/\.+/) != -1) {
				$("#respond_phone").css('border-color', 'red').focus();
				business_contact_form = false;
			}
			else {
				$("#respond_phone").css('border-color', 'green');
			}
		}
		
		//validate the message box
		var val = $('#respond_msg').val();
		var str = jQuery.trim(val);
		
		if (str.length == 0){
			$('#respond_msg').css('border-color','red').focus();
			business_contact_form = false;
		}
		else{
			$('#respond_msg').css('border-color','green');
		}
		
		if (business_contact_form) {
		
			//Data sending to the server
			var postdata = "name=" + $('#respond_name').val();
			postdata += '&phone=' + $('#respond_phone').val();
			postdata += '&email=' + $('#respond_email').val();
			postdata += '&subject=' + $('#respond_sunject').val();
			postdata += '&comment=' + $('#respond_msg').val();
			//postdata += '&Captcha_value=' + $('#contact_Captcha_value').val();
			//postdata += '&hash-key=' + $('#contact_hashkey').val();
			//postdata += '&recaptcha_response_field='+$('#recaptcha_response_field').val();
			//postdata += '&recaptcha_challenge_field='+$('#recaptcha_challenge_field').val();
			postdata += '&bid=' + $('#clsf_id').val();
			
			//On submit , hiding the submit button & showing the status msg
			$('.respond_submit').hide();
			$('#contactrespond_status').removeAttr('class').addClass('msg_sending').text('Message sending , please wait...');
			$('#contactrespond_status').show();
			
			//Ajax 
			$.ajax({
				type: "POST",
				url: "/business/a/contactus/",
				dataType: 'json',
				data: postdata,
				success: function(html_from_server){
					//Assiging the new hash key to the hidden field "#contact_hashkey"
					//$('#contact_hashkey').val(html_from_server.hash);
					//Recaptcha.reload();
					if (html_from_server.success == "1") {
						//If success then staus msg in green
						$('#contactrespond_status').removeAttr('class').addClass('flash_success_alert').text('Thank You!! Your message has been sent.');
						
						//Clearing all the input fields
						$('#contact_form [type="text"]').val('');
						$('.tellfriend textarea').val('');
						$('.tellfriend input').css('border-color', '#069');
						$('.tellfriend textarea').css('border-color', '#069');
						
						//Closing lightbox,loading new captcha image,removing status msg,showing submit button
						window.setTimeout("$('#contactrespond_status').fadeOut(300)", 4000);
						window.setTimeout("hide_lightbox()", 5000);
						window.setTimeout("$('.respond_submit').show();", 6000);
						//$('#contact_catcha_img').attr('src', '/site_media/images/captcha/' + html_from_server.image).load();
					}
					else 
						if (html_from_server.success == "0") {
							$('#contactrespond_status').removeAttr('class').addClass('flash_error_alert');
							$('#Captcha_value').val('');
							
							//if error then showing status msg in red
							//if wrong image key inside if or inside else loop
							if (html_from_server.captcha == "0") {
								$('#contactrespond_status').text('Wrong Image key! Please re-enter the text in the image');
								$('#Captcha_value').css('border-color', 'red').focus();
							}
							else {
								$('#contactrespond_status').text('Sorry, we were unable to send this message, please try again later.');
							}
							//removing status msg,show submit,load new captch image
							window.setTimeout("$('#contactrespond_status').fadeOut(300)", 3000);
							window.setTimeout("$('.respond_submit').fadeIn(300);", 4000);
							//$('#contact_catcha_img').attr('src', '/site_media/images/captcha/' + html_from_server.image).load();
						}
				}
			});
		}
	});
	//Respond email code end
	
});

if(typeof String.prototype.trim !== 'function') {
	  String.prototype.trim = function() {
	    return this.replace(/^\s+|\s+$/g, ''); 
	  }
}

function like_comment(commentid){
		$.ajax({
			type: "GET",
			url: "/business/a/likecomment/?cid="+commentid,
			data: "c=a",
			success: function(html_from_server){
				$('#id_like_comment_'+commentid).remove();
				$('#id_like_abuse_comment'+commentid).prepend('<span class="liked">You liked this</span>');
			}
		});
	}
	function abuse_comment(commentid){
		$.ajax({
			type: "GET",
			url: "/business/a/abusecomment/?cid="+commentid,
			data: "c=a",
			success: function(html_from_server){
				$('#id_abuse_comment_'+commentid).remove();
				$('#id_like_abuse_comment'+commentid).append('<span class="abuse_reported">Reported</span>');
			}
		});
	}
	
	
	
	
function addstaffAddress(status){
	
	var bid = $("#id_bid").val();
	var address1 = $("#id_address1").val().trim();
	var address2 = $("#id_address2").val().trim();
	var pin = $("#id_pin").val().trim();
	var locality = $("#id_locality").val().trim();
	var city= $("#id_city").val().trim();
	var telephone = $("#id_telephone").val().trim();
	var telephone1 = $("#id_telephone1").val().trim();
	var mobile_no = $("#id_mobile_no").val().trim();
	var fax = $("#id_fax").val().trim();
	var email = $("#id_email").val().trim();
	var website= $("#id_website").val().trim();
	var h_aid = $("#id_h_aid").val().trim();
	
	var error = false
	
	if (!address1.length){
		$("#id_address1").addClass("error");
		alert("Please Enter Address");
		error = true;
	}else{
		$("#id_address1").removeClass("error");
	}
	
	if (!pin.length){
		$("#id_pin").addClass("error");
		alert("Please Enter Pin");
		error = true;
	}else{
		$("#id_pin").removeClass("error");
	}
	
	if (!locality.length){
		$("#id_locality").addClass("error");
		alert("Please Select Locality");
		error = true;
	}else{
		$("#id_locality").removeClass("error");
	}
	
	if (error){
		return false;
	}
	
	
   	var lat_lng = marker.getPoint();
	var zoom = map.getZoom();
	jQuery('#top_pre_map').show();
	
	data = {bid:bid, address1:address1, address2:address2, pin:pin, locality:locality, city:city, telephone:telephone, telephone1:telephone1, mobile_no:mobile_no, fax:fax, email:email, website:website, lat_lng:lat_lng, zoom:zoom, h_aid:h_aid, csrfmiddlewaretoken : $('input[name=csrfmiddlewaretoken]').val() }
	
	$("#id_save").hide();
	$("#loading_ajax").show();
	$.post('/staff/business/addsaddress/',data ,function(data){
		
			$('#address_info').empty().html(data)
			$("#add_address").hide();
			clear_fields();
			$("#loading_ajax").hide();
			$("#addnewlocation").show();	
			$("#id_save").show();
	});
		

	}




function adduserAddress(status){
	
	var bid = $("#id_bid").val();
	var address1 = $("#id_address1").val().trim();
	var address2 = $("#id_address2").val().trim();
	var pin = $("#id_pin").val().trim();
	var locality = $("#id_locality").val().trim();
	var city= $("#id_city").val().trim();
	var telephone = $("#id_telephone").val().trim();
	var telephone1 = $("#id_telephone1").val().trim();
	var mobile_no = $("#id_mobile_no").val().trim();
	var fax = $("#id_fax").val().trim();
	var email = $("#id_email").val().trim();
	var website= $("#id_website").val().trim();
	var h_aid = $("#id_h_aid").val().trim();
	var error = false
	
	if (!address1.length){
		$("#id_address1").addClass("error");
		alert("Please Enter Address");
		error = true;
	}else{
		$("#id_address1").removeClass("error");
	}
	
	if (!pin.length){
		$("#id_pin").addClass("error");
		alert("Please Enter Pin");
		error = true;
	}else{
		$("#id_pin").removeClass("error");
	}
	
	if (!locality.length){
		$("#id_locality").addClass("error");
		alert("Please Select Locality");
		error = true;
	}else{
		$("#id_locality").removeClass("error");
	}
	
	if (error){
		return false;
	}
	
	
   	var lat_lng = marker.getPoint();
	var zoom = map.getZoom();
	jQuery('#top_pre_map').show();
	
	data = {bid:bid, address1:address1, address2:address2, pin:pin, locality:locality, city:city, telephone:telephone, telephone1:telephone1, mobile_no:mobile_no, fax:fax, email:email, website:website, lat_lng:lat_lng, zoom:zoom, h_aid:h_aid, csrfmiddlewaretoken : $('input[name=csrfmiddlewaretoken]').val() }
	
	
	$("#id_save").hide();
	$("#loading_ajax").show();
	$.post('/business/b/addsaddress/',data ,function(data){
		$('#address_info').empty().html(data)
		$("#add_address").hide();
		clear_fields();
		$("#loading_ajax").hide();
		$("#addnewlocation").show();
		$("#id_save").show();
	});
		

	}