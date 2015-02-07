function file_upload_sweepstake_offer(url,limit,uploadTemplateId,downloadTemplateId) {
    'use strict';
    // Initialize the jQuery File Upload widget:
    $('#fileupload').fileupload({
 	   sequentialUploads:true,
	   maxNumberOfFiles:limit,
	   autoUpload:true,
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