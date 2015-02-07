//sideBar align
;$.fn.bMalign = function (options) {
	"use strict";
	var defaults = {
		leftStyle:"position:absolute;padding-left:0px;right:auto;",
		rightStyle:"position:absolute;padding-left:12px;right:0px;",
		marginBottom:30
	};
	var settings = $.extend( true, {}, defaults, options ),
		el = $(this),
		$children = el.children(),
		contHeight = el.outerHeight(),
		w = $(window).width(),
		bmAlignOn = false,
		len = $children.length,
		t1, t2, i
	;
	var plugin = {
		init: function () {
			this.build();
			this.resizeWindow();
		},
		build: function () {
			var i;
			if (w < 980 && w > 480) {
				el.css({
					'position': 'relative',
					'height': contHeight
				});
				bmAlignOn = true;
				t1 = $children.eq(0).outerHeight();
				t2 = $children.eq(1).outerHeight();
				for (i = 2; i < len; i++) {
					if(t1 > t2){
						$children.eq(i).css("cssText", settings.rightStyle);
						$children.eq(i).css("top", t2+'px');
						t2 += $children.eq(i).outerHeight();		
					}
					else{
						$children.eq(i).css("cssText", settings.leftStyle);
						$children.eq(i).css("top", t1+'px');
						t1 += $children.eq(i).outerHeight();			
					}
				}
				t1 > t2 ? contHeight = t1 : contHeight = t2;
				el.css('height',contHeight+settings.marginBottom+'px');
			}
		},
		resizeWindow: function () {
			var $this = this
			$(window).on('resize', function () {
				w = $(window).width();
				$this.build();
				$this.destroy();
			});
		},
		destroy: function () {
			if (bmAlignOn && (w >= 980 || w <= 480)) {
				el.add($children).removeAttr('style');
				bmAlignOn = false;
			}
		}
	};
	plugin.init();
	return this;
};





var isTouch = /Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(navigator.userAgent);
//document.createTouch !== undefined || ('ontouchstart' in window) || ('onmsgesturechange' in window) || navigator.msMaxTouchPoints
var site = $('#site');
function enableTouch(){
	if(isTouch){
		var site = $('#site');
		var distance,
		swipeThreshold = 10,
		startCoords = {}, 
		endCoords = {};					
		$('.sub_headder').bind('touchstart', function(e){
			$('.sub_headder').addClass('touchNav');
			endCoords = e.originalEvent.targetTouches[0];
			startCoords.pageX = e.originalEvent.targetTouches[0].pageX;
			$('.touchNav').bind('touchmove',function(e){
				e.preventDefault();
				e.stopPropagation();
				endCoords = e.originalEvent.targetTouches[0];
			});
					
			return false;

			}).bind('click touchend',function(e){
				e.preventDefault();
				e.stopPropagation();
				distance = endCoords.pageX - startCoords.pageX;
				if( distance >= swipeThreshold ){
					$("#mast-head").css('display','block');	
					site.addClass('translate');	
					
				}
				else if( distance <= - swipeThreshold ){
					if(site.hasClass('translate')){
						site.removeClass('translate');
						setTimeout(function(){
							$("#mast-head").css('display','none');	
						},350);
					}
				}
				$('.touchNav').off('touchmove').removeClass('touch');
			
		});		
	}
	
};
function setnavHeight(){
	if(isTouch){
		var navbarHeight = $(window).height();
		$('.navbar').css('height',navbarHeight);
	}
};
$(document).ready(function(e) {
	var site = $('#site');
	setnavHeight();
	$(window).on('orientationchange', function(event) {
		setnavHeight()
	});
   enableTouch();
	$('.btn-navbar').on('click touchend',function(){
		if(site.hasClass('translate')){
			site.removeClass('translate');	
			setTimeout(function(){
				$("#mast-head").css('display','none');	
			},350);	
		}else{
			$("#mast-head").css('display','block');	
			site.addClass('translate');		
		}
	});
	$(window).on("resize orientationchange", function(){
		if($(window).width() > 979){
			$("#mast-head").css('display','block');	
			site.removeClass('translate');
		}else if(!site.hasClass('translate')){
			$("#mast-head").css('display','none');		
		}
	});
});
;$.fn.changeText = function( options ) {
	"use strict";
	var defaults = $.extend({
		dT: 'Follow Question',
		fT: 'Following',
		sT: 'Unfollow',
		icon: true,
		aCl:  'bUi-iCn-oK-16',
		bCl:  'bUi-iCn-rMv-12'
	}, options );
	var settings = $.extend( true, {}, defaults, options ), cL = false, w;
	$(this).each(function(index, element) {
		$(this).on('click',function(){
				if(cL==false){
					$(this).text(settings.fT);
					if(settings.icon == true){
						$(this).find('[class^="bUi-iCn-"]').remove();
						$(this).prepend('<i class="'+settings.aCl+' mRr5 fS12" aria-hidden="true"></i>')
					}
					w = $(this).width();
					$(this).css({'transition':'none','width':w});
					cL = true;
				}
				else{
						$(this).css('width','auto');
						$(this).text(settings.dT);
						if(settings.icon == true){
							$(this).find('[class^="bUi-iCn-"]').remove();
						}
						cL = false;		
					}
			});
		$(this).on('mouseover',function(){
				if(cL==true){
						$(this).text(settings.sT);	
						if(settings.icon == true){
							$(this).find('[class^="bUi-iCn-"]').remove();
							$(this).prepend('<i class="'+settings.bCl+' mRr5 fS11" aria-hidden="true"></i>')
						}	
					}
			})	
		$(this).on('mouseout',function(){
				if(cL==true){
						$(this).text(settings.fT);	
						if(settings.icon == true){
							$(this).find('[class^="bUi-iCn-"]').remove();
							$(this).prepend('<i class="'+settings.aCl+' mRr5 fS12" aria-hidden="true"></i>')
						}	
					}	
			})
    });
	return this;
};

