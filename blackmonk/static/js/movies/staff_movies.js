


//$('.sb-select-menu').selectmenu({style:'dropdown', maxHeight: 160});  // add movie language class


//////////////////////////////////////////////////////
$(document).ready(function(){
	$(".movie-showtimes").colorbox({ width: "770", initialWidth: "770", initialHeight:"200", height:"auto", top:"5%",title:function(){return getLBTitle($(this));}});
	$(".edit_movie_lightbox").colorbox({width: "770", initialWidth: "770", initialHeight:"200", height:"auto", top:"5%",title:function(){return getLBTitle($(this));}});// This one i am using for edit theatre lightbox after adding colorbox
	$(".review-edit").colorbox({
		width: "770", 
		initialWidth: "770", 
		initialHeight:"250",
		height:"auto",
		top:"5%",
		onComplete: function(){$.colorbox.resize();},
		title:function(){return getLBTitle($(this));}
	});
	$(".critic-review-lightbox").colorbox({
		width: "770", 
		initialWidth: "770", 
		initialHeight:"250",
		height:"auto",
		top:"5%",
		onComplete: function(){$.colorbox.resize();},
		title:function(){return getLBTitle($(this));}
	});
	$(".movie-seo").colorbox({ width: "560", initialWidth: "560", height:"auto", initialHeight:"250", top:"5%",title:function(){return getLBTitle($(this));}});
	$(".movie-pic-upload").colorbox({ width: "500", initialWidth: "500", height:"500", initialHeight:"200", top:"5%",title:function(){return getLBTitle($(this));}});


		if($("#id_release_date").length){
				$("#id_release_date").datepicker({ dateFormat: "yy-mm-dd" , minDate:new Date()});
			}
	// nav actions for the movie listing page		
		$('#filter_a a').click(function(){
			$('#id_status').val($(this).attr('name'));
			
			if(!$(this).hasClass('active')){
				$('#filter_a a').removeClass('active');
				$(this).addClass('active');
			}
			filter_content();
		});
			
			$('#filter_c a').click(function(){
			$('#id_created').val($(this).attr('name'));
			
			if(!$(this).hasClass('active')){
				$('#filter_c a').removeClass('active');
				$(this).addClass('active');
			}
			filter_content();
		});
});
//////////////////////////////////////////////////////////////////////////



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
	$('#search_status').val('');
	$('#id_search_keyword').val('');
	$('#id_status').val('');
	$('#close_search').hide();
	$('#id_pagentn').val('1')
	filter_content();
}


function clear_adv_srchfields(){
	$('select#search_type').val("").trigger("liszt:updated");
	$('#id_search_start_date').val("");
	//$('#id_search_end_date').val("");
	$('.search_adv2').val("");
	$('#search_category').val("").trigger("liszt:updated");
	$('#search_status').val("").trigger("liszt:updated");
	
	$('#bottom_search_button').attr('disabled','disabled');
}




function filter_content(){
	var ids=[]
	var dataString='';
	var url= $('#id_hidden_url').val();
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

			show_top_info_bar('Movies');
		
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
			$('html,body').animate({ scrollTop: 0 }, 'slow');
		}
	});
}



function action(){
	var flag=false;
	var flag_action=false;
	if($('#id_action').val()!='0'){
		$('.cbox:checked').each(function(){
			flag=true;
		});
	}	
	if(flag){
		if($('#id_action').val()=='DEL'){
			var con = 	confirm('Are you sure you want to delete the selected Movie(s) ?');
			if (con){
				filter_action(0,'#');
			}
		}
		if($('#id_action').val()=='P'){
			var con = 	confirm('Are you sure you want to activate  the selected Movie(s) ?');
			if (con){
				filter_action(0,'#');
			}
		
		}
		if($('#id_action').val()=='B'){
			var con = 	confirm('Are you sure you want to Deactivate the selected Movie(s) ?');
			if (con){
				filter_action(0,'#');
			}	
		}
	
		
		if(flag_action){filter_action(0,'#');}
		else{return false;}
		}
	else{
			alert(gettext('Please select Movie(s)'));
		}
	//}
}


function filter_action(ids,action){
	
	var all_ids=[];
	var dataString='';
	var url= $('#id_action_url').val();
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
			show_top_info_bar('Movies');
			$("#master_check").attr('checked',false);
			$('#id_content_listing').val('');
			$('#ajax_action_loading').hide();
			$('#actionSelect').val("").trigger("liszt:updated");

		    /*if($('#id_action').val()=='DEL') {
			show_msg('Selected Movie has been deleted successfully');
			}
			if($('#id_action').val()=='P') {
				show_msg('Selected are now activated');
			}
			if($('#id_action').val()=='N') {
				show_msg('Selected video are now inactive');
			}
			if($('#id_action').val()=='B') {
				show_msg('Selected video(s) has been  Blocked successfully');
			}*/
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
				if(data.next){$('#top_pge_next').removeClass('disabled');}
				else{$('#top_pge_next').addClass('disabled');}
				if(data.previous){$('#top_pge_previous').removeClass('disabled');}
				else{$('#top_pge_previous').addClass('disabled');}
				$('#id_from_to').html(data.pagerange);
				$('#top_item_count').html(data.count);
				show_count('all');
				$('.light_box').colorbox({width: "560",initialWidth: "560", top:"60", initialHeight: "200"});
			}
		}
	});
}


function show_count(value){
	$('#ajax_loading').show();
	$('.statefltr').removeClass('active');
	$('#id_status_'+value).addClass('active');
	var count_url= $('#id_movie_status_url').val();
	$.ajax({
	type: "GET",
	url: count_url,
	data: 'status='+value,
	dataType:'JSON',
	success: function(data){
			$('#ajax_loading').hide();
			$('#id_blocked').html(data.blocked);
			$('#id_pub').html(data.published);
			$('#id_tot').html(data.total);
		}
	});
}



/* updating a SEO of a particular video */	
function update_movie_seo(id){
	var flag = $('#mform').validate().form()
	if(flag){
		var url= $('#mform').attr('action');
		//var dataString='movie_id='+id;
		var dataString = 'movie_id='+id+'&slug='+$('#id_slug').val()+'&seo_title='+$('#id_seo_title').val()+'&seo_description='+$('#id_seo_description').val();
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




//  *********************************************************888 Theatre ******************************************************


