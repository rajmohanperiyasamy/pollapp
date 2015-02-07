$(document).ready(function(){
	//$.preloadCssImages();
	$('.call_feedback').click(function(){
			hide_feedback();
	});
	
	//Feed back code
	$('#user_feedback').click(function(){
		show_fb_content('feedback_div');
	});
	
	$('.user_feedback_clr').click(function(){
		$('#fdbk_form [type="text"]').val('');
		$('#fdbk_msg').val('');
		$('#fdbk_form input').css('border-color','#069');
		$('#fdbk_form textarea').css('border-color','#069');
		$('.fdbk_radio').each(function(){
			$(this).attr('checked', false);
		});
		$('#fdbk_form label').css('color','#3D3D3D');
		$('#fdbk_radio').val('no'); 
		$('#fdbk_option').attr('selected','selected');
	});
	$('html').ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
        // Only send the token to relative URLs i.e. locally.
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});
	
	$('#fdbk_form').submit(function(event){
		event.preventDefault();
		var submit = true;
		var exec = $('#execute_text').val();
		
		$("#fdbk_form [type = 'text']").each(function(i) {
			
			var val = $(this).val();
			var str = jQuery.trim(val);
			if (str.length == 0) {
				$(this).css('border-color','red');
				submit = false;
			}
			else{
				$(this).css('border-color','green');
			}
			
			
			if($(this).attr('name') == 'fdbk_to_email'){
				if (!(/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test($(this).val()))) {
					$(this).css('border-color','red');
					submit = false;
				}
				else{
					$(this).css('border-color','green');
				}
			}
			
		});
		
		var val = $('#fdbk_msg').val();
		var str = jQuery.trim(val);
		
		if (str.length == 0){
			$('#fdbk_msg').css('border-color','red');
			submit = false;
		}
		else{
			$('#fdbk_msg').css('border-color','green');
		}
		
		$('.fdbk_radio').each(function(){
			 if($(this).is(':checked')){
				$('#fdbk_radio').val('ok');
				type = $(this).val();
				$('#fdbk_type').css('color','#3D3D3D'); 
			 }
			 else if($('#fdbk_radio').val() == 'no'){
			 	$('#fdbk_type').css('color','red');
			 }
		});
		
		if($('#fdbk_radio').val() == 'no'){
			submit = false;
		}
		
		var selected = $('#fdbk_select').val();
		if(selected == 'deafult'){
			$('#fdbk_select_lbl').css('color','red');
			submit = false;
		}
		else if(selected != 'deafult'){
			$('#fdbk_select_lbl').css('color','#3D3D3D');
		}

		if(submit && $('#fdbk_radio').val() == 'ok'){
			$('.fdbk_submit').hide();
			$('#fdbk_status').removeAttr('class').addClass('msg_sending').text('Message sending , please wait...');
			var fdbk_send = setTimeout("$('#fdbk_status').removeAttr('class').addClass('flash_success_alert').text('Thanks for your feedback !!')",3000);
			setTimeout("feedback()",5000);
			setTimeout("$('.fdbk_submit').show();$('#fdbk_status').removeAttr('class').text('');",6000);
			
			var postdata = 'fdbk_name='+$('#fdbk_name').val();
			postdata += "&fdbk_to_email="+$('#fdbk_to_email').val();
			postdata += "&type="+type; 
			postdata += "&topic="+$('#fdbk_select').val();
			postdata += "&fdbk_msg="+$('#fdbk_msg').val();
			
			$.ajax({
				type: "POST",
				url: '/feedback/',
				data: postdata,
				
				success:function(success){
					//alert(success)
				}
			});
		}
	});
	
	
	//Feed back code end 
	
	//On pressing excape close lightbox
	$(document).keypress(function(e) { 
		if (e == null) { // ie
			keycode = event.keyCode;
		}
		else { // mozilla
			keycode = e.which;
		}
		if (keycode == 27) { // escape, close box
			if ($('.feedback_content_holder').css('display') != 'none') {
				hide_feedback();
			}
		}
	});
	
});
		
function feedback(){
	//Checking the display property of the lightbox and showing or hiding it based on it
	var disp = $('.feedback_content_holder').css('display');
	if (disp == "none") {
		show_feedback();
	}
	else if (disp == "block") {
			hide_feedback();
		}
}

