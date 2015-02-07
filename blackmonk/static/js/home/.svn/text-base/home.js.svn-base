$(document).ready(function(){

        var calendarPicker1 = $("#dTpKr").calendarPicker({
					monthNames:["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
					dayNames: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
					years:0,
					reYe:true,
					months:0,
					days:4,
					showDayArrows:false,
					disablePrvDate:true,
					//useWheel:true,
					colWidth: 52,
					callback:function(cal){
					       retrieve_events_by_date(cal.currentDate.format("yyyy-mm-dd"));
					}

				});	
				// Featured Articles Carousel
				$('#tMbpGrpRw').bUiSlider({
					pagerCustom: '#tMbpGr',
					pagerCustomTmH:true,
					onSliderLoad:function(){
	                    $('.fLxiMgW').setrSpVWidth(0);
						$('.fLxiMgH').setrSpVHeight('mDa-lT');
						$('.fTrD-bL').setfTrDtXtHeight(); 
	                }
				});
				
				// Featured Business Carousel
				$('.fTrD-bSnS-cRsL').bUiSlider({
					pager:false,
					speed:600,
					//auto:true,
					slideWidth: 145,
					adaptiveHeight: true,
					infiniteLoop: false,
					hideControlOnEnd: true,
				    minSlides:1,
				    maxSlides: 5,
				    slideMargin: 12,
				    onSliderLoad:function(){
                    	$('.fLxiMgW').setrSpVWidth();
                    }
				});

				// Featured Gallery Carousel
				$('.fTrD-cRsL-Glry').bUiSlider({
					pager:false,
					speed:600,
					//auto:true,
					slideWidth: 5000,
					adaptiveHeight: true,
					minSlides:5,
					maxSlides: 5,
					slideMargin: 12,
					onSliderLoad:function(){
						$('.fLxiMgH').setrSpVHeight('mDa-lT');
					}
				});
				$('.fTrD-HpMv-cRsL').bUiSlider({
					pager:false,
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
});

function retrieve_events_by_date(sdate){
	$('#id_events_ul').addClass('oP50'); 
	$.ajax({
		type: "get",
		url: event_url,
		data: 'sel_date='+sdate,
		dataType:'json',
		success: function(data){
				if(data.status){
					//$('#id_events_ul').empty().html(data.html).fadeIn(300);
					//$('#id_events_ul').fadeOut('fast', function(){
					    $('#id_events_ul').empty().html(data.html).fadeIn('fast');
						$('.fLxiMgW').setrSpVWidth(0);
						$('#id_events_ul').removeClass('oP50');
					//});
				}
			}
	});
}