$(document).ready(function(){
	
	//Featured Gallery Slider
	$('#fTrDgLrY').bUiSlider({
		pager:false,
		speed:600,
		slideWidth: 5000,
		adaptiveHeight: true,
		onSliderLoad:function(){
		  $('.fLxiMgW').setrSpVWidth(0);
		  $('.fTrD-bL').setfTrDtXtHeight();
	   }
	});
	
	$('.rLtD-cRsL').bUiSlider({
		pager:false,
		speed:600,
		slideWidth: 184,
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
        $('.bm-tabs-content').removeClass('hide').hide();
		$('#'+$(this).attr('id')+'_contents').fadeIn(400);
		try{
			$('.fLxiMgW').setrSpVWidth();
	    	$('.fLxiMgH').setrSpVHeight('mDa-lT');
        }
        catch(e){}
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
	    reports_data(pathname,bids,category,org_path,click);
    }
    catch(e){}
	
});