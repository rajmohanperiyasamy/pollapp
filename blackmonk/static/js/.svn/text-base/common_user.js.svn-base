
function call_the_filter(){
	var filterval=$("#filter_by").val();
	if(filterval == 'N' || filterval == 'P' || filterval == 'D' || filterval == 'R' || filterval == 'B' || filterval == 'E' || filterval == 'S'){
		$('#id_status').val(filterval);
		$('#id_listing_type').val("all");
		$('#id_entry_type').val('')
	}else if(filterval == 'Q' || filterval == 'W' || filterval == 'T'){
		if(filterval == 'W'){
			$('#id_entry_type').val('A');
		}else if(filterval == 'T'){
			$('#id_entry_type').val('P');					
		}else{
			$('#id_entry_type').val(filterval);
		}
		$('#id_listing_type').val("all");
	}else if(filterval == 'F' || filterval == 'O' || filterval == 'Y') {
		if(filterval == 'Y'){
			$('#id_listing_type').val('B');
		}else if(filterval == 'O'){
			$('#id_listing_type').val('S');
		}else{
			$('#id_listing_type').val(filterval);
		}
		$('#id_status').val("");
	}else if(filterval == '-created_on' || filterval == 'created_on' || filterval == '-visits' || filterval == "-most_viewed" || filterval == "-viewed" || filterval == "-video_view") {
		$('#id_sort').val(filterval);
		$('#id_pagentn').val('1')
		$('#id_status').val("");
		$('#id_listing_type').val("all");
	}
	filter_content();
}

function filter_content(){
    var ids = []
    var dataString = '';
    var url = $('#id_hidden_url').val();
    
    dataString += "sort=" + $('#id_sort').val();
    dataString += "&listing=" + $('#id_listing_type').val();
    if ($('#id_entry_type').val() != '' && $('#id_entry_type').val() != null) {
        dataString += "&entry_type=" + $('#id_entry_type').val();
    }
    if ($('#id_status').val() != '' && $('#id_status').val() != null) {
        dataString += "&status=" + $('#id_status').val();
    }
    if ($('#id_pagentn').val() != '' && $('#id_pagentn').val() != null) {
        dataString += "&page=" + $('#id_pagentn').val();
    }
    if ($('#id_item_per_page').val() != '' && $('#id_item_per_page').val() != null) {
        dataString += "&item_perpage=" + $('#id_item_per_page').val();
    }
    if ($('#id_search').val() != '' && $('#id_search').val() != null) {
        dataString += "&search=true";
        dataString += "&kwd=" + $('#content_search').val();
        dataString += "&type=";
    }
    
    if ($('#id_action').val() != '0' && $('#id_action').val() != '') {
        $('.cbox:checked').each(function(){
            ids.push($(this).val());
        });
        dataString += "&action=" + $('#id_action').val();
        dataString += "&ids=" + ids;
    }
    //alert(dataString);
    $('#id_content_listing').addClass('oP50');
    $.ajax({
        type: "GET",
        url: url,
        data: dataString,
        dataType: 'JSON',
        success: function(data){
            $('#id_pagentn').val('');
            $('#id_action').val('');
            $('#id_content_listing').empty().html(data.html);
            $('#id_content_listing').removeClass('oP50');
            $('#total_count').html(data.total);
            if (data.search) {
                $('#close_search').show();
            }
            if (data.next) {
                $('#top_pge_next').removeClass('inactive');
            }
            else {
                $('#top_pge_next').addClass('inactive');
            }
            if (data.previous) {
                $('#top_pge_previous').removeClass('inactive');
            }
            else {
                $('#top_pge_previous').addClass('inactive');
            }
            $('#id_from_to').html(data.pagerange);
            $('#top_item_count').html(data.count);

			// following line is to enhance image quality
			setTimeout(function(){
				$('.fLxiMgW').setrSpVWidth(0);
			});
			$('html,body').animate({ scrollTop: 0 }, 'slow');
        }
    });
}

function hm_sort(){
	$('#id_sort').val("-created_on");
	$('#id_pagentn').val('1')
	$('#id_status').val("all");
	$('#id_listing_type').val("all");
	filter_content();
}

function clear_search(){
    $('#id_search').val('');
    $('#id_pagentn').val('1')
    filter_content();
}

function filter_action(ids, action){
    var dataString = '';
    
    var url = $('#id_action_url').val();
    dataString += "sort=" + $('#id_sort').val();
    dataString += "&listing=" + $('#id_listing_type').val();
    if ($('#id_status').val() != '' && $('#id_status').val() != null) {
        dataString += "&status=" + $('#id_status').val();
    }
    if ($('#id_pagentn').val() != '' && $('#id_pagentn').val() != null) {
        dataString += "&page=" + $('#id_pagentn').val();
    }
    if ($('#id_item_per_page').val() != '' && $('#id_item_per_page').val() != null) {
        dataString += "&item_perpage=" + $('#id_item_per_page').val();
    }
    if ($('#id_search').val() != '' && $('#id_search').val() != null) {
        dataString += "&search=true";
        dataString += "&kwd=" + $('#content_search').val();
        dataString += "&type=" + $('#search_type').val();
        dataString += "&start_date=" + $('#id_search_start_date').val();
        dataString += "&end_date=" + $('#id_search_end_date').val();
        dataString += "&cat=" + $('#search_category').val();
        if ($('#search_status').val() != '' && $('#search_status').val() != null) {
            dataString += "&srch_status=" + $('#search_status').val();
        }
    }
    if (action == '#') {
        dataString += "&action=" + $('#id_action').val();
        if (ids == 0) {
            var ids = [];
            $('.cbox:checked').each(function(){
                ids.push($(this).val());
            });
        }
    }
    else {
        dataString += "&action=" + action;
    }
	if($('#id_module').val() == 'community'){
		$('#id_del_'+ids).hide();
		$('#id_lod_'+ids).show();
	}else{
		$('#id_delete_'+ids).hide();
		$('#id_loding_'+ids).show();
		$('#id_drop_'+ids).addClass('dSbLd');
	}
	
    dataString += "&ids=" + ids;
    $('#ajax_action_loading').show();
    $.ajax({
        type: "GET",
        url: url,
        data: dataString,
        dataType: 'JSON',
        success: function(data){
            //$('#ajax_action_loading').hide();
            if($('#id_module').val() == 'community'){
				$('#id_lod_'+ids).hide();
				$('#id_del_'+ids).show();
			}else{
				$('#id_loding_'+ids).hide();
				$('#id_delete_'+ids).show();
				$('#id_drop_'+ids).removeClass('dSbLd');
			}
            $('#id_content_listing').html(data.html);
			$('#total_count').html(data.total);   
            if (data.search) {
                $('#close_search').show();
            }
            show_msg(data.msg,data.mtype);
            if (data.next) {
                $('#top_pge_next').removeClass('inactive');
            }
            else {
                $('#top_pge_next').addClass('inactive');
            }
            if (data.previous) {
                $('#top_pge_previous').removeClass('inactive');
            }
            else {
                $('#top_pge_previous').addClass('inactive');
            }
            $('#id_from_to').html(data.pagerange);
            $('#top_item_count').html(data.count);
        }
    });
}
