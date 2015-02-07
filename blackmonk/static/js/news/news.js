$(document).ready(function(){
	//Search code
	$('div.search_wrapper .left').click(function(){
		var val = $('input#sp-searchtext').val();
		var string= $.trim(val);
		if (string.length == 0) {
			$('input#sp-searchtext').css('border-color','red');	
			$('input#sp-searchtext').focus();
			return
		}
		else{
			$('#search_submit').submit();
		}
	});
	
	$('.reset').click(function(){
		$('input#sp-searchtext').val('');
		$('.reset').hide();
		$('input#sp-searchtext').focus();
	});
	
	$('#search_submit').submit(function(){
		var val = $('input#sp-searchtext').val();
		var string= $.trim(val);
		if (string.length == 0) {
			$('input#sp-searchtext').css('border-color','red');	
			$('input#sp-searchtext').focus();
			return false
		}
		else{
			return true;
		}
	});
	
	$('input#sp-searchtext').keyup(function(){
		$('input#sp-searchtext').css('border-color','');	
		var val = $('input#sp-searchtext').val();
		var string= $.trim(val);
		if (string.length == 0) {
			$('div.search_wrapper .reset').hide();
		}
		else {
			$('div.search_wrapper .reset').show();
		}
	});
	
	//Search code end

	//Fixing bug on category click begin
	$('li.cat_li').click(function(){
		var url = $(this).children('a').attr('href');
		location.replace(url);
	});
	//Fixing bug on category click end
	
});