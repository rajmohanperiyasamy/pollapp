$(document).ready(function(){
	
	$('.fTrD-cRsL').bUiSlider({
        pager:true,
        speed:600,
        //auto:true,
        slideWidth: 145,
        adaptiveHeight: true,
        minSlides:1,
        maxSlides: 6,
        slideMargin: 12,
        onSliderLoad:function(){
          $('.fLxiMgH').setrSpVHeight('mDa-lT');
       }
    });
	
	var sL1 = $('#movie-hero-media');
    sL1 = sL1.bUiSlider({
           mode: 'fade',
           pager:false,
           speed:600,
           onSlideNext:function(){
                   $('#movie-hero-text').parent().parent().find('.bUi-next').trigger('click');
           },
           onSlidePrev:function(){    
                   $('#movie-hero-text').parent().parent().find('.bUi-prev').trigger('click');
           },
		   onSliderLoad:function(){
				$('.fLxiMgW').setrSpVWidth(0);
			}
            
    });
    var sL2 = $('#movie-hero-text');
    sL2 = sL2.bUiSlider({
           pager:false,
           speed:600,
           onSlideNext:function(){
                   $('#movie-hero-media').parent().parent().find('.bUi-next').trigger('click');
           },
           onSlidePrev:function(){
                   $('#movie-hero-media').parent().parent().find('.bUi-prev').trigger('click');
           },
           onSliderLoad:function(){
                $('.fTrD-bL').setfTrDtXtHeight();
				$('.fLxiMgW').setrSpVWidth(0);
            }
    });
           
    // Star Rate Read Only
    $('.sTr-rT-rD').raty({
        readOnly: true, 
        score: 3.6, 
        //precision: true,
        //target    : '#rw0001',
        //targetKeep: true,
        size      : 16
    });    
    $('.sTr-rT-mNi').raty({
        number: 5,
        readOnly: true, 
        score: 7.6, 
        //precision: true,
        //target    : '#rw0001',
        //targetKeep: true,
        size      : 12
    });  
    
    try{get_recent_reviews();}
	catch(e){}   

});
function get_recent_reviews(){
	$.ajax({
		type: "get",
		url: review_url,
		data: 'type=movies',
		dataType:'json',
		success: function(data){
				if(data.status){
					$('#id_recent_reviews').removeClass('hide').html(data.html);
				}
			}
	});
}


