$(document).ready(function(){
   
   $("#add_qna_form").validate({
        ignore:'',
        highlight: function(element, errorClass){$(element).parent().addClass('error');},
        unhighlight: function(element, errorClass){$(element).parent().removeClass('error');$(element).parent('div').find('.bm-error-txt-spn:first').addClass('hide');},
           rules:{
            question: "required",
            category: "required"
           },
           errorPlacement: function(error, element) {
                $(element).parent('div').find('.bm-error-txt-spn:first').removeClass('hide');
            },
    });
    
    $('.bUiSlCt').bind("change", function(){
        $("#add_qna_form").validate().element($(this));
    });                         
                             
});    

function update_answer_button(hobj)
{
    var postBtn = $(hobj).parents(".dev-aForm").find('.dev-postBtn:first');
    if($.trim(hobj.val()).length >= 1){
            postBtn.removeAttr('disabled');
            postBtn.removeClass('disabled');
        }
    else{
            postBtn.attr('disabled','disabled');
            postBtn.addClass('disabled');
         }
}

function cancel_comment(hobj){
      $(hobj).parents(".dev-aForm").removeClass('hS-fCs');
      $(hobj).parents(".dev-aForm").removeClass('hS-fCs');
      $(hobj).parents(".dev-aForm").find("input[type=text], textarea").val("");
      try{
          $(hobj).parents(".dev-aForm").find('.dev-postBtn:first').attr('disabled','disabled').addClass('disabled');
          $(hobj).parents(".dev-aForm").find('.bm-error-txt-spn').addClass('hide');
      }
      catch(e){}
}

function check_login(aid,type){
   var login_url = ajax_login_url + '?type=' + type;	
   if(type == 'addanswer'){
	   $('#id_hidden_frm_sbmt').val(aid);                     
	   if(!user_login){
	       $.colorbox({width: "722",initialWidth: "722", top:"5%", initialHeight: "200", href:login_url, onOpen:function(){$("#colorbox").addClass("no_title");} });
	   }                    
	   else{save_answer();}
   }

   else if(type == 'postquestion'){
		if(!user_login){
	        $.colorbox({width: "722",initialWidth: "722", top:"5%", initialHeight: "200", href:login_url, onOpen:function(){$("#colorbox").addClass("no_title");} });
	    }                    
	    else{post_question();}
   }	
	
   else if(type == 'addpost'){
        if(!user_login){
            $.colorbox({width: "722",initialWidth: "722", top:"5%", initialHeight: "200", href:login_url, onOpen:function(){$("#colorbox").addClass("no_title");} });
        }                    
        else{check_add_post();}
   }
    
   else if(type == 'subtopic'){
		if(!user_login){
	        $.colorbox({width: "722",initialWidth: "722", top:"5%", initialHeight: "200", href:login_url, onOpen:function(){$("#colorbox").addClass("no_title");} });
	    }                    
	    else{topic_follow(1);}
   }
   else if(type == 'unsubtopic'){
		var login_url = ajax_login_url+'?type=subtopic';
		if(!user_login){
	        $.colorbox({width: "722",initialWidth: "722", top:"5%", initialHeight: "200", href:login_url, onOpen:function(){$("#colorbox").addClass("no_title");} });
	    }                    
	    else{topic_follow(2);}
   }
   
   else if(type == 'flaganswer'){
		$('#id_hidden_ans').val(aid);
		if(!user_login){
	        $.colorbox({width: "722",initialWidth: "722", top:"5%", initialHeight: "200", href:login_url, onOpen:function(){$("#colorbox").addClass("no_title");} });
	    }                    
	    else{answer_flag();}
   }
   
   else if(type == 'followques'){
   		$('#id_hidden_entry').val(aid);
		if(!user_login){
	        $.colorbox({width: "722",initialWidth: "722", top:"5%", initialHeight: "200", href:login_url, onOpen:function(){$("#colorbox").addClass("no_title");} });
	    }                    
	    else{
	    	follow_homeques(1);
	    }
   }
   else if(type == 'unfollowques'){
   		$('#id_hidden_entry').val(aid);
		if(!user_login){
	        $.colorbox({width: "722",initialWidth: "722", top:"5%", initialHeight: "200", href:login_url, onOpen:function(){$("#colorbox").addClass("no_title");} });
	    }                    
	    else{
	   	    follow_homeques(2);
	    }
   }
   else{
		var login_url = ajax_login_url+'?type=subscribe';
		if(!user_login){
	        $.colorbox({width: "722",initialWidth: "722", top:"5%", initialHeight: "200", href:login_url, onOpen:function(){$("#colorbox").addClass("no_title");} });
	    }                    
	    else{
	   		if (type == 'follow'){
	   			follow_entry(1);
	   		}else{
	   			follow_entry(2);
	   		}
	   	}
   }		

}

