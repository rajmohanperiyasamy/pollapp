$(document).ready(function(){   
	$('#id_gs_modules li.sec_tab a').click(function(event){	
	event.preventDefault();
			url=$(this).attr('href');
			ajax_search($(this),url);
			
	});
	
});
var global_url=''
function ajax_search(th,url){
	global_url=url
	$('#id_gs_modules li').removeClass("active");
	th.parent().addClass("active");
	$('html, body').animate({scrollTop:100}, 1000);
	$('#ajax_content').hide()
	$('#ajax_content_loading').show()
	$.ajax({
		type: "GET",
		url: url,
		success: function(html_from_server){																		
			$('#ajax_content').empty();
			$('#ajax_content').html(html_from_server);
			$('#ajax_content_loading').hide();
			$('#ajax_content').fadeIn("slow");
		}			
	});
}
function go_to(page){
	if(global_url==''){
		global_url=$('#global_url').val()
	}
	$('html, body').animate({scrollTop:100}, 1000);
	$('#ajax_content').hide()
	$('#ajax_content_loading').show()
	$.ajax({
		type: "GET",
		url: global_url+'&page='+page,
		success: function(html_from_server){																		
			$('#ajax_content').empty();
			$('#ajax_content').html(html_from_server);
			$('#ajax_content_loading').hide();
			$('#ajax_content').fadeIn("slow");
		}			
	});
}
function OnSubmitForm()
	{
		if(window.document.getElementById("websearchfield").value == ''){
			return false;
		}
	  var search=window.document.primesearch.sitesearch.value;
	  if(search == 'stories'){
	   	window.document.primesearch.action ="/search/article/";
	  }else if(search == 'event'){
	  	window.document.primesearch.action ="/search/event/";
	  }else if(search == 'people'){
	    window.document.primesearch.action ="/search/people/";
	  }else if(search == 'advice'){
	    window.document.primesearch.action ="/search/advice/";
	  }else if(search == 'classified'){
	    window.document.primesearch.action ="/search/classified/";
	  }else if(search == 'locality'){
	    window.document.primesearch.action ="/search/locality/";
	  }else if(search == 'business'){
	    window.document.primesearch.action ="/search/business/";
	  }else{
	    alert("wrong");
	  	return false;
	  }
	  return true;
	}
	
var default_text =
	{
		stories: "e.g. lifestyle, culture",
		classified: "e.g. cars, jobs, realestate",
		event: "e.g. art show, festivals",
		locality: "e.g. koramangala, indiranagar",
		people: "e.g. narayana murthy",
		business: "e.g. hdfc bank",
		advice: "e.g. book shop, stock"
	};
function prepareSearchFields() {
	var flag=1;
	$.each(default_text, function(i, val) {
		if($("#websearchfield").val()==val){
			flag=0;
    	}
    });
	if(flag==0 || $("#websearchfield").val()==''){
		$("#websearchfield").val(default_text[$("#sitesearchradio_id").val()]);
		$("#websearchfield").css({color:"#AAA"});
	}
}

