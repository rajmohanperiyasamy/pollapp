$(document).ready(function(){	
	$('#filter_a a').click(function(){
		$('#id_status').val($(this).attr('name'));
		
		if(!$(this).hasClass('active')){
			$('#filter_a a').removeClass('active');
			$(this).addClass('active');
		}
		filter_content();

	});
	
	$('#filter_b a').click(function(){
			$('#id_listing_type').val($(this).attr('name'));
		if(!$(this).hasClass('active')){
			$('#filter_b a').removeClass('active');
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
	


function display_settings(id){
	$('.dev_settingsdrpdwn').hide();
	$('span.item-manage').removeClass('active')
	$('#settings_id_'+id).toggle();
	$('#id_span_settings_'+id).toggleClass('active')
	$('.dev_hide_list_status ul.dropdown-list').hide();
	$('span.status-inside').removeClass('active')
}
function display_change_status(id,state){
	$('.dev_hide_list_status ul.dropdown-list').hide();
	$('span.status-inside').removeClass('active')
	$('#change_status_id_'+id).toggle();
	$('#id_span_chge_sts_'+id).toggleClass('active')
	$('.dev_settingsdrpdwn').hide();
	$('span.item-manage').removeClass('active')
	status_function(id,state);
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
		dataString+="&cat="+$('#id_search_cat').val();
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
	//alert(dataString);
	$('#id_content_listing').hide();
	$('#ajax_content_loading').show();
	hide_top_info_bar();
	$.ajax({
	type: "GET",
	url: url,
	data: dataString,
	dataType:'JSON',
	success: function(data){
			show_top_info_bar('Videos');
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
			$('.light_box').colorbox({width: "560",initialWidth: "560", top:"60", initialHeight: "200"});
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
			var con = 	confirm('Are you sure you want to delete video(s) ?');
			if (con){
				filter_action(0,'#');
			}
			//function(r){if(r==true){}});	
		
		}
		if($('#id_action').val()=='P'){
			var con = 	confirm('Are you sure you want to publish video(s) ?');
			if (con){
				filter_action(0,'#');
			}
		}
		if($('#id_action').val()=='N'){
			var con = 	confirm('Are you sure you want to keep selected videos in pending ?');
			if (con){
				filter_action(0,'#');
			}
		}
		if($('#id_action').val()=='B'){
			var con = 	confirm('Are you sure you want to block the selected video(s) ?');
			if (con){
				filter_action(0,'#');
			}	
		}
		if($('#id_action').val()=='F'){
			var con = 	confirm('Are you sure you want to feature these  video(s) ?');
			if (con){
				filter_action(0,'#');
			}	
		}
		if($('#id_action').val()=='BAC'){
			var con = 	confirm('Are you sure you want to Unfeature these video(s) ?');
			if (con){
				filter_action(0,'#');
			}	
		}
		if($('#id_action').val()=='R'){
			var con = 	confirm('Are you sure you want to Reject these  video(s) ?');
			if (con){
				filter_action(0,'#');
			}	
		}
		if(flag_action){filter_action(0,'#');}
		else{return false;}
		}
	else{
			alert(gettext('Please select the  Video(s)'));
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
			show_top_info_bar('Videos');
			
			if(action=='UF' || action=='F'){
				show_msg(data.msg,data.mtype);
				filter_content();
			}else{
				$("#master_check").attr('checked',false);
				$('#ajax_action_loading').hide();
			    /*if($('#id_action').val()=='DEL') {
				show_msg('Selected video deleted successfully');
				}
				if($('#id_action').val()=='P') {
					show_msg('Selected video are now published');
				}
				if($('#id_action').val()=='N') {
					show_msg('Selected video are now in pending ');
				}
				if($('#id_action').val()=='R') {
					show_msg('Selected video are now in rejected ');
				}
				if($('#id_action').val()=='B') {
					show_msg('Selected video Blocked successfully');
				}*/
				show_msg(data.msg,data.mtype);
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
					else{$('#top_pge_previous').addClass('inactive');}
					$('#id_from_to').html(data.pagerange);
					$('#top_item_count').html(data.count);
					show_count('all');
					$('.light_box').colorbox({width: "560",initialWidth: "560", top:"60", initialHeight: "200"});
				}
			}
		}
	});
}

function clear_search(){
	$('#id_search').val('');
	$('#id_search_keyword').val('');
	$('#close_search').hide();
	$('#id_pagentn').val('1')
	filter_content();
}


function sort_search(){
	clear_for_search();
	//sort_content()
}
function sort_content(){
	$('#id_pagentn').val('1')
	filter_content();
}
/*		
function show_count(value){   // this function is comented in line 196
	$('#id_module_state_listing').hide();
	$('#ajax_loading').show();
	$('.state-filter').removeClass('active');
	$('#id_status_'+value).addClass('active');
	var count_url= $('#id_video_status_url').val();
	$.ajax({
	type: "GET",
	url: count_url,
	data: 'status='+value,
	success: function(data){
			$('#ajax_loading').hide();
			$('#id_module_state_listing').empty().html(data);
			$('#id_module_state_listing').show();
		}
	});
}*/
function show_count(value){
	$('#ajax_loading').show();
	$('.statefltr').removeClass('active');
	$('#id_status_'+value).addClass('active');
	var count_url= $('#id_video_status_url').val();
	$.ajax({
	type: "GET",
	url: count_url,
	data: 'status='+value,
	dataType:'JSON',
	success: function(data){
			$('#ajax_loading').hide();
			$('#id_pend').html(data.pending);
			$('#id_pub').html(data.published);
			$('#id_blk').html(data.blocked);
			$('#id_rej').html(data.rejected);
			$('#id_tot').html(data.total);
		}
	});
}	
/* updating a particular video */	
function edit_video_prop(id){
	var flag = $('#mform').validate().form()
	if(flag){
		var url= $('#ajax_update').val();
		var dataString='video_id='+id;
		var dataString = 'video_id='+id+'&title='+$('#id_title').val()+'&category='+$('#id_category').val()+'&description='+$('#id_description').val()+'&yt_videos_id='+$('#yt_videos_id').val();
		$('#ajax_content_seo').hide();
		$('#ajax_content_loading_seo').show();
		$.ajax({
			   type: "POST",
			   url: url,
			   data:dataString,
			   dataType:'JSON',
			   success: function(data){	
					clear_search();
				   $('#ajax_content_loading_seo').html(data.msg);
					if(data.status){
						show_msg(data.msg,data.mtype);
						$.colorbox.close().delay(1200);
					}else{
						$('#ajax_content_loading_seo').hide();
						$('#ajax_content_seo').empty().html(data.lightbox_html);
						$('#ajax_content_seo').fadeIn(2000);
					}
					
				}
		});
	}
	
}
	
/* updating a SEO of a particular video */	
function update_video_seo(id){
	var flag = $('#mform').validate().form()
	if(flag){
		var url= $('#mform').attr('action');
		var dataString='video_id='+id;
		var dataString = 'video_id='+id+'&seo_title='+$('#id_seo_title').val()+'&seo_description='+$('#id_seo_description').val();
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
						$('#ajax_content_seo').empty().html(data.lightbox_html);
						$('#ajax_content_seo').fadeIn(2000);
					}
					
				}
		});
	}
	
}	