function show_fb_content(content){
	$('.allhide').hide();
	if ($.browser.msie && $.browser.version == 6.0) {
		$('.lightbox_content_holder #map').html('');
	}
	$('#'+content).show();
	feedback();
}

function show_feedback(){
	
		//$('.display_ad,.video_in,#industy').hide();
	    //Setting the lightbox background in full window top of all other elements
		var hght = $(document).height();
		var width = $(document).width();

		$('.feedback_background').css('width', width);
		$('.feedback_background').css('height', hght);
		
		//Making the lightbox center
		$('.feedback_content_holder').show();
		if ($.browser.msie) {
			var lb_width = $('.feedback_content_holder').width();
			var lb_hgt = $('.feedback_content_holder').height();
		}
		else {
			var div_width = $('.feedback_content_holder').css('width');
			var div_hght = $('.feedback_content_holder').css('height');
			var lb_width = div_width.replace("px","")
			var lb_hgt = div_hght.replace("px","")
		}
		
		var half_lb_width = lb_width/2;
		var mgnLeft = '-'+half_lb_width+'px';
		var half_lb_hght = lb_hgt/2;
		var mgnTop = '-'+half_lb_hght+'px';
		$('.feedback_content_holder').css({
			'margin-left':mgnLeft,
			'margin-top':mgnTop,
			'display':'none'
			});
		$('.feedback_outer').css('visibility','visible');
		$('.feedback_background').show();
		
		$('.feedback_content_holder').show('slow');
	
}

function hide_feedback(){
		
		try{
			feedback_restore();
		}
		catch(e){}
		
		//$('.display_ad,.video_in,#industy').show();

	//Effects Use the one which u like, always keep only one uncommented
		$('.feedback_content_holder').hide('slow');

		$('.feedback_background').hide();
}


function submit_feedback(submit){
	if(submit == false){
		alert('last')
		event.preventDefault();
	}
}


function newsletter_form_validate()
{
	var success=true;
	var filter = /^([a-zA-Z0-9_.-])+@(([a-zA-Z0-9-])+.)+([a-zA-Z0-9]{2,4})+$/;
	
	if($("#id_nl_number").val().length>1){
		if(isNaN($("#id_nl_number").val())){
			$('#id_nl_number').css("border", "2px solid #e33100");
			success=false;
		}
		else{
			$('#id_nl_number').css("border", "2px solid #069"); 
		}
	}
	else{
		$('#id_nl_number').css("border", "2px solid #069"); 
	}
	
	
	if($.trim($('#id_nl_email').val())==''){
		$('#id_nl_email').css("border", "2px solid #e33100");
		success=false;
	}
	else if(!filter.test($.trim($('#id_nl_email').val()))){
			$('#id_nl_email').css("border", "2px solid #e33100");
		    success=false;
		}
	else{
		$('#id_nl_email').css("border", "2px solid #069"); 
	}	
	
	if(success){
		$('#id_nl_submit').hide();
		$('#nl_respond_status').removeAttr('class').addClass('msg_sending').text('Saving , please wait...').show();
		$.get('/alert/subscription/',{ phone: $("#id_nl_number").val() , email :  $("#id_nl_email").val()}
		, function(response_msg){
			if(response_msg == '1'){
				$('#nl_respond_status').removeAttr('class').addClass('flash_success_alert').text('Thank you! Saved successfully');
				setTimeout("restore_news_letter()",5000);
			}
			else if(response_msg == '2'){
				$('#nl_respond_status').removeAttr('class').addClass('flash_error_alert').text('Subcription are already made for these details');
				setTimeout("$('#nl_respond_status').hide();$('#id_nl_submit').show();",5000);
			}
			else{
				$('#news_letter_status').removeAttr('class').addClass('flash_error_alert').text('Unable to save your details.Please try again later.');
				setTimeout("$('#nl_respond_status').hide();$('#id_nl_submit').show();",5000);
			}
		});
	}
	
}

function restore_news_letter(){
	$('#nl_respond_status').removeAttr('class').text('');
	$("#id_nl_number").val('');
	$("#id_nl_email").val('');
	$('#id_nl_submit').show();
	hide_feedback();
}