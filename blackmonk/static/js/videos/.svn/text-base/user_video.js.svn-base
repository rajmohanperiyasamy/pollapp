/* updating a particular video */	
function edit_video_prop(id,status){
	var flag = $('#mform').validate().form()
	if(flag){
		
		var url= $('#ajax_update').val();
		var dataString='video_id='+id;
		var dataString = 'videocode='+$('#videocode').val()+'&video_id='+id+'&title='+$('#id_title').val()+'&category='+$('#id_category').val()+'&description='+$('#id_description').val()+'&yt_videos_id='+$('#yt_videos_id').val()+'&status='+status;
		$.ajax({type: "POST",
			    url: url,
			    data:dataString,
			    dataType:'JSON',
			    success: function(data){	
					if(data.status){
						clear_search();
						show_msg(data.msg,data.mtype);
						$('#update_video_description').modal('hide');
					}else{
						$("#update_video_description .modal-body").html('<div class="alert alert-warning pD0 "><div class="container-fluid"><div class="pD100 cLrFx"><p class="ib fS14 fW-bLd mRb0 mRt4">' + data.msg + '</p><div class="pLrT"></div></div></div></div>' + 	data.lightbox_html);
						$('.bM-sLt').doThis(function(){
							this.bUiSlCt();
						});
					}
				}
		});
		
	}
}
	
//######################## YouTube Functionality ##############################
var start_index=1;	
function next(){
	start_index = start_index+20;
	searching()
}