var status_search='relevence'
function searching(sts)
{
	var text=$('#id_search_from_yt').val();
	if($.trim(text)==''){
		$('#id_search_from_yt').closest('div').addClass('field-error');
	return false;
	}
	else{$('#id_search_from_yt').parent('div').removeClass('field-error');}
	
	status_search=sts
	
	var relevance = status_search
	var yurl='http://gdata.youtube.com/feeds/api/videos?q='+text+'&start-index='+start_index+'&format=5&max-results=20&orderby='+relevance+'&v=2&alt=jsonc'; 
	$('#id_search_div div.lodr').css('display', 'block');
	$('#id_search_div div.tip').css('display', 'none');
	$.ajax({
		type: "GET",url: yurl,
		dataType:"jsonp",
		success: function(response){
			var append_html= '';
			if (response.data == undefined)
			{
			$("#id_search_div  .video_list").empty();
			$('#id_search_div .video-library .hang-items').show();
			$('#id_search_div .video-library .tip').show();
			$('#id_search_div .video-library .lodr').hide();
			$('#id_search_div div.lodr').css('display', 'none');
			return false;
			}
			if(response.data.items)
			{
				$("#id_search_div  .video_list").empty();
		        $.each(response.data.items, function(i,data){
					$('#id_search_div div.lodr').hide();
					var title = data.title;
					var views =data.viewCount;
					var vid =data.id;
			        var description = data.description;
					var uploader = data.uploader;
				    var duration = 	data.duration;
					var viewCount = data.viewCount;

					try{
						var hr = Math.floor(duration / 3600);
						var min = Math.floor((duration - (hr * 3600))/60);
						var sec = duration - (hr * 3600) - (min * 60);
	
						if (hr < 10) {hr = "0" + hr; }
						if (min < 10) {min = "0" + min;}
						if (sec < 10) {sec = "0" + sec;}
						if(hr != 0 ){var durations = hr + ':' + min + ':' + sec;}
						else{var durations = min + ':' + sec;}
					}
					catch(e){var durations=duration;}

					if(description==''){
						description='';
					}
					append_html+='<li class="videos-selectable inline-block"  id="id_'+vid+'"  >'
					append_html+='<div class="video-selectable-area"  onclick="check_selected(\''+vid+'\')"><div class="thumb-wrap inline-block"><div>'
					append_html+='<input type="hidden" value="'+vid+'" name="v_id_'+vid+'" id="hdn_id_'+vid+'"/><input type="hidden" value="'+title+'" name="v_title'+vid+'" id="title_id_'+vid+'"/>'
					append_html+='<input type="hidden" value="'+escape(description)+'" name="v_description_'+vid+'"  id="desc_id_'+vid+'"/>'
					//append_html+='<input type="hidden" value="'+duration+'" name="v_duration_'+vid+'" id="duratn_id_'+vid+'"/>'
					append_html+='<input type="hidden" name="durations'+vid+'"  value="'+durations+'" id = "durations_id'+vid+'">';
					append_html+='<span class="video-thumb" id="id_video_actv_'+vid+'" disabled="disabled" >'
					append_html+='<span class="clip"><img alt="Thumbnail "src="http://i.ytimg.com/vi/'+data.id+'/default.jpg"></span></span>'
					append_html+='<span class="video-duration">'+durations+'</span></div>'
					append_html+='<span class="play-icon preview-item " title="Play this video" id="id_span_play_icon_'+vid+'" onclick="play_in_lightbox(event,\''+vid+'\')"></span></div>'
					append_html+='<div class="result-video-content">'
					append_html+='<h3 id="id_title_span_'+vid+'">'+title.slice(0,25)+'</h3>'
					append_html+='<p class="facets"><span class="video-by">by <a href="javascript:void(0)">'+uploader+'</a></span><br />'+viewCount+' views</p>'
				    append_html+='</div><span id="id_span_icon_tick_'+vid+'" class="icon-tick inline-block" style="display:none;"></span></div></li>'                                    
				   
				});
				$("#id_search_div .video_list").append(append_html);
				$('#id_sel_hangitems').show();
				$('#id_search_div .video-library .tip').css('display', 'none');
				$('#id_search_div .video-library .hang-items').css('display', 'none');
			}
		else{
			$('#id_search_div .video-library .tip').css('display', 'block');
			$('#id_search_div div.lodr').css('display', 'none');
		}	
		}
		
	});
}

