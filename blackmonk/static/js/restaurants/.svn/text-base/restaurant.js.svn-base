$(function(){

        $('.fTrD-cRsL').bUiSlider({
            pager:false,
            speed:600,
            //auto:true,
            slideWidth: 179,
            adaptiveHeight: true,
            minSlides:1,
            maxSlides: 5,
            slideMargin: 12,
            onSliderLoad:function(){
              $('.fLxiMgW').setrSpVWidth(0);
           }
        });

		try{$(".swipebox").swipebox();}
		catch(e){}
       
       var sL1 = $('#restaurant-hero-media');
       sL1 = sL1.bUiSlider({
               mode: 'fade',
               pager:false,
               speed:600,
               onSlideNext:function(){
                       $('#restaurant-hero-text').parent().parent().find('.bUi-next').trigger('click');
               },
               onSlidePrev:function(){    
                       $('#restaurant-hero-text').parent().parent().find('.bUi-prev').trigger('click');
               },
                   onSliderLoad:function(){
                    $('.fLxiMgW').setrSpVWidth(0);
                }
                
       });

       var sL2 = $('#restaurant-hero-text');
       sL2 = sL2.bUiSlider({
               pager:false,
               speed:600,
               onSlideNext:function(){
                       $('#restaurant-hero-media').parent().parent().find('.bUi-next').trigger('click');
               },
               onSlidePrev:function(){
                       $('#restaurant-hero-media').parent().parent().find('.bUi-prev').trigger('click');
               },
               onSliderLoad:function(){
                    $('.fTrD-bL').setfTrDtXtHeight();
                }
       });

	   $('.bM-dEv-rTngs').raty({
			readOnly: true, 
			score: 3.6, 
			//precision: true,
			//target    : '#rw0001',
			//targetKeep: true,
			size      : 12
		});	




});    

function update_selected_values(cuisines,categories,prices,features){
	var dataString='cuisines='+cuisines;
	dataString+='&categories='+categories+'&features='+features+'&prices='+prices;
	$.ajax({
		type: "get",
		url: rest_update_value_url,
		data: dataString,
		dataType:'json',
		success: function(data){
				if(data.status){
					if(data.list_contents){
						$('#id_append_values_div').empty().html(data.html).show();
					}
					else{$('#id_append_values_div').hide();}
				}
		}
	});
}

function remove_selected_values(hobj,type,id){
	$(hobj).fadeOut('slow', function(){
	    $(hobj).remove();
	});
	$('#'+type+'_'+id).prop('checked', false);
	if($('a.bM-dEv-aNchR').length == 1){$('#id_append_values_div').hide();}
	filter_contents();
	return true;
}

function clear_all_selected_values(){
	$('#id_append_values_div').empty().hide();
	$('.bM-dEv-cBx').each(function(){
		$(this).prop('checked', false);
	});
	filter_contents();
}


function filter_contents()
{
	
	var cuisines = [];
	var categories = [0];
	var features = [0];
	var prices = [0];
	
	cuisines.push($('#id_selected_cuisine').val());

	$('#id_rest_categories :checked').each(function() {
   		categories.push($(this).val());
	});

	$('#id_rest_features :checked').each(function() {
   		features.push($(this).val());
	});

	$('#id_rest_prices :checked').each(function() {
   		prices.push($(this).val());
	});
	
	update_selected_values(cuisines,categories,prices,features);
	
	var dataString='cuisines='+cuisines;
	dataString+='&categories='+categories+'&features='+features;
	dataString+='&prices='+prices;
	dataString+='&page='+$('#id_hid_pgntn').val()+'&sort='+$('#id_sort').val();
	dataString+='&sel_cuisine='+$('#id_selected_cuisine').val();
	dataString+='&view='+$('#id_hid_view_type').val();
	
	try{if($('#id_search').val()=='true'){dataString+='&search='+$('#id_search').val()+'&q='+encodeURIComponent($('#id_hid_kw').val())+'&location='+encodeURIComponent($('#id_hid_location').val());}}
	catch(e){}
	$('#id_append_contents_div').addClass('oP50');
	$.ajax({
		type: "get",
		url: rest_filter_url,
		data: dataString,
		dataType:'json',
		success: function(data){
				if(data.status){
					$('#id_append_contents_div').empty().html(data.html);
					$('#id_append_contents_div').removeClass('oP50');
					if(data.pagntn_ranges_txt){$('#id_pgntn_ranges').empty().html(data.pagntn_ranges_txt).show();}
					else{$('#id_pgntn_ranges').empty().hide();}
				}
		}
	});
}
