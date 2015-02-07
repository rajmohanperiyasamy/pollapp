from django import template

register = template.Library()

@register.simple_tag
def cover_upload_js():
    return """
    <script id="cover-upload-template" type="text/x-jquery-tmpl">
        <li class="bm-uploader-file pending template-upload{{if error}} ui-state-error{{/if}}">
            <div class="preview">
                <div class="preview-inner">
                      <!-- div class="icon-16 icon-spinner"></div -->
                      {{if error}}
                          <div class="error" style="color:#F00" colspan="2">Error:
                              {{if error === 'maxFileSize'}}File is too big
                              {{else error === 'minFileSize'}}File is too small
                              {{else error === 'acceptFileTypes'}}Filetype not allowed
                              {{else error === 'maxNumberOfFiles'}}Max number of files exceeded
                              {{else}}${error}
                              {{/if}}
                          </div>
                      {{else}}
                          <div class="progress-wrapper">
                              <div class="progress">
                                  <div></div>
                              </div>
                          </div>
                      {{/if}}
                </div>
            </div>
            <p class="controls"><small class="cancel"><a>Cancel</a></small></p>
        </li>
    </script>
    <script id="cover-download-template" type="text/x-jquery-tmpl">
        <li class="bm-uploader-file finished template-download{{if error}} ui-state-error{{/if}}" style="max-width: 100%;">
            {{if error}}
                <div class="preview">
                      <div class="preview-inner">
                           <div class="error" colspan="2" style="color:#F00" >${error}</div>
                      </div>
                </div>
                <p class="controls" onclick="$(this).parent('li').remove()"><small class="cancel"><a>Cancel</a></small></p>
            {{else}}
                <p style="color: #B8B8B8;" class="cropper_controls cropper_ajax_ctrl">Crop your image:</p>
                <input type="hidden" name="cover_id" value="${cover_id}">
                {{if cover_url}}
                    <class="icon-16 icon-spinner"></div>
                    <div class="cropper_ajax_ctrl"><img id="cover_img" class="cropper" src="${cover_url}"></div>
                {{/if}}
                <p class="controls" style="bottom: 24px;visibility: visible;">
                    <small class="update cropper_controls cropper_ajax_ctrl"><a href="javascript: void(0);" onclick="cropandsave('${update_url}');" style="text-indent: unset; color: white; font-size: 14px; border-radius: 4px; width: 36px; position: relative; background: none no-repeat scroll 50% -33px rgba(0, 0, 0, 0.65);"><span style="vertical-align: top; position: absolute; left: 7px; bottom: 0px;">Save</span></a></small>
                    <small class="modify delete" data-type="DELETE" data-url="${delete_url}">
                        <a data-type="DELETE" data-url="${delete_url}">Delete</a>
                    </small>
                </p>
                <span class="icon-tick"></span>
                <p style="color: #B8B8B8; margin: 5px 0 10px;" class="cropper_controls cropper_ajax_ctrl">Preview:</p>
                <div class="cropper-preview cropper_controls" style="height: 160px; width: 210px;"></div>
            {{/if}}
        </li>
    </script>
    """

