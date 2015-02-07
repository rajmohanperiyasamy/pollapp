$(document).ready(function(){
$('#id_search_keyword').bind('keypress', function(e) {
    var code = (e.keyCode ? e.keyCode : e.which);
     if(code == 13) {
       $('#id_search').val('true');
       $('#id_pagentn').val('1');              
       filter_content();
    }
    });    
}); 

function filter_content(){
    var dataString='';
    var url= $('#id_hidden_url').val();
    dataString+="view_by="+$('#id_view_by').val();
    
    if($('#id_pagentn').val()!='' && $('#id_pagentn').val()!=null){
        dataString+="&page="+$('#id_pagentn').val();
    } 
    
    if($('#id_search').val()!='' && $('#id_search').val()!=null){
        dataString+="&search=true";
        dataString+="&kwd="+$('#id_search_keyword').val();
    }
                          
    $('#id_users_listing').hide();
    $('#ajax_content_loading').show();
    $.ajax({
    type: "GET",
    url: url,
    data: dataString,
    dataType:'JSON',
    success: function(data){
            $('#ajax_content_loading').hide();
            $('#id_users_listing').empty().html(data.html).fadeIn(300);
            $('.light_box').colorbox({width: "560",initialWidth: "560", top:"60", initialHeight: "200", title:function(){return getLBTitle($(this));}});
        }
    });
}

function change_status(id){
  $('.dev_hide_list_status ul.dropdown-list').hide();
  $('span.status-inside').removeClass('active');
  $('#id_change_status_ul_'+id).toggle();
  $('#id_change_status_span_'+id).toggleClass('active');
}

function save_status(id){
    $('#id_change_status_span_icon_'+id).addClass('loading');
    var DataString="id="+id;
    var url = $('#id_change_status_url').val();
    $.ajax({
        type: "GET",
        url: url,
        data: DataString,
        dataType:'JSON',
        success: function(data){
            if(data.success){
                $('#id_change_status_span_icon_'+id).removeClass('loading');
                $('#id_change_status_span_icon_'+id).removeClass('icon-active-user icon-inactive-user').addClass(data.status_class);
                $('#id_change_status_ul_'+id).hide();
                $('#id_change_status_span_'+id).removeClass('active');
                $('#id_change_status_text_'+id).text(gettext(data.status_text));
                show_quick_stats();
                if(data.status_text == 'Active'){
                    $('#id_promote_link_'+id).hide();
                }else{
                    $('#id_promote_link_'+id).show();
                }
            }else{
                show_msg(gettext('Oops!!! Not able to process your request.'),'alert-error');
            }
        }
    });                 
}

function create_user(){
  var success = $('#mform').validate().form();  
  if(success){
        var url= $('#mform').attr('action');
        var dataString='display_name='+$('#id_display_name').val();
        dataString+='&useremail='+$('#id_useremail').val();
        dataString+='&password='+$('#id_password').val();
        dataString+='&groups='+$('#id_groups').val();
        $('#ajax_content').hide();
        var msg_html = '<img src="/static/ui/images/global/loading-s.gif"><br><p>'+gettext("Saving Staff Information")+'</p>';
        $('#ajax_content_loading_admin').empty().html(msg_html).show();
        $.ajax({
        type: "POST",
        url: url,
        data: dataString,
        dataType:'JSON',
        success: function(data){
                $('#ajax_content_loading_admin').html(data.msg);
                if(data.status){
                    $('#bmClose').trigger('click');
                    $('#id_append_list').prepend(data.append_html);  
                    $('.light_box').colorbox({width: "560",initialWidth: "560", top:"0", initialHeight: "200", title:function(){return getLBTitle($(this));}});   
                    show_msg(gettext(data.msg),data.mtype);
                    update_rolls_count();
                    $.colorbox.close();
                }
                $('#ajax_content').empty().html(data.lightbox_html);
                setTimeout(function(){
                    $('#ajax_content_loading_admin').hide();
                    $('#ajax_content').fadeIn(300);
                    $.colorbox.resize();
                },1000);
            }
        });       
              
  }        
}