function load_more(sts)
{
	var text=$('#id_search_from_yt').val();
	if($.trim(text)==''){
		$('#id_search_from_yt').closest('div').addClass('field-error');
	return false;
	}
	else{$('#id_search_from_yt').parent('div').removeClass('field-error');}
	
	status_search=sts;
	start_index=start_index+20;
	
	var relevance = status_search
	var yurl='http://gdata.youtube.com/feeds/api/videos?q='+text+'&start-index='+start_index+'&format=5&max-results=20&orderby='+relevance+'&v=2&alt=jsonc'; 
	
	$('#id_search_div div.lodr').css('display', 'block');
	$.ajax({
		type: "GET",url: yurl,
		dataType:"jsonp",
		success: function(response){
			var append_html= '';
			if(response.data.items)
			{
			
		        $.each(response.data.items, function(i,data){
					$('#id_search_div div.lodr').css('display', 'none');
					$('#id_search_div .video-library .tip').css('display', 'none');
				    $('#id_search_div .video-library .hang-items').css('display', 'none');
					var title = data.title;
					var views =data.viewCount;
					var vid =data.id;
			        var description = data.description;
					var uploader = data.uploader;// apply it after getting the new ui for uploading 
				    var duration = 	data.duration;
					var viewCount = data.viewCount;
					
					try{
						var hr = Math.floor(duration / 3600);
						var min = Math.floor((duration - (hr * 3600))/60);
						var sec = duration - (hr * 3600) - (min * 60);
	
						if (hr < 10) {hr = "0" + hr; }
						if (min < 10) {min = "0" + min;}
						if (sec < 10) {sec = "0" + sec;}
						if(hr != 0 ){var durations = hr + ':' + min + ':' + sec;}
						else{var durations = min + ':' + sec;}
					}
					catch(e){var durations=duration;}

					if(description==''){
						description='';
					}
					append_html+='<li class="videos-selectable inline-block"  id="id_'+vid+'"  >'
					append_html+='<div class="video-selectable-area"  onclick="check_selected(\''+vid+'\')"><div class="thumb-wrap inline-block"><div>'
					append_html+='<input type="hidden" value="'+vid+'" name="v_id_'+vid+'" id="hdn_id_'+vid+'"/><input type="hidden" value="'+title+'" name="v_title'+vid+'" id="title_id_'+vid+'"/>'
					append_html+='<input type="hidden" value="'+escape(description)+'" name="v_description_'+vid+'"  id="desc_id_'+vid+'"/>'
					//append_html+='<input type="hidden" value="'+duration+'" name="v_duration_'+vid+'" id="duratn_id_'+vid+'"/>'
					append_html+='<input type="hidden" name="durations'+vid+'"  value="'+durations+'" id = "durations_id'+vid+'">';
					append_html+='<span class="video-thumb" id="id_video_actv_'+vid+'" disabled="disabled" >'
					append_html+='<span class="clip"><img alt="Thumbnail "src="http://i.ytimg.com/vi/'+data.id+'/default.jpg"></span></span>'
					append_html+='<span class="video-duration">'+durations+'</span></div>'
					append_html+='<span class="play-icon preview-item " title="Play this video" onclick="play_in_lightbox(event,\''+vid+'\')"></span></div>'
					append_html+='<div class="result-video-content">'
					append_html+='<h3 id="id_title_span_'+vid+'">'+title.slice(0,25)+'</h3>'
					append_html+='<p class="facets"><span class="video-by">by <a href="javascript:void(0)">'+uploader+'</a></span><br />'+viewCount+' views</p>'
				    append_html+='</div><span id="id_span_icon_tick_'+vid+'" class="icon-tick inline-block" style="display:none;"></span></div></li>'                                    
				   
				
				});
				$("#id_search_div .video_list").append(append_html);
				$("#ajax_content_loading").hide();
			}
		else{
			$('#id_search_div .video-library .tip').css('display', 'block');
		}	
		}
	});
}
var page_index=1;	
var status_search_viemo='relevence'
function searching_vimeo(sts,vurl){
	var text=$('#id_search_from_yt_viemo').val();
	if($.trim(text)==''){$('#id_search_from_yt_viemo').closest('div').addClass('field-error');return false;}
	else{$('#id_search_from_yt_viemo').parent('div').removeClass('field-error');}
	status_search_viemo=sts
	var relevance = status_search_viemo
	$('#id_search_div_vimeo div.lodr').css('display', 'block');
	$('#id_search_div_vimeo div.tip').css('display', 'none');
	$.ajax({
		type: "GET",
		url: vurl+"?sort="+relevance+"&page=1&q="+text,
		dataType:"json",
		success: function(response){
			var append_html= '';
			if (response == '0'){	
				$("#id_search_div_vimeo  .video_list").empty();
				$('#id_search_div_vimeo  .video-library .hang-items').show();
				$('#id_search_div_vimeo  .video-library .tip').show();
				$('#id_search_div_vimeo  .video-library .lodr').hide();
				$('#id_search_div_vimeo  div.lodr').css('display', 'none');
				return false;
			}
			if(response){
				$("#id_search_div_vimeo .video_list").empty();
		        $.each(response, function(i,data){
					$('#id_search_div_vimeo  div.lodr').hide();
					var title = data.title;
					var vid =data.id;
			        var description = data.description;
					var uploader = data.username;
					var image_url=data.image_url
					var duration = 	data.duration;
					
					try{image_url = image_url.replace('_100','_640')}
					catch(e){}

					try{
						var hr = Math.floor(duration / 3600);
						var min = Math.floor((duration - (hr * 3600))/60);
						var sec = duration - (hr * 3600) - (min * 60);
	
						if (hr < 10) {hr = "0" + hr; }
						if (min < 10) {min = "0" + min;}
						if (sec < 10) {sec = "0" + sec;}
						if(hr != 0 ){var durations = hr + ':' + min + ':' + sec;}
						else{var durations = min + ':' + sec;}
					}
					catch(e){var durations=duration;}				

					append_html+='<li class="videos-selectable inline-block"  id="id_'+vid+'"  >'
					append_html+='<div class="video-selectable-area"  onclick="check_selected_vimeo(\''+vid+'\',\''+image_url+'\')"><div class="thumb-wrap inline-block"><div>'
					append_html+='<input type="hidden" value="'+vid+'" name="v_id_'+vid+'" id="hdn_id_'+vid+'"/><input type="hidden" value="'+title+'" name="v_title'+vid+'" id="title_id_'+vid+'"/>'
					append_html+='<input type="hidden" value="'+escape(description)+'" name="v_description_'+vid+'"  id="desc_id_'+vid+'"/>'
					append_html+='<input type="hidden" name="durations'+vid+'"  value="'+durations+'" id = "durations_id'+vid+'">';
					append_html+='<input type="hidden" name="img_large'+vid+'"  value="'+image_url+'" id = "img_large_'+vid+'">';
					append_html+='<span class="video-thumb" id="id_video_actv_'+vid+'" disabled="disabled" >'
					append_html+='<span class="clip"><img id="vimeo-'+data.id+'" alt="Thumbnail" src="'+image_url+'"></span></span>'
					append_html+='<span class="video-duration">'+durations+'</span></div>'
					append_html+='<span class="play-icon preview-item " title="Play this video" id="id_span_play_icon_'+vid+'" onclick="play_in_lightbox_vimeo(event,\''+vid+'\')"></span></div>'
					append_html+='<div class="result-video-content">'
					append_html+='<h3 id="id_title_span_'+vid+'">'+title.slice(0,25)+'</h3>'
					append_html+='<p class="facets"><span class="video-by">by <a href="javascript:void(0)">'+uploader+'</a></span><br />'+data.no_plays+' views</p>'
				    append_html+='</div><span id="id_span_icon_tick_'+vid+'" class="icon-tick inline-block" style="display:none;"></span></div></li>'                                    
				   
				});
				$("#id_search_div_vimeo .video_list").append(append_html);
				$('#id_sel_hangitems').show();
				$('#id_search_div_vimeo .video-library .tip').css('display', 'none');
				$('#id_search_div_vimeo .video-library .hang-items').css('display', 'none');
				$('#button_hide_id').removeAttr('disabled','disabled');
			}else{
				$('#id_search_div_vimeo .video-library .tip').css('display', 'block');
				$('#id_search_div_vimeo  div.lodr').css('display', 'none');
			}	
		}
	});
}

