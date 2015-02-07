$(document).ready(function(e) {
		$('#id_find').typeahead({
	        ajax: { url: auto_suggest_business_url,type: "GET",
	                triggerLength: 1 }
	    });

		 $('#id_location').typeahead({
		ajax: { url: auto_suggest_business_address_url,type: "GET",
			triggerLength: 1 }
		});    

		
		
		// Calendar 				
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
		
		// Featured Business Carousel
		$('.fTrD-bSnS-cRsL').bUiSlider({
			pager:true,
			speed:600,
			//auto:true,
			slideWidth: 146,
			adaptiveHeight: true,
			infiniteLoop: false,
			hideControlOnEnd: true,
		    minSlides:1,
		    maxSlides: 6,
		    slideMargin: 12,
		    onSliderLoad:function(){
    	$('.fLxiMgW').setrSpVWidth(0);
    	}
		});
		
		// Star Rate Read Only
	
		
		$('.sTr-rT-rD').raty({
	    	readOnly: true,
	    	score: function() {return $(this).attr('data-rating');},
			size: 16
		});



		$('.sTr-rT-mNi').raty({
			readOnly: true, 
			score: function() {return $(this).attr('data-rating');}, 
			//precision: true,
			//target    : '#rw0001',
			//targetKeep: true,
			size      : 12
		});


// Business Category Ajax
		$('.category').click(function(){
			var id = $(this).attr('id');
			$('#catBusiness').addClass('oP50'); 
			$.ajax({  
				type: "GET",  
				url: latest_business_ajax_url,  
				data: 'id='+id,
				dataType:'JSON',
				success : function(data){
							$('.latestBusiness').fadeOut().remove();
							$('#catBusiness').empty().html(data.biz_html).fadeIn();
							$('#catBusiness').removeClass('oP50');

							$('.fLxiMgW').setrSpVWidth(0);
							$('.fLxiMgH').setrSpVHeight('mDa-lT');
					
				},
				error: function(data) {
					alert("Currently Unavailable");
					$('#catBusiness').removeClass('oP50');
			}
					
			});
	});  

//Deal Time

		try{
			$('.defaultCountdown').countdown({
                until: +$('#deal_time_left').val(),
                format: 'HMS',
                layout: '{hnn}:{mnn}:{snn}'
            });
}
catch(e){}

		$('#id_ul_tab li a').click(function(){
			$('#id_ul_tab li').removeClass('active');
			$(this).parent('li').addClass('active');
			$('.bM-tb-cNt').addClass('hide');
			$('#'+$(this).attr('id')+'_contents').removeClass('hide');

			$('.fLxiMgW').setrSpVWidth(0);
		$('.fLxiMgH').setrSpVHeight('mDa-lT');


		});   
		

});

           

// Event Ajax
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