function update_user(){
  var success = $('#mform').validate().form();  
  if(success){
        var url= $('#mform').attr('action');
        var id = $('#id_uid').val();
        var dataString='display_name='+$('#id_display_name').val();
        dataString+='&useremail='+$('#id_useremail').val();
        dataString+='&groups='+$('#id_groups').val();
        dataString+='&uid='+id;
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
                    $('#id_user_list_'+id).remove();      
                    $('#id_append_list').prepend(data.append_html);  
                    $('.light_box').colorbox({width: "560",initialWidth: "560", top:"0", initialHeight: "200", title:function(){return getLBTitle($(this));}});   
                    show_msg(gettext(data.msg),data.mtype);
                    update_rolls_count();
                    $.colorbox.close();
                }
                $('#ajax_content').empty().html(data.lightbox_html);
                setTimeout(function(){
                    $('#ajax_content_loading_admin').hide();
                    $('#ajax_content').fadeIn(300);
                    $.colorbox.resize();
                },1000);
            }
        });       
              
  }                        
}

function deactivate_status(id){
    $('#id_change_status_span_icon_'+id).addClass('loading');
    var DataString="id="+id;
    var url = $('#id_deactivate_status_url').val();
    $.ajax({
        type: "GET",
        url: url,
        data: DataString,
        dataType:'JSON',
        success: function(data){
            if(data.success){
                $('#id_change_status_span_icon_'+id).removeClass('loading');
                $('#id_change_status_span_icon_'+id).removeClass('icon-active-user icon-inactive-user').addClass(data.status_class);
                $('#id_change_status_ul_'+id).hide();
                $('#id_change_status_span_'+id).removeClass('active');
                $('#id_change_status_text_'+id).text(gettext(data.status_text));
                $('#id_promote_link_'+id).hide();
            }else{
                show_msg(gettext('Oops!!! Not able to process your request.'),'alert-error');
            }
        }
    });                 
}

function delete_content(id){
    if($('input[name="delete"]:checked').val()=='deactivate'){
        deactivate_status(id);
    }
    else{
        var all_ids=[];
        var dataString='';
        var url= $('#id_delete_url').val();
        dataString+="&del="+$('#id_delete').val();
        dataString+="sort="+$('#id_sort').val();
        dataString+='&uid='+id;
        
        if($('#id_pagentn').val()!='' && $('#id_pagentn').val()!=null){
            dataString+="&page="+$('#id_pagentn').val();
        }
        
        
        if($('#id_search').val()!='' && $('#id_search').val()!=null){
            dataString+="&search=true";
            dataString+="&kwd="+$('#id_search_keyword').val();
            //$('#id_pagentn').val('1');
        }
        
        $('.dev_allids').each(function(){
          all_ids.push($(this).val());                               
        });
        dataString+='&all_ids='+all_ids;
        //$('#ajax_content_loading').show();
        $.ajax({
        type: "GET",
        url: url,
        data: dataString,
        dataType:'JSON',
        success: function(data){
                $('#id_user_list_'+id).remove();                       
                //$('#ajax_content_loading').hide();
                $('#id_append_list').append(data.html);
                show_msg(gettext(data.msg),data.mtype);
                $('.light_box').colorbox({width: "560",initialWidth: "560", top:"0", initialHeight: "200", title:function(){return getLBTitle($(this));}});
                $('#user_count').html(data.count);
            }
        });
    }
    $.colorbox.close();                    
}                            

function oldcode_delete_content(id){
    var all_ids=[];
    var dataString='';
    var url= $('#id_delete_url').val();
    dataString+="view_by="+$('#id_view_by').val();
    dataString+='&uid='+id;
    
    if($('#id_pagentn').val()!='' && $('#id_pagentn').val()!=null){
        dataString+="&page="+$('#id_pagentn').val();
    }
    
    if($('#id_search').val()!='' && $('#id_search').val()!=null){
        dataString+="&search=true";
        dataString+="&kwd="+$('#id_search_keyword').val();
    }
    
    $('.dev_allids').each(function(){
      all_ids.push($(this).val());                               
    });
    dataString+='&all_ids='+all_ids;
    //$('#ajax_content_loading').show();
    $.ajax({
    type: "GET",
    url: url,
    data: dataString,
    dataType:'JSON',
    success: function(data){
            $('#id_user_list_'+id).remove();                       
            //$('#ajax_content_loading').hide();
            $('#id_append_list').append(data.html);
			update_rolls_count();
            show_msg(gettext(data.msg),data.mtype);
            $('.light_box').colorbox({width: "560",initialWidth: "560", top:"60", initialHeight: "200", title:function(){return getLBTitle($(this));}});
        }
    });                       
}                            

