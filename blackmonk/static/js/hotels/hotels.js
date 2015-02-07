$(document).ready(function(){

//Small photo gallery hotels
$('.hotel_img_thumb').click(function(){
		$('.hotel_img_thumb').parent().removeClass('selected');
		$('.loader_16').show();
		$("#full_imgs").animate({
					opacity:'0.5'
					},300);
		$(this).parent().addClass('selected');
		var img_src = $(this).attr('src');
		var full_img_src = $(this).attr('datasrc');

		/*if ($('#call_from').val() == 're_property_detail') {
			var full_img_src = img_src.replace("t.jpg", "b.jpg");
		}
		else {
			var full_img_src = img_src.replace("t.jpg", "b.jpg");
		}*/

		$("#full_imgs").attr("src", full_img_src).load(function(){
					$('.loader_16').hide();
					$("#full_imgs").animate({
					opacity:'1'
					},300,function(){
						$("#full_imgs").stop();
					});				
		});
		
	});
//Small photo gallery hotels ending

//hotel detail page tab content code

$('#id_hotel_tabs_ul li a,#id_more_photos a').click(function(){
	if(!$(this).closest('h2').hasClass('selected')){
		$('#id_hotel_tabs_ul li h2').removeClass('selected');
		$(this).closest('h2').addClass('selected');
	}
	
	if($(this).hasClass('bm_dev_more_photos')){
		$('#id_hotel_tabs_ul li h2').removeClass('selected');
		$('#id_h2_photos').addClass('selected');
	}
	
	var show_div_id = $(this).attr('id');
	$('.bm_dev_hotel_content').hide();
	$('#'+show_div_id+'_content').fadeIn('slow');
	try{initialize();}
	catch(e){}
	
});
//hotel detail page tab content code ends

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
			postdata += '&Captcha_value=' + $('#contact_Captcha_value').val();
			postdata += '&hash-key=' + $('#contact_hashkey').val();
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
					$('#contact_hashkey').val(html_from_server.hash);
					
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
						$('#contact_catcha_img').attr('src', '/site_media/images/captcha/' + html_from_server.image).load();
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
							$('#contact_catcha_img').attr('src', '/site_media/images/captcha/' + html_from_server.image).load();
						}
				}
			});
		}
	});
	//Respond email code end

});

function content_slide_more_less(first_div,second_div){
if($('#'+second_div).is(':hidden')){
	$('#'+first_div).hide();
	$('#'+second_div).show();
}
else{
	$('#'+second_div).hide();
	$('#'+first_div).show();
}
}

function show_room_amenities(id){

if($('#id_amenity_expand'+id).html()=='[+] Room Amenities'){
	$('#id_amenity_expand'+id).html(gettext('[-] Room Amenities'));
	$('#id_amenity_list'+id).fadeIn('slow');
}
else{
	$('#id_amenity_expand'+id).html(gettext('[+] Room Amenities'));
	$('#id_amenity_list'+id).fadeOut('slow');
	//$('#id_amenity_list'+id).hide();

}

}