@register.simple_tag
def biz_usrcp_prevw_img_upload_js():
    return """
    <script id="template-upload-bizimage" type="text/x-jquery-tmpl">
        <li class="bm-uploader-file pending template-upload{{if error}} ui-state-error{{/if}}">
            <div class="preview">
                <div class="preview-inner">
                      ${name}
                      <!-- div class="icon-16 icon-spinner"></div -->
                      {{if error}}
                          <div class="error" style="color:#F00" colspan="2">Error:
                              {{if error === 'maxFileSize'}}File is too big
                              {{else error === 'minFileSize'}}File is too small
                              {{else error === 'acceptFileTypes'}}Filetype not allowed
                              {{else error === 'maxNumberOfFiles'}}Max number of files exceeded
                              {{else}}${error}
                              {{/if}}
                          </div>
                      {{else}}
                          <div class="progress-wrapper">
                              <div class="progress">
                                  <div></div>
                              </div>
                          </div>
                      {{/if}}
                </div>
            </div>
            <p class="controls"><small class="cancel"><a>Cancel</a></small></p>
        </li>
    </script>
    <script id="template-download-bizimage" type="text/x-jquery-tmpl">
        <li data-src="/site_media/photos/gallery/bd3ffa8c-0634-43b5-8488-9a286f17de04.jpeg" class="bm-uploader-file finished template-download" style="margin: 12px 0px 0px 0px;">
            <a href="#" class="bUi-tMb-wPr tMb-100 fLxiMgH lRg-bRdR swipebox">
                <span class="bUi-tMb">
                    <span class="bUi-tMb-pRpL">
                        <span class="bUi-tMb-cLp">
                            <span class="bUi-tMb-cLp-iN">
                                <img alt="" src="${thumbnail_url}" class="mDa-oT" style="height: 191px;">
                                <span class="vRtL-aLn">
                                </span>
                            </span>
                        </span>
                    </span>
                </span>
            </a>
            <p class="controls">
               <small class="modify delete" data-type="${delete_type}" data-url="${delete_url}"> <a data-type="${delete_type}" data-url="${delete_url}">Delete</a></small>
               {{if update_caption_url}}
                   <small class="update"> <a href="javascript:void(0);" title="Update Caption" onclick="show_update_caption_lb('${update_caption_url}');" class="bm-add-gadget light_box" >Update</a></small>
               {{/if}} 
            </p>
        </li>
    </script>
    
    <script id="template-cover-download-bizimage" type="text/x-jquery-tmpl">
        <span class="bUi-tMb-wPr fLxiMgW">
            <span class="bUi-tMb">
                <span class="bUi-tMb-pRpL">
                    <span class="bUi-tMb-cLp">
                        <span class="bUi-tMb-cLp-iN" itemscope itemtype="http://schema.org/ImageObject">
                                <img class="mDa-oT" src="${thumbnail_url}" style="width: 1205px;" itemprop="image">
                            <span class="vRtL-aLn">
                            </span>
                        </span>
                    </span>
                </span>
            </span>
            <span style="display:none;" id="control_buttons">
                <p class="controls">
                   <small class="modify delete" data-type="${delete_type}" data-url="${delete_url}"> <a data-type="${delete_type}" data-url="${delete_url}">Delete</a></small>
                   {{if update_caption_url}}
                       <small class="update"> <a href="javascript:void(0);" title="Update Caption" onclick="show_update_caption_lb('${update_caption_url}');" class="bm-add-gadget light_box" >Update</a></small>
                   {{/if}} 
                </p>
            </span>
        </span>
    </script>
    """

@register.simple_tag
def gal_usrcp_img_upload_js():
    return """
    <script id="template-upload-galimage" type="text/x-jquery-tmpl">
        <li class="bm-uploader-file pending template-upload{{if error}} ui-state-error{{/if}}">
            <div class="preview">
                <div class="preview-inner">
                      ${name}
                      <!-- div class="icon-16 icon-spinner"></div -->
                      {{if error}}
                          <div class="error" style="color:#F00" colspan="2">Error:
                              {{if error === 'maxFileSize'}}File is too big
                              {{else error === 'minFileSize'}}File is too small
                              {{else error === 'acceptFileTypes'}}Filetype not allowed
                              {{else error === 'maxNumberOfFiles'}}Max number of files exceeded
                              {{else}}${error}
                              {{/if}}
                          </div>
                      {{else}}
                          <div class="progress-wrapper">
                              <div class="progress">
                                  <div></div>
                              </div>
                          </div>
                      {{/if}}
                </div>
            </div>
            <p class="controls"><small class="cancel"><a>Cancel</a></small></p>
        </li>
    </script>
    <script id="template-download-galimage" type="text/x-jquery-tmpl">
        <li data-src="/site_media/photos/gallery/bd3ffa8c-0634-43b5-8488-9a286f17de04.jpeg" class="bm-uploader-file finished template-download" style="margin: 12px 0px 0px 0px;">
            <a href="#" class="bUi-tMb-wPr tMb-100 fLxiMgH lRg-bRdR swipebox">
                <span class="bUi-tMb">
                    <span class="bUi-tMb-pRpL">
                        <span class="bUi-tMb-cLp">
                            <span class="bUi-tMb-cLp-iN">
                                <img alt="" src="${thumbnail_url}" class="mDa-oT" style="height: 191px;">
                                <span class="vRtL-aLn">
                                </span>
                            </span>
                        </span>
                    </span>
                </span>
            </a>
            <p class="controls">
               <small class="modify delete" data-type="${delete_type}" data-url="${delete_url}"> <a data-type="${delete_type}" data-url="${delete_url}">Delete</a></small>
               {{if update_caption_url}}
                   <small class="update"> <a href="javascript:void(0);" title="Update Caption" onclick="show_update_caption_lb('${update_caption_url}');" class="bm-add-gadget light_box" >Update</a></small>
               {{/if}} 
            </p>
        </li>
    </script>"""
        
