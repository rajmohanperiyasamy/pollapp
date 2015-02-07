$(document).ready(function(){
	get_rsvp_user_status();	
	try{$(".fxslider").fxslider();}
	catch(e){}
});

function show_toggle(){
	$('#less_synopsis').toggle();
	$('#more_synopsis').toggle();
}

function imgoing(id,cnt){
	var cnt = cnt + 1;
	$.ajax({
			   type: "GET",
			   url: "{% url events_go_event %}",
			   data:"eid="+id,
			   success: function(html_from_server){
			   		if (html_from_server=='working'){
						$('#nofppl').html('('+cnt);
					}
			   		$('#mostcommented').empty().html(html_from_server);
			   }
		});
}

function add_to_fav(id){
	$('.alert_flash').hide();
	$.ajax({
		type:'get',
		url:'{% url event_add_to_fav %}',
		data:'id='+id,
		success:function(data){
			if(data=='1'){ $('#flash_alert').show();}
			else if(data=='2'){$('#flash_alert1').show();}
			else{alert(gettext('Oops!!! Not able to process your request.'))}
		}
		});
}

function update_event_rsvp(sval){
	$('#id_selected_rsvp_status').val(sval);
	check_login();
}



function check_login(){
	if(uaflag){event_rsvp();}
	//else{$.colorbox({width: "722",initialWidth: "722", top:"5%", initialHeight: "200", href:'/account/ajax-signin/?type=rsvp', onOpen:function(){$("#colorbox").addClass("no_title");} });}
}

function event_rsvp(){
 var url = rsvp_url;
 uaflag = true;
 $.ajax({
        	type: "GET",
			url:url,
			data:'status='+$('#id_selected_rsvp_status').val(),
			dataType:'json',
			success: function(data){
				if(data.success){
					$('#id_rsvp_list').empty().html(data.html);
					$('#id_sel_rsvp_status').bUiSlCt({style: 'btn-primary'});
					$('#id_rsvp_going_count').html(data.going_count);
					$('#id_rsvp_mb_count').html(data.maybe_count);	
				    }
			}
		});
}

function get_rsvp_user_status(){
	 var url = rsvp_status_url;
	 $.ajax({
	        	type: "GET",
				url:url,
				data:'0',
				dataType:'json',
				success: function(data){
					if(data.success){
						 $('#id_rsvp_list').empty().html(data.html);
					     $('#id_sel_rsvp_status').bUiSlCt({style: 'btn-primary'});
						 $('#id_rsvp_going_count').html(data.going_count);
						 $('#id_rsvp_mb_count').html(data.maybe_count);			
					    }
				    else{$('#id_rsvp_going_count').html(data.going_count);$('#id_rsvp_mb_count').html(data.maybe_count);}	
				}
			
			});
}