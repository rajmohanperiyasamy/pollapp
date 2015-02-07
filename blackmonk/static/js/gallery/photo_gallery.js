
$(document).ready(function(){
	
	function setFlScRtXtWidth(){
		$('.fTrD-bL .mDa-oT').each(function() {
			if($(this).closest('.fTrD-bL').hasClass('FlScR')){
				var w = $(this).width();
				var l = ($(window).width()-w)/2;
				$(this).closest('li').find('.fTrD-tXt .fTrD-tXt-iN').css({'width':w,'left':l});
			}
			else{
				$(this).closest('li').find('.fTrD-tXt .fTrD-tXt-iN').css({'width':'auto','left':'auto'});	
			}
		});
	}
			
				
	var tMbpGrpRwpGr;
	var tMbpGrpRw;
	function cLsLpPg(mXsL,sTsL){
		tMbpGrpRwpGr = $('#tMbpGr').bUiSlider({
			slideWidth: 95,
			minSlides: 1,
			maxSlides: mXsL,
			slideMargin: 6,
			infiniteLoop: false,
			hideControlOnEnd: true,
			startSlide:sTsL,
			onSliderLoad:function(){
			  $('.fLxiMgW').setrSpVWidth(0);
			  $('.fTrD-bL').setfTrDtXtHeight();
		   }
	
		});
	};
	cLsLpPg(8,0);
	function cLsLpR(sTsLpR){
		tMbpGrpRw = $('#tMbpGrpRw').bUiSlider({
			pagerCustom: '#tMbpGr',
			animatepager: true,
			infiniteLoop: false,
			pagerSl:tMbpGrpRwpGr,
			hideControlOnEnd: true,
			startSlide:sTsLpR,
			onSliderLoad:function(){
			  $('.fLxiMgH').setrSpVHeight('mDa-lT');
			  $('.fTrD-bL').setfTrDtXtHeight();
			  setFlScRtXtWidth();
		   }
		});
	}
	cLsLpR(0);




	


});





						
					
					