// more menu
;$.fn.moreNav = function( options ) {
	"use strict";
	var defaults = $.extend({
		html : '<li id="more" class="dropdown">\
                	<div class="rLvE">\
						<a href="#" class="dropdown-toggle">More<b class="caret"></b></a>\
                        <ul class="dropdown-menu pLrT more"></ul>\
				</div>',
		maxWidth:1200,
		minWidth:980	
	}, options );
	var settings = $.extend( true, {}, defaults, options ),$this = $(this),w, mW,flag = false,des=false, newW=settings.maxWidth,dRcHw=0;
	var plugin = {
			init: function(){
					plugin.resizeWindow();
					$(window).on('resize', function(){setTimeout(function(){
						plugin.resizeWindow()	
					},350);	});
				},
			resizeWindow : function(){
					w = $(window).width(); 
					mW = $this.width();
					if((w >= settings.maxWidth) && (mW>settings.maxWidth)){
								plugin.build();

						}
					else if(w <= mW){
							plugin.build();	
						}
					else if((w>settings.minWidth && w<mW) && (des==true && flag==false)){
							plugin.build();
						}
					else if((newW+dRcHw)<=mW){
							plugin.rebuild();
						};
					if(w<settings.minWidth)
						plugin.destroy();
				},
			build: function(){
				var lEn = $this.children().length;
				var lW=100, mN=0, oVcH;
				for(var i=0;i<lEn-1;i++){
						lW += $this.children().eq(i).width();
						if (lW>=mW || lW>=settings.maxWidth)
							break;
						mN = i;
					}
				mN = mN-1;
				oVcH = $this.children().eq(mN).nextUntil($this.children().eq(lEn-1));
				if(flag==false){
						var lCh = $this.children().eq(lEn-1);
						$this.children().eq(lEn-1).after(settings.html);	
						$this.find('.more').html(lCh)
						flag = true;
					}
				dRcHw = $this.children().eq(lEn-2).outerWidth();
				$this.find('.more').prepend(oVcH);
				newW = $this.width();
			},
			rebuild: function(){
				if($this.find('.more').children().length>1){
					var lEn = $this.children().length;
					var dRfC = $this.find('.more').children().eq(0);
					$this.children().eq(lEn-1).before(dRfC);
					newW = newW+dRcHw;
				}
				else{
						plugin.destroy();
						newW = $this.width();	
					}
			},
			destroy: function(){
				if(flag == true){
					var addedCh = $this.find('.more').children();
					$this.append(addedCh);
					$this.find('#more').remove();
					des=true;
					flag=false;
				}	
			}
		};
	plugin.init();
	
	return this;
};
 
