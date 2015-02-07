$(document).ready(function(){
	//Ie 6     
	if ($.browser.msie && $.browser.version == 6.0 && $('#as_ie6').val()=='yes') {
		show_content('as_ie6_alert');
	}

	//Featured Video Slider
	$('.bM-Ftrd-ViDs').bUiSlider({
		pager:false,
		speed:600,
		//auto:true,
		slideWidth: 394,
		adaptiveHeight: true,
		minSlides:1,
		maxSlides: 2,
		slideMargin: 12,
		onSliderLoad:function(){
		  $('.fLxiMgW').setrSpVWidth(0);
	   }
	});

	//Related Video Slider Detail Page
	$('.rLtD-cRsL').bUiSlider({
		pager:false,
		speed:600,
		//auto:true,
		slideWidth: 183,
		//infiniteLoop: false,
		//hideControlOnEnd: true,
		adaptiveHeight: true,
	    minSlides:1,
	    maxSlides: 4,
	    slideMargin: 12,
		onSliderLoad:function(){
		  $('.fLxiMgW30').setrSpVWidth(30);
	   }
	});

	
	//Latest and Trending Tabs
	$('#id_tabs_ul li a').click(function(){
		$('.bm-tabs-li').removeClass('active');
		$(this).parent('li').addClass('active');
        $('.bm-tabs_content').hide();
		$('#'+$(this).attr('id')+'_videos').fadeIn(400);
		try{
			$('.fLxiMgW').setrSpVWidth(0);
	    	$('.fLxiMgH').setrSpVHeight('mDa-lT');
        }
        catch(e){}
    });
    
    //Ajax Search retrievel
	$('#search_button').click(function(event){
		event.preventDefault();
		$.ajax({
			type: "GET",
			url: "/videos/a/videos-search/",
			data: "keyword=" + $('#search_keyword').val() + "&category=" + $('#search_category').val(),
			success: function(html_from_server){
				$('#video_thumbnails').html(html_from_server);
			}
		});
	});	

	try{
		var pathname = window.location.pathname;
    	org_path=pathname;
		var bids=new Array();
	    var cat='';
	    var category=new Array();
	    var category_name='';
	    var click = false;
	     $('.bids').each(function(){
	            bids.push($(this).val());
	        });
	        $('.bicts').each(function(){
	            var cat=$(this).val();
	            cat=cat.toString();
	            var a='&';
	            var b='and';
	            category_name=cat.replace(a,b)
	            category.push(category_name);
	            });
	    reports_data(pathname,bids,category,org_path,click)
	}
	catch(e){}



});
