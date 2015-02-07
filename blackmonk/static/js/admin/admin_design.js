

function add_menu_item(){

var success = $('#mform').validate().form();  
  if(success){
        var url= $('#mform').attr('action');
        var dataString='name='+encodeURIComponent($('#id_name').val());
        dataString+='&base_url='+encodeURIComponent($('#id_base_url').val());
        //dataString+='&parent='+encodeURIComponent($('#id_parent').val());
        $('#ajax_content').hide();
        $('#ajax_content_loading_admin').show();
        $.ajax({
        type: "POST",
        url: url,
        data: dataString,
        dataType:'JSON',
        success: function(data){
				$('#ajax_content_loading_admin').html(data.msg);
				if(data.status){
                if(data.edit){
					if($('.sortable li').size()==1){$('#list_'+data.id).remove();$('.sortable').prepend(data.menu_list_html);}
					else{
					var next_li = $('#list_'+data.id).next('li').attr('id');
					if(!next_li){next_li=$('#list_'+data.id).prev('li').attr('id');$('#list_'+data.id).replaceWith(data.menu_list_html);}
					else{$('#list_'+data.id).remove();$('#'+next_li).before(data.menu_list_html);}
					}
				}
				else{$('.sortable').prepend(data.menu_list_html);}

				$('.bm-menu-content').colorbox({width:"600",initialWidth:"600",initialHeight:"200",top:"170", title:function(){return getLBTitle($(this));}});
                show_msg(gettext(data.msg),data.mtype);
                $.colorbox.close();
				}
                $('#ajax_content').empty().html(data.html);
                setTimeout(function(){
                    $('#ajax_content_loading_admin').hide();
                    $('#ajax_content').fadeIn(300);
                    $.colorbox.resize();
                },1000);
            }
        });       
  }   

}


function delete_menu(id,url){
	$.ajax({
        type: "GET",
        url: url,
        data: 'mid='+id,
        dataType:'JSON',
        success: function(data){
            if(data.success){
				$('#list_'+id).remove();
                show_msg(gettext(data.msg),data.mtype);
            }else{
                show_msg(gettext(data.msg),data.mtype);
            }
        }
    }); 

}



function add_subheader_menu_item(){

  var success = $('#mform').validate().form();  
  if(success){
        var url= $('#mform').attr('action');
        var dataString='name='+encodeURIComponent($('#id_name').val());
        dataString+='&base_url='+encodeURIComponent($('#id_base_url').val());
        //dataString+='&parent='+encodeURIComponent($('#id_parent').val());
        $('#ajax_content').hide();
        $('#ajax_content_loading_admin').show();
        $.ajax({
        type: "POST",
        url: url,
        data: dataString,
        dataType:'JSON',
        success: function(data){
				$('#ajax_content_loading_admin').html(data.msg);
				if(data.status){
                if(data.edit){
					if($('.sortable li').size()==1){$('#list_'+data.id).remove();$('.sortable').prepend(data.menu_list_html);}
					else{
					var next_li = $('#list_'+data.id).next('li').attr('id');
					if(!next_li){next_li=$('#list_'+data.id).prev('li').attr('id');$('#list_'+data.id).replaceWith(data.menu_list_html);}
					else{$('#list_'+data.id).remove();$('#'+next_li).before(data.menu_list_html);}
					}
				}
				else{$('.sortable').prepend(data.menu_list_html);}

				$('.bm-menu-content').colorbox({width:"600",initialWidth:"600",initialHeight:"200",top:"170", title:function(){return getLBTitle($(this));}});
                show_msg(gettext(data.msg),data.mtype);
                $.colorbox.close();
				}
                $('#ajax_content').empty().html(data.html);
                setTimeout(function(){
                    $('#ajax_content_loading_admin').hide();
                    $('#ajax_content').fadeIn(300);
                    $.colorbox.resize();
                },1000);
            }
        });       
  } 


}

function add_footer_item(){

  var success = $('#mform').validate().form();  
  if(success){
        var url= $('#mform').attr('action');
        var dataString='name='+encodeURIComponent($('#id_name').val());
        dataString+='&base_url='+encodeURIComponent($('#id_base_url').val());
        //dataString+='&parent='+encodeURIComponent($('#id_parent').val());
        $('#ajax_content').hide();
        $('#ajax_content_loading_admin').show();
        $.ajax({
        type: "POST",
        url: url,
        data: dataString,
        dataType:'JSON',
        success: function(data){
				$('#ajax_content_loading_admin').html(data.msg);
				if(data.status){
                if(data.edit){
					if($('.sortable li').size()==1){$('#list_'+data.id).remove();$('.sortable').prepend(data.menu_list_html);}
					else{
					var next_li = $('#list_'+data.id).next('li').attr('id');
					if(!next_li){next_li=$('#list_'+data.id).prev('li').attr('id');$('#list_'+data.id).replaceWith(data.menu_list_html);}
					else{$('#list_'+data.id).remove();$('#'+next_li).before(data.menu_list_html);}
					}
				}
				else{$('.sortable').prepend(data.menu_list_html);}

				$('.bm-menu-content').colorbox({width:"600",initialWidth:"600",initialHeight:"200",top:"170", title:function(){return getLBTitle($(this));}});
                show_msg(gettext(data.msg),data.mtype);
                $.colorbox.close();
				}
                $('#ajax_content').empty().html(data.html);
                setTimeout(function(){
                    $('#ajax_content_loading_admin').hide();
                    $('#ajax_content').fadeIn(300);
                    $.colorbox.resize();
                },1000);
            }
        });       
  }
}