function follow_homeques(sub){
    var eid = $('#id_hidden_entry').val();
	if (sub == 1){
		var url = "/community/follow_entry/"+eid;
	}else{
		var url = "/community/unfollow_entry/"+eid;
	}
    $('#id_follow_icon_'+eid).removeClass("bUi-iCn-oK-aLt-16");
    $('#id_follow_icon_'+eid).addClass("bUi-iCnlDg-16");
	user_login = true;
	$.ajax({
		type:'get',
		url: url,
	    dataType:'json',
	    success: function(data){
	    	if(data.status){
            $('#id_follow_icon_'+eid).removeClass("bUi-iCnlDg-16");
            $('#id_follow_icon_'+eid).addClass("bUi-iCn-oK-aLt-16");
	    	if(data.follow_class == 'class'){
	    		$('#id_home_follow_'+eid).removeClass("cKd");
	    		$('#id_home_follow_'+eid).attr('title',"Follow Question");
                $('#id_home_follow2_'+eid).empty().html("Follow Question");
	    	}else{
	    		$('#id_home_follow_'+eid).addClass("cKd");
	    		$('#id_home_follow_'+eid).attr('title',"Following");
                $('#id_home_follow2_'+eid).empty().html("Unfollow");
	    	}
	    	if(data.subscribers_count == 1){
	    			$('#id_home_text_'+eid).attr('placeholder',+data.subscribers_count+" person is waiting for an answer...");
	    		}
			else{
					$('#id_home_text_'+eid).attr('placeholder',+data.subscribers_count+" people are waiting for an answer...");
				}
			$('#id_home_follow_'+eid).attr("onclick", data.function2);
			$('#id_home_follow2_'+eid).attr("onclick", data.function2);
			}else{alert(gettext('Oops !!! Not able to process your request.'));}
	    }
    });
}


function save_answer(){
	user_login = true;
    $('#ansbmt_'+$('#id_hidden_frm_sbmt').val()).submit();                    
}

function post_question(){
	user_login = true;
    $('#button_add_qna').attr('data-toggle','modal');
    $('#button_add_qna').attr('data-target','#add_entry');
    $('#button_add_qna').attr('data-href', add_question_url);
    target = add_question_url;
    $("#add_entry .modal-body").load(target, function() {
        $("#add_entry").modal("show");
    });
    //$( "#button_add_qna" ).trigger( "click" );
    //$("#add_entry").modal("show");
}

function check_add_post(){
    user_login = true;
    $('#add_post_form').submit();
}

function limit_charecters(textArea,len){
    var txtvalue = textArea.value;
    var the_len = txtvalue.length;
    if (the_len > len){
        textArea.value = txtvalue.substring(0,len);
    }
}

function show_toggle(id){
    $('#less_content_'+id).toggle();
    $('#more_content_'+id).toggle();
} 

function reply_thread(id){
	$('#replay_signup_'+id).hide();
	$('#replay_'+id).show();
}

