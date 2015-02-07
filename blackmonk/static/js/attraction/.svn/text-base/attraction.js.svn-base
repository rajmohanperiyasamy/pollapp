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
	
	//Attraction photo Gallery begin
	
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
		
	
	
	
	//Respond email code begin
	
	//On calling the respond , making all the fields empty
	$('.contact_form_clr').click(function(){
		$('#contact_form [type="text"]').val('');
		$('#respond_msg').val('');
		$('.tellfriend input').css('border-color', '#069');
		$('.tellfriend textarea').css('border-color', '#069');
	});
	
	
	$('.tellfriend textarea').keyup(function(){
		$(this).css('border-color', '#069');
	});
	
	
	
	//Assigning the "#contact_hashkey" hidden input box with the comment hash key value only at the first loading of the page  
	//$('#contact_hashkey').val($('#id_hashkey').val());
	
	$('.respond_submit').click(function(){
		$('.tellfriend input').css('border-color', 'green');
		$('.tellfriend textarea').css('border-color', 'green');
	});
	
});

if(typeof String.prototype.trim !== 'function') {
	  String.prototype.trim = function() {
	    return this.replace(/^\s+|\s+$/g, ''); 
	  }
}

