function poll_voting(elmnt){

		if ($("#status").val() == 'voted' && $(elmnt).attr('id') != 'view_results') {
			alert('You have already voted.?');
			
		}
		the_value = $('#poll_form input:radio:checked').val();
		if (!the_value) {
			var the_value = '';
			$('.poll_input').each(function(){
				if ($(this).is(':checked')) {
					value = $(this).val();
					the_value += value + '>>';
				}
			})
		}
		the_value = escape(the_value);
		var id = $(elmnt).attr('id');
		if (id == 'view_results') {
			var pass = 'yes'
			var dataString = 'view=results' + '&id=' + $('#pid').val();
		}
		else 
			if (id == 'poll_vote') {
				var dataString = 'mode=' + $('#mode').val() + '&pid=' + $('#pid').val() + '&vote=' + the_value;
			}
		if (the_value || pass == "yes") {
			//$('#poll_loading').html('<img src=STATIC_URL+"themes/green/images/global/comment-loader.gif"/>');
			$.ajax({
				type: "GET",
				url: "/polls/ajax-voting/",
				data: dataString,
				success: function(html_from_server){
					//$('#poll_loading').html('');
					//$('.quick_vote4').remove();
					//$('.quick_vote_submit').remove();
					$('#poll_vote').remove();
					$('#id_poll_div').empty().html(html_from_server);
				}
			});
			
		}
		else {
			alert(gettext('Please make your choice'));
			return false;
		}
}

function poll_detail(id){ 
	$.ajax({
	    type:       "GET", 
	    url:         'polls/ajax-return/', 
	    data:  'id='+id,
	    dataType:     "html", 
	    success:     function( poll_return ) { 
				$("#id_polls_div").html(poll_return);
			}, 
	    error:        function( poll_return ) { 
			    $("#id_polls_div").html("Error loading");
			} 
	  });     
} 

function return_to_poll(){
	$.ajax({
		type: "GET",
		url: "/polls/ajax-view/",
		data: 'pid=' + $('#pid').val() +"&view=poll",
		success: function(html_from_server){
			$('#id_poll_div').empty().html(html_from_server);
		}
	});
}

function poll_view_result(){
	$.ajax({
		type: "GET",
		url: "/polls/ajax-view/",
		data: 'pid=' + $('#pid').val() +"&view=result",
		success: function(html_from_server){
			$('#poll_loading').html('');
			$('.quick_vote4').remove();
			$('.quick_vote_submit').remove();
			$('#id_poll_div').empty().html(html_from_server);
		}
	});
}