function update_roll(uid,roll_id,url){
    var DataString="uid="+uid+'&roll_id='+roll_id;
    $.ajax({
        type: "GET",
        url: url,
        data: DataString,
        dataType:'JSON',
        success: function(data){
            if(data.success){
                show_msg(gettext(data.msg),data.mtype);
                update_rolls_count();
            }else{
                show_msg(gettext('Oops!!! Not able to process your request.'),'alert-error');
            }
        }
    }); 
                             
}    

function update_rolls_count(){
    var url = $('#id_update_rolls_url').val();
    $.ajax({
        type: "GET",
        url: url,
        data: 1,
        dataType:'JSON',
        success: function(data){
            if(data.success){
                $('#role-mngt').empty().html(data.append_html);
                $(".bm-add-gadget").colorbox({width: "560",initialWidth: "560", top:"5%",initialHeight: "200",title:function(){return getLBTitle($(this));}});
            }else{
                show_msg(gettext('Oops!!! Not able to process your request.'),'alert-error');
            }
        }
    });                            
                              
}

function filter_action(ids,action){
	var all_ids=[];
	var dataString='';
    var url= $('#id_hidden_action_url').val();
    dataString+="sort="+$('#id_sort').val();
    dataString+="&view_by="+$('#id_view_by').val();
    
    if($('#id_pagentn').val()!='' && $('#id_pagentn').val()!=null){
        dataString+="&page="+$('#id_pagentn').val();
    }
    
    if($('#id_search').val()!='' && $('#id_search').val()!=null){
        dataString+="&search=true";
        dataString+="&kwd="+$('#id_search_keyword').val();
    }
    
	if(action=='#'){
		dataString+="&action="+$('#id_action').val();
		if(ids==0){
			var ids=[];
			$('.cbox:checked').each(function(){
				ids.push($(this).val());
			});
		}
	}else{dataString+="&action="+action;}
	$('.cbox').each(function(){
		all_ids.push($(this).val());
	});
	dataString+="&ids="+ids;
	dataString+="&all_ids="+all_ids;

    $.ajax({
    type: "GET",
    url: url,
    data: dataString,
    dataType:'JSON',
    success: function(data){
			$("#master_check").attr('checked',false);
			$('#actionSelect').val("").trigger("liszt:updated");
			$('#id_action').val('');
			if(data.status==1){
				try{for(i=0;i<ids.length;i++){$('#id_user_list_'+ids[i]).remove();}$('#id_user_list_'+ids).remove();}
				catch(e){$('#id_user_list_'+ids).remove();}
				$('#id_append_list').append(data.html);
				$('#pagenation').empty().html(data.pagination);
			}
			update_rolls_count();
			show_msg(data.msg,data.mtype);
			if(data.search){$('#close_search').show();}
			if(data.status==1){
				if(data.next){$('#top_pge_next').removeClass('inactive');}
				else{$('#top_pge_next').addClass('inactive');}
				if(data.previous){$('#top_pge_previous').removeClass('inactive');}
				else{$('#top_pge_previous').addClass('inactive');}
				$('#id_from_to').html(data.pagerange);
				$('.light_box').colorbox({width: "560",initialWidth: "560", top:"60", initialHeight: "200", title:function(){return getLBTitle($(this));}});
			}
        }
    });
}

function action(){
	var flag=false;
	var flag_action=false;
	if($('#id_action').val()!='0'){
		$('.cbox:checked').each(function(){
			flag=true;
		});
		if(flag){
			if($('#id_action').val()=='DEL'){
				if(confirm(gettext('Deleting staff(s) will delete all the records related to it,\n Are you sure you want to delete selected staff(s) ?'))){flag_action=true;}
			}
			if($('#id_action').val()=='SACTS'){
				if(confirm(gettext('Are you sure you want to Activate selected staff(s) ?'))){flag_action=true;}
			}
			if($('#id_action').val()=='SDCTS'){
				if(confirm(gettext('Are you sure you want to Deactivate selected staff(s) ?'))){flag_action=true;}
			}
			if(flag_action){filter_action(0,'#');}
		}else{
			$('#actionSelect').val("").trigger("liszt:updated");
			alert(gettext('Please select staff(s)'));
		}
	}
}
                                                     