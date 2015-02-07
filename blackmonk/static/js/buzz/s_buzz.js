$(document).ready(function(){
	$('.click_pvnt').click(function(event){
		event.preventDefault();
	});
	
	$('.submit_pvnt').submit(function(event){
		event.preventDefault();
	});
	
	$('.delete').click(function(event){
		if(!confirm(gettext("Are you sure you want to delete this? There is no undo?"))){
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
			alert(gettext('You didnt select anything'));
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
		var msg = gettext("Are you sure you want to "+action+" "+count+" "+content_msg);
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
			$(this).html(gettext('+ Add To List'));
			$('#add_to_lists').slideUp(300);
		}
		
	});
	
	$('#submit_add_lists').click(function(event){
		var is_occupied = $('#s_category option:selected').attr('class');
		if(is_occupied == "True"){
			if(confirm(gettext('This category is already occupied , Do you want to replace the existing lists ?'))){
					$('#form_add_lists').submit();
			}
			else{
				return false;
			}
		}
	});
	
	//Buzz settings page
	//Add keyword
	$('#as_add_keyword').click(function(){
		var keyword = $('#as_newkeyowrd').val();
		var whiteSpace = " ";
		var start = 0;
		var searchThis = keyword.indexOf(whiteSpace, start);
		var keyword_trim = $.trim(keyword);
		var key_len = 1 	
		
		if(keyword.search(/\,+/) != -1){
			keyword = keyword.toLowerCase().split(',');
			key_len = keyword.length;
		}
		
		//error status
		if (searchThis != -1) {
			$('.as_status').addClass('red').text(gettext('Space is not allowed'));
			return
		}
		if($('#keyword_ul li').length==5 || $('#keyword_ul li').length+key_len > 5 ){
			$('#as_newkeyowrd').css('border-color','red');
			$('.as_status').addClass('red').text(gettext('Maximum 5 keywords are only allowed'));
			return
		}
		if (keyword_trim.length==0){
			$('#as_newkeyowrd').css('border-color','red');
			$('.as_status').addClass('red').text(gettext('Please enter a keyword'));
			return
		}
		
		//if all ok then send to server
		$('<img src="/static/themes/green/images/global/comment-loader.gif" alt="Adding keyword.."/>').appendTo('#loading');
		$.get("/staff/buzz/twitter/ajax-add-keywords/", {keyword: keyword}, function(id){
			$('#loading').html('');
			$('#as_newkeyowrd').val('');
			if(id.search(/\,+/) != -1){
				id = id.replace('[','').replace(']','').split(',');
				for (var i=0;i<id.length;i++){
					$('#keyword_ul').append('<li><span onclick="remove_me(this,'+id[i]+');">&nbsp;</span>'+keyword[i]+'</li>');						
				}
			}
			else{
				$('#keyword_ul').append('<li><span onclick="remove_me(this,'+id+');">&nbsp;</span>'+keyword+'</li>');
			}
		});
		
		
	});
	
	$('#as_newkeyowrd').keyup(function(e){
		var keyword = $('#as_newkeyowrd').val();
		var whiteSpace = " ";
		var start = 0;
		var searchThis = keyword.indexOf(whiteSpace, start);
		if ( searchThis != -1 ) {
			$('#as_newkeyowrd').css('border-color', 'red');
			$('.as_status').addClass('red').text(gettext('Space is not allowed'));
		}
		else {
			$('#as_newkeyowrd').css('border-color', '');
			$('.as_status').text(gettext('Add multiple keywords separated by comma (,)')).removeClass('red');
		}
	});
	
	//Block user
	$('.username').each(function(index){
		var username  = $(this).html().replace('-','');
		$(this).html(username);
	});
	
	 
	$('#as_add_blocked_user').click(function(){
		var username = $('#as_new_blocked_user').val();
		username = "-"+username
		var whiteSpace = " ";
		var start = 0;
		var searchThis = username.indexOf(whiteSpace, start);
		var username_trim = $.trim(username);
		var key_len = 1 	
		
		if(username.search(/\,+/) != -1){
			username = username.replace(',',',-');
			username = username.split(',');
			key_len = username.length;
		}
		
		//error status
		if (searchThis != -1) {
			$('.as_b_status').addClass('red').text(gettext('Space is not allowed'));
			return
		}
		
		if (username_trim.length==0){
			$('#as_new_blocked_user').css('border-color','red');
			$('.as_b_status').addClass('red').text(gettext('Please enter a username'));
			return
		}
		
		//if all ok then send to server
		$('<img src="/static/themes/green/images/global/comment-loader.gif" alt="Adding username.."/>').appendTo('#loading2');
		$.get("/staff/buzz/twitter/ajax-block-user/", {username: username}, function(id){
			$('#loading2').html('');
			$('#as_new_blocked_user').val('');
			if(id.search(/\,+/) != -1){
				id = id.replace('[','').replace(']','').split(',');
				for (var i=0;i<id.length;i++){
					$('#blocked_user_ul').append('<li><span onclick="remove_me(this,'+id[i]+');">&nbsp;</span>'+username[i].replace('-','')+'</li>');						
				}
			}
			else{
				$('#blocked_user_ul').append('<li><span onclick="remove_me(this,'+id+');">&nbsp;</span>'+username.replace('-','')+'</li>');
			}
		});
		
		
	});
	
	$('#as_new_blocked_user').keyup(function(e){
		var username = $('#as_new_blocked_user').val();
		var whiteSpace = " ";
		var start = 0;
		var searchThis = username.indexOf(whiteSpace, start);
		if ( searchThis != -1 ) {
			$('#as_new_blocked_user').css('border-color', 'red');
			$('.as_b_status').addClass('red').text(gettext('Space is not allowed'));
		}
		else {
			$('#as_new_blocked_user').css('border-color', '');
			$('.as_b_status').text(gettext('Add multiple usernames separated by comma (,)')).removeClass('red');
		}
	});
	
	//Per page
	$('#perpage').val($('#perapge_value').val());
	
	$('#as_add_perpage').click(function(){
		clearTimeout(status);
		var perpage = $('#perpage').val();
		var whiteSpace = " ";
		var start = 0;
		var searchThis = perpage.indexOf(whiteSpace, start);
		var perpage_trim = $.trim(perpage);
		
		//blank space
		if (perpage_trim.length==0){
			$('#perpage').css('border-color', 'red');
			$('.as_perpage_status').addClass('red').text(gettext('Please enter a number'));
			return
		}
		
		//is number valid
		if (isNaN(perpage) || perpage.search(/\.+/) != -1 || searchThis != -1) {
			$('#perpage').css('border-color', 'red');
			$('.as_perpage_status').addClass('red').text(gettext('Invalid Number'));
			return
		}
		
		//cannot exceed 100
		if (perpage>100) {
			$('#perpage').css('border-color', 'red');
			$('.as_perpage_status').addClass('red').text(gettext('Cannot exceed more than 100'));
			return
		}
		
		$('<img src="/static/themes/green/images/global/comment-loader.gif" alt="Adding keyword.."/>').appendTo('#loading1');
		$.get("/staff/buzz/twitter/ajax-perpage/", {perpage: perpage}, function(perpage){
			$('#loading1').html('');
			$('.as_perpage_status').addClass('tip_status').text(gettext('Number of tweets updated to '+perpage+' tweets per page'))
			var status = setTimeout("$('.as_perpage_status').text(gettext('Default is 20 tweets per page')).removeClass('tip_status')",6000);
		});
		
	});
	
	$('#perpage').keyup(function(e){
		clearTimeout(status);
		var perpage = $('#perpage').val();
		var whiteSpace = " ";
		var start = 0;
		var searchThis = perpage.indexOf(whiteSpace, start);
		
		if (isNaN(perpage) || perpage.search(/\.+/) != -1 || searchThis != -1) {
			$('#perpage').css('border-color', 'red');
			$('.as_perpage_status').addClass('red').text(gettext('Invalid Number')).removeClass('tip_status');
		}
		else {
			$('#perpage').css('border-color', '');
			$('.as_perpage_status').text(gettext('Default is 20 tweets per page')).removeClass('red').removeClass('tip_status');
		}
	});
	
	//Buzz seo page begin
	$('#seoform').submit(function(event){
		var val = $('#category').val();
		if(val == 'none'){
			event.preventDefault();
			$('label[for = "category"]').css('color','red');
		}
	});
	//Buzz seo page end
	
	//Buzz Category Ordering Ajax begin
	
	$('#order_save').click(function(){
		if (confirm(gettext('Are you sure? You want to change the order'))) {
			$('#manage_cat').submit();
		}
	});
	
	//Buzz Category Ordering Ajax end
	
});

//Buzz settings page
function remove_me(element,kid){
	$(element).prepend('<img src="/static/themes/green/images/js/s_buzz_kw.gif" />')
	$.get("/staff/buzz/twitter/ajax-delete-keywords/", {kid:kid}, function(data){
		$(element).parent('li').remove();
		$('#as_newkeyowrd').css('border-color','');
		$('.as_status').text(gettext('Add multiple keywords separated by comma (,)')).removeClass('red');
	});
}

//Retreieving the seo contents of the selected categories begin

function retrieve_seo(){
	var val = $('#category').val();
	if (val != 'none') {
		$('#as_loader').html('<img src="/static/themes/green/images/global/comment-loader.gif" />');
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