$.fn.doThis = function(func){
	this.length && func.apply(this);
	return this;
}

//addClass to parent
$.fn.addCl = function(cl){
	$(this).click(function(){
		$(this).parent().addClass(cl);
	})
	return this;
}
//Responsive image width
$.fn.setrSpVWidth = function(w){
	$(this).each(function(index, element) {
    	var fLxcOnTWidth =	$(this).width();
		$(this).find('img').css('width',fLxcOnTWidth+1+w);    
    });
	return this;
}
//Responsive Video size
$.fn.fLxVideoWidth = function(w,h){
	$(this).each(function(index, element) {
		var r = w/h;
    	var fLxVideoW =	$(this).width();
		var height = fLxVideoW/r;
		$(this).find('iframe').css({'width':fLxVideoW+1,'height':height});    
    });
	return this;
}
//Featured textblock height
$.fn.setfTrDtXtHeight = function(){
	$(this).each(function(){
		if($(this).hasClass('aDpTv') && !$(this).hasClass('tXt-oTsD')){
			aDpTvHeight = $(this).height();
			$(this).find('.fTrD-tXt').css('height',aDpTvHeight);     	
		}	
	})	
	return this;
}
//Responsive image height
$.fn.setrSpVHeight = function(mDaLt){
	var w = $(window).width();
	$(this).each(function(index, element) {
        var fLxcOnTWidth =	$(this).height();
		$(this).find('img').css('height',fLxcOnTWidth+1); 
    });	
	/** /
	$('.'+mDaLt+'').find($(this)).each(function(index, element) {
		if(w<=480){
			var fLxcOnTWidth =	$(this).width();
			$(this).find('img').css({'width':fLxcOnTWidth+1,'height':'auto'});	
		}
		else $(this).find('img').css('width','auto');   
	});
	/**/
	return this;
}


//	toggleClass
$.fn.classToggle = function(){
	$(this).click(function(){
		$(this).toggleClass('active');
	})
	return this;
}
// toggleClassParent;
$.fn.classTogglep = function(){
	$(this).click(function(){
		$(this).parent().toggleClass('active');
	})
	return this;
}

//	toggleicon
$.fn.iconToggle = function(){
	
	$(this).each(function(index, element) {
        var cLlT = $(this).find('[class^="bUi-iCn-"]:last').attr('class').split(/\s+/), oC,	nC = $(this).attr('data-toggle-icon');
		for (var i = 0; i < cLlT.length; i++) {
		   if (cLlT[i].match(/bUi-iCn-/i)) {
			   oC = cLlT[i];
		   }
		};
		var oB = $(this).find('[class^="bUi-iCn-"]:last');
		$(this).click(function(){
			oB.toggleClass(oC);
			if(oB.hasClass(oC))
				oB.removeClass(nC);
				else
					oB.addClass(nC);
		})
    });
	return this;
}

$.fn.collapseM480 = function(){
	var w = $(window).width();
	var el = $(this).attr('data-target');
	if(w <= 480){ 
		if($(el).hasClass('in')) $(el).removeClass('in');
	}
	else {
		if(!$(el).hasClass('in')) $(el).addClass('in');
		$(el).removeAttr('style');
	}
	return this;
}




//	Fold
$.fn.fold = function(){
	var w = $(window).width();
	el = $(this).parent().find('.fLdED');
	if(w <= 480){
		if(el.height() > 200) el.addClass('on',300);	
	}
	else el.removeClass( "on", 300);	
	$(window).on("resize orientationchange", (function () {
			w = $(window).width();	
			if(w <= 480){
				if(el.height() > 200) el.addClass('on',300);	
			}
			else el.removeClass('on',300);		
				
		}))
	$(this).click(function(){
			el.toggleClass('on',300);
			if(!el.hasClass('on'))$(this).find('a').html('Read Less <i class="bUi-iCn-aNg-t-12" aria-hidden="true"></i>');
			else $(this).find('a').html('Read More <i class="bUi-iCn-aNg-b-12" aria-hidden="true"></i>')
		})
	return this;
}

// textarea focus
$.fn.autoFocus = function(){
	$(this).focus(function(){
		$(this).closest('form').addClass('hS-fCs');
	})
	return this;
}

