$(".add-theare").colorbox({ width: "770", initialWidth: "770", initialHeight: "200", height:"auto", top:"5%"});
$(".edit-theare").colorbox({ width: "770", initialWidth: "770",initialHeight: "200", height:"auto", top:"5%",onComplete: function(){$.colorbox.resize();}});
$(".theatre-seo").colorbox({ width: "550", initialWidth: "550",initialHeight: "200", height:"auto", top:"5%",title:function(){return getLBTitle($(this));}});
$(".theatres-showtimes").colorbox({ width: "770", initialWidth: "770",initialHeight: "200", height:"auto", top:"5%",title:function(){return getLBTitle($(this));}});
$(".movie-showtimes").colorbox({ width: "770", initialWidth: "770",initialHeight: "200", height:"auto", top:"5%",title:function(){return getLBTitle($(this));}});

$(".edit_movie_lightbox").colorbox({width: "770", initialWidth: "770",initialHeight: "200", height:"auto", top:"5%",title:function(){return getLBTitle($(this));}});// This one i am using for edit theatre lightbox after adding colorbox
//$(".critic-review-lightbox").colorbox({width: "880", initialWidth: "880", height:"auto", top:"5%"});// This one i am using for edit theatre lightbox after adding colorbox




function theatre_action(){
	var flag=false;
	var flag_action=false;
	if($('#id_action').val()!='0'){
		$('.cbox:checked').each(function(){
			flag=true;
		});
	}	
	if(flag){
		if($('#id_action').val()=='DEL'){
			var con = 	confirm('Are you sure you want to delete the selected Theatre(s)');
			if (con){
				filter_action(0,'#');
			}
		}
		
		if(flag_action){filter_action(0,'#');}
		else{return false;}
		}
	else{
			alert(gettext('Please select Theatre(s)'));
		}
}

function filter_action(ids,action){
	var all_ids=[];
	var dataString='';
	var url= $('#id_theatre_action_url').val();
	dataString+="sort="+$('#id_sort').val();
	dataString+="&listing="+$('#id_listing_type').val();
	dataString+="&created="+$('#id_created').val();
	if($('#id_status').val()!='' && $('#id_status').val()!=null){
			dataString+="&status="+$('#id_status').val();
		}
	if($('#id_pagentn').val()!='' && $('#id_pagentn').val()!=null){
		dataString+="&page="+$('#id_pagentn').val();
	}
	if($('#id_item_per_page').val()!='' && $('#id_item_per_page').val()!=null){
		dataString+="&item_perpage="+$('#id_item_per_page').val();
	}
	if($('#id_search').val()!='' && $('#id_search').val()!=null){
		dataString+="&search=true";
		dataString+="&kwd="+$('#id_search_keyword').val();
		dataString+="&type="+$('#search_type').val();
		dataString+="&start_date="+$('#id_search_start_date').val();
		dataString+="&end_date="+$('#id_search_end_date').val();
		dataString+="&cat="+$('#search_category').val();
		if($('#search_status').val()!='' && $('#search_status').val()!=null){
			dataString+="&status="+$('#search_status').val();
		}
	}
	if(action=='#'){
		dataString+="&action="+$('#id_action').val();
		if(ids==0){
			var ids=[];
			$('.cbox:checked').each(function(){
				ids.push($(this).val());
			});
		}
	}else{dataString+="&action="+action;}
	$('.cbox').each(function(){
		all_ids.push($(this).val());
	});
	dataString+="&ids="+ids;
	dataString+="&all_ids="+all_ids;
	$('#ajax_action_loading').show();
	hide_top_info_bar();
	$.ajax({
	type: "GET",
	url: url,
	data: dataString,
	dataType:'JSON',
	success: function(data){
			show_top_info_bar('Theaters');
			$("#master_check").attr('checked',false);
			$('#id_content_listing').val('');
			$('#ajax_action_loading').hide();
			//$('#actionSelect').selectmenu('refresh', true);
		    //if($('#id_action').val()=='DEL') {
			//show_msg('Selected Movie deleted successfully');
			//}
			$('#id_action').val('');
			if(data.status==1){
				try{for(i=0;i<ids.length;i++){$('#li_'+ids[i]).remove();}$('#li_'+ids).remove();}
				catch(e){$('#li_'+ids).remove();}
				$('#ajax_content_list').append(data.html);
				$('#pagenation').empty().html(data.pagenation);
			}			
			show_msg(data.msg,data.mtype);
			if(data.search){$('#close_search').show();}
			if(data.status==1){
				if(data.next){$('#top_pge_next').removeClass('inactive');}
				else{$('#top_pge_next').addClass('inactive');}
				if(data.previous){$('#top_pge_previous').removeClass('inactive');}
				else{$('#top_pge_previous').addClass('inactive');}$('#id_from_to').html(data.pagerange);
				$('#top_item_count').html(data.count);
				
				$(".theatre-seo").colorbox({ width: "550", initialWidth: "550", height:"auto", top:"5%",title:function(){return getLBTitle($(this));}});
				$(".edit-theare").colorbox({ width: "880", initialWidth: "880", height:"auto", top:"5%",title:function(){return getLBTitle($(this));}});
				$('.light_box').colorbox({width: "560",initialWidth: "560", top:"60", initialHeight: "200"});
			}
	}
	});
}


