//Ashin code begin
$(document).ready(function(){
	//Respond email code begin
	
	//On calling the respond , making all the fields empty
	$('.respond_clr').click(function(){
		$('#contact_form [type="text"]').val('');
		$('#respond_msg').val('');
		$('.tellfriend input').css('border-color','#069');
		$('.tellfriend textarea').css('border-color','#069');
	});
	
	$('#contact_form [type="text"]').keyup(function(){
		$(this).css('border-color','#069');
	});
	$('.tellfriend textarea').keyup(function(){
		$(this).css('border-color','#069');
	});
	
	//Assigning the "#contact_hashkey" hidden input box with the comment hash key value only at the first loading of the page  
	$('#contact_hashkey').val($('#id_hashkey').val());
	
	$('.respond_submit').click(function(){
		$('.tellfriend input').css('border-color','green');
		$('.tellfriend textarea').css('border-color','green');
	});
	$("#contact_form").submit(function(event){
		event.preventDefault();
		var clfds_contact_form = true;
		
		//validate all the text boxes
		$("#contact_form [type = 'text']").each(function(i) {
		
			var val = $(this).val();
			var str = jQuery.trim(val);
			if (str.length == 0) {
				$(this).css('border-color','red').focus();
				clfds_contact_form = false;
			}
			else{
				$(this).css('border-color','green');
			}
			
			if($(this).attr('name') == 'respond_email'){
				if (!(/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test($(this).val()))) {
					$(this).css('border-color','red').focus();
					clfds_contact_form = false;
				}
				else{
					$(this).css('border-color','green');
				}
			}
		
		});
		
		//validate the message box
		var val = $('#respond_msg').val();
		var str = jQuery.trim(val);
		
		if (str.length == 0){
			$('#respond_msg').css('border-color','red').focus();
			clfds_contact_form = false;
		}
		else{
			$('#respond_msg').css('border-color','green');
		}
		
		if(clfds_contact_form){
			//Data sending to the server
			var postdata = "respond_name=" + $('#respond_name').val();
			postdata += '&respond_email=' + $('#respond_email').val();
			postdata += '&respond_msg=' + $('#respond_msg').val();
			postdata += '&respond_phone=' + $('#respond_phone').val();
			//postdata += '&Captcha_value=' + $('#contact_captcha_value').val();
			//postdata += '&hash-key=' + $('#contact_hashkey').val();
			postdata += '&cid=' + $('#clsf_id').val();
			
			//On submit , hiding the submit button & showing the status msg
			$('.respond_submit').hide();
			$('#contactstatus').removeAttr('class').addClass('msg_sending').text('Message sending , please wait...');
			$('#contactstatus').show();
			
			//Ajax 
			$.ajax({
				type: "POST",
				url: "/classifieds/a/contact/",
				dataType: 'json',
				data: postdata,
				success: function(html_from_server){
				
					//Assiging the new hash key to the hidden field "#contact_hashkey"
					$('#contact_hashkey').val(html_from_server.hash);
					
					if (html_from_server.success == "1") {
					
						//If success then staus msg in green
						$('#contactstatus').removeAttr('class').addClass('flash_success_alert').text('Thank You!! Your message has been sent.');
						
						//Clearing all the input fields
						$('#contact_form [type="text"]').val('');
						$('.tellfriend textarea').val('');
						$('.tellfriend input').css('border-color', '#069');
						$('.tellfriend textarea').css('border-color', '#069');
						
						//Closing lightbox,loading new captcha image,removing status msg,showing submit button
						window.setTimeout("$('#contactstatus').fadeOut(300)", 4000);
						window.setTimeout("hide_lightbox()", 5000);
						window.setTimeout("$('.respond_submit').show();", 6000);
						//$('#contact_catcha_img').attr('src', '/site_media/images/captcha/' + html_from_server.image).load();
					}
					else 
						if (html_from_server.success == "0") {
							$('#contactstatus').removeAttr('class').addClass('flash_error_alert');
							//$('#Captcha_value').val('');
							
							//if error then showing status msg in red
							//if wrong image key inside if or inside else loop
							if (html_from_server.captcha == "0") {
								$('#contactstatus').text('Wrong Image key! Please re-enter the text in the image');
								$('#Captcha_value').css('border-color', 'red').focus();
							}
							else {
								$('#contactstatus').text('Sorry, we were unable to send this message, please try again later.');
							}
							//removing status msg,show submit,load new captch image
							window.setTimeout("$('#contactstatus').fadeOut(300)", 3000);
							window.setTimeout("$('.respond_submit').fadeIn(300);", 4000);
							//$('#contact_catcha_img').attr('src', '/site_media/images/captcha/' + html_from_server.image).load();
						}
					}
				});
			   }
			});
//Respond email code end


});

//Integrate map and respond to in the lightbox code begin
function show_content(id){
	$('.allhide').hide();
	$('#'+id).show();
	lightbox();
	if (id == 'map' ){
		load_accdn_map();
	}
}
//Integrate map and respond to in the lightbox code end


//Ashin code end

//Shahanar

function ajax_comment()
{
		var dataString = 'hashkey=' + $('#id_hashkey').val() + '&id=' + $('#id_classified').val();
		if ($('#id_hashvalue').val() != '') {
			dataString += '&hashvalue=' + $('#id_hashvalue').val();
		}
		if($('#id_comment').val()!=''){
			dataString += '&comment=' + $('#id_comment').val();
		}
		if ($('#id_name').val() != '') {
			dataString += '&name=' + $('#id_name').val();
		}
		if($('#id_email').val()!=''){
			dataString += '&email=' + $('#id_email').val();
		}
		$('.as_comment_loading').html('<img src="/site_media/themes/green/images/global/comment-loader.gif" alt="Posting Comment.."/>');
		$.ajax({
			type: "POST",
			url: $('#frmAddComment').attr('action'),
			data: dataString,
			success: function(html_from_server){
				$('#frmAddComment').hide();
				$('#respond').empty().html(html_from_server);
				$('#id_hashvalue').val('');
				$('#frmAddComment').fadeIn(300)
			}
		});
}

//ajax code for like comment
function like_comment(commentid){
	$.ajax({
		type: "GET",
		url: "/classifieds/ajaxlikecomment/?cid="+commentid,
		data: "c=a",
		success: function(html_from_server){
			$('#id_like_comment_'+commentid).remove();
			$('#id_like_abuse_comment'+commentid).prepend('<span class="liked">You liked this</span>');
		}
	});
}

//ajax code for abuse comment
function abuse_comment(commentid){
	$.ajax({
		type: "GET",
		url: "/classifieds/ajaxabusecomment/?cid="+commentid,
		data: "c=a",
		success: function(html_from_server){
			$('#id_abuse_comment_'+commentid).remove();
			$('#id_like_abuse_comment'+commentid).append('<span class="abuse_reported">Reported</span>');
		}
	});
}    

function setVal(val){
	form = window.document.getElementById('attr_search')
	window.document.getElementById('id_attrval').value = val
	form.submit(); 
}