@register.simple_tag
def upload_js():
    return """
    <script id="template-upload" type="text/x-jquery-tmpl">
        <li class="bm-uploader-file pending template-upload{{if error}} ui-state-error{{/if}}">
            <div class="preview">
                <div class="preview-inner">
                      ${name}
                      <!-- div class="icon-16 icon-spinner"></div -->
                      {{if error}}
                          <div class="error" style="color:#F00" colspan="2">Error:
                              {{if error === 'maxFileSize'}}File is too big
                              {{else error === 'minFileSize'}}File is too small
                              {{else error === 'acceptFileTypes'}}Filetype not allowed
                              {{else error === 'maxNumberOfFiles'}}Max number of files exceeded
                              {{else}}${error}
                              {{/if}}
                          </div>
                      {{else}}
                          <div class="progress-wrapper">
                              <div class="progress">
                                  <div></div>
                              </div>
                          </div>
                      {{/if}}
                </div>
            </div>
            <p class="controls"><small class="cancel"><a>Cancel</a></small></p>
        </li>
    </script>
    <script id="template-download" type="text/x-jquery-tmpl">
        <li class="bm-uploader-file finished template-download{{if error}} ui-state-error{{/if}}">
            {{if error}}
                <div class="preview">
                      <div class="preview-inner">
                           ${name}
                           <div class="error" colspan="2" style="color:#F00" >${error}</div>
                      </div>
                </div>
                <p class="controls" onclick="$(this).parent('li').remove()"><small class="cancel"><a>Cancel</a></small></p>
            {{else}}
            <div class="preview">
                <div class="preview-inner">
                    <input type="hidden" name="gal_id" id="gal_id" value="${gal_id}">
                    <input type="hidden" name="photo_id" value="${photo_id}">
                    <input type="hidden" name="new_pic" id="pic${id}" value="${id}" class="new_pic_uploaded">
                    {{if thumbnail_url}}
                        <!-- div class="icon-16 icon-spinner"></div -->
                        <a href="#"><img src="${thumbnail_url}" style="height:90px;"></a>
                    {{/if}}
                      <p class="controls">
                       <small class="modify delete" data-type="${delete_type}" data-url="${delete_url}"> <a data-type="${delete_type}" data-url="${delete_url}">Delete</a></small>
                       {{if update_caption_url}}
                       <small class="update"> <a href="javascript:void(0);" title="Update Caption" onclick="show_update_caption_lb('${update_caption_url}');" class="bm-add-gadget light_box" >Update</a></small>
                       {{/if}} 
                    </p>
                     <span class="icon-tick"></span>
                </div>
            </div>            
            {{/if}}
            <!-- div class="delete">
                <button data-type="${delete_type}" data-url="${delete_url}">Delete</button>
            </div -->
        </li>
    </script>
    <script id="template-upload-fav" type="text/x-jquery-tmpl">
        <li class="bm-uploader-file pending template-upload{{if error}} ui-state-error{{/if}}">
            <div class="preview">
                <div class="preview-inner">
                      ${name}
                      <!-- div class="icon-16 icon-spinner"></div -->
                      {{if error}}
                          <div class="error" style="color:#F00" colspan="2">Error:
                              {{if error === 'maxFileSize'}}File is too big
                              {{else error === 'minFileSize'}}File is too small
                              {{else error === 'acceptFileTypes'}}Filetype not allowed
                              {{else error === 'maxNumberOfFiles'}}Max number of files exceeded
                              {{else}}${error}
                              {{/if}}
                          </div>
                      {{else}}
                          <div class="progress-wrapper">
                              <div class="progress">
                                  <div></div>
                              </div>
                          </div>
                      {{/if}}
                </div>
            </div>
            <p class="controls"><small class="cancel"><a>Cancel</a></small></p>
        </li>
    </script>
    <script id="template-download-fav" type="text/x-jquery-tmpl">
        <li class="bm-uploader-file finished template-download{{if error}} ui-state-error{{/if}}">
            {{if error}}
                <div class="preview">
                      <div class="preview-inner">
                           ${name}
                           <div class="error" colspan="2" style="color:#F00" >${error}</div>
                      </div>
                </div>
                <p class="controls" onclick="$(this).parent('li').remove()"><small class="cancel"><a>Cancel</a></small></p>
            {{else}}
            <div class="preview">
                <div class="preview-inner">
                    <input type="hidden" name="new_pic" id="pic${id}" value="${id}" class="new_pic_uploaded">
                    {{if thumbnail_url}}
                        <!-- div class="icon-16 icon-spinner"></div -->
                        <a href="#" onclick="show_image('${url}')">
                            <span class="item-thumb thumb-140">
                                <span class="thumb-in">
                                    <span class="thumb">
                                        <img class="inline-block" src="${thumbnail_url}">
                                        <span class="inline-block h100"></span>
                                    </span>
                                </span>
                            </span>
                        </a>
                    {{/if}}
                      <p class="controls">
                       <small class="modify delete" data-type="${delete_type}" data-url="${delete_url}"> <a data-type="${delete_type}" data-url="${delete_url}">Delete</a></small>
                       {{if update_caption_url}}
                       <small class="update"> <a href="javascript:void(0);" title="Update Caption" onclick="show_update_caption_lb('${update_caption_url}');" class="bm-add-gadget light_box" >Update</a></small>
                       {{/if}} 
                    </p>
                </div>
            </div>            
            {{/if}}
            <!-- div class="delete">
                <button data-type="${delete_type}" data-url="${delete_url}">Delete</button>
            </div -->
        </li>
    </script>
    <script id="template-upload-sitelogo" type="text/x-jquery-tmpl">
        <li class="bm-uploader-file pending template-upload{{if error}} ui-state-error{{/if}}">
            <div class="preview">
                <div class="preview-inner">
                      <!-- div class="icon-16 icon-spinner"></div -->
                      {{if error}}
                          <div class="error" style="color:#F00" colspan="2">Error:
                              {{if error === 'maxFileSize'}}File is too big
                              {{else error === 'minFileSize'}}File is too small
                              {{else error === 'acceptFileTypes'}}Filetype not allowed
                              {{else error === 'maxNumberOfFiles'}}Max number of files exceeded
                              {{else}}${error}
                              {{/if}}
                          </div>
                      {{else}}
                          <div class="progress-wrapper">
                              <div class="progress">
                                  <div></div>
                              </div>
                          </div>
                      {{/if}}
                </div>
            </div>
            <p class="controls"><small class="cancel"><a>Cancel</a></small></p>
        </li>
    </script>
    <script id="template-download-sitelogo" type="text/x-jquery-tmpl">
        <li class="bm-uploader-file finished template-download{{if error}} ui-state-error{{/if}}">
            {{if error}}
                <div class="preview">
                      <div class="preview-inner">
                           <div class="error" colspan="2" style="color:#F00" >${error}</div>
                      </div>
                </div>
                <p class="controls" onclick="$(this).parent('li').remove()"><small class="cancel"><a>Cancel</a></small></p>
            {{else}}
            <div class="preview">
                <div class="preview-inner">
                    <input type="hidden" name="new_pic" id="pic${id}" value="${id}" class="new_pic_uploaded">
                    {{if thumbnail_url}}
                        <!-- div class="icon-16 icon-spinner"></div -->
                        <a href="#" onclick="show_image('${url}')">
                            <span class="item-thumb thumb-140">
                                <span class="thumb-in">
                                    <span class="thumb">
                                        <img class="inline-block" src="${thumbnail_url}">
                                        <span class="inline-block h100"></span>
                                    </span>
                                </span>
                            </span>
                        </a>
                    {{/if}}
                      <p class="controls">
                       <small class="modify delete" data-type="${delete_type}" data-url="${delete_url}"> <a data-type="${delete_type}" data-url="${delete_url}">Delete</a></small>
                       {{if update_caption_url}}
                       <small class="update"> <a href="javascript:void(0);" title="Update Caption" onclick="show_update_caption_lb('${update_caption_url}');" class="bm-add-gadget light_box" >Update</a></small>
                       {{/if}} 
                    </p>
                </div>
            </div>            
            {{/if}}
            <!-- div class="delete">
                <button data-type="${delete_type}" data-url="${delete_url}">Delete</button>
            </div -->
        </li>
    </script>
    <script id="template-upload-1" type="text/x-jquery-tmpl">
        <li class="bm-uploader-file pending template-upload{{if error}} ui-state-error{{/if}}">
            <div class="preview">
                <div class="preview-inner" style="height:40px;width:500px;">
                      ${name}
                      <!-- div class="icon-16 icon-spinner"></div -->
                      {{if error}}
                          <div class="error" style="color:#F00" colspan="2">Error:
                              {{if error === 'maxFileSize'}}File is too big
                              {{else error === 'minFileSize'}}File is too small
                              {{else error === 'acceptFileTypes'}}Filetype not allowed
                              {{else error === 'maxNumberOfFiles'}}Max number of files exceeded
                              {{else}}${error}
                              {{/if}}
                          </div>
                      {{else}}
                          <div class="progress-wrapper">
                              <div class="progress">
                                  <div></div>
                              </div>
                          </div>
                      {{/if}}
                </div>
            </div>
            <p class="controls"><small class="cancel"><a>Cancel</a></small></p>
        </li>
    </script>
    <script id="template-download-1" type="text/x-jquery-tmpl">
        <li class="bm-uploader-file finished template-download{{if error}} ui-state-error{{/if}}">
            {{if error}}
                <div class="preview">
                    <div class="preview-inner" style="height:40px;width:500px;color:#FF0000;background:none;">
                        <span style="display: block; float: left; padding-right: 10px;">${error}</span>
                        <span onclick="$(this).parent('div').remove()" style="display: block; float: right; width: 16px; height: 16px; opacity: 0.35; background: url(/static/ui/images/icons/b/51.png) no-repeat scroll 0 0 transparent;"></span>
                    </div>
                </div>
            {{else}}
            <div class="preview">
                    <div class="preview-inner" style="height:40px;width:500px;color:#000;background:none;">
                        <input type="hidden" name="new_files" id="files${id}" value="${id}" class="new_files_uploaded">
                        <span style="display: block; float: left; padding-right: 10px;">${title}</span>
                        <p class="controls" style="margin:0px;visibility:visible;">
                           <small class="modify delete" data-type="${delete_type}" data-url="${delete_url}"> <a data-type="${delete_type}" data-url="${delete_url}">Delete</a></small>
                           {{if update_caption_url}}
                           <small class="update"> <a href="javascript:void(0);" title="Update Caption" onclick="show_update_caption_lb('${update_caption_url}');" class="bm-add-gadget light_box" >Update</a></small>
                           {{/if}} 
                        </p>
                    </div>
                </div>          
            {{/if}}
            <!-- div class="delete">
                <button data-type="${delete_type}" data-url="${delete_url}">Delete</button>
            </div -->
        </li>
    </script>
     <script id="template-upload-p" type="text/x-jquery-tmpl">
        <li class="bm-uploader-file pending template-upload{{if error}} ui-state-error{{/if}}">
             {{if error}}
                <div class="preview">
                    <div class="preview-inner" style="height:200px;width:200px;color:#000;">
                    ${name}
                      <!-- div class="icon-16 icon-spinner"></div -->
                      <div class="error" style="color:#F00" colspan="2">Error:
                          {{if error === 'maxFileSize'}}File is too big
                          {{else error === 'minFileSize'}}File is too small
                          {{else error === 'acceptFileTypes'}}Filetype not allowed
                          {{else error === 'maxNumberOfFiles'}}Max number of files exceeded
                          {{else}}${error}
                          {{/if}}
                      </div>
                    </div>
                </div>
              {{else}}
                  <span class="img_name" style="display:none;">${name}</span>
                  <div class="preview"></div>
              {{/if}}
               <div class="start">&nbsp;</div>
            <p class="controls"><small class="cancel"><a>Cancel</a></small></p>
        </li>
    </script>
    <script id="template-download-p" type="text/x-jquery-tmpl">
         <li class="bm-uploader-file finished template-download{{if error}} ui-state-error{{/if}}">
            {{if error}}
                <div class="preview">
                      <div class="preview-inner">
                           ${name}
                           <div class="error" colspan="2" style="color:#F00" >${error}</div>
                      </div>
                </div>
                <p class="controls" onclick="$(this).parent('li').remove()"><small class="cancel"><a>Cancel</a></small></p>
            {{else}}
            <div class="preview">
                <div>
                    <input type="hidden" name="new_pic" id="pic${id}" value="${id}" class="new_pic_uploaded">
                    {{if thumbnail_url}}
                        <!-- div class="icon-16 icon-spinner"></div -->
                        <a href="#" onclick="show_image('${url}')"><img src="${thumbnail_url}" style="max-height:200px;max-width:200px;"></a>
                    {{/if}}
                      <p class="controls">
                       <small class="modify delete" data-type="${delete_type}" data-url="${delete_url}"> <a data-type="${delete_type}" data-url="${delete_url}">Delete</a></small>
                       {{if update_caption_url}}
                       <small class="update"> <a href="javascript:void(0);" title="Update Caption" onclick="show_update_caption_lb('${update_caption_url}');" class="bm-add-gadget light_box" >Update</a></small>
                       {{/if}} 
                    </p>
                </div>
            </div>            
            {{/if}}
            <!-- div class="delete">
                <button data-type="${delete_type}" data-url="${delete_url}">Delete</button>
            </div -->
        </li>
    </script>
      <script id="template-upload-profile" type="text/x-jquery-tmpl">
         <li class="bm-uploader-file pending template-upload{{if error}} ui-state-error{{/if}}">
             {{if error}}
                <div class="preview">
                    <div class="preview-inner" style="height:75px;width:75px;color:#000;">
                    ${name}
                      <!-- div class="icon-16 icon-spinner"></div -->
                      <div class="error" style="color:#F00" colspan="2">Error:
                          {{if error === 'maxFileSize'}}File is too big
                          {{else error === 'minFileSize'}}File is too small
                          {{else error === 'acceptFileTypes'}}Filetype not allowed
                          {{else error === 'maxNumberOfFiles'}}Max number of files exceeded
                          {{else}}${error}
                          {{/if}}
                      </div>
                    </div>
                </div>
              {{else}}
                  <div class="preview"></div>
              {{/if}}
               <div class="start">&nbsp;</div>
            <p class="controls"><small class="cancel"><a>Cancel</a></small></p>
        </li>
    </script>
    <script id="template-download-profile" type="text/x-jquery-tmpl">
         <li class="bm-uploader-file finished template-download{{if error}} ui-state-error{{/if}}">
            {{if error}}
                <div class="preview">
                      <div class="preview-inner">
                           ${name}
                           <div class="error" colspan="2" style="color:#F00" >${error}</div>
                      </div>
                </div>
                <p class="controls" onclick="$(this).parent('li').remove()"><small class="cancel"><a>Cancel</a></small></p>
            {{else}}
            <div class="preview">
            
                <div class="label">
                    <input type="hidden" name="new_pic" id="pic${id}" value="${id}" class="new_pic_uploaded">
                    <div id="profile-photo-wrap">
                        <!-- img width="32" height="32" src="/static/ui/images/global/loading.gif" id="profile-photo-status" -->
                        <img width="75" height="75" id="profile-photo" src="${thumbnail_url}">
                        <small class="delete" style="background:none !important;text-indent:0;color:blue;" data-type="${delete_type}" data-url="${delete_url}">
                            <a class="modify delete call-edit" style="background:none !important;text-indent:0;color:blue;width:auto;"  data-type="${delete_type}" data-url="${delete_url}">Clear photo</a>
                        </small>
                        {{if update_caption_url}}
                           <small class="update"> <a href="javascript:void(0);" title="Update Caption" onclick="show_update_caption_lb('${update_caption_url}');" class="bm-add-gadget light_box" >Update</a></small>
                        {{/if}} 
                   </div>                                                
               </div>
               
            </div>            
            {{/if}}
            <!-- div class="delete">
                <button data-type="${delete_type}" data-url="${delete_url}">Delete</button>
            </div -->
        </li>
    </script>
    <script id="template-upload-attraction" type="text/x-jquery-tmpl">
        <li class="bm-uploader-file pending template-upload{{if error}} ui-state-error{{/if}}">
            <div class="preview">
                <div class="preview-inner" style="width:220px;height:180px;">
                      ${name}
                      <!-- div class="icon-16 icon-spinner"></div -->
                      {{if error}}
                          <div class="error" style="color:#F00" colspan="2">Error:
                              {{if error === 'maxFileSize'}}File is too big
                              {{else error === 'minFileSize'}}File is too small
                              {{else error === 'acceptFileTypes'}}Filetype not allowed
                              {{else error === 'maxNumberOfFiles'}}Max number of files exceeded
                              {{else}}${error}
                              {{/if}}
                          </div>
                      {{else}}
                          <div class="progress-wrapper" >
                              <div class="progress">
                                  <div></div>
                              </div>
                          </div>
                      {{/if}}
                </div>
            </div>
            <p class="controls"><small class="cancel"><a>Cancel</a></small></p>
        </li>
    </script>
    <script id="template-download-attraction" type="text/x-jquery-tmpl">
        <li id="li_${id}" style="width:220px;" class="bm-uploader-file finished template-download{{if error}} ui-state-error{{/if}} table-list-row manage-items gallery_list_count">
            {{if error}}
                <div class="preview">
                      <div class="preview-inner" style="width:220px;height:180px;">
                           ${name}
                           <div class="error" colspan="2" style="color:#F00" >${error}</div>
                      </div>
                </div>
                <p class="controls" onclick="$(this).parent('li').remove()"><small class="cancel"><a>Cancel</a></small></p>
            {{else}}
             <div class="preview">
                 <div class="table-list-row-inner group">
                    <div class="thumb-wrap">
                        <span class="inline-block">
                            <img src="${thumbnail_url}" style="max-width:180px;height:120px;">
                        </span>
                    </div>   
                    <div class="clear"></div>
                    <div class="item-detail">
                        <p class="ltxtAA txt11"><span>Updated on:  ${uploaded_on}</span><br><span>Updated by:  ${uploaded_by}</span></p>
                    </div>
                    <div class="action-buttons">
                        <div>
                            
                            <small class="modify delete" data-type="${delete_type}" data-url="${delete_url}"> 
                                <a data-type="${delete_type}" data-url="${delete_url}" style="background:none;" original-title="Delete"><span class="action-icon icon-delete"></span></a>
                            </small>
                            {{if update_caption_url}}
                               <small class="update"> <a href="javascript:void(0);" title="Update Caption" onclick="show_update_caption_lb('${update_caption_url}');" class="bm-add-gadget light_box" >Update</a></small>
                            {{/if}} 
                            {{if is_approved}}
                            <a style="float:left;" onclick="approve(${id})" id="a_${id}" href="javascript:void(0)" class="tttxt" title="Approve" original-title="Approve"><span class="action-icon icon-edit"></span></a>
                            {{/if}}
                        </div>  
                    </div>
                </div>
            </div>
            {{/if}}
            <!-- div class="delete">
                <button data-type="${delete_type}" data-url="${delete_url}">Delete</button>
            </div -->
        </li>
    </script>
    <script id="logo-download-template" type="text/x-jquery-tmpl">
        <li class="bm-uploader-file finished template-download{{if error}} ui-state-error{{/if}}" style="max-width: 100%;">
            {{if error}}
                <div class="preview">
                      <div class="preview-inner">
                           ${name}
                           <div class="error" colspan="2" style="color:#F00" >${error}</div>
                      </div>
                </div>
                <p class="controls" onclick="$(this).parent('li').remove()"><small class="cancel"><a>Cancel</a></small></p>
            {{else}}
                <p style="color: #B8B8B8;" class="cropper_controls">Crop your image:</p>
                <input type="hidden" name="gal_id" id="gal_id" value="${gal_id}">
                <input type="hidden" name="photo_id" value="${photo_id}">
                <input type="hidden" name="new_pic" id="pic${id}" value="${id}" class="new_pic_uploaded">
                {{if thumbnail_url}}
                    <!-- div class="icon-16 icon-spinner"></div -->
                    <div><img id="logo_img" class="cropper" src="${thumbnail_url}"></div>
                {{/if}}
                <p class="controls" style="bottom: 24px;">
                    <small class="modify delete" data-type="${delete_type}" data-url="${delete_url}"> <a data-type="${delete_type}" data-url="${delete_url}">Delete</a></small>
                    {{if update_caption_url}}
                       <small class="update"> <a href="javascript:void(0);" title="Update Caption" onclick="show_update_caption_lb('${update_caption_url}');" class="bm-add-gadget light_box" >Update</a></small>
                    {{/if}} 
                </p>
                <span class="icon-tick"></span>
                <p style="color: #B8B8B8;" class="cropper_controls">Preview:</p>
                <div class="cropper-preview cropper_controls" style="height: 160px; width: 210px;"></div>
            {{/if}}
        </li>
    </script>
    """