var status_search='relevence'
function searching()
{	
	if($('#id_search_from_yt').val()){}else{alert("Please enter a keyword"); return False;}
	var text=$('#id_search_from_yt').val();

	$("#service_youtube_video").hide();
	$("#service_youtube_novideo").hide();
	$("#service_youtube_loading").fadeIn();

	status_search=$('#service_youtube_searchbox .sort_by').val();
	var relevance = status_search
	var yurl='http://gdata.youtube.com/feeds/api/videos?q='+text+'&start-index='+start_index+'&format=5&max-results=20&orderby='+relevance+'&v=2&alt=jsonc'; 
	//$('#id_search_div div.lodr').css('display', 'block');
	//$('#id_search_div div.tip').css('display', 'none');
	$.ajax({
		type: "GET",url: yurl,
		dataType:"jsonp",
		success: function(response){
			var append_html= '';
			$("#service_youtube_searchbox .video_list").empty();
			if (response.data == undefined)
			{
				$("#service_youtube_loading").hide();
				$("#service_youtube_video").hide();
				$("#service_youtube_novideo").fadeIn();
				$("#service_youtube_searchbox .search-results").removeClass('vScRl');
				return false;
			}
		    if(response.data.items)
			{
				$("#service_youtube_searchbox .search-results").addClass('vScRl');
				$.each(response.data.items, function(i,data){
					//$('#service_youtube_searchbox div.lodr').hide();
					var title = data.title;
					var views =data.viewCount;
					var vid =data.id;
			        var description = data.description;
					var uploader = data.uploader;
				    var duration = 	data.duration;
					var viewCount = data.viewCount;
					
					try{
						var hr = Math.floor(duration / 3600);
						var min = Math.floor((duration - (hr * 3600))/60);
						var sec = duration - (hr * 3600) - (min * 60);
	
						if (hr < 10) {hr = "0" + hr; }
						if (min < 10) {min = "0" + min;}
						if (sec < 10) {sec = "0" + sec;}
						if(hr != 0 ){var durations = hr + ':' + min + ':' + sec;}
						else{var durations = min + ':' + sec;}
					}
					catch(e){var durations=duration;}
					
					if(description==''){
						description='';
					}
					
					append_html += '<li class="mDa" id="id_' + vid + '">'
					append_html += '    <div class="mDa-iN" onclick="check_selected(\'' + vid + '\')">'
					append_html += '		<input type="hidden" value="'+vid+'" name="v_id_'+vid+'" id="hdn_id_'+vid+'"/><input type="hidden" value="'+title+'" name="v_title'+vid+'" id="title_id_'+vid+'"/>'
					append_html += '		<input type="hidden" value="'+escape(description)+'" name="v_description_'+vid+'"  id="desc_id_'+vid+'"/>'
					append_html += '		<input type="hidden" name="durations'+vid+'"  value="'+durations+'" id = "durations_id'+vid+'">';
					append_html += '        <div class="mDa-wPr mRr10">'
					append_html += '            <span class="bUi-tMb-wPr tMb-60 bUi-tMb-120 fLxiMgH">'
					append_html += '                <span class="bUi-tMb">'
					append_html += '                    <span class="bUi-tMb-pRpL">'
					append_html += '                        <span class="bUi-tMb-cLp">'
					append_html += '                            <span class="bUi-tMb-cLp-iN"> <img class="mDa-oT" src="http://i.ytimg.com/vi/'+data.id+'/mqdefault.jpg" alt="">'
					append_html += '                                <span class="vRtL-aLn"> </span>'
					append_html += '                            </span>'
					append_html += '                        </span>'
					append_html += '                    </span>'
					append_html += '                </span>'
					append_html += '            </span>'
					append_html += '            <div class="mDa-hVr cVr tR-hVr"><span class="bR5"><span class="lBl dRk mNi" href="javascript:void(0);">'+durations+'</span></span></div>' 
					append_html += '            <div class="mDa-hVr cVr tR-hVr fxslider"><a href="javascript:void(0);" data-src="http://www.youtube.com/watch?v=' + vid + '" class="s-32 cTr"><i aria-hidden="true" class="bUi-iCn-pLy-aLt-24 hT-aTo fS32-1 pLy-iCn"></i></a></div>'
					append_html += '        </div>'
					append_html += '        <div class="mDa-bDy pD0">'
					append_html += '            <h5 class="mDa-hD fS13 mRb0 tRnCt0 mRt4" title="' + title + '"><span class="cLr-dRk  mXh35 dSlH bLk">' + title.slice(0,25) + '</span></h5>'
					append_html += '            <div class="mDa-dTa fS11 cLr-gRy mRb5">'
					append_html += '				<span>by <a href="javascript:void(0);" class="cLr-lTbLu">' + uploader + '</a></span><span class="sPrTr">' + viewCount + ' views</span><span class="cLr-lTgRy bLk lH1">'+durations+'</span>'
					append_html += '            </div>'
					append_html += '        </div>'
					append_html += '        <span class="sLcT-iCn aBsLt bR10"><i aria-hidden="true" class="bUi-iCn-oK-aLt-16 fS18"></i></span>'
					append_html += '    </div>'
					append_html += '</li>'				   

				});
				$("#service_youtube_searchbox .video_list").append(append_html);
				setTimeout(function(){
					$('.fLxiMgH').setrSpVHeight('mDa-lT');
				});
				$(".fxslider").fxslider({thumbnail:false,mobileSrc:false});

				$("#service_youtube_loading").hide();
				$("#service_youtube_novideo").hide();
				$("#service_youtube_video").fadeIn();
			}else{
				$("#service_youtube_loading").hide();
				$("#service_youtube_video").hide();
				$("#service_youtube_novideo").fadeIn();
				$("#service_youtube_searchbox .search-results").removeClass('vScRl');
			}	
		}
		
	});
}
var fxsliderNumber = 0;
function load_more()
{
	if($('#id_search_from_yt').val()){}else{alert("Please enter a keyword"); return False;}
	var text=$('#id_search_from_yt').val();

	$("#service_youtube_searchbox .extra_loading").removeClass('hide');

	status_search=$('#service_youtube_searchbox .sort_by').val();
	start_index=start_index+20;
	var relevance = status_search
	var yurl='http://gdata.youtube.com/feeds/api/videos?q='+text+'&start-index='+start_index+'&format=5&max-results=20&orderby='+relevance+'&v=2&alt=jsonc';
	$.ajax({
		type: "GET",url: yurl,
		dataType:"jsonp",
		success: function(response){
			var append_html= '';
			if(response.data.items)
			{
		        $.each(response.data.items, function(i,data){
					//$('#id_search_div div.lodr').css('display', 'none');
					//$('#id_search_div .video-library .tip').css('display', 'none');
				    //$('#id_search_div .video-library .hang-items').css('display', 'none');
					var title = data.title;
					var views = data.viewCount;
					var vid = data.id;
			        var description = data.description;
					var uploader = data.uploader;// apply it after getting the new ui for uploading 
				    var duration = data.duration;
					var viewCount = data.viewCount;

					try{
						var hr = Math.floor(duration / 3600);
						var min = Math.floor((duration - (hr * 3600))/60);
						var sec = duration - (hr * 3600) - (min * 60);
	
						if (hr < 10) {hr = "0" + hr; }
						if (min < 10) {min = "0" + min;}
						if (sec < 10) {sec = "0" + sec;}
						if(hr != 0 ){var durations = hr + ':' + min + ':' + sec;}
						else{var durations = min + ':' + sec;}
					}
					catch(e){var durations=duration;}

					append_html += '<li class="mDa" id="id_' + vid + '">'
					append_html += '    <div class="mDa-iN" onclick="check_selected(\'' + vid + '\')">'
					append_html += '		<input type="hidden" value="'+vid+'" name="v_id_'+vid+'" id="hdn_id_'+vid+'"/><input type="hidden" value="'+title+'" name="v_title'+vid+'" id="title_id_'+vid+'"/>'
					append_html += '		<input type="hidden" value="'+escape(description)+'" name="v_description_'+vid+'"  id="desc_id_'+vid+'"/>'
					append_html += '		<input type="hidden" name="durations'+vid+'"  value="'+durations+'" id = "durations_id'+vid+'">';
					append_html += '        <div class="mDa-wPr mRr10">'
					append_html += '            <span class="bUi-tMb-wPr tMb-60 bUi-tMb-120 fLxiMgH">'
					append_html += '                <span class="bUi-tMb">'
					append_html += '                    <span class="bUi-tMb-pRpL">'
					append_html += '                        <span class="bUi-tMb-cLp">'
					append_html += '                            <span class="bUi-tMb-cLp-iN"> <img class="mDa-oT" src="http://i.ytimg.com/vi/'+data.id+'/mqdefault.jpg" alt="">'
					append_html += '                                <span class="vRtL-aLn"> </span>'
					append_html += '                            </span>'
					append_html += '                        </span>'
					append_html += '                    </span>'
					append_html += '                </span>'
					append_html += '            </span>'
					append_html += '            <div class="mDa-hVr cVr tR-hVr"><span class="bR5"><span class="lBl dRk mNi" href="javascript:void(0);">'+durations+'</span></span></div>' 
					append_html += '            <div class="mDa-hVr cVr tR-hVr fxslider'+fxsliderNumber+'"><a href="javascript:void(0);" data-src="http://www.youtube.com/watch?v=' + vid + '" class="s-32 cTr"><i aria-hidden="true" class="bUi-iCn-pLy-aLt-24 hT-aTo fS32-1 pLy-iCn"></i></a></div>'
					append_html += '        </div>'
					append_html += '        <div class="mDa-bDy pD0">'
					append_html += '            <h5 class="mDa-hD fS13 mRb0 tRnCt0 mRt4" title="' + title + '"><span class="cLr-dRk  mXh35 dSlH bLk">' + title.slice(0,25) + '</span></h5>'
					append_html += '            <div class="mDa-dTa fS11 cLr-gRy mRb5">'
					append_html += '				<span>by <a href="javascript:void(0);" class="cLr-lTbLu">' + uploader + '</a></span><span class="sPrTr">' + viewCount + ' views</span><span class="cLr-lTgRy bLk lH1">'+durations+'</span>'
					append_html += '            </div>'
					append_html += '        </div>'
					append_html += '        <span class="sLcT-iCn aBsLt bR10"><i aria-hidden="true" class="bUi-iCn-oK-aLt-16 fS18"></i></span>'
					append_html += '    </div>'
					append_html += '</li>'                                    
				});
				$("#service_youtube_searchbox .extra_loading").addClass('hide');
				$("#service_youtube_searchbox .video_list").append(append_html);
				$(".fxslider"+fxsliderNumber).fxslider({thumbnail:false,mobileSrc:false});
			}
			else{
				$("#service_youtube_searchbox .extra_loading").addClass('hide');
			}	
		},
		
	});
	fxsliderNumber++;
}

