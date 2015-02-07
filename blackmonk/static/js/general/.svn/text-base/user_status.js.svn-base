$(document).ready(function() {
		$.getJSON("/account/userstatus/",
        function(data){
			$('#guest_nav').empty().html(data.status_html).fadeIn();
			$('#guest_nav_1').empty().html(data.mob_html)
        });
        var search_q = $("#websearchfield");
        var search_m = $("#sitesearchradio_id");
        search_q.bind('focus',function(e){
        if (search_q.val() == default_text[search_m.val()]) {
            search_q.val("");
            search_q.css({color:"#000"});
        }
        });
        search_q.bind('blur',function(e){
            if (search_q.val() == "") {
                search_q.val(default_text[search_m.val()]);
                search_q.css({color:"#AAA"});
            }
        });
        
       // prepareSearchFields();
  });

function user_status_checklogin(){
	
	$.getJSON("/account/userstatus/",
        function(data){
			$('#guest_nav').empty().html(data.status_html).fadeIn();
			$('#guest_nav_1').empty().html(data.mob_html)
        });
        var search_q = $("#websearchfield");
        var search_m = $("#sitesearchradio_id");
        search_q.bind('focus',function(e){
        if (search_q.val() == default_text[search_m.val()]) {
            search_q.val("");
            search_q.css({color:"#000"});
        }
        });
        search_q.bind('blur',function(e){
            if (search_q.val() == "") {
                search_q.val(default_text[search_m.val()]);
                search_q.css({color:"#AAA"});
            }
        });
  }

















