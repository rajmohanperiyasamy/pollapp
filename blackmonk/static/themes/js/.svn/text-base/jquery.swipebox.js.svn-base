
;(function (window, document, $, undefined) {
	
	$.swipebox = function(elem, options) {
		"use strict";
		var defaults = {
			useCSS : true,
			easing: 'cubic-bezier(0.25, 0, 0.25, 1)',
			removeCaption:false,
			thumbPager: true,
			exThumbImage: false,
			fade:true,
			speed: 600,
			videomaxWidth : 1140,
			vimeoColor : 'CCCCCC',
			videoAutoplay:true,
			openOneSlide:false
		},
		
			plugin = this,
			$elem = $(elem),
			selector = elem.selector,
			$selector = $(selector),
			flag,
			bMGallery,
			slider,
			slide,
			prev,
			next,
			index,
			slectedIndex,
			isTouch = document.createTouch !== undefined || ('ontouchstart' in window) || ('onmsgesturechange' in window) || navigator.msMaxTouchPoints,
			html = '<div id="bM-Gallery"><div id="flexBox-slider"></div><div id="flexBox-caption"></div><div id="flexBox-close" class="close"><i aria-hidden="true" class="bUi-iCn-rMv-16"></i></div><div id="flexBox-action"><a id="flexBox-prev"></a><a id="flexBox-next"></a></div></div>';
			

		plugin.settings = {};

		plugin.init = function(){

			plugin.settings = $.extend({}, defaults, options);
			
			$selector.click(function(e){
				flag = true;
				e.preventDefault();
				e.stopPropagation();
				if(plugin.settings.openOneSlide == true)
					$elem = $(this);
				index = $elem.index($(this));
				if(plugin.settings.openOneSlide == true)
					index = 0;
				slectedIndex = $elem.index($(this));
				ui.target = $(e.target);
				ui.init(index);
			});
		};

		var ui = {

			init : function(index){
				this.target.trigger('flexBox-start');
				this.build();
				this.pReloadImg(index);
				this.openSlide(index);
				this.loadImg(index);
				//this.preloadImg(index+1);
				//this.preloadImg(index-1);
			},

			build : function(){
				var $this = this;
				
				$('body').append(html);
				bMGallery = $('#bM-Gallery');
				slider = bMGallery.find('#flexBox-slider');
				prev = bMGallery.find('#flexBox-prev');
				next = bMGallery.find('#flexBox-next');
				if($this.doCssTrans() && !plugin.settings.fade){
					slider.css({
						'-webkit-transition' : 'left '+plugin.settings.speed+'ms '+plugin.settings.easing+'',
						'-moz-transition' : 'left '+plugin.settings.speed+'ms '+plugin.settings.easing+'',
						'-o-transition' : 'left '+plugin.settings.speed+'ms '+plugin.settings.easing+'',
						'-khtml-transition' : 'left '+plugin.settings.speed+'ms '+plugin.settings.easing+'',
						'transition' : 'left '+plugin.settings.speed+'ms '+plugin.settings.easing+''
					});
					bMGallery.css({
						'-webkit-transition' : 'opacity 1s ease',
						'-moz-transition' : 'opacity 1s ease',
						'-o-transition' : 'opacity 1s ease',
						'-khtml-transition' : 'opacity 1s ease',
						'transition' : 'opacity 1s ease'
					});
				}

				$this.setDim();
				$this.actions();
				$this.keyboard();
				$this.gesture();

				$(window).resize(function() {
					$this.setDim();
				}).resize();
			},

			setDim : function(){
				var sliderCss = {
					width : $(window).width(),
					height : window.innerHeight ? window.innerHeight : $(window).height() // fix IOS bug
				};

				$('#bM-Gallery').css(sliderCss);

			},

			supportTransition : function() {
				var transition = 'transition WebkitTransition MozTransition OTransition msTransition KhtmlTransition'.split(' ');
				var div = document.createElement('div');
				for(var i = 0; i < transition.length; i++) {
					if(div.style[transition[i]] !== undefined) {
						return transition[i];
					}
				}
				return false;
			},

			doCssTrans : function(){
				if(plugin.settings.useCSS && this.supportTransition() ){
					return true;
				}
			},

			gesture : function(){
				if ( isTouch ){
					var $this = this,
					distance = null,
					swipMinDistance = 10,
					startCoords = {}, 
					endCoords = {};
					var b = $('#flexBox-caption, #flexBox-action');

					
					$('body').bind('touchstart', function(e){

						$(this).addClass('touching');
		  				endCoords = e.originalEvent.targetTouches[0];
		    			startCoords.pageX = e.originalEvent.targetTouches[0].pageX;
						$('.touching').bind('touchmove',function(e){
							e.preventDefault();
							e.stopPropagation();
		    				endCoords = e.originalEvent.targetTouches[0];

						});
			           			
			           	return false;

	           			}).bind('touchend',function(e){
	           				e.preventDefault();
							e.stopPropagation();
	   				
	   						distance = endCoords.pageX - startCoords.pageX;
	       				
	       					if( distance >= swipMinDistance ){
	       					// swipeLeft
	       						$this.getPrev();
	       					}

	       					else if( distance <= - swipMinDistance ){
	       						// swipeRight
	       						$this.getNext();
	       				
	       					}

	       					$('.touching').off('touchmove').removeClass('touching');
						
					});

           			}
			},
			
			clearTimeout: function(){	
				window.clearTimeout(this.timeout);
				this.timeout = null;
			},

			keyboard : function(){
				var $this = this;
				$(window).bind('keyup', function(e){
					e.preventDefault();
					e.stopPropagation();
					if (e.keyCode == 37){
						$this.getPrev();
					}
					else if (e.keyCode==39){
						$this.getNext();
					}
					else if (e.keyCode == 27) {
						$this.closeSlide();
					}
				});
			},

			actions : function(){
				var $this = this;
				
				if( $elem.length < 2 ){
					prev.add(next).remove();
				}else{
					prev.bind('click touchend', function(e){
						e.preventDefault();
						e.stopPropagation();
						$this.getPrev();
					});
					
					next.bind('click touchend', function(e){
						e.preventDefault();
						e.stopPropagation();
						$this.getNext();
					});
				}

				$('#flexBox-close').bind('click touchend', function(e){
					e.preventDefault();
					e.stopPropagation();
					$this.closeSlide();
				});
			},
			
			setSlide : function (index, isFirst){
				isFirst = isFirst || false;
				if(!plugin.settings.fade){
					if(this.doCssTrans()){
						slider.css({ left : (-index*100)+'%' });
					}else{
						slider.animate({ left : (-index*100)+'%' });
					}
				}
				if(plugin.settings.fade){
					if(flag){
						slide.css({'position':'absolute','left':'0'});
						slider.find('.video_cont').css('max-width',plugin.settings.videomaxWidth+'px');
						if(this.doCssTrans()){
							slide.css({
								'-webkit-transition' : 'opacity '+plugin.settings.speed+'ms ease',
								'-moz-transition' : 'opacity '+plugin.settings.speed+'ms ease',
								'-o-transition' : 'opacity '+plugin.settings.speed+'ms ease',
								'-khtml-transition' : 'opacity '+plugin.settings.speed+'ms ease',
								'transition' : 'opacity '+plugin.settings.speed+'ms ease'
							});
							slide.css('opacity','0');
							slide.eq(slectedIndex).css('opacity','1');
						}
						else{
								slide.fadeOut(100);
								slide.eq(slectedIndex).fadeIn(100);
							}
					}
					else{
						if(this.doCssTrans()){
							$('#flexBox-slider .slide.current').css('opacity','0');
							slide.eq(index).css('opacity','1');;
						}
						else{
								$('#flexBox-slider .slide.current').fadeOut(plugin.settings.speed);
								slide.eq(index).fadeIn(plugin.settings.speed);
							}
					}
					flag = false;		
				}
				$('#flexBox-slider .slide.current').removeClass('current');
				slide.eq(index).addClass('current');
				$('#bM-Gallery .thumb').removeClass('active');
				$('#bM-Gallery .thumb').eq(index).addClass('active');
				this.setTitle(index);

				if( isFirst ){
					slider.fadeIn();
				}
				prev.add(next).removeClass('disabled');
				if(index == 0){
					prev.addClass('disabled');
				}else if( index == $elem.length - 1 ){
					next.addClass('disabled');
				}
			},
		
			openSlide : function (index){
				
				$('html').addClass('flexBox');
				$(window).trigger('resize'); // fix scroll bar visibility on desktop
				this.createThumbPager();
				this.setSlide(index, true);
			},
			/** /
			preloadImg : function (index){
				var $this = this;
				setTimeout(function(){
					//$this.openImg(index);
				}, 1000);
			},
			/**/
			/** /
			openImg : function (index){
				var $this = this;
				if(index < 0 || index >= $elem.length){
					return false;
				}

				$this.loadImg($elem.eq(index).attr('href'), function(){
					$('#swipebox-slider .slide').eq(index).html(this);
				});
			},
			/**/


			setTitle : function(index, isFirst){
				$('#flexBox-caption').empty();
				
				if($elem.eq(index).attr('title')){
					$('#flexBox-caption').append($elem.eq(index).attr('title'));
				}
				if(plugin.settings.removeCaption == true) $('#flexBox-caption').remove();
			},
			
			isVideo : function (src){

				if( src ){
					if( 
						src.match(/youtube\.com\/watch\?v=([a-zA-Z0-9\-_]+)/) 
						|| src.match(/vimeo\.com\/([0-9]*)/) 
					){
						return true;
					}
				}
					
			},

			getVideo : function(url,a,_id){
				var iframe = '';
				var output = '';
				var youtubeUrl = url.match(/watch\?v=([a-zA-Z0-9\-_]+)/);
				var vimeoUrl = url.match(/vimeo\.com\/([0-9]*)/);
				if( youtubeUrl ){
					if(plugin.settings.videoAutoplay == true && a == true)
						a = '?autoplay=1&rel=0&wmode=opaque';		
					else
						a = '?wmode=opaque';	
							
					iframe = '<iframe id="video'+_id+'" width="560" height="315" src="//www.youtube.com/embed/'+youtubeUrl[1]+a+'" frameborder="0" allowfullscreen></iframe>';	
									
				}else if(vimeoUrl){
					if(plugin.settings.videoAutoplay == true && a == true)
						a = 'autoplay=1&amp;';		
					else
						a = '';	
					
					iframe = '<iframe id="video'+_id+'" width="560" height="315"  src="http://player.vimeo.com/video/'+vimeoUrl[1]+'?'+a+'byline=0&amp;portrait=0&amp;color='+plugin.settings.vimeoColor+'" frameborder="0" webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe>';
				
				}
				return '<div class="video_cont"><div class="video">'+iframe+'</div></div>';
			},
			
			pReloadImg : function (index){
				/** /
				var img = $('<img>').on('load', function(){
					callback.call(img);
				});
				/**/
				//var eQ = 0;
				//alert($elem.length);
				var slideList = '';
				$elem.each(function() {
					slideList += '<div class="slide"></div>'
				});
				slider.append(slideList);
				slide = bMGallery.find('.slide');
				/** /
				$elem.each(function() {
					var src = $(this).attr('href');
					slider.append('<div class="slide"><img src="'+src+'" /></div>');
				});
				/**/
			},
			loadImg : function (index){
				/** /
				var img = $('<img>').on('load', function(){
					callback.call(img);
				});
				/**/
				//var eQ = 0;
				//alert($elem.length);
				var $this = this;
				var i,j,ob,l= $elem.length - index;
				var src = $elem.eq(index).attr('href');
				if(!$this.isVideo(src)){ 
					slider.find('.slide').eq(index).html('<img src="'+src+'" />');
					ob = $('img');
				}
				else{
						slider.find('.slide').eq(index).html($this.getVideo(src,true,index));
						ob = $('iframe');
					}
				slider.find('.slide').eq(index).find(ob).on('load',function(){
					for (i=0; i<=index-1; i++){ 
						var src = $elem.eq(index-i-1).attr('href');
						//alert($elem.eq(index-i-1).html())
						if(!$this.isVideo(src)){ 
							slider.find('.slide').eq(index-i-1).html('<img src="'+src+'" />');
							//slider.prepend('<div class="slide"><img src="'+src+'" /></div>');
						}
						else{
								slider.find('.slide').eq(index-i-1).html($this.getVideo(src,false,index-i-1));
							}
					}
					for (j=1; j<l; j++){
						var src = $elem.eq(index+j).attr('href');
						//alert('jjjjj'+$elem.eq(index+j).html())
						if(!$this.isVideo(src)){
							slider.find('.slide').eq(index+j).html('<img src="'+src+'" />')
							//slider.append('<div class="slide"><img src="'+src+'" /></div>');
						}
						else{
								slider.find('.slide').eq(index+j).html($this.getVideo(src,false,index+j));
								//slider.append($this.getVideo(src));	
							}
					}
				})
				/** /
				var $this = this;
				var i,j,l= $elem.length - index;
				for (i=0; i<=index; i++){ 
					var src = $elem.eq(index-i).attr('href');
					if(!$this.isVideo(src)){ 
						slider.prepend('<div class="slide"><img src="'+src+'" /></div>');
					}
					else{
							slider.prepend($this.getVideo(src));
						}
				}
				for (j=1; j<l; j++){
					var src = $elem.eq(index+j).attr('href');
					if(!$this.isVideo(src)){
						slider.append('<div class="slide"><img src="'+src+'" /></div>');
					}
					else{
							slider.append($this.getVideo(src));	
						}
				}
				/**/
				/** /
				$elem.each(function() {
					var src = $(this).attr('href');
					slider.append('<div class="slide"><img src="'+src+'" /></div>');
				});
				/**/
			},
			
			getNext : function (){
				var $this = this;
				index = slide.index($('#flexBox-slider .slide.current'));
				if(index+1 < $elem.length){
					index++;
					$this.setSlide(index);
					//$this.preloadImg(index+1);
				}
				else{
					if(!plugin.settings.fade){
						slider.addClass('rightSpring');
						setTimeout(function(){
							slider.removeClass('rightSpring');
						},500);
					}
					else $('#bM-Gallery').find('.pager_cont').addClass('open');
				}
			},
			
			getPrev : function (){
				var $this = this;
				index = slide.index($('#flexBox-slider .slide.current'));
				if(index > 0){
					index--;
					$this.setSlide(index);
					//$this.preloadImg(index-1);
				}
				else{
					if(!plugin.settings.fade){					
						slider.addClass('leftSpring');
						setTimeout(function(){
							slider.removeClass('leftSpring');
						},500);
					}
					else $('#bM-Gallery').find('.pager_cont').addClass('open');
				}
			},
			
			createThumbPager: function(){
				if(plugin.settings.thumbPager && $elem.length > 1){
					var $this = this;
					bMGallery.append('<div class="pager_cont"><div class="pager_info"><span class="close ib"><i class="bUi-iCn-rMv-16" aria-hidden="true"></i></span></div><div class="pager"></div></div>');
					prev.after('<a class="cLpager"></a>');
					bMGallery.find('.cLpager').bind('click touchend', function(e){
						bMGallery.find('.pager_cont').addClass('open');		
					});
					bMGallery.find('.close').bind('click touchend', function(e){
						bMGallery.find('.pager_cont').removeClass('open');		
					});
					var pagerInfo = bMGallery.find('.pager_info');
					var pager = bMGallery.find('.pager');
					var thumbList = '';
					var thumbImg;
					$elem.each(function() {
						if(plugin.settings.exThumbImage == false){
								thumbImg = $(this).find('img').attr('src');	
							}
							else{
									thumbImg = $(this).attr(plugin.settings.exThumbImage);	
								}
                    	thumbList += '<div class="thumb"><img src="'+thumbImg+'" /></div>';
                    });	
					pager.append(thumbList);
					var thumb = pager.find('.thumb');
					thumb.bind('click touchend', function(e){
						var index = $(this).index();
						thumb.removeClass('active');
						$(this).addClass('active');
						$this.setSlide(index);
					});	
					pagerInfo.prepend('<span class="ib count">All photos ('+thumb.length+')</span>');
				}
				
			},

			closeSlide : function (){
				var $this = this;
				$(window).trigger('resize');
				$('html').removeClass('flexBox');
				$this.destroy();
			},

			destroy : function(){
				var $this = this;
				$(window).unbind('keyup');
				$('body').unbind('touchstart');
				$('body').unbind('touchmove');
				$('body').unbind('touchend');
				slider.unbind();
				$('#bM-Gallery').remove();
				$elem.removeData('_flexBox');
				$this.target.trigger('flexBox-destroy');
 			}

		};

		plugin.init();
		
	};

	$.fn.swipebox = function(options){
		if (!$.data(this, "_flexBox")) {
			var swipebox = new $.swipebox(this, options);
			this.data('_flexBox', swipebox);
		}
	}

}(window, document, jQuery));