var status_search_viemo='relevence'
function searching_vimeo(){
	
	if($('#id_search_from_yt_viemo').val()){}else{alert("Please enter a keyword"); return False;}
	var text=$('#id_search_from_yt_viemo').val();

	$("#service_vimeo_video").hide();
	$("#service_vimeo_novideo").hide();
	$("#service_vimeo_loading").fadeIn();

	if($.trim(text)==''){$('#id_search_from_yt_viemo').closest('div').addClass('field-error');return false;}
	else{$('#id_search_from_yt_viemo').parent('div').removeClass('field-error');}
	status_search_viemo=$('#service_vimeo_searchbox .sort_by').val();
	var relevance = status_search_viemo
	$.ajax({
		type: "GET",
		url: "/staff/videos/vimeo-video-search?sort="+relevance+"&page=1&q="+text,
		dataType:"json",
		success: function(response){
			var append_html= '';
			$("#id_search_div_vimeo .video_list").empty();
			if(response != '0'){
				$("#service_vimeo_searchbox .search-results").addClass('vScRl');
		        $.each(response, function(i,data){
					$('#id_search_div_vimeo div.lodr').hide();
					var title = data.title;
					var vid =data.id;
			        var description = data.description;
					var uploader = data.username;
					var image_url=data.image_url
					var duration = 	data.duration;
					try{image_url = image_url.replace('_100','_640')}
					catch(e){}

					try{
						var hr = Math.floor(duration / 3600);
						var min = Math.floor((duration - (hr * 3600))/60);
						var sec = duration - (hr * 3600) - (min * 60);
	
						if (hr < 10) {hr = "0" + hr; }
						if (min < 10) {min = "0" + min;}
						if (sec < 10) {sec = "0" + sec;}
						if(hr != 0 ){var durations = hr + ':' + min + ':' + sec;}
						else{var durations = min + ':' + sec;}
					}
					catch(e){var durations=duration;}

					append_html += '<li class="mDa" id="id_' + vid + '">'
					append_html += '    <div class="mDa-iN" onclick="check_selected_vimeo(\'' + vid + '\')">'
					append_html += '		<input type="hidden" value="'+vid+'" name="v_id_'+vid+'" id="hdn_id_'+vid+'"/><input type="hidden" value="'+title+'" name="v_title'+vid+'" id="title_id_'+vid+'"/>'
					append_html += '		<input type="hidden" value="'+escape(description)+'" name="v_description_'+vid+'"  id="desc_id_'+vid+'"/>'
					append_html += '		<input type="hidden" name="durations'+vid+'"  value="'+durations+'" id = "durations_id'+vid+'">';
					append_html += '		<input type="hidden" name="img_large'+vid+'"  value="'+image_url+'" id = "img_large_'+vid+'">';
					append_html += '        <div class="mDa-wPr mRr10">'
					append_html += '            <span class="bUi-tMb-wPr tMb-60 bUi-tMb-120 fLxiMgH">'
					append_html += '                <span class="bUi-tMb">'
					append_html += '                    <span class="bUi-tMb-pRpL">'
					append_html += '                        <span class="bUi-tMb-cLp">'
					append_html += '                            <span class="bUi-tMb-cLp-iN"> <img class="mDa-oT" src="'+image_url+'" alt="'+ title.slice(0,25) +'">'
					append_html += '                                <span class="vRtL-aLn"> </span>'
					append_html += '                            </span>'
					append_html += '                        </span>'
					append_html += '                    </span>'
					append_html += '                </span>'
					append_html += '            </span>'
					append_html += '            <div class="mDa-hVr cVr tR-hVr"><span class="bR5"><span class="lBl dRk mNi" href="javascript:void(0);">'+durations+'</span></span></div>' 
					append_html += '            <div class="mDa-hVr cVr tR-hVr fxslider"><a href="javascript:void(0);" data-src="http://vimeo.com/' + vid + '" class="s-32 cTr"><i aria-hidden="true" class="bUi-iCn-pLy-aLt-24 hT-aTo fS32-1 pLy-iCn"></i></a></div>'
					append_html += '        </div>'
					append_html += '        <div class="mDa-bDy pD0">'
					append_html += '            <h5 class="mDa-hD fS13 mRb0 tRnCt0 mRt4" title="' + title + '"><span class="cLr-dRk  mXh35 dSlH bLk">' + title.slice(0,25) + '</span></h5>'
					append_html += '            <div class="mDa-dTa fS11 cLr-gRy mRb5">'
					append_html += '				<span>by <a href="javascript:void(0);" class="cLr-lTbLu">' + uploader + '</a></span><span class="sPrTr">' + data.no_plays + ' views</span><span class="cLr-lTgRy bLk lH1">'+durations+'</span>'
					append_html += '            </div>'
					append_html += '        </div>'
					append_html += '        <span class="sLcT-iCn aBsLt bR10"><i aria-hidden="true" class="bUi-iCn-oK-aLt-16 fS18"></i></span>'
					append_html += '    </div>'
					append_html += '</li>'                                    
				   
				});
				$('#user-selected-submit').removeAttr('disabled','disabled');
				$("#service_vimeo_searchbox .video_list").html(append_html);
				setTimeout(function(){
					$('.fLxiMgH').setrSpVHeight('mDa-lT');
				});
				$(".fxslider").fxslider({thumbnail:false,mobileSrc:false});
				$("#service_vimeo_loading").hide();
				$("#service_vimeo_novideo").hide();
				$("#service_vimeo_video").fadeIn();
			}else{
				$("#service_vimeo_loading").hide();
				$("#service_vimeo_video").hide();
				$("#service_vimeo_novideo").fadeIn();
				$("#service_vimeo_searchbox .search-results").removeClass('vScRl');
			}		
		}
	});
}

