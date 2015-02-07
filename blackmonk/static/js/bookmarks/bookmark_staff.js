$(document).ready(function(){

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

});  // Document ready end 

///// BOOKMARK LISTING FILTERING
function filter_content(){
	var ids=[]
	var dataString='';
	var url= $('#id_listbookmark_url').val();
	dataString+="sort="+$('#id_sort').val();
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
			dataString+="&srch_status="+$('#search_status').val();
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
			show_top_info_bar('Bookmarks');
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
function filter_action(ids,action){
	var all_ids=[];
	var dataString='';
	
	var url= $('#id_action_url').val();
	dataString+="sort="+$('#id_sort').val();
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
			dataString+="&srch_status="+$('#search_status').val();
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
		show_top_info_bar('Bookmarks');
			$("#master_check").attr('checked',false);
			$('.cbox').attr('checked',false);
			$('#ajax_action_loading').hide();
			
			$('#actionSelect').val("").trigger("liszt:updated");
			$('#id_action').val('');
			
			if(data.status==1){
				try{for(i=0;i<ids.length;i++){$('#li_'+ids[i]).remove();}$('#li_'+ids).remove();}
				catch(e){$('#li_'+ids).remove();}
				$('#ajax_content_list').append(data.html);
				$('#pagenation').empty().html(data.pagination);
			}
			show_msg(data.msg,data.mtype);
			if(data.search){$('#close_search').show();}
			
			if(data.status==1){
				if(data.next){$('#top_pge_next').removeClass('inactive');}
				else{$('#top_pge_next').addClass('inactive');}
				if(data.previous){$('#top_pge_previous').removeClass('inactive');}
				else{$('#top_pge_previous').addClass('inactive');}
				show_count('all');
				$('#id_from_to').html(data.pagerange);
				$('#top_item_count').html(data.count);
				$('.light_box').colorbox({width: "560",initialWidth: "560", top:"60", initialHeight: "200"});
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
function hm_search(){
    clear_for_search();
	hm_sort();
}
function hm_sort(){
	$('#id_pagentn').val('1')
	filter_content();
}
function show_count(value){
	$('#ajax_loading').show();
	$('.statefltr').removeClass('active');
	$('#id_status_'+value).addClass('active');
	var count_url = $('#id_bookmark_status_url').val();
	$.ajax({
	type: "GET",
	url: count_url,
	data: 'status='+value,
	dataType:'JSON',
	success: function(data){
			$('#ajax_loading').hide();
			$('#id_pend').html(data.pending);
			$('#id_pub').html(data.published);
			$('#id_rej').html(data.rejected);
			$('#id_blk').html(data.blocked);
			$('#id_tot').html(data.total);
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
		if(flag){
			if($('#id_action').val()=='DEL'){
				if(confirm(gettext('Are you sure you want to delete selected bookmark(s) ?'))){flag_action=true;}
			}
			if($('#id_action').val()=='P'){
				if(confirm(gettext('Are you sure you want to Publish selected bookmark(s) ?'))){flag_action=true;}
			}
			if($('#id_action').val()=='R'){
				if(confirm(gettext('Are you sure you want to Reject selected bookmark(s) ?'))){flag_action=true;}
			}
			if($('#id_action').val()=='B'){
				if(confirm(gettext('Are you sure you want to Block selected bookmark(s) ?'))){flag_action=true;}
			}
			if(flag_action){filter_action(0,'#');}
		}else{
			alert('Please select bookmark(s)')
		}
	}
}
//// Manage Slug 
	var var_editslug=1;
	function fillslug(data){
		data = slugify(data)
		if(var_editslug==1){
			window.document.getElementById('id_slug').value=data;
		}
	}
	function slugify(text) {
       text=text.toLowerCase();	
       text = text.replace(/[^-a-zA-Z0-9,&\s]+/ig, '');
       text = text.replace(/-/gi, "_");
       text = text.replace(/\s/gi, "-");
       return text;
	}
	function fillslug_add(data){
		data = data.replace(/ /g, "-");
		if(var_editslug==1){
			window.document.getElementById('id_slug').value=data;
		}
	}