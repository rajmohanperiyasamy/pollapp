function file_upload_buz(url,limit,uploadTemplateId,downloadTemplateId) {
    'use strict';
    // Initialize the jQuery File Upload widget:
    $('#fileupload').fileupload({
 	   //dropZone:$("#bm-dropzone"),
 	   sequentialUploads:true,
	   maxNumberOfFiles:limit,
	   autoUpload:true,
	   uploadTemplate:$('#'+uploadTemplateId),
	   downloadTemplate:$('#'+downloadTemplateId),
	   url:url,
	   acceptFileTypes:/(\.|\/)(gif|jpe?g|png)$/i
    });
	
 // Load existing files:
   get_files(url)
    // Open download dialogs via iframes,
    // to prevent aborting current uploads:
    $('#fileupload .files a:not([target^=_blank])').live('click', function (e) {
        e.preventDefault();
        $('<iframe style="display:none;"></iframe>')
            .prop('src', this.href)
            .appendTo('body');
    });
}
function get_files(url){
	var noCache = Date();
	 $.getJSON(url,{ "noCache": noCache }, function (files) {
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
	   acceptFileTypes:/(\.|\/)(gif|jpe?g|png)$/i,
	   send: function (e, data) {data.formData = {pr_id: $("#product_id").val()};} 
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
	 $.getJSON(url,{ "noCache": noCache }, function (files) {
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