var page_index=1
function load_more_vimeo(){
	page_index=page_index+1
	if($('#id_search_from_yt_viemo').val()){}else{alert("Please enter a keyword"); return False;}
	var text=$('#id_search_from_yt_viemo').val();

	$("#service_vimeo_searchbox .extra_loading").removeClass('hide');
	status_search_viemo = $('#service_vimeo_searchbox .sort_by').val();
	var relevance = status_search_viemo;
	$.ajax({
		type: "GET",
		url: "/staff/videos/vimeo-video-search?sort="+relevance+"&q="+text+"&page="+page_index,
		dataType:"json",
		success: function(response){
			var append_html= '';
			if(response){
		        $.each(response, function(i,data){
					$('#id_search_div_vimeo div.lodr').hide();
					var title = data.title;
					var vid =data.id;
			        var description = data.description;
					var uploader = data.username;
					var image_url=data.image_url
					var duration = 	data.duration;

					try{image_url = image_url.replace('_100','_640')}
					catch(e){}

					try{
						var hr = Math.floor(duration / 3600);
						var min = Math.floor((duration - (hr * 3600))/60);
						var sec = duration - (hr * 3600) - (min * 60);
	
						if (hr < 10) {hr = "0" + hr; }
						if (min < 10) {min = "0" + min;}
						if (sec < 10) {sec = "0" + sec;}
						if(hr != 0 ){var durations = hr + ':' + min + ':' + sec;}
						else{var durations = min + ':' + sec;}
					}
					catch(e){var durations=duration;}

					append_html += '<li class="mDa" id="id_' + vid + '">'
					append_html += '    <div class="mDa-iN" onclick="check_selected_vimeo(\'' + vid + '\')">'
					append_html += '		<input type="hidden" value="'+vid+'" name="v_id_'+vid+'" id="hdn_id_'+vid+'"/><input type="hidden" value="'+title+'" name="v_title'+vid+'" id="title_id_'+vid+'"/>'
					append_html += '		<input type="hidden" value="'+escape(description)+'" name="v_description_'+vid+'"  id="desc_id_'+vid+'"/>'
					append_html += '		<input type="hidden" name="durations'+vid+'"  value="'+durations+'" id = "durations_id'+vid+'">';
					append_html += '		<input type="hidden" name="img_large'+vid+'"  value="'+image_url+'" id = "img_large_'+vid+'">';
					append_html += '        <div class="mDa-wPr mRr10">'
					append_html += '            <span class="bUi-tMb-wPr tMb-60 bUi-tMb-120 fLxiMgH">'
					append_html += '                <span class="bUi-tMb">'
					append_html += '                    <span class="bUi-tMb-pRpL">'
					append_html += '                        <span class="bUi-tMb-cLp">'
					append_html += '                            <span class="bUi-tMb-cLp-iN"> <img class="mDa-oT" src="'+image_url+'" alt="'+ title.slice(0,25) +'">'
					append_html += '                                <span class="vRtL-aLn"> </span>'
					append_html += '                            </span>'
					append_html += '                        </span>'
					append_html += '                    </span>'
					append_html += '                </span>'
					append_html += '            </span>'
					append_html += '            <div class="mDa-hVr cVr tR-hVr"><span class="bR5"><span class="lBl dRk mNi" href="javascript:void(0);">'+durations+'</span></span></div>' 
					append_html += '            <div class="mDa-hVr cVr tR-hVr fxslider'+fxsliderNumber+'"><a href="javascript:void(0);" data-src="http://vimeo.com/' + vid + '" class="s-32 cTr"><i aria-hidden="true" class="bUi-iCn-pLy-aLt-24 hT-aTo fS32-1 pLy-iCn"></i></a></div>'
					append_html += '        </div>'
					append_html += '        <div class="mDa-bDy pD0">'
					append_html += '            <h5 class="mDa-hD fS13 mRb0 tRnCt0 mRt4" title="' + title + '"><span class="cLr-dRk  mXh35 dSlH bLk">' + title.slice(0,25) + '</span></h5>'
					append_html += '            <div class="mDa-dTa fS11 cLr-gRy mRb5">'
					append_html += '				<span>by <a href="javascript:void(0);" class="cLr-lTbLu">' + uploader + '</a></span><span class="sPrTr">' + data.no_plays + ' views</span><span class="cLr-lTgRy bLk lH1">'+durations+'</span>'
					append_html += '            </div>'
					append_html += '        </div>'
					append_html += '        <span class="sLcT-iCn aBsLt bR10"><i aria-hidden="true" class="bUi-iCn-oK-aLt-16 fS18"></i></span>'
					append_html += '    </div>'
					append_html += '</li>'                                     
				   
				});
				$("#service_vimeo_searchbox .extra_loading").addClass('hide');
				$("#service_vimeo_searchbox .video_list").append(append_html);
				setTimeout(function(){
					$('.fLxiMgH').setrSpVHeight('mDa-lT');
				});
				$(".fxslider"+fxsliderNumber).fxslider({thumbnail:false,mobileSrc:false});
			}else{
				$("#service_youtube_searchbox .extra_loading").addClass('hide');
			}	
		}
	});
	fxsliderNumber++;
}
var vimeo_scroll_reaching_bottom = false;
$("#service_vimeo_searchbox .search-results").scroll(function() {
    var pad = 20;
    var buffer = 40 + pad;
    var myPos = $("#service_vimeo_searchbox .search-results").prop('scrollHeight') - $("#service_vimeo_searchbox .search-results").scrollTop();
    var endPos = $("#service_vimeo_searchbox .search-results").height(); 
    if (myPos <= endPos + buffer )   {
		if ( vimeo_scroll_reaching_bottom ){
			if( myPos <= endPos + pad ){
				vimeo_scroll_reaching_bottom = false;
			}
		}
		else{
			vimeo_scroll_reaching_bottom = true;
			load_more();
		} 
    }
});
//***************************************888 Adding Video Using Url ************************************************
function share_by_url(){
    src = $("#share_by_video_url").val();

    var youtube = src.match(/^(?:https?:\/\/)?(?:www\.)?(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))((\w|-){11})(?:\S+)?$/);
    var vimeo = src.match(/vimeo\.com\/([0-9]*)/);

    if(youtube){
        addInput();
    }
    else if(vimeo){
        addInput_vimeo();
    }
    else{
        alert('enter valid url');
    }
}