function load_more_vimeo(sts,vurl){
	page_index=page_index+1
	var text=$('#id_search_from_yt_viemo').val();
	if($.trim(text)==''){$('#id_search_from_yt_viemo').closest('div').addClass('field-error');return false;}
	else{$('#id_search_from_yt_viemo').parent('div').removeClass('field-error');}
	status_search_viemo=sts
	var relevance = status_search_viemo
	$('#id_search_div_vimeo  div.lodr').css('display', 'block');
	$('#id_search_div_vimeo  div.tip').css('display', 'none');
	$.ajax({
		type: "GET",
		url: vurl+"?sort="+relevance+"&page="+page_index+"&q="+text,
		dataType:"json",
		success: function(response){
			var append_html= '';
			if(response){
		        $.each(response, function(i,data){
					$('#id_search_div_vimeo  div.lodr').hide();
					var title = data.title;
					var vid =data.id;
			        var description = data.description;
					var uploader = data.username;
					var image_url=data.image_url
					var duration = 	data.duration;

					try{image_url = image_url.replace('_100','_640')}
					catch(e){}
					
					try{
						var hr = Math.floor(duration / 3600);
						var min = Math.floor((duration - (hr * 3600))/60);
						var sec = duration - (hr * 3600) - (min * 60);
	
						if (hr < 10) {hr = "0" + hr; }
						if (min < 10) {min = "0" + min;}
						if (sec < 10) {sec = "0" + sec;}
						if(hr != 0 ){var durations = hr + ':' + min + ':' + sec;}
						else{var durations = min + ':' + sec;}
					}
					catch(e){var durations=duration;}				

					append_html+='<li class="videos-selectable inline-block"  id="id_'+vid+'"  >'
					append_html+='<div class="video-selectable-area"  onclick="check_selected_vimeo(\''+vid+'\',\''+image_url+'\')"><div class="thumb-wrap inline-block"><div>'
					append_html+='<input type="hidden" value="'+vid+'" name="v_id_'+vid+'" id="hdn_id_'+vid+'"/><input type="hidden" value="'+title+'" name="v_title'+vid+'" id="title_id_'+vid+'"/>'
					append_html+='<input type="hidden" value="'+escape(description)+'" name="v_description_'+vid+'"  id="desc_id_'+vid+'"/>'
					append_html+='<input type="hidden" name="durations'+vid+'"  value="'+durations+'" id = "durations_id'+vid+'">';
					append_html+='<input type="hidden" name="img_large'+vid+'"  value="'+image_url+'" id = "img_large_'+vid+'">';
					append_html+='<span class="video-thumb" id="id_video_actv_'+vid+'" disabled="disabled" >'
					append_html+='<span class="clip"><img id="vimeo-'+data.id+'" alt="Thumbnail" src="'+image_url+'"></span></span>'
					append_html+='<span class="video-duration">'+durations+'</span></div>'
					append_html+='<span class="play-icon preview-item " title="Play this video" id="id_span_play_icon_'+vid+'" onclick="play_in_lightbox_vimeo(event,\''+vid+'\')"></span></div>'
					append_html+='<div class="result-video-content">'
					append_html+='<h3 id="id_title_span_'+vid+'">'+title.slice(0,25)+'</h3>'
					append_html+='<p class="facets"><span class="video-by">by <a href="javascript:void(0)">'+uploader+'</a></span><br />'+data.no_plays+' views</p>'
				    append_html+='</div><span id="id_span_icon_tick_'+vid+'" class="icon-tick inline-block" style="display:none;"></span></div></li>'                                    
				   
				});
				$("#id_search_div_vimeo .video_list").append(append_html);
				$('#id_sel_hangitems').show();
				$('#id_search_div_vimeo .video-library .tip').css('display', 'none');
				$('#id_search_div_vimeo .video-library .hang-items').css('display', 'none');
				$('#button_hide_id').removeAttr('disabled','disabled');
			}else{
				$('#id_search_div_vimeo .video-library .tip').css('display', 'block');
				$('#id_search_div_vimeo  div.lodr').css('display', 'none');
			}	
		}
	});
}

