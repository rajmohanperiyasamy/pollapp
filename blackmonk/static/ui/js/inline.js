/* Selectmenue */
$(document).ready(function() {
	$('.modal-form .select-menu').chosen({disable_search_threshold:10}); 
	$('.lb_select-menu').chosen({disable_search_threshold:10}); 
	//$('.field-group [title]').tipsy({trigger: 'focus', gravity: 'w',ftip:true});
	$('.tttxt-n').tipsy({gravity: 'n'});
	  
	$(".distroy-preview").live("click",function(event){
		$('#large_image').attr('src','');
		$(".item-preview-wrapper").hide();
	});
});
