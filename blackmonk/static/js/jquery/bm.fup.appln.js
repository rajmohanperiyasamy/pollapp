function file_upload(url,limit) {
    'use strict';
    // Initialize the jQuery File Upload widget:
    $('#fileupload').fileupload({
 	   dropZone:$("#bm-dropzone"),
 	   sequentialUploads:true,
	   maxNumberOfFiles:limit,
	   autoUpload:true,
	   url:url,
	   acceptFileTypes:/(\.|\/)(gif|jpe?g|png)$/i,
 	   drop:function (e, data) {
 	   	  	$("#bm-dropzone_area").hide();
 	   }
 	  
    });
	$(document).bind('dragover', function (e) {
		$("#bm-dropzone_area").show();
    	e.preventDefault();
	});
	$(document).bind('drop', function (e) {
		$("#bm-dropzone_area").hide();
		e.preventDefault();
    	
	});
 // Load existing files:
    get_images(url)
    // Open download dialogs via iframes,
    // to prevent aborting current uploads:
    $('#fileupload .files a:not([target^=_blank])').live('click', function (e) {
        e.preventDefault();
        $('<iframe style="display:none;"></iframe>')
            .prop('src', this.href)
            .appendTo('body');
        setTimeout(function(){
        	inline_text()
        },1000);
    });
   //inline_text()
}
function get_images(url){
     var noCache = Date();
	 $.getJSON(url, { "noCache": noCache }, function (files) {
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
function inline_text(){
	try{
		$.colorbox.resize();
		//if($('.bm-uploader-file').length>=1){$('.upload-button').html(gettext('Upload More Photos'));}
		//else{$('.upload-button').html(gettext('Add Images'));}
	}catch(ex){}
}
function cropandsave(updateUrl){
	$.ajax({
		type: "POST",
		url: updateUrl,
		data: "cover_x1="+$('#cover_x1').val()+"&cover_y1="+$('#cover_y1').val()+"&cover_x2="+$('#cover_x2').val()+"&cover_y2="+$('#cover_y2').val()+"&cover_height="+$('#cover_height').val()+"&cover_width="+$('#cover_width').val(),
		dataType:'HTML',
		success: function(data){
			if(data=="Success"){
				$('#cover_x1').val('');
				$('#cover_y1').val('');
				$('#cover_x2').val('');
				$('#cover_y2').val('');
				$('#cover_height').val('');
				$('#cover_width').val('');
				$('.cropper_ajax_ctrl').hide();
			}
		}
	});
}
function cover_photo_upload(coverUploadUrl, aspectRatio) {
    // Initialize the jQuery File Upload widget:
    $('#fileuploadcover').fileupload({
 	   dropZone: $("#bm-dropzone"),
 	   sequentialUploads: true,
	   maxNumberOfFiles: 1,
	   autoUpload: true,
	   downloadTemplate: $('#cover-download-template'),
	   url: coverUploadUrl,
	   acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
	   complete: function () {
		    setTimeout(function(){
				$(".cropper").cropper({
				    aspectRatio: aspectRatio,
				    preview: ".cropper-preview",
				    done: function(data) {
				    	$('#cover_x1').val(data.x1);
				    	$('#cover_y1').val(data.y1);
				    	$('#cover_x2').val(data.x2);
				    	$('#cover_y2').val(data.y2);
				    	$('#cover_height').val(data.height);
				    	$('#cover_width').val(data.width);
				    }
				});
	        },1000);
	   },
 	   drop: function (e, data) {
 	   	  	$("#bm-dropzone_area").hide();
 	   }
    });
	$(document).bind('dragover', function (e) {
		$("#bm-dropzone_area").show();
    	e.preventDefault();
	});
	$(document).bind('drop', function (e) {
		$("#bm-dropzone_area").hide();
		e.preventDefault();
	});
	// Load existing files:
    get_cover_images(coverUploadUrl)
    setTimeout(function(){
    	$('.cropper_controls').hide();
	},300);
    $('#fileuploadcover .files a:not([target^=_blank])').live('click', function (e) {
        e.preventDefault();
        $('<iframe style="display:none;"></iframe>')
            .prop('src', this.href)
            .appendTo('body');
        setTimeout(function(){
        	inline_text()
        },1000);
    });
}
function get_cover_images(url){
     var noCache = Date();
	 $.getJSON(url, { "noCache": noCache }, function (files) {
	        var fu = $('#fileuploadcover').data('fileupload');
	        fu._adjustMaxNumberOfFiles(-files.length);
	        fu._renderDownload(files)
	            .appendTo($('#fileuploadcover .files'))
	            .fadeIn(function () {
	                // Fix for IE7 and lower:
	                $(this).show();
	        });
	 });
}