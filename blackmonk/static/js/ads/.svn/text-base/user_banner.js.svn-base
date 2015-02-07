$(document).ready(function(){
	$('.tool.action_status .chzn-container').addClass('chzn-disabled , disabled_chosen');
	/*{% if recent %}
			$('#id_status').val('N');
			$('#filter_a a').removeClass('active');
			$('#listing_pending').addClass('active');
			filter_content();
	{% endif %}*/
	
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
	$('#master_check').click(function(){
		if($("#master_check").is(':checked')){$(".cbox").attr('checked',true);}
		else{$(".cbox").attr('checked',false);}
	});
});


function clear_adv_srchfields(){
	$('select#search_type').val("").trigger("liszt:updated");
	$('#search_category').val("").trigger("liszt:updated");
	//$('#search_status').val("").trigger("liszt:updated");
}

function filter_action(ids,action){
	var all_ids=[];
	var dataString='';
    var url = $('#id_banner_action_url').val();
	
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
	$('#id_delete_'+ids).hide();
	$('#id_loding_'+ids).show();
	$('#id_drop_'+ids).addClass('dSbLd');
	dataString+="&ids="+ids;
	dataString+="&all_ids="+all_ids;
	$('#ajax_action_loading').show();
	$.ajax({
	type: "get",
	url: url,
	data: dataString,
	dataType:'json',
	success: function(data){
			$('#id_loding_'+ids).hide();
			$('#id_delete_'+ids).show();
			$('#id_drop_'+ids).removeClass('dSbLd');
			$('#id_pagentn').val('');
			$('#id_action').val('');
			$('#ajax_content_loading').hide();
			$('#total_count').html(data.total);
			show_msg(data.msg,data.mtype);
			$('#id_content_listing').empty().html(data.html);
			$('#id_content_listing').show();
			if(data.search){$('#close_search').show();}
			if(data.next){$('#top_pge_next').removeClass('inactive');}
			else{$('#top_pge_next').addClass('inactive');}
			if(data.previous){$('#top_pge_previous').removeClass('inactive');}
			else{$('#top_pge_previous').addClass('inactive');}
			$('#id_from_to').html(data.pagerange);
			$('#top_item_count').html(data.count);
			show_count('all');
			
		}
	});
}
function filter_content(){
	var ids=[]
	var dataString='';
	var url = $('#id_banner_listing_url').val();
	
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
	}
	if($('#id_action').val()!='0' && $('#id_action').val()!=''){
		$('.cbox:checked').each(function(){
			ids.push($(this).val());
		});
		dataString+="&action="+$('#id_action').val();
		dataString+="&ids="+ids;
	}
	$('#ajax_content_cls').hide();
	$('#ajax_content_loading').show();
	$.ajax({
	type: "GET",
	url: url,
	data: dataString,
	dataType:'JSON',
	success: function(data){
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
			$('.light_box').colorbox({width: "560",initialWidth: "560", top:"5%", initialHeight: "200"});
			$(".bm-create-gallery").colorbox({width: "880", initialWidth: "880", top:"5%"});
		}
	});
}

function custom_clear_top_info_bar(){
	$('#id_search').val('');
	$('#id_search_keyword').val('');
	$('#id_pagentn').val('1');
	
	$('#id_status').val('all');
	$('#id_listing_type').val('all');
	$('#id_created').val('all');
	
	$('#filter_a a').removeClass('active');
	$('#filter_b a').removeClass('active');
	$('#filter_c a').removeClass('active');
	
	$('#filter_a .first').addClass('active');
	$('#filter_b .first').addClass('active');
	$('#filter_c .first').addClass('active');
	
	$('#top_info_bar').hide();
}

function show_count(value){
	var url=$('#id_banner_state_url').val();
	$('#ajax_loading').show();
	$('.statefltr').removeClass('active');
	$('#id_status_'+value).addClass('active');
	$.ajax({
	type: "GET",
	url: url,
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
/*function clear_search(){
	$('#id_search').val('');
	$('#id_search_keyword').val('');
	$('#close_search').hide();
	$('#id_pagentn').val('1');
	$("#search_status option:first").attr('selected','selected')
	filter_content();
}*/
function sort_search(){
	clear_for_search();
	sort_content()
}
function sort_content(){
	$('#id_pagentn').val('1')
	filter_content();
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
				 if(confirm(gettext('Are you sure you want to delete banner(s) ?'))){flag_action=true;}
			}
			if($('#id_action').val()=='P'){
				if(confirm(gettext('Are you sure you want to Publish banner(s) ?'))){flag_action=true;}
			}
			if($('#id_action').val()=='B'){
				if(confirm(gettext('Are you sure you want to Block banner(s) ?'))){flag_action=true;}
			}
			if(flag_action){filter_action(0,'#');}
		}else{
			alert('Please select banner(s)');
		}
	}
}

function file_upload_buz(url,limit,uploadTemplateId,downloadTemplateId) {
    'use strict';
    // Initialize the jQuery File Upload widget:
    $('#fileuploaddoc').fileupload({
 	   //dropZone:$("#bm-dropzone"),
 	   sequentialUploads:true,
	   maxNumberOfFiles:limit,
	   autoUpload:true,
	   uploadTemplate:$('#'+uploadTemplateId),
	   downloadTemplate:$('#'+downloadTemplateId),
	   url:url,
	   acceptFileTypes:/(\.|\/)(jpe?g|png|x-png|pjpeg|docx?|pdf)$/i
    });
	
 // Load existing files:
   get_files(url)
    // Open download dialogs via iframes,
    // to prevent aborting current uploads:
    $('#fileuploaddoc .files a:not([target^=_blank])').live('click', function (e) {
        e.preventDefault();
        $('<iframe style="display:none;"></iframe>')
            .prop('src', this.href)
            .appendTo('body');
    });
}
function get_files(url){
	var noCache = Date();
	 $.getJSON(url, { "noCache": noCache }, function (files) {
	        var fu = $('#fileuploaddoc').data('fileupload');
	        fu._adjustMaxNumberOfFiles(-files.length);
	        fu._renderDownload(files)
	            .appendTo($('#fileuploaddoc .files'))
	            .fadeIn(function () {
	                // Fix for IE7 and lower:
	                $(this).show();
	            });
	    });
}