var start_index=1;	
function next(){
	start_index=start_index+20;
	if(start_index>20){
	}
	
	searching()
}
var video_ids=[];
var vimeo_video_ids=[];
var selected_ids = [];

function check_selected(id){
	var title = $('#title_id_'+id).val();
	var description =$('#desc_id_'+id).val();
	var duration = $('#durations_id'+id).val();
	$('#id_span_icon_tick_'+id).show();
	$('#id_span_play_icon_'+id).css('pointer-events','none');
	
	$('#id_'+id).addClass('checked');
	$('#id_'+id).attr('disabled','disabled');
	$('#id_'+id).css('pointer-events','none');

	var ahtml='<li class="videos-selectable inline-block" id="sid_'+id+'" > <div class="video-selectable-area">';
    ahtml+='<input type = "hidden" name="videoids" id = "id_'+id+'" value = "'+id+'"><input type = "hidden" name="title_'+id+'" value="'+title+'" id="title_'+id+'">'
	ahtml+='<input type="hidden" name="description_'+id+'"  value="'+description+'" id = "description_'+id+'">'
	ahtml+='<input type="hidden" name="durations'+id+'"  value="'+duration+'" id = "durations'+id+'">';
    ahtml+='<div class="thumb-wrap inline-block" ><div><span class="video-thumb"><span class="clip"><img alt="Thumbnail "src="http://i2.ytimg.com/vi/'+id+'/default.jpg"></span></span><span class="video-duration">'+duration+'</span></div><span class="play-icon" title="Play video" onclick="play_in_lightbox(event,\''+id+'\')"></span></div>';
	ahtml+='<div class="result-video-content"><h3>'+title+'</h3></div>'
	ahtml+='<span class="icon-remove inline-block" onclick="remove_video(\''+id+'\')" title="Remove this video"></span></div></li>'
	$('#id_video_slider').prepend(ahtml);	
	$('#d_selected_videos_count').text(''+$('#id_video_slider li').size()+' Videos Selected');
    video_ids.push(id);
    $('#id_sel_hangitems').hide();
    if (video_ids.length>0){$('#button_hide_id').removeAttr('disabled','disabled');}
	else{$('#button_hide_id').attr('disabled','disabled');}

}

function check_selected_vimeo(id,url){
	var title = $('#title_id_'+id).val();
	var description =$('#desc_id_'+id).val();
	var duration = $('#durations_id'+id).val();
    var image_url = $('#img_large_'+id).val();
	$('#id_span_icon_tick_'+id).show();
	$('#id_span_play_icon_'+id).css('pointer-events','none');
	
	$('#id_'+id).addClass('checked');
	$('#id_'+id).attr('disabled','disabled');
	$('#id_'+id).css('pointer-events','none');

	var ahtml='<li class="videos-selectable inline-block" id="sid_'+id+'" > <div class="video-selectable-area">';
    ahtml+='<input type = "hidden" name="videoids" id = "id_'+id+'" value = "'+id+'"><input type = "hidden" name="title_'+id+'" value="'+title+'" id="title_'+id+'">'
	ahtml+='<input type="hidden" name="description_'+id+'"  value="'+description+'" id = "description_'+id+'">'
	ahtml+='<input type="hidden" name="durations'+id+'"  value="'+duration+'" id = "durations'+id+'">';
	ahtml+='<input type="hidden" name="img_large'+id+'"  value="'+image_url+'" id = "img_large_'+id+'">';
    ahtml+='<div class="thumb-wrap inline-block" ><div><span class="video-thumb"><span class="clip"><img alt="Thumbnail" src="'+url+'"></span></span><span class="video-duration">'+duration+'</span></div><span class="play-icon" title="Play video" onclick="play_in_lightbox_vimeo(event,\''+id+'\')"></span></div>';
	ahtml+='<div class="result-video-content"><h3>'+title+'</h3></div>'
	ahtml+='<span class="icon-remove inline-block" onclick="remove_video_vimeo(\''+id+'\')" title="Remove this video"></span></div></li>'
	$('#id_video_slider').prepend(ahtml);	
	$('#d_selected_videos_count').text(''+$('#id_video_slider li').size()+' Videos Selected');
    vimeo_video_ids.push(id);
    $('#id_sel_hangitems').hide();
    if (vimeo_video_ids.length>0){$('#button_hide_id').removeAttr('disabled','disabled');}
	else{$('#button_hide_id').attr('disabled','disabled');}

}

