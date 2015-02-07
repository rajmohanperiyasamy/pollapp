$(document).ready(function(){
	
	//Keybode navigation
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
		if (keycode == 39) { // If right key is pressed
			if ($('#as_image_gallery').css('display') != 'none' && $('.lb_next').css('display') != 'none'){
				$('.loader_32').show();
				load_next();
			}
		}
		if (keycode == 37) { // If left key is pressed
			if ($('#as_image_gallery').css('display') != 'none' && $('.lb_prev').css('display') != 'none') {
				$('.loader_32').show();
				load_prev();
			}
		}
	}
	
	
	var initial = 0;
	$('.as_lb_gallery').click(function(){
		
		//Setting the whole lightbox background black
		$('.lightbox_content_holder').css({
				'background-color':'black',
				'padding':'2px'
				});
		
		$('.lightbox_background').css('background-color','black');
		
		//Getting the current image index
		var name = $(this).attr('name');
		var name_split = name.split('_wallpaper');
		index = name_split[1];
		
		//Setting the current image index to the next and prev button so that it can be acces globally
		set_index(index,'direct');
		
		//Showing the next and prev buttons,gif,opening lightbox
		hide_buttons();
		$('.loader_32').show();
		show_content('as_image_gallery');

		//Loading the first image directly if it is being clicked initial itself	
		if (name_split[1] != initial) {
			load_full_img(name_split[1]);
		}
		else {
			$('.loader_32').hide();
			initial = 1000;
		}
	});
	
	$('.lb_next').click(function(){
		$('.loader_32').show();
		load_next();
	});
	
	$('.lb_prev').click(function(){
		$('.loader_32').show();
		load_prev();
	});
	
});

function load_next(){
	set_index('dummy','next');
	hide_buttons();
	load_full_img();
}

function load_prev(index){
	set_index('dummy','prev');
	hide_buttons();
	load_full_img();
}

function load_full_img(){
		$('#as_load_hack').val('yes');
		index = get_index();
		var src = lb_img_arr[index];
		
		$("#lb_main_img").animate({
					opacity:'0.5'
					},300);
		
		$('#lb_next_img').attr('src',src).load(function(){
						load_callback_hack();
						});
}

function load_callback_hack(){
	var exec = $('#as_load_hack').val();
	if (exec == 'yes') {
		lb_centering();
		$('#as_load_hack').val('no');
	}		
}

function hide_buttons(){
	index = get_index();
	$('.lb_next').hide();
	$('.lb_prev').hide();
	if(index < total_imgs-1 ){
		$('.lb_next').show();
	}
	if(index > 0 ){
		$('.lb_prev').show();
	}
}

function lb_centering(){
			if ($.browser.msie) {
				var next_width = $('#lb_next_img').width();
				var next_hght = $('#lb_next_img').height();
			}
			else {
				var next_width = $('#lb_next_img').css('width');
				var next_hght = $('#lb_next_img').css('height');
				var next_width = next_width.replace("px","")
				var next_hght = next_hght.replace("px","")
			}
			var half_next_width = next_width/2;
			var mgnLeft = '-'+half_next_width+'px';
			var half_next_hght = next_hght/2;
			var mgnTop = '-'+half_next_hght+'px';		
			
			$('#lb_main_img,.loader_32,.as_nav,.lb_close').hide();
			
			index = get_index();
			var src = lb_img_arr[index];
			$('#lb_main_img').attr('src',src);
			
			if ($.browser.msie && $.browser.version == 6.0) {
				$('html, body').animate({scrollTop:'0'}, 700);
			}
			$('.lightbox_content_holder').animate({
			'top' : '50%',
			'left': '50%',
			marginLeft:mgnLeft,
			marginTop:mgnTop,
			'width' : next_width,
			'height' : next_hght
			},700,function(){
				lb_load_real_img();
			});
			
}

function lb_load_real_img(){
	$("#lb_main_img").animate({
		opacity:'1'
		},10,function(){
			$("#lb_main_img").fadeIn(700);
			$('.lb_close').show();
			hide_buttons();	
		});
}

function set_index(direct_index,lb_call){
	var index = $('.lb_prev').attr('id');
	index = parseInt(index.replace('prev_',''));
	if (lb_call == 'next') {
		index = index + 1;	
	}
	if (lb_call == 'prev') {
		index = index - 1;
	}
	if (lb_call == 'direct') {
		$('.lb_prev ').removeAttr('id').attr('id', 'prev_' + direct_index);
		$('.lb_next ').removeAttr('id').attr('id', 'next_' + direct_index);
	}
	else{
		$('.lb_prev ').removeAttr('id').attr('id', 'prev_' + index);
		$('.lb_next ').removeAttr('id').attr('id', 'next_' + index);
	}
	
}

function get_index(){
	var index = $('.lb_prev ').attr('id');
	index = parseInt(index.replace('prev_',''));
	return index
}
