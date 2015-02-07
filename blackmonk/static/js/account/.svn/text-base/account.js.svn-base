$(document).ready(function() {

setTimeout("$('.flash_success_alert').fadeOut(300)",5000);

$("#cancel_button").click(function() {
	location.href='/accounts/profile/'
});

$('.as_click_pvnt').click(function(event){
	event.preventDefault();
});

//disabling the location
if($('#not_in_city').is(':checked')){
		$('#locality').attr('disabled','disabled').css('color','#bbb');
}

$('#not_in_city').change(function(){
	if($('#not_in_city').is(':checked')){
		$('#locality').attr('disabled','disabled').css('color','#bbb');
	}
	else{
		$('#locality').removeAttr('disabled').css('color','');
	}
});

//Account page validation
$("#basicInformation").submit(function(){
	remove_error();
});

$("#basicInformation").validate({
		rules: {
		email: {
			required: true,
			email: true
		}
	},
	errorPlacement: function(error, element){
		$(element).addClass('error');
	
	},
	 submitHandler: function(form) {form.submit();}
});

//profile page validation
$('.as_remove_empty').click(function(){
	show_tip_url(this);
	fill_username(this);
});

$('.as_remove_empty').keyup(function(){
	fill_username(this);
});

$('#required_info').submit(function(){
	remove_error();
	
	$('.as_remove_empty').each(function(){
		if($(this).val()== ''){
			$(this).removeAttr('name');
		}
	});	
});

$('#website').click(function(){
	if ($('#website').val().length < 8){
		$('#website').val('http://');				
	}
});

$('#website').blur(function(){
	if($('#website').val() == 'http://'){
		$('#website').val('');
	}	
});

$("#required_info").validate({
		onkeyup: false,
		focusInvalid : true,
		rules: {
			display_name: {
				required: true
			},
			email: {
				required: true,
				email: true
			},
			website: {
				required: false,
				url: true
			},
			pin: {
				required: false
			},
			phone: {
				required: false
			},
			mobile: {
				required: false
			},
			},			
			errorPlacement: function(error, element){
				$(element).addClass('error');
			    
			},
			submitHandler: function(form){form.submit();}
});

//Add more links
var link_initial=parseInt($('#as_link_initial').val());
var link_max=parseInt($('#as_link_max').val());
$('#add_link').click(function(){
	link_initial += 1;
	if (link_initial < link_max+1) {
		$('.as_link_tip').remove();
		var clone_obj = '<div class="profile_link"><select class="selectField xsmall" onchange="call_ap_fn(this)"><option value="twitter" selected ="selected">Twitter</option><option value="facebook">Facebook</option><option value="linkedin">LinkedIn</option><option value="google">Google</option></select> <input type="text" value="" onkeyup = "fill_username(this)" onclick = "show_tip_url(this)" name="twitter" class="textField small as_remove_empty" ><br /><span class="tip display_url as_disp_none">http://twitter.com/<span class="tip_username">username</span></span></div><span class="tip as_link_tip">If you use social network profiles , you can link to your account from your profile.</span>'
		$(clone_obj).appendTo('.profile_links');
	}
	if(link_initial==link_max){
		$('#add_link').remove();
	}
});

$('.as_change').change(function(){
	change_tip_url(this);
	add_name(this);
});

//Add more screen name
var screen_initial=parseInt($('#as_screen_initial').val());
var screen_max=parseInt($('#as_screen_max').val());
$('#add_screen').click(function(){
	screen_initial += 1;
	if (screen_initial < screen_max+1) {
		var clone_obj = '<div class="screen_name"><select class="selectField xsmall" onchange="add_name(this)"><option value="aim"  selected="selected">AIM</option><option value="gtalk">G - Talk</option><option value="skype">Skype</option><option value="msn_msgr">Windows Live</option><option value="ymsgr">Yahoo</option></select> <input type="text" name="aim" value="" class="textField small as_remove_empty"></div>'
		$(clone_obj).appendTo('.screen_names');
	}
	if(screen_initial==screen_max){
		$('#add_screen').remove();
	}
});

});

//Add more screen or links
function call_ap_fn(element){
	change_tip_url(element);
	add_name(element);
}

function add_name(element){
	var val = $(element).val();
	$(element).parent().children('input').attr('name',val);
	$(element).removeAttr('name');
}

function change_tip_url(element){
	var username = $(element).parent().children('input').val();
	if(username == ''){
		username = 'username'
	}
	var val = $(element).val();
	if(val == 'facebook' || val == 'flickr' || val == 'twitter' ){
		html = 'http://'+val+'.com/<span class="tip_username">'+username+'</span>';
	}
	else if(val == 'linkedin'){
		html = 'http://linkedin.com/in/<span class="tip_username">'+username+'</span>';
	}
	else if(val == 'google'){
		html = 'http://google.com/profiles/<span class="tip_username">'+username+'</span>';
	}
	
	$(element).parent().children('span.display_url').html(html);
}

function show_tip_url(element){
	$(element).parent().children('span.display_url').removeClass('as_disp_none');
}

function fill_username(element){
	var val = $(element).val(); 
	$(element).parent().children('span.display_url').children('span.tip_username').html(val);
}

function remove_error(){
	$('.error').each(function(){
			$(this).removeClass('error').show();
		});
}