function remove_video(id){
 	$('#sid_'+id).remove();
	$('#d_selected_videos_count').text(''+$('#id_video_slider li').size()+' Videos Selected');
	$('#id_'+id).removeAttr('disabled','disabled');
	$('#id_'+id).css('pointer-events','auto');
	$('#id_span_play_icon_'+id).css('pointer-events','auto');
	video_ids.splice( $.inArray(id, video_ids), 1 );
	$('#id_'+id).removeClass('checked');
    $('#id_span_icon_tick_'+id).hide();
	if (video_ids.length == 0){
		$('#button_hide_id').attr('disabled','disabled');
		$('#id_sel_hangitems').show();
	}
	else{$('#button_hide_id').removeAttr('disabled','disabled');}
}
function remove_video_vimeo(id){
 	$('#sid_'+id).remove();
	$('#d_selected_videos_count').text(''+$('#id_video_slider li').size()+' Videos Selected');
	$('#id_'+id).removeAttr('disabled','disabled');
	$('#id_'+id).css('pointer-events','auto');
	$('#id_span_play_icon_'+id).css('pointer-events','auto');
	vimeo_video_ids.splice( $.inArray(id, vimeo_video_ids), 1 );
	$('#id_'+id).removeClass('checked');
    $('#id_span_icon_tick_'+id).hide();
	if (vimeo_video_ids.length == 0){
		$('#button_hide_id').attr('disabled','disabled');
		$('#id_sel_hangitems').show();
	}
	else{$('#button_hide_id').removeAttr('disabled','disabled');}
}
function savevideo_now(){
	var url = $('#youtube_video_add').val();
	var dataString='video_ids='+video_ids+'&vimeo_video_ids='+vimeo_video_ids;
	for(i=0;i<video_ids.length;i++){
		dataString+='&title_'+video_ids[i]+"="+$('#title_'+video_ids[i]).val();
		dataString+='&description_'+video_ids[i]+"="+$('#description_'+video_ids[i]).val();
		dataString+='&durations'+video_ids[i]+"="+$('#durations'+video_ids[i]).val();
	}
	for(i=0;i<vimeo_video_ids.length;i++){
		dataString+='&vimeo_title_'+vimeo_video_ids[i]+"="+$('#title_'+vimeo_video_ids[i]).val();
		dataString+='&vimeo_description_'+vimeo_video_ids[i]+"="+$('#description_'+vimeo_video_ids[i]).val();
		dataString+='&img_large'+vimeo_video_ids[i]+"="+$('#img_large_'+vimeo_video_ids[i]).val();
		dataString+='&durations'+vimeo_video_ids[i]+"="+$('#durations'+vimeo_video_ids[i]).val();
	}
	$.ajax({
		type: "POST",
		url: url,
		data:dataString,
		dataType:'html',
		success: function(response){
			video_ids=[];
			vimeo_video_ids=[]
			$('#share-videos').html(response);
			$.colorbox.resize();
			$.colorbox.resize({ width: "880",height:"auto",top:"5%"});
			
		},
		error:function(response){
			$('#share-videos').html(response);
		}
	});
}

function play_in_lightbox(evt,id){
	evt.stopPropagation();
	var html_var = '';
	$('.item-preview-wrapper').empty();
	html_var+='<div class="preview">';
    html_var+='<iframe  wmode="opaque" width="514px" height="289px" src="http://www.youtube.com/embed/'+id+'/?rel=0&autoplay=1&wmode=transparent" frameborder="0" allowfullscreen></iframe><span class="icon-close distroy-preview inline-block"></span>';
	html_var+='</div>';
	$('.item-preview-wrapper').append(html_var);
	$('.item-preview-wrapper').show();
}

function play_in_lightbox_vimeo(evt,id){
	evt.stopPropagation();
	var html_var = '';
	$('.item-preview-wrapper').empty();
	html_var+='<div class="preview">';
	html_var+='<iframe src="http://player.vimeo.com/video/'+id+'" width="514px" height="289px" frameborder="0" webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe><span class="icon-close distroy-preview inline-block"></span>'
	html_var+='</div>';
	$('.item-preview-wrapper').append(html_var);
	$('.item-preview-wrapper').show();
}