function follow_entry(fol){
    $("#id_follow_icon").removeClass("bUi-iCn-pLs-16");
    $("#id_follow_icon").removeClass("bUi-iCn-oK-16");
    $("#id_follow_icon").addClass("bUi-iCnlDg-16");
	if (fol == 1){
		var url = ajax_follow_entry_url
	}else{
		var url = ajax_unfollow_entry_url
	}
	user_login = true;
	$.ajax({
		type:'get',
		url:url,
	    dataType:'json',
		success:function(data){
			if(data.status){
                if(data.action == 'Following'){
                    $('#id_follow_icon').removeClass("bUi-iCnlDg-16");
                    $('#id_follow_icon').addClass("bUi-iCn-oK-16");
                    $('#id_follow_entry .btntxt_hover').html("Unfollow");
                    $('#id_follow_entry').addClass("following");
                }else{
                    $('#id_follow_icon').removeClass("bUi-iCnlDg-16");
                    $('#id_follow_icon').addClass("bUi-iCn-pLs-16");
                    $('#id_follow_entry .btntxt_hover').html(data.action);
                    $('#id_follow_entry').removeClass("following");
                }
                $('#id_follow_entry .btntxt').html(data.action);
                $('#id_follow_entry').attr("onclick", data.function);
				$('#followers').empty().html(data.subscribers_html);
				$('#id_subscribers_count').empty().html(data.subscribers_count);
			}
			else{alert(gettext('Oops !!! Not able to process your request.'));}
		}
	});
}


   
function answer_flag(){
	aid = $('#id_hidden_ans').val();
	url = ajax_flag_url  
    $.ajax({
        type: "get",
        url: url,
        data: 'aid='+aid,
        dataType:'json',
        success: function(data){
                if(data.status){
                	$('#id_flag_'+aid).html("Already Flagged");
                	if (data.msg){
                		alert(data.msg);
                	}else{
						alert('flagged successfully');
					}
                }
                else{alert('Oops !!! Not able to process your request.');}                
            }
    });                                    
}

function answer_response(aid,rating,url){
    $.ajax({
        type: "get",
        url: url,
        data: 'aid='+aid+'&rating='+rating,
        dataType:'json',
        success: function(data){
                if(data.status){
					$('#id_rate_count_'+aid).html(data.total_count);
					if(data.rating == 'like'){
						$('#id_rate_vote_'+aid).html("Upvoted");
						$('#id_vote_colorup_'+aid).addClass("uPvTd");
						$('#id_vote_colordw_'+aid).removeClass("dWnvTd");
						$('#id_rate_vote_'+aid).attr("onclick", data.function);
					}else if (data.rating == 'dislike'){
						$('#id_rate_vote_'+aid).html("Downvoted");
						$('#id_vote_colorup_'+aid).removeClass("uPvTd");
						$('#id_vote_colordw_'+aid).addClass("dWnvTd");
						$('#id_rate_vote_'+aid).attr("onclick", data.function);
					}else{
						$('#id_vote_colorup_'+aid).removeClass("uPvTd");
						$('#id_vote_colordw_'+aid).removeClass("dWnvTd");
						$('#id_rate_vote_'+aid).html("Upvote");
						$('#id_rate_vote_'+aid).attr("onclick", data.function);
					}
                }
                else{alert('Oops !!! Not able to process your request.');}                
            }
    });                                    
}

function topic_follow(sub){
    $("#id_follow_icon").removeClass("bUi-iCn-pLs-16");
    $("#id_follow_icon").removeClass("bUi-iCn-oK-16");
    $("#id_follow_icon").addClass("bUi-iCnlDg-16");
	if (sub == 1){
		var url = ajax_follow_topic_url
	}
	else{
		var url = ajax_unfollow_topic_url
	}
	user_login = true;
	$.ajax({
		type:'get',
		url:url,
	    dataType:'json',
		success:function(data){
			if(data.status){
				if (sub==1){
                    $('#id_follow_icon').removeClass("bUi-iCnlDg-16");
                    $('#id_follow_icon').addClass("bUi-iCn-oK-16");
					$('#id_follow_topic .btntxt_hover').html("Unfollow");
                    $('#id_follow_topic').addClass("following");
                    $('#id_follow_topic .btntxt').html("Following");
					}
				else{
                    $('#id_follow_icon').removeClass("bUi-iCnlDg-16");
                    $('#id_follow_icon').addClass("bUi-iCn-pLs-16");
					$('#id_follow_topic .btntxt_hover').html("Follow");
                    $('#id_follow_topic .btntxt').html("Follow");
                    $('#id_follow_topic').removeClass("following");
				}
				$('#id_follow_topic').attr("onclick", data.function);
				$('#id_subscribers_count').empty().html(data.followers+" Follower(s)");
			}
			else{
			
			alert(gettext('Oops !!! Not able to process your request.'));}
		}
	});
}



    