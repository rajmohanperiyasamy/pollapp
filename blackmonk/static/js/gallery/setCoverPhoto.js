function set_cover_photo_lightbox(gid){
    $.colorbox({
        width: "550",
        initialWidth: "550",
        top:"60",
        title: gettext("Set Cover Image"),
        initialHeight: "200",
        href:'/staff/photos/ajax-set-cover-image/?gid='+gid+''
    });
}
function save_cover_photo(gid, pid){
    if(pid){
        var dataString="gid="+gid+"&pid="+pid;
        $.ajax({
            type: "POST",
            url: "/staff/photos/ajax-set-cover-image/",
            data: dataString,
            success: function(data){
                if(data){
                    $.colorbox.close();
                    show_msg(gettext('Cover image updated successfully.'),'alert-success');
                }else{
                    show_msg(gettext('Oops!!! Not able to process your request.'),'alert-error');
                }
            }
        }); 
    }else{
        alert('You should select an image before saving.')
    }
}