function addInput(){
	var text=$('#youtube_url').val();
	if($.trim(text)==''){$('#youtube_url').closest('div').addClass('field-error');return false;}
	else{$('#youtube_url').parent('div').removeClass('field-error');}
	
	var matches = $('#youtube_url').val().match(/(http|https):\/\/(?:www\.)?youtube.com\/watch\?(?=.*v=((\w|-){11}))(?:\S+)?$/);	
  	if (matches) {
		try{
	      matches=text.split('v=')[1].split('&')[0];
	      if (matches.match("^-")) {matches=text;}
	      }
	 	catch(err){matches=matches;}  
	  	var yurl='http://gdata.youtube.com/feeds/api/videos?q='+matches+'&format=5&max-results=20&v=2&alt=jsonc'; 
	  	var ahtml = '';	
	  	$.ajax({
			type: "GET",url: yurl,
			dataType:"jsonp",
			success: function(response){
				if(response.data.items){   
					$.each(response.data.items, function(i,data){
						var title = data.title;
						var views =data.viewCount;
						var vid =data.id;
				        var description = data.description;
						var duration = 	data.duration;
						
						try{
							var hr = Math.floor(duration / 3600);
							var min = Math.floor((duration - (hr * 3600))/60);
							var sec = duration - (hr * 3600) - (min * 60);
		
							if (hr < 10) {hr = "0" + hr; }
							if (min < 10) {min = "0" + min;}
							if (sec < 10) {sec = "0" + sec;}
							if(hr != 0 ){var durations = hr + ':' + min + ':' + sec;}
							else{var durations = min + ':' + sec;}
						}
						catch(e){var durations=duration;}

						$('#id_title').val(title) ;
						$('#id_description').val(description);
						var ahtml='<li class="videos-selectable inline-block" id="sid_'+vid+'" > <div class="video-selectable-area">';
					    ahtml+='<input type = "hidden" name="videoids" id = "id_'+vid+'" value = "'+vid+'"><input type = "hidden" name="title_'+vid+'" value="'+title+'" id="title_'+vid+'">'
						ahtml+='<input type="hidden" name="description_'+vid+'"  value="'+description+'" id = "description_'+vid+'">'
						ahtml+='<input type="hidden" name="durations'+vid+'"  value="'+durations+'" id = "durations'+vid+'">';
					    ahtml+='<div class="thumb-wrap inline-block"><div><span class="video-thumb"><span class="clip"><img alt="Thumbnail "src="http://i2.ytimg.com/vi/'+vid+'/default.jpg"></span></span><span class="video-duration">'+durations+'</span></div><span class="play-icon" title="Play video" onclick="play_in_lightbox(event,\''+vid+'\')"></span></div>';
						ahtml+='<div class="result-video-content"><h3>'+title+'</h3></div>'
						ahtml+='<span class="icon-remove inline-block" onclick="remove_video(\''+vid+'\')" title="Remove this video"></span></div></li>'
						
						$('#id_sel_hangitems ').css('display', 'none');
						$('#button_hide_id').removeAttr('disabled','disabled');
						$('#id_video_slider').prepend(ahtml);	
						$('#d_selected_videos_count').text(''+$('#id_video_slider li').size()+' Videos Selected');
						video_ids.push(vid);
					});
					$("#id_video_slider").prepend(ahtml);
					$('#id_selected_videos_count').text('Total selected videos ('+$('#id_video_slider li').size()+')');// jus to count how many videos are in the slider
					$('#youtube_url').val('');
				}
			}
		});
	}else {
		alert(gettext('Please Enter a valid url'));
		$('#youtube_url').val('');
		return false;
	}
}
function addInput_vimeo(){
	var text=$('#viemo_url').val();
	if($.trim(text)==''){$('#viemo_url').closest('div').addClass('field-error');return false;}
	else{$('#viemo_url').parent('div').removeClass('field-error');}
	
	var matches = $('#viemo_url').val().match(/^(http|https):\/\/(?:www\.|player\.)?(vimeo)\.com\/(watch\?[^#]*v=(\w+)|(\d+)).+$/);
	var video_id=text.split('.com/')
	video_id=video_id[1].split('/')
	video_id=video_id[0]
  	if (matches) {
	  	var yurl='http://vimeo.com/api/v2/video/'+video_id+'.json'; 
	  	var ahtml = '';	
	  	$.ajax({
			type: "GET",url: yurl,
			dataType:"jsonp",
			success: function(response){
				if(response[0]){	
					var title = response[0].title;
					var vid =response[0].id;
			        var description = escape(response[0].description);
					var uploader = response[0].user_name;
					var image_url=response[0].thumbnail_small
					var img_large = response[0].thumbnail_large;
					var duration = response[0].duration;
					
					try{
						var hr = Math.floor(duration / 3600);
						var min = Math.floor((duration - (hr * 3600))/60);
						var sec = duration - (hr * 3600) - (min * 60);
	
						if (hr < 10) {hr = "0" + hr; }
						if (min < 10) {min = "0" + min;}
						if (sec < 10) {sec = "0" + sec;}
						if(hr != 0 ){var durations = hr + ':' + min + ':' + sec;}
						else{var durations = min + ':' + sec;}
					}
					catch(e){var durations=duration;}				

					var ahtml='<li class="videos-selectable inline-block" id="sid_'+vid+'" > <div class="video-selectable-area">';
				    ahtml+='<input type = "hidden" name="videoids" id = "id_'+vid+'" value = "'+vid+'"><input type = "hidden" name="title_'+vid+'" value="'+title+'" id="title_'+vid+'">'
					ahtml+='<input type="hidden" name="img_large'+vid+'"  value="'+img_large+'" id = "img_large_'+vid+'">';
					ahtml+='<input type="hidden" name="durations'+vid+'"  value="'+durations+'" id = "durations'+vid+'">';
					ahtml+='<input type="hidden" name="description_'+vid+'"  value="'+description+'" id = "description_'+vid+'">'
				    ahtml+='<div class="thumb-wrap inline-block"><div><span class="video-thumb"><span class="clip"><img alt="Thumbnail "src="'+image_url+'"></span></span><span class="video-duration">'+durations+'</span></div><span class="play-icon" title="Play video" onclick="play_in_lightbox_vimeo(event,\''+vid+'\')"></span></div>';
					ahtml+='<div class="result-video-content"><h3>'+title+'</h3></div>'
					ahtml+='<span class="icon-remove inline-block" onclick="remove_video_vimeo(\''+vid+'\')" title="Remove this video"></span></div></li>'
					
					$('#id_sel_hangitems ').css('display', 'none');
					$('#button_hide_id').removeAttr('disabled','disabled');
					$('#id_video_slider').prepend(ahtml);	
					$('#d_selected_videos_count').text(''+$('#id_video_slider li').size()+' Videos Selected');
					vimeo_video_ids.push(vid);
					$('#id_selected_videos_count').text('Total selected videos ('+$('#id_video_slider li').size()+')');// just to count how many videos are in the slider
					$('#viemo_url').val('');
				}else {
					alert(gettext('Please Enter a valid url'));
					$('#viemo_url').val('');
					return false;
				}
			}
		});
	}else {
		alert(gettext('Please Enter a valid url'));
		$('#viemo_url').val('');
		return false;
	}
}
function statics_seo(id){
	var url=$('#ajax_add_seo').val();
	dataString = 'video-id='+id;
	$.ajax({
         type:"POST",	
		 url:url,
		 data:dataString,
		 success:function(response){
		 	$('.seo-video').html(response);
		 },
		 error:function(response){
		 	alert('somthing  wrong');
		 }
	});
}			

function get_video_status(status){
if(status=='all'){
	$('#id_status_all').addClass('active');
	$('#id_status_mine').removeClass('active');
}else{
	$('#id_status_mine').addClass('active');	
	$('#id_status_all').removeClass('active');
}
var url= $('#id_video_status_url').val();
$("#id_module_state_listing").hide();
$("#ajax_loading").show();
$.ajax({
		   type: "GET",
		   url: url,
		   data:'status='+status,
		   success: function(html_from_server){	
		   		$("#ajax_loading").hide();
				$("#ajax_content_loading").hide();
				$("#id_module_state_listing").empty().html(html_from_server);
				$("#id_module_state_listing").fadeIn(300);
			}
});
}

function video_action_confirm(value){
			var selected = false;
			$('.cbox:checked').each(function(){
				selected=true
			});
			if(selected){
				if(value=='delete'){
						if(confirm('Are you sure you want to delete the selected video(s)?')){video_action(value); return false;}
					}
					else if(value=='activate'){
						if(confirm('Are you sure you want to publish the selected video(s)?')){video_action(value); return false;}
					}
					else if(value=='deactivate'){
						if(confirm('Are you sure you want to keep selected video(s) in pending ?')){video_action(value); return false;}
					}
					else if (value=='blocked'){
						if (confirm('Are you sure you want to block the selected video(s) ?')){video_action(value); return false;}
					}
					else if (value=='featured'){
						if (confirm('Are you sure you want to featured the selected video(s)')){video_action(value); return false;}
					}
			}else{
				alert("Please select the Video(s) !");
			}	
		}
function video_action(value)
	  {	
	  	$("#id_video_listing").hide();
	  	$("#ajax_content_loading").show()
	  	var url= $('#id_hidden_url').val();
	  		var ids=[]
	  	$('.cbox:checked').each(function(){
	  		ids.push($(this).val());
	  	});
	  		dataString = 'ids='+ids+'&selvalue='+value+'&status='+$('#id_status').val()+'&listing='+$('#id_listing_type').val()+'&created='+$('#id_created').val()+'&sort='+$('#id_sort').val()+'&page='+$('#id_pagentn').val()+'&item_perpage='+$('#id_item_per_page').val();
	  		$.ajax({
	  			   type: "GET",
	  			   url: url,
	  			   data:dataString,
	  			    success: function(html_from_server){	
	  					$("#ajax_content_loading").hide();
	  					$("#video_id").remove();
	  			   		$("#id_video_listing").html(html_from_server);
	  			   		$("#id_video_listing").fadeIn(300);
	  			   		$('#id_from_to').text($('#id_from_to_range').val());
	  					$('#top_item_count').text($('#id_count').val());
	  					show_msg($('#id_action_msg').val(),'s');
	  				}
	  		});
	  	
	  }
	  

function get_video_status(status){
	if(status=='all'){
		$('#id_status_all').addClass('active');
		$('#id_status_mine').removeClass('active');
	}else{
		$('#id_status_mine').addClass('active');	
		$('#id_status_all').removeClass('active');
	}
	var url= $('#id_video_status_url').val();
	$("#id_module_state_listing").hide();
	$("#ajax_loading").show();
	$.ajax({
			   type: "GET",
			   url: url,
			   data:'status='+status,
			   success: function(html_from_server){	
			   		$("#ajax_loading").hide();
					$("#id_module_state_listing").empty().html(html_from_server);
					$("#id_module_state_listing").fadeIn(300);
				}
	});
}

function play_lightbox(id){
	var html_var = '';
	$('.item-preview-wrapper').empty();
	html_var+='<div class="preview">';
    html_var+='<iframe  wmode="opaque" width="514px" height="289px" src="http://www.youtube.com/embed/'+id+'/?rel=0&autoplay=1&wmode=transparent" frameborder="0" allowfullscreen></iframe><span class="icon-close distroy-preview inline-block"></span>';
	html_var+='</div>';
	$('.item-preview-wrapper').append(html_var);
	$('.item-preview-wrapper').show();
}	
function play_lightbox_vimeo(id){
	var html_var = '';
	$('.item-preview-wrapper').empty();
	html_var+='<div class="preview">';
	html_var+='<iframe src="http://player.vimeo.com/video/'+id+'?api=1&autoplay=1" width="514px" height="289px" frameborder="0" webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe><span class="icon-close distroy-preview inline-block"></span>';
	html_var+='</div>';
	$('.item-preview-wrapper').append(html_var);
	$('.item-preview-wrapper').show();
}
// ************************************ Clearing Search 
function clear_adv_srchfields(){
	$('select#search_type').val("").trigger("liszt:updated");
	$('#id_search_start_date').val("");
	//$('#id_search_end_date').val("");
	$('.search_adv2').val("");
	$('#search_category').val("").trigger("liszt:updated");
	$('#search_status').val("").trigger("liszt:updated");
	
	$('#bottom_search_button').attr('disabled','disabled');
}

				
				
				
				
