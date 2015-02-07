$(document).ready(function(){

    if ($("#id_start_date").length) {
        $("#id_start_date").datepicker({
            dateFormat: "dd/mm/yy",
            minDate: new Date()
			,onSelect: function() { $(this).valid(); }
        });
    }
    if ($("#id_end_date").length) {
        $("#id_end_date").datepicker({
            dateFormat: "dd/mm/yy",
            minDate: new Date(),
			onSelect: function() { $(this).valid(); }
        });
    }
    if ($("#id_search_start_date").length) {
        $("#id_search_start_date").datepicker({
            dateFormat: "dd/mm/yy"
        });
    }
    if ($("#id_search_end_date").length) {
        $("#id_search_end_date").datepicker({
            dateFormat: "dd/mm/yy"
        });
    }
    if ($("#id_listing_start").length) {
        $("#id_listing_start").datepicker({
            dateFormat: "dd/mm/yy",
            minDate: new Date()
        });
    }
    if ($("#id_listing_end").length) {
        $("#id_listing_end").datepicker({
            dateFormat: "dd/mm/yy",
            minDate: new Date()
        });
    }
    
    
    //scheduler_load();
    
    $(".day_names").click(function(){
        show_hide_day_timings();
    });
    
    $('.listing_type_val:checked').each(function(){
        if ($(this).val() == 'B') {
            $('#id_listing_price_span').hide();
        }
    });
    
    $('#filter_a a').click(function(){
        $('#id_status').val($(this).attr('name'));
        
        if (!$(this).hasClass('active')) {
            $('#filter_a a').removeClass('active');
            $(this).addClass('active');
        }
        filter_content();
        
    });
    $('#filter_b a').click(function(){
        $('#id_listing_type').val($(this).attr('name'));
        
        if (!$(this).hasClass('active')) {
            $('#filter_b a').removeClass('active');
            $(this).addClass('active');
        }
        filter_content();
    });
    
}); // Document ready end 
function filter_content(){
    var ids = []
    var dataString = '';
    var url = $('#id_hidden_url').val();
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
        dataString += "&kwd=" + $('#id_search_keyword').val();
        dataString += "&type=" + $('#search_type').val();
        dataString += "&start_date=" + $('#id_search_start_date').val();
        dataString += "&end_date=" + $('#id_search_end_date').val();
        dataString += "&cat=" + $('#search_category').val();
        if ($('#search_status').val() != '' && $('#search_status').val() != null) {
            dataString += "&srch_status=" + $('#search_status').val();
        }
    }
    if ($('#id_action').val() != '0' && $('#id_action').val() != '') {
        $('.cbox:checked').each(function(){
            ids.push($(this).val());
        });
        dataString += "&action=" + $('#id_action').val();
        dataString += "&ids=" + ids;
    }
    //alert(dataString);
    $('#id_content_listing').hide();
    $('#ajax_content_loading').show();
    hide_top_info_bar();
    $.ajax({
        type: "GET",
        url: url,
        data: dataString,
        dataType: 'JSON',
        success: function(data){
        	show_top_info_bar('Events');
            $('#id_pagentn').val('');
            $('#id_action').val('');
            $('#ajax_content_loading').hide();
            $('#id_content_listing').empty().html(data.html);
            $('#id_content_listing').show();
            
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
			$(".bm-business-listing").colorbox({width: "880", initialWidth: "880",initialHeight: "200", top:"5%",title:function(){return getLBTitle($(this));}});
            $('.light_box').colorbox({
                width: "560",
                initialWidth: "560",
                top: "60",
                initialHeight: "200"
            });
        }
    });
}

function filter_action(ids, action){
    var all_ids = [];
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
        dataString += "&kwd=" + $('#id_search_keyword').val();
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
    $('.cbox').each(function(){
        all_ids.push($(this).val());
    });
    dataString += "&ids=" + ids;
    dataString += "&all_ids=" + all_ids;
    $('#ajax_action_loading').show();
    hide_top_info_bar();
    $.ajax({
        type: "GET",
        url: url,
        data: dataString,
        dataType: 'JSON',
        success: function(data){
        	show_top_info_bar('Events');
            $("#master_check").attr('checked', false);
            $('#ajax_action_loading').hide();
            
            $('#actionSelect').val("").trigger("liszt:updated");
            
            $('#id_action').val('');
            try {
                for (i = 0; i < ids.length; i++) {
                    $('#li_' + ids[i]).remove();
                }
                $('#li_' + ids).remove();
            } 
            catch (e) {
                $('#li_' + ids).remove();
            }
            //$('#pagination').remove();
            $('#ajax_content_list').append(data.html);
            $('#pagenation').empty().html(data.pagination);
            show_msg(data.msg, data.mtype);
            
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
            show_count('all');
            $('.light_box').colorbox({
                width: "560",
                initialWidth: "560",
                top: "60",
                initialHeight: "200"
            });
        }
    });
}

function action(){
    var flag = false;
    var flag_action = false;
    if ($('#id_action').val() != '0') {
        $('.cbox:checked').each(function(){
            flag = true;
        });
        if (flag) {
            if ($('#id_action').val() == 'DEL') {
                if (confirm(gettext('Are you sure you want to delete selected event(s) ?'))) {
                    flag_action = true;
                }
            }
            if (flag_action) {
                filter_action(0, '#');
            }
        }
        else {
            $('#actionSelect').val("").trigger("liszt:updated");
            alert(gettext('Please select event(s)'));
        }
    }
}

function show_count(value){
    $('.statefltr').removeClass('active');
    $('#id_status_' + value).addClass('active');
    var count_url = $('#id_event_status_url').val();
    $.ajax({
        type: "GET",
        url: count_url,
        data: 'status=' + value,
        dataType: 'JSON',
        success: function(data){
            $('#id_pend').html(data.pending);
            $('#id_pub').html(data.published);
            $('#id_rej').html(data.rejected);
            $('#id_exp').html(data.expired);
			$('#id_drft').html(data.drafted);
            $('#id_blk').html(data.blocked);
            $('#id_tot').html(data.total);
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
    	hm_sort()
}
function hm_sort(){
	$('#id_pagentn').val('1')
	filter_content();
}
function clear_adv_srchfields(){
    $('select#search_type').val("").trigger("liszt:updated");
    $('#id_search_start_date').val("");
    $('#id_search_end_date').val("");
    $('#search_category').val("").trigger("liszt:updated");
    $('#search_status').val("").trigger("liszt:updated");
}
function free_event1()
		{	
			if($('#id_free_Event').attr('checked')){
				$('#id_tkt_prize').attr('disabled','disabled');
				$('#id_tkt_prize').val('');
				$('#id_ticket_site').attr('disabled','disabled');
				$('#id_ticket_site').val('');
				$('#id_tkt_phone').attr('disabled','disabled');
				$('#id_tkt_phone').val('');
		
			}
			else{
				$('#id_tkt_prize').removeAttr('disabled');
				$('#id_ticket_site').removeAttr('disabled','disabled');
				$('#id_tkt_phone').removeAttr('disabled','disabled');
			}		
		}

