$(document).ready(function(){
	//$.preloadCssImages();
	$('.call_lightbox').click(function(){
		lightbox();		
	});
	
	//On pressing excape close lightbox
	if ($.browser.mozilla) {
	    $(document).keypress (checkKey);
	} else {
	    $(document).keydown (checkKey);
	}
	
	function checkKey(e){
		if (e == null) { // ie
			keycode = event.keyCode;
		}
		else { // mozilla
			keycode = e.which;
		}
		if (keycode == 27) { // escape, close box
			if ($('.lightbox_content_holder').css('display') != 'none') {
				hide_lightbox();
			}
		}
	}
	
});
		
//Calling lightbox & displaying the correct content
function show_content(content){
	$('.allhide').hide();
	if ($.browser.msie && $.browser.version == 6.0) {
		$('.lightbox_content_holder #map').html('');
	}
	$('#'+content).show();
	lightbox();
}
		
function lightbox(){
	//Checking the display property of the lightbox and showing or hiding it based on it
	var disp = $('.lightbox_content_holder').css('display');
	if (disp == "none") {
		show_lightbox();
	}
	else if (disp == "block") {
			hide_lightbox();
		}
}

function show_lightbox(){
		//$('.display_ad , .video_in').hide();
		
		if($.browser.msie && $.browser.version == 6.0){
			$('.module_search select').hide();
		}
	
	    //Setting the lightbox background in full window top of all other elements
		var hght = $(document).height();
		var width = $(document).width();
		$('.lightbox_background').css('width', width);
		$('.lightbox_background').css('height', hght);
		//Making the lightbox center
		$('.lightbox_content_holder').show();
		if ($.browser.msie) {
			var lb_width = $('.lightbox_content_holder').width();
			var lb_hgt = $('.lightbox_content_holder').height();
		}
		else {
			var div_width = $('.lightbox_content_holder').css('width');
			var div_hght = $('.lightbox_content_holder').css('height');
			var lb_width = div_width.replace("px","")
			var lb_hgt = div_hght.replace("px","")
		}
		
		var half_lb_width = lb_width/2;
		var mgnLeft = '-'+half_lb_width+'px';
		var half_lb_hght = (lb_hgt/2)+14;
		var mgnTop = '-'+half_lb_hght+'px';
		$('.lightbox_content_holder').css({
			'margin-left':mgnLeft,
			'margin-top':mgnTop,
			'display':'none'
			});
		$('.lightbox_outer').css('visibility','visible');
		
		$('.lightbox_background').show();
		
		$('.lightbox_content_holder').show();
}

function hide_lightbox(){
		//$('.display_ad , .video_in').show();
		if($.browser.msie && $.browser.version == 6.0){
			$('.module_search select').show();
		}
	//Effects Use the one which u like, always keep only one uncommented
	
		$('.lightbox_content_holder').css({
		'width':'',
		'height':''
		});
	
		$('.lightbox_content_holder').hide();
		$('.lightbox_background').hide();
		$('#as_trailer_fix').val('yes');
		
			try{
				restore();
			}
			catch(e){}
}