function filter_content(){
	var ids=[]
	var dataString='';
	var url= $('#id_theatre_hidden_url').val();
	dataString+="sort="+$('#id_sort').val();
	dataString+="&listing="+$('#id_listing_type').val();
	dataString+="&created="+$('#id_created').val();
	if($('#id_status').val()!='' && $('#id_status').val()!=null){
			dataString+="&status="+$('#id_status').val();
		}
	if($('#id_pagentn').val()!='' && $('#id_pagentn').val()!=null){
		dataString+="&page="+$('#id_pagentn').val();
	}
	if($('#id_item_per_page').val()!='' && $('#id_item_per_page').val()!=null){
		dataString+="&item_perpage="+$('#id_item_per_page').val();
	}
	if($('#id_search').val()!='' && $('#id_search').val()!=null){
		dataString+="&search=true";
		dataString+="&kwd="+$('#id_search_keyword').val();
		dataString+="&type="+$('#search_type').val();
		dataString+="&cat="+$('#search_category').val();
		if($('#search_status').val()!='' && $('#search_status').val()!=null){
			dataString+="&status="+$('#search_status').val();
		}
	}
	if($('#id_action').val()!='0' && $('#id_action').val()!=''){
		$('.cbox:checked').each(function(){
			ids.push($(this).val());
		});
		dataString+="&action="+$('#id_action').val();
		dataString+="&ids="+ids;
	}
	$('#id_content_listing').hide();
	$('#ajax_content_loading').show();
	hide_top_info_bar();
	$.ajax({
	type: "GET",
	url: url,
	data: dataString,
	dataType:'JSON',
	success: function(data){
			show_top_info_bar('Theaters');
			$('#id_pagentn').val('');
			$('#id_action').val('');
			$('#ajax_content_loading').hide();
			$('#id_content_listing').empty().html(data.html);
			$('#id_content_listing').show();
			
			if(data.search){$('#close_search').show();}
			if(data.next){$('#top_pge_next').removeClass('inactive');}
			else{$('#top_pge_next').addClass('inactive');}
			if(data.previous){$('#top_pge_previous').removeClass('inactive');}
			else{$('#top_pge_previous').addClass('inactive');}
			$('#id_from_to').html(data.pagerange);
			$('#top_item_count').html(data.count);
		}
	});
}

function sort_search(){
	//clear_for_search();
	sort_content()
}
function sort_content(){
	$('#id_pagentn').val('1')
	filter_content();
}

function clear_search(){
	$('#id_search').val('');
	$('#id_search_keyword').val('');
	$('#close_search').hide();
	$('#id_pagentn').val('1')
	filter_content();
}

  /// ######################################## Show Time Functionality #############################


function show_buttons(id)
{		
	$('ul.dropdown-list').hide();
	$('span.item-manage').removeClass('active')
	$('#id_action_ul_'+id).toggle();
	$('#id_span_settings_'+id).toggleClass('active')
	
}

//#########################################


function update_theatre_seo(id){
	var flag = $('#mform_theatre').validate().form()
	if(flag){
		var url= $('#mform_theatre').attr('action');
		var dataString='movie_id='+id;
		var dataString = 'theatre_id='+id+'&theatreseo_title='+$('#id_theatreseo_title').val()+'&theatreseo_description='+$('#id_theatreseo_description').val();
		$('#ajax_content_seo').hide();
		$('#ajax_content_loading_seo').show();
		$.ajax({
			   type: "POST",
			   url: url,
			   data:dataString,
			   dataType:'JSON',
			   success: function(data){	
				   $('#ajax_content_loading_seo').html(data.msg);
					if(data.status){
						show_msg(data.msg,data.mtype);
						$.colorbox.close().delay(1200);
					}else{
						$('#ajax_content_loading_seo').hide();
						$('#ajax_content_seo').fadeIn(2000);
					}
					
				}
		});
	}
	
}	

 