function addInput(){
	var text=$("#share_by_video_url").val();
	var p = /^(?:https?:\/\/)?(?:www\.)?(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))((\w|-){11})(?:\S+)?$/;
  	var matches = (text.match(p)) ? RegExp.$1 : false;
  	var yurl='http://gdata.youtube.com/feeds/api/videos?q='+matches+'&format=5&max-results=1&v=2&alt=jsonc'; 
  	var ahtml = '';
	var classid = uniqId();
  	$.ajax({
		type: "GET",url: yurl,
		dataType:"jsonp",
		success: function(response){
			if(response.data.items)
			{   
		        $.each(response.data.items, function(i,data){
					var title = data.title;
					var views =data.viewCount;
					var id =data.id;
			        var description = data.description;
					var duration = 	data.duration;
					try{
						var hr = Math.floor(duration / 3600);
						var min = Math.floor((duration - (hr * 3600))/60);
						var sec = duration - (hr * 3600) - (min * 60);
	
						if (hr < 10) {hr = "0" + hr; }
						if (min < 10) {min = "0" + min;}
						if (sec < 10) {sec = "0" + sec;}
						if(hr != 0 ){var durations = hr + ':' + min + ':' + sec;}
						else{var durations = min + ':' + sec;}
					}
					catch(e){var durations=duration;}
					
					ahtml+='<li class="mDa" id="sid_' + id + '">'
					ahtml+='    <div class="mDa-iN">'
					ahtml+='		<input type = "hidden" name="videoids" id = "id_'+id+'" value = "'+id+'"><input type = "hidden" name="title_'+id+'" value="'+title+'" id="title_'+id+'">'
					ahtml+='		<input type="hidden" name="description_'+id+'"  value="'+description+'" id = "description_'+id+'">'
					ahtml+='		<input type="hidden" name="durations'+id+'"  value="'+duration+'" id = "durations'+id+'">';
					ahtml+='        <div class="mDa-wPr mRr10">' 
					ahtml+='            <span class="bUi-tMb-wPr tMb-60 bUi-tMb-120 fLxiMgW">'
					ahtml+='                <span class="bUi-tMb">'
					ahtml+='                    <span class="bUi-tMb-pRpL">'
					ahtml+='                        <span class="bUi-tMb-cLp">'
					ahtml+='                            <span class="bUi-tMb-cLp-iN"> <img class="mDa-oT" src="http://i1.ytimg.com/vi/'+id+'/mqdefault.jpg" alt="'+title+'">'
					ahtml+='                                <span class="vRtL-aLn"> </span>'
					ahtml+='                            </span>'
					ahtml+='                        </span>'
					ahtml+='                    </span>'
					ahtml+='                </span>'
					ahtml+='            </span>'
					ahtml+='            <div class="mDa-hVr cVr tR-hVr"><span class="bR5"><span class="lBl dRk mNi" href="#">'+duration+'</span></span></div>'
					ahtml+='            <div class="mDa-hVr cVr tR-hVr fxslider'+classid+'"><a href="javascript:void(0);" data-src="http://www.youtube.com/watch?v='+id+'" class="s-32 cTr"><i aria-hidden="true" class="bUi-iCn-pLy-aLt-24 hT-aTo fS32-1 pLy-iCn"></i></a></div>'
					ahtml+='        </div>'
					ahtml+='        <div class="mDa-bDy pD0">'
					ahtml+='            <h5 class="mDa-hD fS13 mRb0 tRnCt0 mRt10" title="'+title+'"><span class="cLr-dRk h35 dSlH bLk">'+title+'</span></h5>'
					ahtml+='        </div>'
					ahtml+='        <span onclick="remove_video(\''+id+'\')" class="aBsLt tR-5 lH1 zI1"><a href="javascript:void(0);" class="ib lH1"><i aria-hidden="true" class="bUi-iCn-rMv-aLt-16 cLs-iCn"></i></a></span>'
					ahtml+='    </div>'
					ahtml+='</li>'

					$('#id_video_slider').prepend(ahtml);
					setTimeout(function(){
						$('.fLxiMgW').setrSpVWidth(0);
					});
					$("#share_by_video_url").val("");
					$('#selected_videos').show();
					$(".fxslider"+classid).fxslider({thumbnail:false,mobileSrc:false});	
					$('#d_selected_videos_count').text(''+$('#id_video_slider li').size());
				
				    video_ids.push(id);
				    var vcount = $('#id_video_slider li').size();
					if(vcount == 0){
						$('#selected_videos').fadeOut();
						$('#user-selected-submit').attr('disabled','disabled');
						$('#user-selected-submit').addClass("dSbLd");
					}
					else{
						$('#user-selected-submit').removeAttr('disabled','disabled');
						$('#user-selected-submit').removeClass("dSbLd");
					}

				});
			}
		}
	});
}

