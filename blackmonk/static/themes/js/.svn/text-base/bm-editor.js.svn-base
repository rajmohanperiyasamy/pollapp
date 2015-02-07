function bMEditor(elements, options) {
    'use strict';
    return this.init(elements, options);
}

if (typeof module === 'object') {
    module.exports = bMEditor;
}

(function (window, document) {
    'use strict';

    function extend(b, a) {
        var prop;
        if (b === undefined) {
            return a;
        }
        for (prop in a) {
            if (a.hasOwnProperty(prop) && b.hasOwnProperty(prop) === false) {
                b[prop] = a[prop];
            }
        }
        return b;
    }
    var currentEl = null;
    var appendToEl = null;
    var newSel = null, prevSel = null;
    var activeToolbar = false;
    var videoId = 0;
    var videoLoaded = true;
    // http://stackoverflow.com/questions/5605401/insert-link-in-contenteditable-element
    // by Tim Down
    function saveSelection() {
        var i,
            len,
            ranges,
            sel = window.getSelection();
        if (sel.getRangeAt && sel.rangeCount) {
            ranges = [];
            for (i = 0, len = sel.rangeCount; i < len; i += 1) {
                ranges.push(sel.getRangeAt(i));
            }
            return ranges;
        }
        return null;
    }

    function restoreSelection(savedSel) {
        var i,
            len,
            sel = window.getSelection();
        if (savedSel) {
            sel.removeAllRanges();
            for (i = 0, len = savedSel.length; i < len; i += 1) {
                sel.addRange(savedSel[i]);
            }
        }
    }

    // http://stackoverflow.com/questions/1197401/how-can-i-get-the-element-the-caret-is-in-with-javascript-when-using-contentedi
    // by You
    function getSelectionStart() {
        var node = document.getSelection().anchorNode,
            startNode = (node && node.nodeType === 3 ? node.parentNode : node);
        return startNode;
    }

    // http://stackoverflow.com/questions/4176923/html-of-selected-text
    // by Tim Down
    function getSelectionHtml() {
        var i,
            html = '',
            sel,
            len,
            container;
        if (window.getSelection !== undefined) {
            sel = window.getSelection();
            if (sel.rangeCount) {
                container = document.createElement('div');
                for (i = 0, len = sel.rangeCount; i < len; i += 1) {
                    container.appendChild(sel.getRangeAt(i).cloneContents());
                }
                html = container.innerHTML;
            }
        } else if (document.selection !== undefined) {
            if (document.selection.type === 'Text') {
                html = document.selection.createRange().htmlText;
            }
        }
        return html;
    }

    bMEditor.prototype = {
        defaults: {
            allowMultiParagraphSelection: true,
            anchorInputPlaceholder: 'Paste or type a link',
            buttons: ['bold', 'italic', 'underline', 'anchor', 'header1', 'header2', 'quote'],
            buttonLabels: false,
            delay: 0,
            imageUploadUrl:'',
            diffLeft: 0,
            diffTop: -10,
            disableReturn: false,
            disableToolbar: false,
            firstHeader: 'h2',
            forcePlainText: true,
            placeholder: 'Type your text',
            secondHeader: 'h3',
            targetBlank: false,
            insert:true,
            insertItem:['video','break','image'],
            anchorPreviewHideDelay: 500
        },

        // http://stackoverflow.com/questions/17907445/how-to-detect-ie11#comment30165888_17907562
        // by rg89
        isIE: ((navigator.appName === 'Microsoft Internet Explorer') || ((navigator.appName === 'Netscape') && (new RegExp("Trident/.*rv:([0-9]{1,}[.0-9]{0,})").exec(navigator.userAgent) !== null))),

        init: function (elements, options) {
            this.elements = typeof elements === 'string' ? document.querySelectorAll(elements) : elements;
            if (this.elements.length === 0) {
                return;
            }
            this.isActive = true;
            this.parentElements = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'pre'];
            this.id = document.querySelectorAll('.bM-editor-toolbar').length + 1;
            this.options = extend(options, this.defaults);
            return this.initElements()
                       .bindSelect()
                       .bindPaste()
                       .setPlaceholders();
                       //.bindWindowActions();
        },

        initElements: function () {
            var i,
                addToolbar = false;
            for (i = 0; i < this.elements.length; i += 1) {
                this.elements[i].setAttribute('contentEditable', true);
                this.elements[i].setAttribute('data-bM-element', true);
                this.bindParagraphCreation(i).bindReturn(i).bindTab(i).bindAnchorPreview(i);
                if (!this.options.disableToolbar && !this.elements[i].getAttribute('data-disable-toolbar')) {
                    addToolbar = true;
                }
            }
            if(this.options.insert){
                this.insertEl();
            }
            // Init toolbar
            if (addToolbar) {
                this.initToolbar()
                    .bindButtons()
                    .bindAnchorForm();
            }
            return this;
        },

        serialize: function () {
            var i,
                elementid,
                content = {};
            for (i = 0; i < this.elements.length; i += 1) {
                elementid = (this.elements[i].id !== '') ? this.elements[i].id : 'element-' + i;
                content[elementid] = {
                    value: this.elements[i].innerHTML.trim()
                };
            }
            return content;
        },

        bindParagraphCreation: function (index) {
            var self = this;
            this.elements[index].addEventListener('keypress', function (e) {
                var node = getSelectionStart(),
                    tagName;
                if (node && node.getAttribute('data-bM-element') && node.children.length === 0 &&
                        !(self.options.disableReturn || node.getAttribute('data-disable-return'))) {
                    document.execCommand('formatBlock', false, 'p');
                }
                if (e.which === 13 && !e.shiftKey) {
                    node = getSelectionStart();
                    tagName = node.tagName.toLowerCase();

                    if (!(self.options.disableReturn || this.getAttribute('data-disable-return')) &&
                            tagName !== 'li' && tagName !== 'figcaption' && !self.isListItemChild(node)) {
                        document.execCommand('formatBlock', false, 'p');
                        if (tagName === 'a') {
                            document.execCommand('unlink', false, null);
                        }
                    }else{
                        e.preventDefault();
                    }
                }
            });
            return this;
        },

        isListItemChild: function (node) {
            var parentNode = node.parentNode,
                tagName = parentNode.tagName.toLowerCase();
            while (this.parentElements.indexOf(tagName) === -1 && tagName !== 'div') {
                if (tagName === 'li') {
                    return true;
                }
                parentNode = parentNode.parentNode;
                if (parentNode && parentNode.tagName) {
                    tagName = parentNode.tagName.toLowerCase();
                } else {
                    return false;
                }
            }
            return false;
        },

        bindReturn: function (index) {       
            /** /
            $(".no-copy-paste").keydown(function(e)
            {
                if (ctrlDown && (e.keyCode == vKey || e.keyCode == cKey)) return false;
            });
            /**/
            var self = this;
            this.elements[index].addEventListener('keypress', function (e) {
                var node = getSelectionStart(),
                    tagName = node.tagName.toLowerCase();

                if (e.ctrlKey && (e.which === 97 || e.which === 65) && tagName==='figcaption'){
                    e.preventDefault();
                }
                if (e.which === 13) {
                    if (self.options.disableReturn || this.getAttribute('data-disable-return')) {
                        e.preventDefault();
                    }
                }
            });
            return this;
        },

        bindTab: function (index) {
            this.elements[index].addEventListener('keydown', function (e) {
                if (e.which === 9) {
                    // Override tab only for pre nodes
                    var tag = getSelectionStart().tagName.toLowerCase();
                    if (tag === "pre") {
                        e.preventDefault();
                        document.execCommand('insertHtml', null, '    ');
                    }
                }
            });
            return this;
        },

        buttonTemplate: function (btnType) {
            var buttonLabels = this.getButtonLabels(this.options.buttonLabels),
                buttonTemplates = {
                    'bold': '<li><button class="bM-editor-action bM-editor-action-bold" data-action="bold" data-element="b"><span class="bold"></span></button></li>',
                    'italic': '<li><button class="bM-editor-action bM-editor-action-italic" data-action="italic" data-element="i"><span class="italic"></span></button></li>',
                    'underline': '<li><button class="bM-editor-action bM-editor-action-underline" data-action="underline" data-element="u"><span class="underline"></span></button></li>',
                    'strikethrough': '<li><button class="bM-editor-action bM-editor-action-strikethrough" data-action="strikethrough" data-element="strike"><span class="strikethrough"></span></button></li>',
                    'superscript': '<li><button class="bM-editor-action bM-editor-action-superscript" data-action="superscript" data-element="sup"><span class="superscript"></span></button></li>',
                    'subscript': '<li><button class="bM-editor-action bM-editor-action-subscript" data-action="subscript" data-element="sub"><span></span></button></li>',
                    'anchor': '<li><button class="bM-editor-action bM-editor-action-anchor" data-action="anchor" data-element="a"><span class="anchor"></span></button></li>',
                    'image': '<li><button class="bM-editor-action bM-editor-action-image" data-action="image" data-element="img"><span class="image"></span></button></li>',
                    'header1': '<li><button class="bM-editor-action bM-editor-action-header1" data-action="append-' + this.options.firstHeader + '" data-element="' + this.options.firstHeader + '"><span class="h1"></span></button></li>',
                    'header2': '<li><button class="bM-editor-action bM-editor-action-header2" data-action="append-' + this.options.secondHeader + '" data-element="' + this.options.secondHeader + '"><span class="h2"></span></button></li>',
                    'quote': '<li><button class="bM-editor-action bM-editor-action-quote" data-action="append-blockquote" data-element="blockquote"><span class="quote"></span></button></li>',
                    'orderedlist': '<li><button class="bM-editor-action bM-editor-action-orderedlist" data-action="insertorderedlist" data-element="ol"><span class="unorderedlist"></span></button></li>',
                    'unorderedlist': '<li><button class="bM-editor-action bM-editor-action-unorderedlist" data-action="insertunorderedlist" data-element="ul"><span class="orderedlist"></span></button></li>',
                    'pre': '<li><button class="bM-editor-action bM-editor-action-pre" data-action="append-pre" data-element="pre"><span class="pre"></span></button></li>'
                };
            return buttonTemplates[btnType] || false;
        },

        // TODO: break method
        getButtonLabels: function (buttonLabelType) {
            var customButtonLabels,
                attrname,
                buttonLabels = {
                    'bold': '<b>B</b>',
                    'italic' : '<b><i>I</i></b>',
                    'underline': '<b><u>U</u></b>',
                    'superscript': '<b>x<sup>1</sup></b>',
                    'subscript': '<b>x<sub>1</sup></b>',
                    'anchor': '<b>#</b>',
                    'image': '<b>image</b>',
                    'header1': '<b>H1</b>',
                    'header2': '<b>H2</b>',
                    'quote': '<b>&ldquo;</b>',
                    'orderedlist': '<b>1.</b>',
                    'unorderedlist': '<b>&bull;</b>',
                    'pre': '<b>0101</b>'
                };
            if (buttonLabelType === 'fontawesome') {
                customButtonLabels = {
                    'bold': '<i class="fa fa-bold"></i>',
                    'italic' : '<i class="fa fa-italic"></i>',
                    'underline': '<i class="fa fa-underline"></i>',
                    'superscript': '<i class="fa fa-superscript"></i>',
                    'subscript': '<i class="fa fa-subscript"></i>',
                    'anchor': '<i class="fa fa-link"></i>',
                    'image': '<i class="fa fa-picture-o"></i>',
                    'quote': '<i class="fa fa-quote-right"></i>',
                    'orderedlist': '<i class="fa fa-list-ol"></i>',
                    'unorderedlist': '<i class="fa fa-list-ul"></i>',
                    'pre': '<i class="fa fa-code fa-lg"></i>'
                };
            } else if (typeof buttonLabelType === 'object') {
                customButtonLabels = buttonLabelType;
            }
            if (typeof customButtonLabels === 'object') {
                for (attrname in customButtonLabels) {
                    if (customButtonLabels.hasOwnProperty(attrname)) {
                        buttonLabels[attrname] = customButtonLabels[attrname];
                    }
                }
            }
            return buttonLabels;
        },

        //TODO: actionTemplate
        toolbarTemplate: function () {
            var btns = this.options.buttons,
                html = '<ul id="bM-editor-toolbar-actions" class="bM-editor-toolbar-actions clearfix">',
                i,
                tpl;

            for (i = 0; i < btns.length; i += 1) {
                tpl = this.buttonTemplate(btns[i]);
                if (tpl) {
                    html += tpl;
                }
            }
            html += '</ul>' +
                '<div class="bM-editor-toolbar-form-anchor" id="bM-editor-toolbar-form-anchor">' +
                '    <input type="text" value="" placeholder="' + this.options.anchorInputPlaceholder + '">' +
                '    <a href="#">&times;</a>' +
                '</div>';
            return html;
        },

        initToolbar: function () {
            if (this.toolbar) {
                return this;
            }
            this.toolbar = this.createToolbar();
            this.keepToolbarAlive = false;
            this.anchorForm = this.toolbar.querySelector('.bM-editor-toolbar-form-anchor');
            this.anchorInput = this.anchorForm.querySelector('input');
            this.toolbarActions = this.toolbar.querySelector('.bM-editor-toolbar-actions');
            this.anchorPreview = this.createAnchorPreview();

            return this;
        },

        createToolbar: function () {
            var toolbar = document.createElement('div');
            toolbar.id = 'bM-editor-toolbar-' + this.id;
            toolbar.className = 'bM-editor-toolbar';
            toolbar.innerHTML = this.toolbarTemplate();
            document.getElementsByTagName('body')[0].appendChild(toolbar);
            return toolbar;
        },
        insertEl:function(){
            var $this = this;
            var clImg = false;
            var imgId = 0;
            var $el = $(this.elements);
            var elLeft = $el.offset().left -18,
                elTop = $el.offset().top;
            $('body').append('<div class="insertEl" style="top:'+elTop+'px;left:'+elLeft+'px"><a href="javascript:void(0)"><span></span></a></div>');
            var item = this.options.insertItem;
            var length = item.length;
            var elList = '';
            for(var i=0;i<length;i++){
                if(item[i] === 'image'){
                    elList += '<li class="'+item[i]+'"><span><span class="icon"></span>'+item[i]+'</span><input accept="image/*" class="editorImg" type="file" /></li>';
                }else{
                    elList += '<li class="'+item[i]+'"><span><span class="icon"></span>'+item[i]+'</span></li>';
                }
            }
            $('.insertEl').append('<ul class="insertItems unstyled">'+elList+'</ul>');
            $('.insertEl > a').click(function(event) {
                /* Act on the event */
                if(!videoLoaded){
                    $('.insertItems').addClass('videoLoading');       
                }
                appendToEl = currentEl;
                var el = $(this);
                if(el.parent().hasClass('active')){
                    el.parent().removeClass('move');
                    $('.insertEl').removeClass('url');
                    setTimeout(function(){
                        el.parent().removeClass('active');
                        $('.addVideoUrl').remove();
                    },'400');
                }else{
                    el.parent().addClass('active');
                    $('.insertEl').removeClass('url');
                    $('.addVideoUrl').remove();
                    setTimeout(function(){
                        el.parent().addClass('move');
                    },'10')
                }
            });
            /** /
            $('body').click(function(event) {
                $('.insertEl').removeClass('active')
            });
            $('.insertEl').click(function(event){
                event.stopPropagation();
            });
            /**/
            
            $('.insertEl .video').on('click', function() {
                $('.insertEl').append('<div class="addVideoUrl"><input placeholder="Enter youtube or vimeo url" type="text" class="videoUrl" /></div>');
                $('.videoUrl').focus();
                $('.insertEl').addClass('url');
                $this.insertVideo();
            });
            $('.insertEl .break').on('click', function() {
                $('.insertEl').removeClass('active') ;
                $('.insertEl').removeClass('url');
                $this.insertBreak();
            });
            var files;
            var val;
            $('.insertEl .image > span').on('click', function() {
                imgId ++;
                $('.insertEl').removeClass('active move');
                $('.insertEl').removeClass('url');
                $('.addVideoUrl').remove();
                clImg = true;
                $('.editorImg').trigger('click');
                $('.body').children().off('mouseenter');
                //$this.insertImge(clImg,imgId);
            });
                $('.editorImg').change(function(event) {
                    var id = imgId;
                    files = event.target.files;
                    val = $(this).val();
                    val = val.replace("C:\\fakepath\\", "");
                    if(clImg){
                        //$this.insertImge(clImg,imgId);
                        var data = new FormData();
                        $.each(files, function(key, value)
                        {
                        	//data.append(key, value);
                            data.append('photo', value);
                        });
                        var imgLoadingTemplate = '<div class="loadingImg fade in"><span class="icon"></span><span></class="text">Loading Image..</span></div>';
                        if(appendToEl === null){
                            $($this.elements).find('p').first().after(imgLoadingTemplate) ;   
                        }else{
                            appendToEl.before(imgLoadingTemplate);
                        }
                        var imageToolbarTemplate = '<ul class="unstyled imageToolbar">\
                            <li class="pull-left alignLeft"><span></span></li>\
                            <li class="pull-left alignCenter active"><span></span></li>\
                            <li class="pull-left alignRight"><span></span></li>\
                            <li class="pull-left alignLeftOut"><span></span></li>\
                            <li class="pull-left alignCenterOut"><span></span></li>\
                            <li class="pull-left alignRightOut"><span></span></li>\
							<li class="pull-left delete"><span></span></li>\
                            </ul>';
                        var imgTemplate = ""
                        $.ajax({
                            url: $this.options.imageUploadUrl,
                            type: 'POST',
                            data: data,
                            dataType: 'json',
                            processData: false, 
                            contentType: false, 
                            success: function(data, textStatus, jqXHR)
                            {
                            	imgTemplate += '<figure class="image" contenteditable="false">'+imageToolbarTemplate+'<img class="fade" id="image'+id+'" style="min-height:200px" src="'+data[0].url+'"/><input type="hidden" name="pageimg" value="'+data[0].photo_id+'" /><figcaption data-disable-toolbar="true" contenteditable="true" class="iMg-cPtN">Type caption for image (optional)</figcaption></figure>'; 
                                clImg = false;
                                /**/
                                $('.loadingImg').removeClass('in');
                                setTimeout(
                                    function(){
                                        $('.loadingImg').remove();
                                        if(data.error){
                                            alert('An error occurred please try again..');
                                        }else{
                                            if(appendToEl === null){
                                                $($this.elements).find('p').first().after(imgTemplate) ;   
                                            }else{
                                                appendToEl.before(imgTemplate);
                                            }
                                            $('#image'+id).on('load',function(){
                                                $('#image'+id).removeAttr('style');
                                                $('#image'+id).addClass('in');
                                                $('#image'+id).parent().addClass('active');
                                                setTimeout(function(){
                                                    $('#image'+id).parent().addClass('move');
                                                },'100');
                                                $(document).mouseup(function (e){
                                                    var container = $('#image'+id).parent();
                                                    if (!container.is(e.target)&& container.has(e.target).length === 0){
                                                        container.removeClass('move');
                                                        setTimeout(function(){
                                                            container.removeClass('active');
                                                        },'400');
                                                    }
                                                });
                                                $('#image'+id).on('click',function(event) {
                                                    var $el  = $(this);
                                                    if($el.parent().hasClass('active')){
                                                        $el.parent().removeClass('move');
                                                        setTimeout(function(){
                                                            $el.parent().removeClass('active');
                                                        },'400');
                                                    }else{
                                                        $el.parent().addClass('active');
                                                        setTimeout(function(){
                                                            $el.parent().addClass('move');
                                                        },'100');    
                                                    }
                                                });
                                                function toolbarAction(el,cl){
                                                    el.on('click',function(event) {
                                                        $(this).parent().find('li').removeClass('active');
                                                        $(this).addClass('active');
                                                        $(this).parent().parent().attr('class','active move').addClass(cl);
                                                    });
                                                }
                                                toolbarAction($('.alignLeft'),'iMg-lT');
                                                toolbarAction($('.alignCenter'),'iMg-cTr');
                                                toolbarAction($('.alignRight'),'iMg-rT');
                                                toolbarAction($('.alignLeftOut'),'iMg-lTO');
                                                toolbarAction($('.alignCenterOut'),'iMg-cTrO');
                                                toolbarAction($('.alignRightOut'),'iMg-rTO');
												$('.imageToolbar .delete').on('click',function(){
													var r=confirm("Do you Want To Delete!");
													if (r==true){
														$(this).parent().parent().remove();	
													}
												});
                                                /** /
                                                $('.iMg-cPtN').on('keydown keyup', function(event) {
                                                    if($(this).text()===''){
                                                        $(this).addClass('captionPlaceholder');
                                                    }else{
                                                        $(this).removeClass('captionPlaceholder');
                                                    }
                                                });
/**/
                                                //$('#image'+id).parent().find('.iMg-cPtN').focus();
                                                $('.iMg-cPtN').on('focus', function(event) {
                                                    if($(this).text()==='Type caption for image (optional)'){
                                                        $(this).text('').removeClass('captionPlaceholder');
                                                    }
                                                    $el.attr('contenteditable', 'false');
                                                })
                                                $('.iMg-cPtN').on('blur', function(event) {
                                                    if($(this).text() === ''){
                                                        $(this).text('Type caption for image (optional)').addClass('captionPlaceholder');    
                                                    }
                                                    $el.attr('contenteditable', 'true');
                                                })

                                                /** /
                                                $('.iMg-cPtN').each(function() {
                                                    $(this).focus(function(event) {
                                                        if($(this).html() === 'Type caption for image (optional)'){
                                                            $(this).html('').removeClass('placeholder');
                                                        }
                                                    });
                                                    $(this).blur(function(event) {
                                                        if($(this).html() === '' || $(this).html() === '<br>'){
                                                            $(this).html('Type caption for image (optional)').addClass('placeholder');
                                                        }
                                                    });
                                                });
                                                /**/
                                                //$el.focus();
                                            });

                                        }
                                    },'500'
                                );
                                /** /
                                setTimeout(function(){
                                    $('img').addClass('in');
                                },'1000')
                                /**/
                                /**/
                                //alert(jqXHR.responseText)
                            },
                            error: function(jqXHR, textStatus, errorThrown)
                            {
                                clImg = false;
                                $('.loadingImg').removeClass('in');
                                setTimeout(
                                    function(){
                                        $('.loadingImg').remove();
                                    },'500'
                                );
                                alert('An error occurred please try again..');
                                //console.log('ERRORS: ' + textStatus);
                            }
                        });
                    }
                    /* Act on the event */
                });
            return this;
        },
        insertVideo:function(){
            videoId ++;
            var $this = this;
            var $el = $(this.elements);
            var activeVideoToolbar = false;
            $(window).bind('keyup', function(e){
                e.preventDefault();
                e.stopPropagation();
                if (e.keyCode === 13){
                    var val = $('.videoUrl').val();
                    if(typeof val === "undefined"){
                        val = '';
                    }
                    if($('.insertEl').hasClass('url') && val!== ''){
                        $('.addVideoUrl').remove();
                        $('.insertEl').removeClass('active');
                        var loadVideo = function(){
                            var youtube = val.match(/(?:https?:\/{2})?(?:w{3}\.)?youtu(?:be)?\.(?:com|be)(?:\/watch\?v=|\/)([^\s&]+)/);
                            var vimeo = val.match(/vimeo\.com\/([0-9]*)/);
                            var video = '';
                            var videoToolbarTemplate ='<ul class="unstyled imageToolbar">\
                                    <li class="pull-left alignLeft"><span></span></li>\
                                    <li class="pull-left alignCenter active"><span></span></li>\
                                    <li class="pull-left alignRight"><span></span></li>\
									<li class="pull-left delete"><span></span></li>\
                                </ul>'
                            if(youtube){  
								videoLoaded = false;
                                video = '<figure contenteditable="false" class="video">'+videoToolbarTemplate+'<div class="iframeCont"><iframe class="fade" id="video'+videoId+'" width="560" height="315" src="//www.youtube.com/embed/'+youtube[1]+'?wmode=opaque" frameborder="0" allowfullscreen></iframe></div><figcaption data-disable-toolbar="true" contenteditable="true" class="iMg-cPtN">Type caption for video (optional)</figcaption></figure>';                                          
                                //video = '<iframe width="560" height="315" src="//www.youtube.com/embed/'+youtube[1]+'?wmode=opaque" frameborder="0" allowfullscreen></iframe>';  
                                                
                            }else if(vimeo){
								videoLoaded = false;
                                video = '<figure contenteditable="false" class="video">'+videoToolbarTemplate+'<div class="iframeCont"><iframe class="fade" id="video'+videoId+'"  width="560" height="315"  src="http://player.vimeo.com/video/'+vimeo[1]+'?byline=0&amp;portrait=0&amp;" frameborder="0" webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe><div><figcaption data-disable-toolbar="true" contenteditable="true" class="iMg-cPtN">Type caption for video (optional)</figcaption></figure>';    
                                //video = '<iframe  width="560" height="315"  src="http://player.vimeo.com/video/'+vimeo[1]+'?byline=0&amp;portrait=0&amp;" frameborder="0" webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe>';
                            
                            }else{
                                alert('url is not valid');
                            }
                            if(appendToEl === null){
                                $($this.elements).prepend(video) ;   
                            }else{
                                appendToEl.before(video);
                            }
                            $('#video'+videoId).on('load',function(){
                                videoLoaded = true;
                                $('.insertItems').removeClass('videoLoading');       
                                $('#video'+videoId).addClass('in');
                                if(!activeVideoToolbar){
                                    $('#video'+videoId).parent().parent().addClass('active');
                                    setTimeout(function(){
                                        $('#video'+videoId).parent().parent().addClass('move');
                                    },'100');
                                    activeVideoToolbar = true;
                                }
                                $(document).mouseup(function (e){
                                    var videocontainer = $('#video'+videoId).parent().parent();
                                    if (!videocontainer.is(e.target)&& videocontainer.has(e.target).length === 0){
                                        $('figure.video').removeClass('move');
                                        setTimeout(function(){
                                            $('figure.video').removeClass('active');
                                        },'400');
                                        activeVideoToolbar = false;
                                    }
                                });

                                $('#video'+videoId).parent().mouseenter(function(event) {
                                    var $videoCont = $(this).parent();
                                    if(!activeVideoToolbar){
                                        $videoCont.addClass('active');
                                        setTimeout(function(){
                                            $videoCont.addClass('move');
                                        },'100');
                                        activeVideoToolbar = true;
                                    }
                                });


                                function toolbarAction(el,cl){
                                    el.on('click',function(event) {
                                        $(this).parent().find('li').removeClass('active');
                                        $(this).addClass('active');
                                        $(this).parent().parent().attr('class','active move video').addClass(cl);
                                    });
                                }
                                toolbarAction($('.alignLeft'),'iMg-lT');
                                toolbarAction($('.alignCenter'),'iMg-cTr');
                                toolbarAction($('.alignRight'),'iMg-rT');
								
								$('.imageToolbar .delete').on('click',function(){
									var r=confirm("Do you Want To Delete!");
									if (r==true){
										$(this).parent().parent().remove();	
									}
								});

                                $('.iMg-cPtN').on('focus', function(event) {
                                    if($(this).text()==='Type caption for video (optional)'){
                                        $(this).text('').removeClass('captionPlaceholder');
                                    }
                                    $el.attr('contenteditable', 'false');
                                })
                                $('.iMg-cPtN').on('blur', function(event) {
                                    if($(this).text() === ''){
                                        $(this).text('Type caption for video (optional)').addClass('captionPlaceholder');    
                                    }
                                    $el.attr('contenteditable', 'true');
                                })
                            })
                            $('#video'+videoId).on('error', function(event) {
                                videoLoaded = true;
                                $('.insertItems').removeClass('videoLoading');   
                                alert('An error occurred please try again..');
                                $('#video'+videoId).parent().parent().remove();
                            });
                        };
                        loadVideo();
                    }
                }
            });
        },
        insertBreak :function(){
            if(appendToEl === null){
                $(this.elements).find('p').first().after('<hr/>') ;   
            }else{
                appendToEl.before('<hr/>');
            }
        },
        bindSelect: function () {
            var self = this,
                timer = '',
                i;

            this.checkSelectionWrapper = function (e) {

                // Do not close the toolbar when bluring the editable area and clicking into the anchor form
                if (e && self.clickingIntoArchorForm(e)) {
                    return false;
                }

                clearTimeout(timer);
                timer = setTimeout(function () {
                    self.checkSelection();
                }, self.options.delay);
            };

            document.documentElement.addEventListener('mouseup', this.checkSelectionWrapper);

            for (i = 0; i < this.elements.length; i += 1) {
                this.elements[i].addEventListener('keyup', this.checkSelectionWrapper);
                this.elements[i].addEventListener('blur', this.checkSelectionWrapper);
            }
            return this;
        },

        checkSelection: function () {
            var $el = $(this.elements);
            var $toolbar = $(this.toolbar);
            $('.body').children().on('mouseenter',function(event) {
                currentEl = $(this);
                var elTop = currentEl.offset().top;
                if(!$(this).parent().hasClass('placeholder')){
                    $('.insertEl').addClass('on');
                }
                if(!$('.insertEl').hasClass('active')){
                    $('.insertEl').css('top', elTop+'px')
                }
            });
            $('.body').children().on('mouseout',function(event) {
                if(!$('.insertEl').hasClass('active')){
                    $('.insertEl').removeClass('on');
                }
            });
            
            /** /
            $(el).blur(function(event) {
                if($(el).html() === '' || $(el).html() === '<br>'){
                    $(el).html($this.options.placeholder).addClass('placeholder');
                }
            });
            $('.iMg-cPtN').on('focus', function(event) {
                console.log('f');
                //var node = getSelectionStart();
                //var node = document.getSelection().anchorNode
                //var node = getSelectionStart(),
                //tagName = node.tagName.toLowerCase();
                //console.log(tagName);
                if($(this).text()===''){
                    $(this).addClass('captionPlaceholder');
                }else{
                    $(this).removeClass('captionPlaceholder');
                }
            });
            /**/
            var newSelection,
                selectionElement;

            if (this.keepToolbarAlive !== true && !this.options.disableToolbar) {
                newSelection = window.getSelection();
                newSel = newSelection.toString().trim();
                if (newSelection.toString().trim() === '' ||
                        (this.options.allowMultiParagraphSelection === false && this.hasMultiParagraphs())) {
                    this.hideToolbarActions();
                } else {
                    selectionElement = this.getSelectionElement();
                    if (!selectionElement || selectionElement.getAttribute('data-disable-toolbar')) {
                        this.hideToolbarActions();
                    } else {
                        //console.log('newSel'+newSel);
                        //console.log('prevSel'+prevSel);
                        if(newSel !== prevSel){
                            console.log('selection same')
                            this.checkSelectionElement(newSelection, selectionElement);
                        }
                        //if(!$toolbar.hasClass('bM-editor-toolbar-active')){
                        prevSel = newSel;
                        //}
                    }
                }
            }
            return this;
        },

        clickingIntoArchorForm: function(e) {
            var self = this;
            if (e.type && e.type.toLowerCase() === 'blur' && e.relatedTarget && e.relatedTarget === self.anchorInput) {
                return true;
            }
            return false;
        },

        hasMultiParagraphs: function () {
            var selectionHtml = getSelectionHtml().replace(/<[\S]+><\/[\S]+>/gim, ''),
                hasMultiParagraphs = selectionHtml.match(/<(p|h[0-6]|blockquote)>([\s\S]*?)<\/(p|h[0-6]|blockquote)>/g);

            return (hasMultiParagraphs ? hasMultiParagraphs.length : 0);
        },

        checkSelectionElement: function (newSelection, selectionElement) {
            var i;
            this.selection = newSelection;
            var $this = this;
            this.selectionRange = this.selection.getRangeAt(0);
            for (i = 0; i < this.elements.length; i += 1) {
                if (this.elements[i] === selectionElement) {
                    setTimeout(function(){
                        $this.setToolbarPosition();
                    })
                    this.setToolbarButtonStates()
                        .showToolbarActions();
                    return;
                }
            }
            this.hideToolbarActions();
        },

        getSelectionElement: function () {
            var selection = window.getSelection(),
                range = selection.getRangeAt(0),
                current = range.commonAncestorContainer,
                parent = current.parentNode,
                result,
                getbMElement = function(e) {
                    var parent = e;
                    try {
                        while (!parent.getAttribute('data-bM-element')) {
                            parent = parent.parentNode;
                        }
                    } catch (errb) {
                        return false;
                    }
                    return parent;
                };
            // First try on current node
            try {
                if (current.getAttribute('data-bM-element')) {
                    result = current;
                } else {
                    result = getbMElement(parent);
                }
            // If not search in the parent nodes.
            } catch (err) {
                result = getbMElement(parent);
            }
            return result;
        },

        setToolbarPosition: function () {
            var buttonHeight = 50,
                selection = window.getSelection(),
                range = selection.getRangeAt(0),
                boundary = range.getBoundingClientRect(),
                defaultLeft = (this.options.diffLeft) - (this.toolbar.offsetWidth / 2),
                middleBoundary = (boundary.left + boundary.right) / 2,
                halfOffsetWidth = this.toolbar.offsetWidth / 2;
            if (boundary.top < buttonHeight) {
                this.toolbar.classList.add('bM-toolbar-arrow-over');
                this.toolbar.classList.remove('bM-toolbar-arrow-under');
                this.toolbar.style.top = buttonHeight + boundary.bottom - this.options.diffTop + window.pageYOffset - this.toolbar.offsetHeight + 'px';
            } else {
                this.toolbar.classList.add('bM-toolbar-arrow-under');
                this.toolbar.classList.remove('bM-toolbar-arrow-over');
                this.toolbar.style.top = boundary.top + this.options.diffTop + window.pageYOffset - this.toolbar.offsetHeight + 'px';
            }
            if (middleBoundary < halfOffsetWidth) {
                this.toolbar.style.left = defaultLeft + halfOffsetWidth + 'px';
            } else if ((window.innerWidth - middleBoundary) < halfOffsetWidth) {
                this.toolbar.style.left = window.innerWidth + defaultLeft - halfOffsetWidth + 'px';
            } else {
                this.toolbar.style.left = defaultLeft + middleBoundary + 'px';
            }

            this.hideAnchorPreview();

            return this;
        },

        setToolbarButtonStates: function () {
            var buttons = this.toolbarActions.querySelectorAll('button'),
                i;
            for (i = 0; i < buttons.length; i += 1) {
                buttons[i].classList.remove('bM-editor-button-active');
            }
            this.checkActiveButtons();
            return this;
        },

        checkActiveButtons: function () {
            var parentNode = this.selection.anchorNode;
            if (!parentNode.tagName) {
                parentNode = this.selection.anchorNode.parentNode;
            }
            while (parentNode.tagName !== undefined && this.parentElements.indexOf(parentNode.tagName.toLowerCase) === -1) {
                this.activateButton(parentNode.tagName.toLowerCase());
                parentNode = parentNode.parentNode;
            }
        },

        activateButton: function (tag) {
            var el = this.toolbar.querySelector('[data-element="' + tag + '"]');
            if (el !== null && el.className.indexOf('bM-editor-button-active') === -1) {
                el.className += ' bM-editor-button-active';
            }
        },

        bindButtons: function () {
            var buttons = this.toolbar.querySelectorAll('button'),
                i,
                self = this,
                triggerAction = function (e) {
                    e.preventDefault();
                    e.stopPropagation();
                    if (self.selection === undefined) {
                        self.checkSelection();
                    }
                    if (this.className.indexOf('bM-editor-button-active') > -1) {
                        this.classList.remove('bM-editor-button-active');
                    } else {
                        this.className += ' bM-editor-button-active';
                    }
                    self.execAction(this.getAttribute('data-action'), e);
                };
            for (i = 0; i < buttons.length; i += 1) {
                buttons[i].addEventListener('click', triggerAction);
            }
            this.setFirstAndLastItems(buttons);
            return this;
        },

        setFirstAndLastItems: function (buttons) {
            buttons[0].className += ' bM-editor-button-first';
            buttons[buttons.length - 1].className += ' bM-editor-button-last';
            return this;
        },

        execAction: function (action, e) {
            if (action.indexOf('append-') > -1) {
                this.execFormatBlock(action.replace('append-', ''));
                this.setToolbarPosition();
                this.setToolbarButtonStates();
            } else if (action === 'anchor') {
                this.triggerAnchorAction(e);
            } else if (action === 'image') {
                document.execCommand('insertImage', false, window.getSelection());
            } else {
                document.execCommand(action, false, null);
                this.setToolbarPosition();
            }
        },

        triggerAnchorAction: function () {
            if (this.selection.anchorNode.parentNode.tagName.toLowerCase() === 'a') {
                document.execCommand('unlink', false, null);
            } else {
                if (this.anchorForm.style.display === 'block') {
                    this.showToolbarActions();
                } else {
                    this.showAnchorForm();
                }
            }
            return this;
        },

        execFormatBlock: function (el) {
            var selectionData = this.getSelectionData(this.selection.anchorNode);
            // FF handles blockquote differently on formatBlock
            // allowing nesting, we need to use outdent
            // https://developer.mozilla.org/en-US/docs/Rich-Text_Editing_in_Mozilla
            if (el === 'blockquote' && selectionData.el &&
                    selectionData.el.parentNode.tagName.toLowerCase() === 'blockquote') {
                return document.execCommand('outdent', false, null);
            }
            if (selectionData.tagName === el) {
                el = 'p';
            }
            // When IE we need to add <> to heading elements and
            //  blockquote needs to be called as indent
            // http://stackoverflow.com/questions/10741831/execcommand-formatblock-headings-in-ie
            // http://stackoverflow.com/questions/1816223/rich-text-editor-with-blockquote-function/1821777#1821777
            if (this.isIE) {
                if (el === 'blockquote') {
                    return document.execCommand('indent', false, el);
                }
                el = '<' + el + '>';
            }
            return document.execCommand('formatBlock', false, el);
        },

        getSelectionData: function (el) {
            var tagName;

            if (el && el.tagName) {
                tagName = el.tagName.toLowerCase();
            }

            while (el && this.parentElements.indexOf(tagName) === -1) {
                el = el.parentNode;
                if (el && el.tagName) {
                    tagName = el.tagName.toLowerCase();
                }
            }

            return {
                el: el,
                tagName: tagName
            };
        },

        getFirstChild: function (el) {
            var firstChild = el.firstChild;
            while (firstChild !== null && firstChild.nodeType !== 1) {
                firstChild = firstChild.nextSibling;
            }
            return firstChild;
        },

        hideToolbarActions: function () {
            this.keepToolbarAlive = false;
            $(this.toolbar).removeClass('bM-editor-toolbar-active');
        },

        showToolbarActions: function () {
            var self = this,
                timer;
            this.anchorForm.style.display = 'none';
            this.toolbarActions.style.display = 'block';
            this.keepToolbarAlive = false;
            clearTimeout(timer);
            timer = setTimeout(function() {
                if (!self.toolbar.classList.contains('bM-editor-toolbar-active')) {
                    self.toolbar.classList.add('bM-editor-toolbar-active');
                    if(activeToolbar === false){
                        self.toolbar.classList.add('move');
                    }
                    activeToolbar = true;
                }
            }, 100);
        },

        showAnchorForm: function (link_value) {
            this.toolbarActions.style.display = 'none';
            this.savedSelection = saveSelection();
            this.anchorForm.style.display = 'block';
            this.keepToolbarAlive = true;
            this.anchorInput.focus();
            this.anchorInput.value = link_value || '';
        },

        bindAnchorForm: function () {
            var linkCancel = this.anchorForm.querySelector('a'),
                self = this;
            this.anchorForm.addEventListener('click', function (e) {
                e.stopPropagation();
            });
            this.anchorInput.addEventListener('keyup', function (e) {
                if (e.keyCode === 13) {
                    e.preventDefault();
                    self.createLink(this);
                }
            });
            this.anchorInput.addEventListener('click', function (e) {
                // make sure not to hide form when cliking into the input
                e.stopPropagation();
                self.keepToolbarAlive = true;
            });
            this.anchorInput.addEventListener('blur', function () {
                self.keepToolbarAlive = false;
                self.checkSelection();
            });
            linkCancel.addEventListener('click', function (e) {
                e.preventDefault();
                self.showToolbarActions();
                restoreSelection(self.savedSelection);
            });
            return this;
        },


        hideAnchorPreview: function() {
            this.anchorPreview.classList.remove('bM-editor-anchor-preview-active');
        },

        // TODO: break method
        showAnchorPreview: function (anchor_el) {
            if (this.anchorPreview.classList.contains('bM-editor-anchor-preview-active')) {
                return true;
            }

            var self = this,
                buttonHeight = 40,
                boundary = anchor_el.getBoundingClientRect(),
                middleBoundary = (boundary.left + boundary.right) / 2,
                halfOffsetWidth,
                defaultLeft,
                timer;

            self.anchorPreview.querySelector('i').innerHTML = anchor_el.href;
            halfOffsetWidth = self.anchorPreview.offsetWidth / 2;
            defaultLeft = self.options.diffLeft - halfOffsetWidth;

            clearTimeout(timer);
            timer = setTimeout(function() {
                if (!self.anchorPreview.classList.contains('bM-editor-anchor-preview-active')) {
                    self.anchorPreview.classList.add('bM-editor-anchor-preview-active');
                }
            }, 100);

            self.observeAnchorPreview(anchor_el);

            self.anchorPreview.classList.add('bM-toolbar-arrow-over');
            self.anchorPreview.classList.remove('bM-toolbar-arrow-under');
            /**/
            self.anchorPreview.style.top = Math.round(buttonHeight + boundary.bottom - self.options.diffTop + window.pageYOffset - self.anchorPreview.offsetHeight) -10 + 'px';
            if (middleBoundary < halfOffsetWidth) {
                self.anchorPreview.style.left = defaultLeft + halfOffsetWidth + 'px';
            } else if ((window.innerWidth - middleBoundary) < halfOffsetWidth) {
                self.anchorPreview.style.left = window.innerWidth + defaultLeft - halfOffsetWidth + 'px';
            } else {
                self.anchorPreview.style.left = defaultLeft + middleBoundary + 'px';
            }

            /**/
            return this;
        },

        // TODO: break method
        observeAnchorPreview: function(anchorEl) {
            var self = this,
                lastOver = (new Date()).getTime(),
                over = true,
                stamp = function() {
                    lastOver = (new Date()).getTime();
                    over = true;
                },
                unstamp = function(e) {
                    if (!e.relatedTarget || !/anchor-preview/.test(e.relatedTarget.className)) {
                        over = false;
                    }
                },
                interval_timer = setInterval(function() {
                    if (over) {
                        return true;
                    }
                    var durr = (new Date()).getTime() - lastOver;
                    if (durr > self.options.anchorPreviewHideDelay) {
                        // hide the preview 1/2 second after mouse leaves the link
                        self.hideAnchorPreview();

                        // cleanup
                        clearInterval(interval_timer);
                        self.anchorPreview.removeEventListener('mouseover', stamp);
                        self.anchorPreview.removeEventListener('mouseout', unstamp);
                        anchorEl.removeEventListener('mouseover', stamp);
                        anchorEl.removeEventListener('mouseout', unstamp);

                    }
                }, 200);

            self.anchorPreview.addEventListener('mouseover', stamp);
            self.anchorPreview.addEventListener('mouseout', unstamp);
            anchorEl.addEventListener('mouseover', stamp);
            anchorEl.addEventListener('mouseout', unstamp);
        },

        createAnchorPreview: function () {
            var self = this,
                anchorPreview = document.createElement('div');
            anchorPreview.id = 'bM-editor-anchor-preview-' + this.id;
            anchorPreview.className = 'bM-editor-anchor-preview';
            anchorPreview.innerHTML = this.anchorPreviewTemplate();
            document.getElementsByTagName('body')[0].appendChild(anchorPreview);

            anchorPreview.addEventListener('click', function() { self.anchorPreviewClickHandler(); });

            return anchorPreview;
        },

        anchorPreviewTemplate: function () {
            return '<div class="bM-editor-toolbar-anchor-preview" id="bM-editor-toolbar-anchor-preview">' +
                '    <i class="bM-editor-toolbar-anchor-preview-inner">http://google.com/</i>' +
                '</div>';
        },

        anchorPreviewClickHandler: function(e) {
            if (this.activeAnchor) {

                var self = this,
                    range = document.createRange(),
                    sel = window.getSelection();

                range.selectNodeContents(self.activeAnchor);
                sel.removeAllRanges();
                sel.addRange(range);
                setTimeout(function() {
                    self.showAnchorForm(self.activeAnchor.href);
                    self.keepToolbarAlive = false;
                }, 100 + self.options.delay);

            }

            this.hideAnchorPreview();
        },

        editorAnchorObserver: function(e) {
            var self = this,
                overAnchor = true,
                leaveAnchor = function() {
                    // mark the anchor as no longer hovered, and stop listening
                    overAnchor = false;
                    self.activeAnchor.removeEventListener('mouseout', leaveAnchor);
                };

            if (e.target && e.target.tagName.toLowerCase() === 'a') {
                // only show when hovering on anchors
                if (this.toolbar.classList.contains('bM-editor-toolbar-active')) {
                    // only show when toolbar is not present
                    return true;
                }
                this.activeAnchor = e.target;
                this.activeAnchor.addEventListener('mouseout', leaveAnchor);
                // show the anchor preview according to the configured delay
                // if the mouse has not left the anchor tag in that time
                setTimeout(function() {
                    if (overAnchor) {
                        self.showAnchorPreview(e.target);
                    }
                }, self.options.delay);


            }
        },

        bindAnchorPreview: function (index) {
            var self = this;
            this.elements[index].addEventListener('mouseover', function(e) {
                self.editorAnchorObserver(e);
            });
            return this;
        },

        setTargetBlank: function () {
            var el = getSelectionStart(),
                i;
            if (el.tagName.toLowerCase() === 'a') {
                el.target = '_blank';
            } else {
                el = el.getElementsByTagName('a');
                for (i = 0; i < el.length; i += 1) {
                    el[i].target = '_blank';
                }
            }
        },

        createLink: function (input) {
            restoreSelection(this.savedSelection);
            document.execCommand('createLink', false, input.value);
            if (this.options.targetBlank) {
                this.setTargetBlank();
            }
            this.showToolbarActions();
            input.value = '';
        },

        bindWindowActions: function () {
            var timerResize,
                self = this;
            this.windowResizeHandler = function () {
                clearTimeout(timerResize);
                timerResize = setTimeout(function () {
                    if (self.toolbar && self.toolbar.classList.contains('bM-editor-toolbar-active')) {
                        self.setToolbarPosition();
                    }
                }, 100);
            };
            window.addEventListener('resize', this.windowResizeHandler);
            return this;
        },

        activate: function () {
            var i;
            if (this.isActive) {
                return;
            }

            if (this.toolbar !== undefined) {
                this.toolbar.style.display = 'block';
            }

            this.isActive = true;
            for (i = 0; i < this.elements.length; i += 1) {
                this.elements[i].setAttribute('contentEditable', true);
            }

            //this.bindWindowActions()
            this.bindSelect();
        },

        deactivate: function () {
            var i;
            if (!this.isActive) {
                return;
            }
            this.isActive = false;

            if (this.toolbar !== undefined) {
                this.toolbar.style.display = 'none';
            }

            document.documentElement.removeEventListener('mouseup', this.checkSelectionWrapper);
            window.removeEventListener('resize', this.windowResizeHandler);

            for (i = 0; i < this.elements.length; i += 1) {
                this.elements[i].removeEventListener('keyup', this.checkSelectionWrapper);
                this.elements[i].removeEventListener('blur', this.checkSelectionWrapper);
                this.elements[i].removeEventListener('paste', this.pasteWrapper);
                this.elements[i].removeAttribute('contentEditable');
            }
        },

        bindPaste: function () {
            var i, self = this;
            this.pasteWrapper = function (e) {
                var paragraphs,
                    html = '',
                    p;

                if (!self.options.forcePlainText) {
                    return this;
                }
                function pasteIe(){
                    var selectedText = document.selection.createRange();
                    if (!self.options.disableReturn) {
                        paragraphs = window.clipboardData.getData('Text').split(/[\r\n]/g);
                        for (p = 0; p < paragraphs.length; p += 1) {
                            if (paragraphs[p] !== '') {
                                html += '<p>' + paragraphs[p] + '</p>';
                            }
                        }
                        selectedText.pasteHTML(html);
                    } else {
                        var paragraph = window.clipboardData.getData('Text').split(/[\r\n]/g);;
                        selectedText.pasteHTML(paragraph);
                    }
                }
                if (navigator.appName == 'Microsoft Internet Explorer'){
                    e.preventDefault();
                    pasteIe();
                    return this;
                }else if (navigator.appName == 'Netscape')
                {
                    var ua = navigator.userAgent;
                    var re  = new RegExp("Trident/.*rv:([0-9]{1,}[\.0-9]{0,})");
                    if (re.exec(ua) != null){
                        pasteIe();
                        return this;
                    }
                }
                if (e.clipboardData && e.clipboardData.getData && !e.defaultPrevented) {
                    e.preventDefault();
                    if (!self.options.disableReturn) {
                        paragraphs = e.clipboardData.getData('text/plain').split(/[\r\n]/g);
                        for (p = 0; p < paragraphs.length; p += 1) {
                            if (paragraphs[p] !== '') {
                                html += '<p>' + paragraphs[p] + '</p>';
                            }
                        }
                        document.execCommand('insertHTML', false, html);
                    } else {
                        document.execCommand('insertHTML', false, e.clipboardData.getData('text/plain'));
                    }
                }
            };
            for (i = 0; i < this.elements.length; i += 1) {
                this.elements[i].addEventListener('paste', this.pasteWrapper);
            }
            return this;
        },

        setPlaceholders: function () {
            var $this = this;
            var i,
                activatePlaceholder = function (el) {
                    if($(el).text()===''){
                        $(el).html($this.options.placeholder).addClass('placeholder');
                    }
                    $(el).focus(function(event) {
                        if($(el).html() === $this.options.placeholder){
                            $(el).html('').removeClass('placeholder');
                        }
                    });
                    $(el).blur(function(event) {
                        if($(el).html() === '' || $(el).html() === '<br>'){
                            $(el).html($this.options.placeholder).addClass('placeholder');
                        }
                    });
                }
            for (i = 0; i < this.elements.length; i += 1) {
                activatePlaceholder(this.elements[i]);
                //this.elements[i].addEventListener('blur', placeholderWrapper);
                //this.elements[i].addEventListener('keypress', placeholderWrapper);
            }
            return this;
        }

    };

}(window, document));
