function file_upload_buz(url,limit,uploadTemplateId,downloadTemplateId) {
    'use strict';
    // Initialize the jQuery File Upload widget:
    $('#fileuploaddoc').fileupload({
 	   //dropZone:$("#bm-dropzone"),
 	   sequentialUploads:true,
	   maxNumberOfFiles:limit,
	   autoUpload:true,
	   uploadTemplate:$('#'+uploadTemplateId),
	   downloadTemplate:$('#'+downloadTemplateId),
	   url:url,
	   acceptFileTypes:/(\.|\/)(jpe?g|png|x-png|pjpeg|docx?|pdf)$/i
    });
	
 // Load existing files:
   get_files(url)
    // Open download dialogs via iframes,
    // to prevent aborting current uploads:
    $('#fileuploaddoc .files a:not([target^=_blank])').live('click', function (e) {
        e.preventDefault();
        $('<iframe style="display:none;"></iframe>')
            .prop('src', this.href)
            .appendTo('body');
    });
}
function get_files(url){
	var noCache = Date();
	 $.getJSON(url, { "noCache": noCache }, function (files) {
	        var fu = $('#fileuploaddoc').data('fileupload');
	        fu._adjustMaxNumberOfFiles(-files.length);
	        fu._renderDownload(files)
	            .appendTo($('#fileuploaddoc .files'))
	            .fadeIn(function () {
	                // Fix for IE7 and lower:
	                $(this).show();
	            });
	    });
}
function file_upload_buz_product(url,limit,uploadTemplateId,downloadTemplateId) {
    'use strict';
    // Initialize the jQuery File Upload widget:
    $('#fileupload').fileupload({
 	   sequentialUploads:true,
	   maxNumberOfFiles:limit,
	   autoUpload:false,
	   previewRequired:true,
	   previewMaxWidth:200,
	   previewMaxHeight:200,
	   uploadTemplate:$('#'+uploadTemplateId),
	   downloadTemplate:$('#'+downloadTemplateId),
	   url:url,
	   acceptFileTypes:/(\.|\/)(jpe?g|pjpeg|gif|png|x-png)$/i
    });
    get_product_images(url)
    $('#fileupload .files a:not([target^=_blank])').live('click', function (e) {
        e.preventDefault();
        $('<iframe style="display:none;"></iframe>')
            .prop('src', this.href)
            .appendTo('body');
    });
}
function get_product_images(url){
	var noCache = Date();
	 $.getJSON(url,{ "noCache": noCache },  function (files) {
	        var fu = $('#fileupload').data('fileupload');
	        fu._adjustMaxNumberOfFiles(-files.length);
	        fu._renderDownload(files)
	            .appendTo($('#fileupload .files'))
	            .fadeIn(function () {
	                // Fix for IE7 and lower:
	                $(this).show();
	            });
	    });
}
$(document).ready(function(){
	$('#app_all').click(function(){
        $('.starttime.on').val($('#id_mon_start').val());
        $('.endtime.on').val($('#id_mon_end').val());
		
		if($('#id_closed_1').prop('checked')){
			$('.ws_closed').attr('checked','checked');
			$('.starttime').attr('disabled','disabled')
			$('.endtime').attr('disabled','disabled')
		}
		if($('#id_allday_1').prop('checked')){
			$('.ws_open').attr('checked','checked');
		}

		if(!$('#id_closed_1').prop('checked')){
			$('.ws_closed').removeAttr('checked');
			$('.starttime').removeAttr('disabled')
			$('.endtime').removeAttr('disabled')
			$('.starttime').addClass('on')
			$('.endtime').addClass('on')
			if($('#id_mon_start').val() == ''){
				$('.starttime').attr('placeholder','09:00 AM');
			}
			if($('#id_mon_end').val() == ''){
				$('.endtime').attr('placeholder','06:00 PM');
			}
		}
		if(!$('#id_allday_1').prop('checked')){
			$('.ws_open').removeAttr('checked');
		}
    })

    $('.ws_closed').click(function(){
        if($(this).is(':checked')){
            $(this).parent().parent().parent().find('input[type=text]').val('');
            $(this).parent().parent().parent().find('input[type=text]').attr('placeholder','');
            $(this).parent().parent().parent().find('input[type=text]').attr('disabled','disabled');
            $(this).parent().parent().parent().find('input[type=text]').removeClass('on');
			$(this).parent().parent().parent().find('.ws_open').removeAttr('checked');
        }
        else{
            $(this).parent().parent().parent().find('.starttime').attr('placeholder',gettext('09:00 AM'));
            $(this).parent().parent().parent().find('.endtime').attr('placeholder',gettext('06:00 PM'));
            $(this).parent().parent().parent().find('input[type=text]').removeAttr('disabled');
            $(this).parent().parent().parent().find('input[type=text]').addClass('on');
        }
    });
	$('.ws_open').click(function(){
		if($(this).is(':checked')){
			$(this).parent().parent().parent().find('.starttime').val('12:00 AM');
			$(this).parent().parent().parent().find('.endtime').val('12:00 AM');
			$(this).parent().parent().parent().find('input[type=text]').removeAttr('disabled');
			$(this).parent().parent().parent().find('input[type=text]').addClass('on');
			$(this).parent().parent().parent().find('.ws_closed').removeAttr('checked');
		}
	});
});