// textarea autoExpand
$.fn.autoExpand = function(){
	var $ta=this,$clone,timer=null,mh=70;

	function resize(){
		var h = $clone.val($ta.val()+'\n').get(0).scrollHeight;
		$ta.css('height', (h<mh)?'':h+18);
	};

	function onkeydown(event){
		this.scrollTop = 0;
		clearTimeout(timer);
		timer = setTimeout(resize,50);
	};

	if($clone) $clone.remove();
	$clone = $ta.clone().removeAttr('id').removeAttr('name').css({padding:0,margin:0}).addClass('cLn').attr('tabindex','-1').insertAfter($ta);

	$ta.css('overflow','hidden').off('keydown.expand').on('keydown.expand',onkeydown);

	return $ta;
};



//rSpV image
/** /
function setrSpVWidth(){
	var fLxiMg = $('.fLxiMgW');
	fLxiMg.each(function(index, element) {
		fLxcOnTWidth =	$(this).width();
		$(this).find('img').css('width',fLxcOnTWidth+1);
	});
}
/**/



$(function() { 
	//switch 
	$("[data-toggle='switch']").doThis(function(){
		this.wrap('<div class="switch" />').parent().bootstrapSwitch();
	});
	
	//tags
	$(".tagsinput").doThis(function(){
		this.tagsInput();;
	});
	
	$("[data-toggle='popover']").doThis(function(){
		this.popover();
	});

	$('.sD-bR').bMalign();	
	$('#moreNav').moreNav();
	$('[data-toggle-class]').doThis(function(){
		this.classToggle();	//active	
	});
	$('[data-toggle-class-p]').doThis(function(){
		this.classTogglep();	//active	
	});
	$('.fLd-bTn').doThis(function(){
		this.fold();
	});
	$('[data-expand="true"]').doThis(function(){
		this.autoExpand();
	});
	$('[data-focus="true"]').doThis(function(){
		this.autoFocus();
	});
	
	//select menu
	$('.bM-sLt').doThis(function(){
		this.bUiSlCt();
	});
	$('.uSr-aCnT-sLt').doThis(function(){
		this.bUiSlCt({style: 'btn-light vP'});
	});
	$('.bUiSlCt').doThis(function(){
		this.bUiSlCt({style: ''});
	});
	$('.bUiSlCt-wHt').doThis(function(){
		this.bUiSlCt({style: 'btn-light'});
	});
	$('.bUiSlCtbtn-light').doThis(function(){
		this.bUiSlCt({style: 'btn-light btn-small pLrT'});
	});
	$('.discussion').doThis(function(){
		this.bUiSlCt({style: 'btn-light vP pLlTp w100pP h38p tEx-aLl'});
	});
	$('.bTn-lT-sLcT').doThis(function(){
		this.bUiSlCt({style: 'btn-light w100P h40 tXt-lT bXShD0'});
	});
	$('.bUiSlCtbtn-link').doThis(function(){
		this.bUiSlCt({style: 'btn-link'});
	});
	$('.sLcFlTr').doThis(function(){
		this.bUiSlCt({style: 'btn-link, w100P tXt-lT fS11 fW-bLd'});
	});
	
	$('.tBlbUiSlCtbtn-light').doThis(function(){
		this.bUiSlCt({style: 'btn-light btn-small'});
	});
	
	
	$('[data-toggle-icon]').doThis(function(){
		this.iconToggle();
	});
	$('.browse').doThis(function(){
		this.collapseM480();
	});
	$('.sHw-sRcH').doThis(function(){
		this.addCl('eXpD');
	});
	$('#fLw_btn').doThis(function(){
		this.changeText();
	});
	
	
	
	
	
	
    
    
    
    
	

	
	//Responsive menu
	// 		/**/on!		/** / off!
	/**/

	/** /
	if( /Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(navigator.userAgent) ) {
		$(function() {		
			$("#mast-head").swipe( {
				swipe:function(event, direction) {
					if(direction == "left"){
						site.removeClass('translate');	
						setTimeout(function(){
							$("#mast-head").css('display','none');	
						},350);
					}
				},
			   threshold:0,
			   allowPageScroll:"vertical"
			});
			
			$(".sub_headder").swipe( {
				swipe:function(event, direction) {
					if(direction == "right"){
						$("#mast-head").css('display','block');	
						site.addClass('translate');	
					}
					if(direction == "left"){
						if(site.hasClass('translate')){
							site.removeClass('translate');
							setTimeout(function(){
								$("#mast-head").css('display','none');	
							},350);
						}
					}
				},
			   threshold:0,
			});
		});
		function setnavHeight(){
			var navbarHeight = $(window).height();
			$('.navbar').css('height',navbarHeight);
		}
		setnavHeight();
		$(window).on('orientationchange', function(event) {
			setnavHeight()
		});
				
	}
	/** //**/
	
	//views
	/*
	var views = $('#views');
	var figureItems = $('.main').find('.figure-items');
	views.on('click', '.list-view', function() {
		views.find('i').removeClass('active');
		$(this).addClass('active');
		figureItems.removeClass('grid');
	});
	views.on('click', '.grid-view', function() {
		views.find('i').removeClass('active');
		$(this).addClass('active');
		figureItems.addClass('grid');
	});
	*/
	
	
	//rSpV image
	
	$('.fLxiMgW').setrSpVWidth(0);
	$('.fLxiMgW30').setrSpVWidth(30);
	$('.fLxiMgH').setrSpVHeight('mDa-lT');
	$('.fLxVdO').doThis(function(){
		this.fLxVideoWidth(560,315);
	});
	$('.fTrD-bL').setfTrDtXtHeight();
	
	/** /
	setTimeout(function(){
	      setrSpVWidth();
	      setrSpVHeight()
	},200);
	/**/
	$(window).load(function(){
		$('.sD-bR').bMalign();	
	});
	$(window).on("resize orientationchange", (function () {
		$('.fLxiMgW').setrSpVWidth(0);
		$('.fLxiMgW30').setrSpVWidth(30);
	  	$('.fLxiMgH').setrSpVHeight('mDa-lT');
		$('.fLxVdO').doThis(function(){
			this.fLxVideoWidth(560,315);
		});
		$('.fTrD-bL').setfTrDtXtHeight();
		$('.browse').doThis(function(){
			this.collapseM480();
		});
		$('.fTrDfLxiMgH').setrSpVHeight('fTrD-bL');
			
	}))
	
	
	//views
	var views = $('#media-toggle');
	var figureItems = $('.main').find('.modulesBrowseData');
	var thumbnaiItem = $('.modulesBrowseData').find('.mDa-oT');
	
	
	function setGridColumn(){		
		$('.mDa-gD').each(function(index, element) {
			if(!$(this).hasClass('dSgDwDt')){
				var gridColumnWidth = $(this).find('.mDa').width();
				$(this).find('.mDa .mDa-oT').css({'width':''+gridColumnWidth+'','height':'auto'}); 
			}
        });	
	}
	views.on('click', '.c-lT', function() {
		views.find('.btn').removeClass('active');
		$(this).addClass('active');
		figureItems.removeClass('mDa-gD mDa-oT-tP').addClass('mDa-lT mDa-oT-lT');
		if(figureItems.children('li').hasClass('mDa-gRp')){
			figureItems.find('.mDa-gRp > ul').removeClass('pDfX')
		}
		else{
				figureItems.removeClass('pDfX');	
			}
		thumbnaiItem.css('width','auto');
		$('.fLxiMgH').setrSpVHeight('mDa-lT');
		$('.fLxiMgW').setrSpVWidth(0);
		$('.fLxiMgW30').setrSpVWidth(30);
	});
	views.on('click', '.c-gD', function() {
		views.find('.btn').removeClass('active');
		$(this).addClass('active');
		figureItems.removeClass('mDa-lT mDa-oT-lT').addClass('mDa-gD mDa-oT-tP');
		if(figureItems.children('li').hasClass('mDa-gRp')){
			figureItems.find('.mDa-gRp > ul').addClass('pDfX')
		}
		else{
				figureItems.addClass('pDfX');	
			}
		$('.fLxiMgH').setrSpVHeight('mDa-lT');
		$('.fLxiMgW').setrSpVWidth(0);
		$('.fLxiMgW30').setrSpVWidth(30);
		setGridColumn();
	});
	setGridColumn();
	
	
	$(window).on("resize orientationchange", (function () {
		setGridColumn();			
	}))
		  
	
	
	
	
});