function addInput_vimeo(){
	var text=$("#share_by_video_url").val();
	
	var matches = $("#share_by_video_url").val().match(/^(http|https):\/\/(?:www\.|player\.)?(vimeo)\.com\/(watch\?[^#]*v=(\w+)|(\d+)).+$/);
	var video_id=text.split('.com/')
	video_id=video_id[1].split('/')
	video_id=video_id[0]
	var classid = uniqId();
  	if (matches) {
	  	var yurl='http://vimeo.com/api/v2/video/'+video_id+'.json'; 
	  	var ahtml = '';	
	  	$.ajax({
			type: "GET",url: yurl,
			dataType:"jsonp",
			success: function(response){
				if(response[0]){	
					var title = response[0].title;
					var id =response[0].id;
			        var description = escape(response[0].description);
					var uploader = response[0].user_name;
					var image_url=response[0].thumbnail_small
					var img_large = response[0].thumbnail_large;
					var duration = response[0].duration;
					
					try{
						var hr = Math.floor(duration / 3600);
						var min = Math.floor((duration - (hr * 3600))/60);
						var sec = duration - (hr * 3600) - (min * 60);
	
						if (hr < 10) {hr = "0" + hr; }
						if (min < 10) {min = "0" + min;}
						if (sec < 10) {sec = "0" + sec;}
						if(hr != 0 ){var durations = hr + ':' + min + ':' + sec;}
						else{var durations = min + ':' + sec;}
					}
					catch(e){var durations=duration;}	
									
					ahtml+='<li class="mDa" id="sid_' + id + '">'
					ahtml+='    <div class="mDa-iN">'
					ahtml+='		<input type="hidden" name="videoids" id = "id_'+id+'" value = "'+id+'"><input type = "hidden" name="title_'+id+'" value="'+title+'" id="title_'+id+'">'
					ahtml+='		<input type="hidden" name="description_'+id+'"  value="'+description+'" id = "description_'+id+'">'
					ahtml+='		<input type="hidden" name="durations'+id+'"  value="'+duration+'" id = "durations'+id+'">';
					ahtml+='		<input type="hidden" name="img_large'+id+'"  value="'+image_url+'" id = "img_large_'+id+'">';
					ahtml+='        <div class="mDa-wPr mRr10">' 
					ahtml+='            <span class="bUi-tMb-wPr tMb-60 bUi-tMb-120 fLxiMgW">'
					ahtml+='                <span class="bUi-tMb">'
					ahtml+='                    <span class="bUi-tMb-pRpL">'
					ahtml+='                        <span class="bUi-tMb-cLp">'
					ahtml+='                            <span class="bUi-tMb-cLp-iN"> <img class="mDa-oT" src="'+image_url+'" alt="'+title+'">'
					ahtml+='                                <span class="vRtL-aLn"> </span>'
					ahtml+='                            </span>'
					ahtml+='                        </span>'
					ahtml+='                    </span>'
					ahtml+='                </span>'
					ahtml+='            </span>'
					ahtml+='            <div class="mDa-hVr cVr tR-hVr"><span class="bR5"><span class="lBl dRk mNi" href="#">'+duration+'</span></span></div>'
					ahtml+='            <div class="mDa-hVr cVr tR-hVr fxslider'+classid+'"><a href="javascript:void(0);" data-src="http://vimeo.com/'+id+'" class="s-32 cTr"><i aria-hidden="true" class="bUi-iCn-pLy-aLt-24 hT-aTo fS32-1 pLy-iCn"></i></a></div>'
					ahtml+='        </div>'
					ahtml+='        <div class="mDa-bDy pD0">'
					ahtml+='            <h5 class="mDa-hD fS13 mRb0 tRnCt0 mRt10" title="'+title+'"><span class="cLr-dRk h35 dSlH bLk">'+title+'</span></h5>'
					ahtml+='        </div>'
					ahtml+='        <span onclick="remove_video_vimeo(\''+id+'\')" class="aBsLt tR-5 lH1 zI1"><a href="javascript:void(0);" class="ib lH1"><i aria-hidden="true" class="bUi-iCn-rMv-aLt-16 cLs-iCn"></i></a></span>'
					ahtml+='    </div>'
					ahtml+='</li>'

					$('#id_video_slider').prepend(ahtml);
					setTimeout(function(){
						$('.fLxiMgW').setrSpVWidth(0);
					});
					$("#share_by_video_url").val("");
					$('#selected_videos').show();	
					$(".fxslider"+classid).fxslider({thumbnail:false,mobileSrc:false});
					$('#d_selected_videos_count').text(''+$('#id_video_slider li').size());
				    vimeo_video_ids.push(id);
				    var vcount = $('#id_video_slider li').size();
					if(vcount == 0){
						$('#selected_videos').fadeOut();
						$('#user-selected-submit').attr('disabled','disabled');
						$('#user-selected-submit').addClass("dSbLd");
					}
					else{
						$('#user-selected-submit').removeAttr('disabled','disabled');
						$('#user-selected-submit').removeClass("dSbLd");
					}

				}else {
					alert('Please Enter a valid url');
					return false;
				}
			}
		});
	}else {
		alert('Please Enter a valid url');
		return false;
	}
}





//  *****************************************  Select And remove frm the bucket ***************************************8

var video_ids=[];
var selected_ids = [];
var vimeo_video_ids=[];

function check_selected(id){
	var title = $('#title_id_'+id).val();
	var description =$('#desc_id_'+id).val();
	var duration = $('#durations_id'+id).val();
	//$('#id_span_icon_tick_'+id).show();
	//$('#id_span_play_icon_'+id).css('pointer-events','none');
	
	$('#id_'+id).addClass('sLcT');
	//$('#id_'+id).attr('disabled','disabled');
	$('#id_'+id).css('pointer-events','none');

	var ahtml="";
	
	ahtml+='<li class="mDa" id="sid_' + id + '">'
	ahtml+='    <div class="mDa-iN">'
	ahtml+='		<input type = "hidden" name="videoids" id = "id_'+id+'" value = "'+id+'"><input type = "hidden" name="title_'+id+'" value="'+title+'" id="title_'+id+'">'
	ahtml+='		<input type="hidden" name="description_'+id+'"  value="'+description+'" id = "description_'+id+'">'
	ahtml+='		<input type="hidden" name="durations'+id+'"  value="'+duration+'" id = "durations'+id+'">';
	ahtml+='        <div class="mDa-wPr mRr10">' 
	ahtml+='            <span class="bUi-tMb-wPr tMb-60 bUi-tMb-120 fLxiMgW">'
	ahtml+='                <span class="bUi-tMb">'
	ahtml+='                    <span class="bUi-tMb-pRpL">'
	ahtml+='                        <span class="bUi-tMb-cLp">'
	ahtml+='                            <span class="bUi-tMb-cLp-iN"> <img class="mDa-oT" src="http://i1.ytimg.com/vi/'+id+'/mqdefault.jpg" alt="'+title+'">'
	ahtml+='                                <span class="vRtL-aLn"> </span>'
	ahtml+='                            </span>'
	ahtml+='                        </span>'
	ahtml+='                    </span>'
	ahtml+='                </span>'
	ahtml+='            </span>'
	ahtml+='            <div class="mDa-hVr cVr tR-hVr"><span class="bR5"><span class="lBl dRk mNi" href="#">'+duration+'</span></span></div>'
	ahtml+='            <div class="mDa-hVr cVr tR-hVr" id="fxslider_'+id+'"><a href="javascript:void(0);" data-src="http://www.youtube.com/watch?v='+id+'" class="s-32 cTr"><i aria-hidden="true" class="bUi-iCn-pLy-aLt-24 hT-aTo fS32-1 pLy-iCn"></i></a></div>'
	ahtml+='        </div>'
	ahtml+='        <div class="mDa-bDy pD0">'
	ahtml+='            <h5 class="mDa-hD fS13 mRb0 tRnCt0 mRt10" title="'+title+'"><span class="cLr-dRk h35 dSlH bLk">'+title+'</span></h5>'
	ahtml+='        </div>'
	ahtml+='        <span onclick="remove_video(\''+id+'\')" class="aBsLt tR-5 lH1 zI1"><a href="javascript:void(0);" class="ib lH1"><i aria-hidden="true" class="bUi-iCn-rMv-aLt-16 cLs-iCn"></i></a></span>'
	ahtml+='    </div>'
	ahtml+='</li>'

	$('#id_video_slider').prepend(ahtml);
	setTimeout(function(){
		$('.fLxiMgW').setrSpVWidth(0);
	});

	$('#selected_videos').show();
	$("#fxslider_"+id).fxslider({thumbnail:false,mobileSrc:false});	
	$('#d_selected_videos_count').text(''+$('#id_video_slider li').size());

    video_ids.push(id);
    var vcount = $('#id_video_slider li').size();
	if(vcount == 0){
		$('#selected_videos').fadeOut();
		$('#user-selected-submit').attr('disabled','disabled');
		$('#user-selected-submit').addClass("dSbLd");
	}
	else{
		$('#user-selected-submit').removeAttr('disabled','disabled');
		$('#user-selected-submit').removeClass("dSbLd");
	}

}

function check_selected_vimeo(id,url){
	var title = $('#title_id_'+id).val();
	var description =$('#desc_id_'+id).val();
	var duration = $('#durations_id'+id).val();
    var image_url = $('#img_large_'+id).val();

	$('#id_'+id).addClass('sLcT');
	$('#id_'+id).css('pointer-events','none');

	var ahtml="";

	ahtml+='<li class="mDa" id="sid_' + id + '">'
	ahtml+='    <div class="mDa-iN">'
	ahtml+='		<input type="hidden" name="videoids" id = "id_'+id+'" value = "'+id+'"><input type = "hidden" name="title_'+id+'" value="'+title+'" id="title_'+id+'">'
	ahtml+='		<input type="hidden" name="description_'+id+'"  value="'+description+'" id = "description_'+id+'">'
	ahtml+='		<input type="hidden" name="durations'+id+'"  value="'+duration+'" id = "durations'+id+'">';
	ahtml+='		<input type="hidden" name="img_large'+id+'"  value="'+image_url+'" id = "img_large_'+id+'">';
	ahtml+='        <div class="mDa-wPr mRr10">' 
	ahtml+='            <span class="bUi-tMb-wPr tMb-60 bUi-tMb-120 fLxiMgW">'
	ahtml+='                <span class="bUi-tMb">'
	ahtml+='                    <span class="bUi-tMb-pRpL">'
	ahtml+='                        <span class="bUi-tMb-cLp">'
	ahtml+='                            <span class="bUi-tMb-cLp-iN"> <img class="mDa-oT" src="'+image_url+'" alt="'+title+'">'
	ahtml+='                                <span class="vRtL-aLn"> </span>'
	ahtml+='                            </span>'
	ahtml+='                        </span>'
	ahtml+='                    </span>'
	ahtml+='                </span>'
	ahtml+='            </span>'
	ahtml+='            <div class="mDa-hVr cVr tR-hVr"><span class="bR5"><span class="lBl dRk mNi" href="#">'+duration+'</span></span></div>'
	ahtml+='            <div class="mDa-hVr cVr tR-hVr" id="fxslider_'+id+'"><a href="javascript:void(0);" data-src="http://vimeo.com/'+id+'" class="s-32 cTr"><i aria-hidden="true" class="bUi-iCn-pLy-aLt-24 hT-aTo fS32-1 pLy-iCn"></i></a></div>'
	ahtml+='        </div>'
	ahtml+='        <div class="mDa-bDy pD0">'
	ahtml+='            <h5 class="mDa-hD fS13 mRb0 tRnCt0 mRt10" title="'+title+'"><span class="cLr-dRk h35 dSlH bLk">'+title+'</span></h5>'
	ahtml+='        </div>'
	ahtml+='        <span onclick="remove_video_vimeo(\''+id+'\')" class="aBsLt tR-5 lH1 zI1"><a href="javascript:void(0);" class="ib lH1"><i aria-hidden="true" class="bUi-iCn-rMv-aLt-16 cLs-iCn"></i></a></span>'
	ahtml+='    </div>'
	ahtml+='</li>'

	$('#id_video_slider').prepend(ahtml);
	setTimeout(function(){
		$('.fLxiMgW').setrSpVWidth(0);
	});
	$('#selected_videos').show();	
	$("#fxslider_"+id).fxslider({thumbnail:false,mobileSrc:false});
	$('#d_selected_videos_count').text(''+$('#id_video_slider li').size());
    vimeo_video_ids.push(id);
    var vcount = $('#id_video_slider li').size();
	if(vcount == 0){
		$('#selected_videos').fadeOut();
		$('#user-selected-submit').attr('disabled','disabled');
		$('#user-selected-submit').addClass("dSbLd");
	}
	else{
		$('#user-selected-submit').removeAttr('disabled','disabled');
		$('#user-selected-submit').removeClass("dSbLd");
	}
}

function remove_video(id){
	$('#sid_'+id).remove();
	$('#d_selected_videos_count').text(''+$('#id_video_slider li').size());
	$('#id_'+id).css('pointer-events','auto');
	video_ids.splice( $.inArray(id, video_ids), 1 );
	$('#id_'+id).removeClass('sLcT');
	var vcount = $('#id_video_slider li').size();
	if(vcount == 0){
		$('#selected_videos').fadeOut();
		$('#user-selected-submit').attr('disabled','disabled');
		$('#user-selected-submit').addClass("dSbLd");
	}
	else{
		$('#user-selected-submit').removeAttr('disabled','disabled');
		$('#user-selected-submit').removeClass("dSbLd");
	}
}
function remove_video_vimeo(id){
 	$('#sid_'+id).remove();
	$('#d_selected_videos_count').text(''+$('#id_video_slider li').size());
	$('#id_'+id).css('pointer-events','auto');
	vimeo_video_ids.splice( $.inArray(id, vimeo_video_ids), 1 );
	$('#id_'+id).removeClass('sLcT');
	var vcount = $('#id_video_slider li').size();
	if(vcount == 0){
		$('#selected_videos').fadeOut();
		$('#user-selected-submit').attr('disabled','disabled');
		$('#user-selected-submit').addClass("dSbLd");
	}
	else{
		$('#user-selected-submit').removeAttr('disabled','disabled');
		$('#user-selected-submit').removeClass("dSbLd");
	}
}
// ********************************   Save Selected Video *******************************

function savevideo_now(){
	$('#user-selected-submit').attr('disabled','disabled');
	$('#user-selected-submit').addClass("dSbLd");
	$('#user-selected-submit').text('Saving...');
	var vcount = $('#id_video_slider li').size();
	if(vcount > 0){
		var url = $('#youtube_user_video_add').val();
		var dataString='video_ids='+video_ids+'&vimeo_video_ids='+vimeo_video_ids;
		for(i=0;i<video_ids.length;i++){
			dataString+='&title_'+video_ids[i]+"="+$('#title_'+video_ids[i]).val();
			dataString+='&description_'+video_ids[i]+"="+$('#description_'+video_ids[i]).val();
			dataString+='&durations'+video_ids[i]+"="+$('#durations'+video_ids[i]).val();
		}
		for(i=0;i<vimeo_video_ids.length;i++){
			dataString+='&vimeo_title_'+vimeo_video_ids[i]+"="+$('#title_'+vimeo_video_ids[i]).val();
			dataString+='&vimeo_description_'+vimeo_video_ids[i]+"="+$('#description_'+vimeo_video_ids[i]).val();
			dataString+='&img_large'+vimeo_video_ids[i]+"="+$('#img_large_'+vimeo_video_ids[i]).val();
			dataString+='&durations'+vimeo_video_ids[i]+"="+$('#durations'+vimeo_video_ids[i]).val();
		}
	
		$.ajax({
			type: "POST",
			url: url,
			data:dataString,
			dataType:'html',
			success: function(response){
				video_ids=[];
				$('#share-videos').html(response);
				//select menu
				$('.bM-sLt').doThis(function(){
					this.bUiSlCt();
				});
				$('.fLxiMgH').setrSpVHeight('mDa-lT');
			},
			error:function(response){
				$('#share-videos').html(response);
			}
		});
	}
}

function clear_adv_srchfields(){
	$('select#search_type').val("").trigger("liszt:updated");
	$('#id_search_start_date').val("");
	//$('#id_search_end_date').val("");
	$('.search_adv2').val("");
	$('#search_category').val("").trigger("liszt:updated");
	$('#search_status').val("").trigger("liszt:updated");
	
	$('#bottom_search_button').attr('disabled','disabled');
}

function uniqId() {
  return Math.round(new Date().getTime() + (Math.random() * 100));
}