$(document).ready(function(){
	$('.click_pvnt').click(function(event){
		event.preventDefault();
	});
	
	$('.submit_pvnt').submit(function(event){
		event.preventDefault();
	});
	
	$('.delete').click(function(event){
		if(!confirm("Are you sure you want to delete this? There is no undo?")){
			event.preventDefault();
		}
	});
	
	$('#select_all').click(function(){
		if($('#select_all').is(':checked')){	
			$('.cb').attr('checked','true');
		}
		else {
			$('.cb').removeAttr('checked');
		}
	});
	
	
	$('select#actions').change(function(){
		var call_from = $('#call_from').val();
		var count = $(".cb:checked").length;
		if(count==0){
			alert('You didnt select anything');
			return
		}
		if(count>1){
			var count = "all the "+count;
			if (call_from == "buzz_manage_categroies") {
				var content_msg = "categories"
			}
			if (call_from == "twitter_manage_users") {
				var content_msg = "Users"
			}
			if (call_from == "buzz_manage_lists") {
				var content_msg = "Lists"
			}
		}
		else{
			var count = "this";
			if (call_from == "buzz_manage_categroies") {
				var content_msg = "category"
			}
			if (call_from == "twitter_manage_users") {
				var content_msg = "User"
			}
			if (call_from == "buzz_manage_lists") {
				var content_msg = "Lists"
			}
		}
		var action = $('select#actions').val();
		var msg = "Are you sure you want to "+action+" "+count+" "+content_msg;
		if(confirm(msg)){
			if (call_from == "buzz_manage_categroies") {
				$('form#manage_cat').submit();	
			}
			if (call_from == "twitter_manage_users") {
				$('form#manage_users').submit();	
			}
			if (call_from == "buzz_manage_lists") {
				$('form#manage_lists').submit();	
			}
		}
	});
	
	$('#expand').click(function(event){
		event.preventDefault();
		var disp = $('#add_to_lists').css('display');			
		if(disp=="none"){
			$(this).html('- Add To List');
			$('#add_to_lists').slideDown(300);
		}
		else if(disp=="block"){
			$(this).html('+ Add To List');
			$('#add_to_lists').slideUp(300);
		}
		
	});
	
	$('#submit_add_lists').click(function(event){
		var is_occupied = $('#s_category option:selected').attr('class');
		if(is_occupied == "True"){
			if(confirm('This category is already occupied , Do you want to replace the existing lists ?')){
					$('#form_add_lists').submit();
			}
			else{
				return false;
			}
		}
	});
	
	//Buzz settings page
	//Add keyword
	
});































//Retreieving the seo contents of the selected categories begin

function retrieve_seo(){
	var val = $('#category').val();
	if (val != 'none') {
		$('#as_loader').html('<img src="/site_media/themes/green/images/global/comment-loader.gif" />');
		$('.iterate').each(function(){
			$(this).attr('disabled', 'disabled');
			if ($(this).attr('id') != 'seo_submit') {
				$(this).val('');
			}
		});
		$('.iterate').css('background-color', ' #E5E5E5');
		//Ajax
		$.ajax({
				type: "GET",
				url: '/staff/buzz/retrieve-seo?cid='+val,
				dataType: 'json',
				success: function(html_from_server){
					$('#as_loader').html('');
					$('.iterate').removeAttr('disabled').css('background-color', '');
					if (html_from_server != '0') {
						$('#seo_title').val(html_from_server.seo_title);
						$('#seo_description').val(String(html_from_server.seo_description));
					}
					else{
						alert('Ajax error');
					}
				}
			  });
	}
}

//Retreieving the seo contents of the selected categories end










/*
function addtag(){
	var tags=window.document.getElementById('id_newtag').value;
	var taglist = tags.split(",")
	var tag='';
	var len_tag = taglist.length;
	for(var i=0; i<len_tag; i++){
		tag=trim(taglist[i]);
		if(tag!=''){
			var newtag="<li id='id_stag_"+tagcount+"'><span onclick='deletetag("+tagcount+")'>&nbsp;</span>";
			newtag += tag;
			newtag += "<input type='hidden' name='tagselected' value='"+tag+"'/>";
			newtag += "</li>";
			window.document.getElementById('id_alltags').innerHTML += newtag;
			tagcount +=1;
			window.document.getElementById('id_newtag').value='';
			}
		}
	}


function trim(str){
	if(!str || typeof str != 'string')
		return '';
	return str.replace(/^[\s]+/,'').replace(/[\s]+$/,'').replace(/[\s]{2,}/,' ');
}


*/




