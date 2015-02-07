$(document).ready(function(){
	
	//setTimeout("$('.no_more_tweets').remove()",5000);

	//Search validation
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
	
	
	//Ajax twitter retrieve more
	$('.more_twitts').click(function(){
		if( $('#more_loader_span').html() == gettext("No more tweets") || $('#more_loader_span').html() == "No tweets found" ){
			return
		}
		
		$('#more_twitts').removeClass('button').addClass('more_twittes_loading');
		$('#more_loader_span').html('');
		$('<img src="/static/themes/green/images/global/buzz_twitter_more.gif" alt="Fetching twitts..."/>').appendTo('#more_loader_span');
		var url = $('a#more_twitts').attr('href');
		if(url.search(/\/?q+/) != -1 ){
			var url_split = url.split("&page=");
			var page = parseInt(url_split[1])+1;
			var next_href =  url_split[0]+"&page="+page;
		}
		else{
			var url_split = url.split("?page=");
			var page = parseInt(url_split[1])+1;
			var next_href =  url_split[0]+"?page="+page;
		}
		$.ajax({
				type: "GET",
				url: $('a#more_twitts').attr('href'),
				success: function(html_from_server){
					//alert(html_from_server)
					if(html_from_server == "empty"){
						$('#more_loader_span').html('No more tweets');
						setTimeout("$('#more_twitts').hide()",5000);
					}
					else{
						$('#more_loader_span').html('more');
						$('#more_twitts').removeClass('more_twittes_loading').addClass('button');
						$('#more_twitts').attr('href',next_href);
						$(html_from_server).appendTo('#tweets_wrapper');
					}
				}
		});
	});

});