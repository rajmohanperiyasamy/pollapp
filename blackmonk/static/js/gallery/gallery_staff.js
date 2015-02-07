function search_filter(sort){
    $('.strong_disp').hide();
    $('.a_link').show();
    $('#a_'+sort).hide();
    $('#s_'+sort).show();
    SORT=sort;
    PAGE=1;
    $("#images").html('');
    getPhotos();
}
function load_more(){
    PAGE=PAGE+1;
    var text = document.getElementById("id_title").value;
    strRE = new RegExp( );
    strRE.compile( '^[\s ]*$', 'gi' );
    if(strRE.test(text)==true){alert("Please enter photo title");}
    else{
    $('#default_text').hide();
    $("#ajax_content_loading_flicker_search").show();
    var url = "https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key="+$('#fapikey').val();
    url += "&safe_search=1";
    url += "&per_page=30"
    url += "&page="+PAGE;
    url += "&sort="+SORT;
    url += "&text="+text;
    $.getJSON(url + "&format=json&jsoncallback=?", function(data){
    $("#ajax_content_loading_flicker_search_page").hide();
        if(data.photos.photo==null || data.photos.photo=='')
        { 
        $("#mform").hide();
        alert("No search result found try another keyword.");
        }
        else{ 
            $.each(data.photos.photo, function(i,item){
                var src = "http://farm"+ item.farm +".static.flickr.com/"+ item.server +"/"+ item.id +"_"+ item.secret;
                var l_img = src + ".jpg";
                var s_img = src + "_s.jpg";
                src += "_t.jpg";
                var html ="<li onclick='select_photo(\""+item.id+"\")' class='photos-selectable inline-block' id='image_"+item.id+"'>";
                html +="<div class='photos-selectable-area inline-block'><input type='hidden' id='src_s_"+item.id+"' value='"+s_img+"'><input type='hidden' id='src_l_"+item.id+"' value='"+l_img+"'>";
                html += "<div class='photos-selectable-preview'><img src='"+src+"'><a href='#' title='Large preview' class='icon-view'></a></div>";
                html += "</div>";                              
                html += "<p class='photos-selectable-meta'>"+item.title+"</p>";    
                html += "</li>";
                
                $("#images").append(html);
            });
        }
    });
    }
}
var flag=false;
function getPhotos(){
    flag=true;
    $('#ajax_content_loading_flicker_search_page').hide();
    var text = document.getElementById("id_title").value;
    strRE = new RegExp( );
    strRE.compile( '^[\s ]*$', 'gi' );
    if(strRE.test(text)==true){alert("Please enter photo title?");}
    else{
    $("#images").html('');
    $('#default_text').show();
    $('#default_text').find('.tip').hide();
    $("#ajax_content_loading_flicker_search").show();
    var url = "https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key="+$('#fapikey').val();
    url += "&safe_search=1";
    url += "&per_page=30"
    url += "&page="+PAGE;
    url += "&sort="+SORT;
    url += "&text="+text;
    $.getJSON(url + "&format=json&jsoncallback=?", function(data){
        $("#ajax_content_loading_flicker_search").hide();
        if(data.photos.photo==null || data.photos.photo=='')
        { 
        $("#mform").hide();
        alert("No search result found try another keyword.");
        }
        else{ 
            $.each(data.photos.photo, function(i,item){
                var src = "http://farm"+ item.farm +".static.flickr.com/"+ item.server +"/"+ item.id +"_"+ item.secret;
                var l_img = src + ".jpg";
                var s_img = src + "_s.jpg";
                src += "_t.jpg";
                var html ="<li onclick='select_photo(\""+item.id+"\")' class='photos-selectable inline-block' id='image_"+item.id+"'>";
                html +="<div class='photos-selectable-area inline-block'><input type='hidden' id='src_s_"+item.id+"' value='"+s_img+"'><input type='hidden' id='src_l_"+item.id+"' value='"+l_img+"'>";
                html += "<div class='photos-selectable-preview'><img src='"+src+"'><a href='#' onclick='view_large_image(event,\""+l_img+"\")' title='Large preview' class='icon-view preview-item''></a></div>";
                html += "</div>";                              
                html += "<p class='photos-selectable-meta'>"+item.title+"</p>";    
                html += "</li>";
                $("#images").append(html);
            });
        }
    });
    }
}
function view_large_image(ev,src){
    ev.stopPropagation();
    $('#large_image').attr('src',src);
    $(".item-preview-wrapper").show();
}
var load_url="/static/ui/images/global/loading-s.gif";
function select_photo(id){
    if($('#image_'+id).hasClass('checked')){
        deselect_photo(id);
    }else{
        $('#selected_default_text').hide();
        $('#image_'+id).addClass('checked');
        var src=$('#src_s_'+id).val();
        var html ="<li data-flickrid='"+id+"' class='photos-selectable selected-flickr-images inline-block' id='simage_"+id+"' style='min-width:75px;min-height:75px;background:url("+load_url+") no-repeat center transparent;'>";
        html+="<div class='photos-selectable-area inline-block'>";
        html+="<div class='photos-selectable-preview'><img src='"+src+"'><a class='icon-remove' title='Remove' href='javascript:deselect_photo(\""+id+"\")'></a>";
        html+="<a href='#' onclick='view_large_image(event,\""+$('#src_l_'+id).val()+"\")' title='Large preview' class='icon-view preview-item''></a></div></div></li>";
        $('#selected_images').prepend(html);
        $('#photo_count').html($('.selected-flickr-images').length);
    }
    
}
function deselect_photo(id){
    $('#simage_'+id).remove();
    $('#image_'+id).removeClass('checked');
    
    if($('.selected-flickr-images').length==0){
        $('#selected_default_text').show();
    }
    $('#photo_count').text($('.selected-flickr-images').length);
}
function save_description(){
    var dataString='';
    $('input[name=ids]').each(function(){
        id=$(this).val();
        //dataString+='&title_'+id+'='+encodeURIComponent($('#title_'+id).val());
        dataString+='&description_'+id+'='+encodeURIComponent($('#description_'+id).val());
    });
    $('#ajax_content_gallery').hide();
    $('#ajax_content_loading_gallery').show();
    $.ajax({
        type: "POST",
        url: $('#descmform').attr('action'),
        data: dataString,
        dataType:'JSON',
        success: function(data){
            window.location.reload(true);
            $.colorbox.close();
            show_msg(data.msg,data.mtype);
        }
    });
}
function save_photo(){
    var flickr_ids = [];
    $( ".selected-flickr-images" ).each(function() {
        flickr_ids.push($( this ).attr('data-flickrid'));
    });
    var dataString='&flickr_ids='+flickr_ids.valueOf();
    $('#ajax_content_gallery_photo').hide();
    $('#ajax_content_loading_gallery_photo').show();
    $.ajax({
    type: "POST",
    url: $('#photomform').attr('action'),
    data: dataString,
    success: function(data){
                try{
                    $('#ajax_content_loading_gallery').hide();
                    $('#ajax_content_gallery').show();
                }
                catch(e){}
                $('#ajax_content_loading_gallery_photo').hide();
                $('#ajax_content_gallery_photo').empty().html(data);//lightbox_html
                $('#ajax_content_gallery_photo').show();
                $.colorbox.resize({width: "880", height:"auto", top:"5%"});
                $.colorbox.resize();
                $('#bmTitle').html(gettext('Update Caption'));
        }
    });
}
function save_updated_album(){
    var flag=$('#galleryeditform').validate().form();
    if(flag){
        var dataString='title='+$('#id_title').val();
        dataString+='&summary='+$('#id_summary').val();
        dataString+='&category='+$('#id_category').val();
        dataString+='&tags='+$('input[name=tags]').val();   
        $('#ajax_content_gallery_update').hide();
        $('#ajax_content_loading_update_gallery').show();
        $.ajax({
        type: "POST",
        url: $('#galleryeditform').attr('action'),
        data: dataString,
        dataType:'JSON',
        success: function(data){
            if(data.status){
                window.location.reload(true);
            }else{
                $('#ajax_content_loading_update_gallery').hide();
                $('#ajax_content_gallery_update').empty().html(data.html);
                $('#ajax_content_gallery_update').show();
                $.colorbox.resize();
            }
            }
        });
    }
}
function save_album(){
    var flag = $('#mform').validate().form()
    if(flag){
        var dataString='title='+encodeURIComponent($('#id_title').val());
        dataString+='&summary='+encodeURIComponent($('#id_summary').val());
        dataString+='&category='+$('#id_category').val();
        dataString+='&tags='+encodeURIComponent($('input[name=tags]').val());       
        $('#ajax_content_gallery').hide();
        $('#ajax_content_loading_gallery').show();
        $.ajax({
        type: "POST",
        url: $('#staff_add_gallery').val(),
        data: dataString,
        dataType:'JSON',
        success: function(data){
                    $('#ajax_content_loading_gallery').hide();
                    $('#ajax_content_gallery').empty().html(data.html);
                    $('#ajax_content_gallery').show();
                    $.colorbox.resize();
            },
        error:function(data){
                    $('#ajax_content_loading_gallery').hide();
                    $('#ajax_content_gallery').empty().html(data.responseText);//lightbox_html
                    $('#ajax_content_gallery').show();
                    $.colorbox.resize({width: "880", height:"630", top:"5%"});
                    $('#bmTitle').html(gettext('Upload Photos'));
            }
        });
    }
}
function save_detail(id){
    var flag = $('#mform').validate().form()
    if(flag==true){
        //var dataString='&title='+encodeURIComponent($('#id_title').val());
        //dataString+='&summary='+encodeURIComponent($('#id_summary').val());
        var dataString='summary='+encodeURIComponent($('#id_summary').val());
        $('#ajax_content').hide();
        $('#ajax_content_loading').show();
        $.ajax({
        type: "POST",
        url: $("#mform").attr("action"),
        data: dataString,
        dataType:'JSON',
        success: function(responseData){
                $('#ajax_content_loading').html(responseData.msg);
                $('#li_'+id).remove();
                $('#ajax_content_loading').hide();
                $('#photo-grid').prepend(responseData.html);
                $(".bm-add-photo-details").colorbox({width:"700",initialWidth: "700", top:"5%", initialHeight: "200",title:function(){return getLBTitle($(this));}});
                show_msg(responseData.msg,responseData.mtype);
                $.colorbox.close();
            }
        });
    }
}
function txtarealimit(txtobj,len){
    var txtvalue = txtobj.value;
    var the_len = txtvalue.length;
    if (the_len > len){
        txtobj.value = txtvalue.substring(0,len);
    }
    txtobj.scrollTop=txtobj.scrollHeight;
}