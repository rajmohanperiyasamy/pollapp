$(document).ready(function(){
		
$('#justin_tab').click(function(){
               $('#justin_tab').html('Just in');
               $("#related_tab").html('<a href="#" onclick = "return false;">Related</a>');
               $('#related_content').hide();
               $('#justin_content').fadeIn("slow");
       });
       
       $('#related_tab').click(function(){
               $('#related_tab').html('Related');
               $("#justin_tab").html('<a href="#" onclick = "return false;">Just in</a>');
               $('#justin_content').hide();
               $('#related_content').fadeIn("slow");
       });
});


function setrate(css,rate,aid){
	$('#id_rating').addClass(css);
	$.ajax({
		type: "GET",
		url: "/staff/bookmarks/setrate/?aid="+aid+"&rate="+rate,
		data: "",
		success: function(html_from_server){
			if(html_from_server!='error'){
    			alert("Thanks! For rating the bookmark.");
    		}else{
    			alert('Sorry! You have rated the bookmark.');
    		}
		}
	});
	
}


