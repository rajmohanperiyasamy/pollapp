$(document).ready(function(){
    //articles tab content code
	$('#id_tabs_ul li a').click(function(){
		$('.bm-tabs-li').removeClass('active');
		$(this).parent('li').addClass('active');
        $('.bm-tabs_content').hide();
		$('#'+$(this).attr('id')+'_articles').fadeIn(300);
		try{
			$('.fLxiMgW').setrSpVWidth(0);
	    	$('.fLxiMgH').setrSpVHeight('mDa-lT');
        }
        catch(e){}
    });

});

function setrate(css,rate,aid){
	$('#id_rating').addClass(css);
	$.ajax({
		type: "GET",
		url: "/staff/article/setrate/?aid="+aid+"&rate="+rate,
		data: "",
		success: function(html_from_server){
			if(html_from_server!='error'){
    			alert("Thanks! For rating the article.");
    		}else{
    			alert('Sorry! You have rated the article.');
    		}
		}
	});
	
}


