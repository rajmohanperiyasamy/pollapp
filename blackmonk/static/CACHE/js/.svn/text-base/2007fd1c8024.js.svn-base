$(document).ready(function(){$(document).ajaxSend(function(event,xhr,settings){function getCookie(name){var cookieValue=null;if(document.cookie&&document.cookie!=''){var cookies=document.cookie.split(';');for(var i=0;i<cookies.length;i++){var cookie=jQuery.trim(cookies[i]);if(cookie.substring(0,name.length+1)==(name+'=')){cookieValue=decodeURIComponent(cookie.substring(name.length+1));break;}}}
return cookieValue;}
function sameOrigin(url){var host=document.location.host;var protocol=document.location.protocol;var sr_origin='//'+host;var origin=protocol+sr_origin;return(url==origin||url.slice(0,origin.length+1)==origin+'/')||(url==sr_origin||url.slice(0,sr_origin.length+1)==sr_origin+'/')||!(/^(\/\/|http:|https:).*/.test(url));}
function safeMethod(method){return(/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));}
if(!safeMethod(settings.type)&&sameOrigin(settings.url)){xhr.setRequestHeader("X-CSRFToken",getCookie('csrftoken'));}});});function preuploadjs(scripts,initapp){var totalscripts=0;var executeWhenDone=function()
{this.callback=initapp;this.addDone=function(){totalscripts=totalscripts+1;if(totalscripts===scripts.length)
{this.callback();}};return this;};var listenerdone=executeWhenDone();for(var i=0;i<scripts.length;i++){$.getScript(scripts[i],function(){listenerdone.addDone();});}}
!function($){"use strict";$(function(){$.support.transition=(function(){var transitionEnd=(function(){var el=document.createElement('bootstrap'),transEndEventNames={'WebkitTransition':'webkitTransitionEnd','MozTransition':'transitionend','OTransition':'oTransitionEnd otransitionend','transition':'transitionend'},name
for(name in transEndEventNames){if(el.style[name]!==undefined){return transEndEventNames[name]}}}())
return transitionEnd&&{end:transitionEnd}})()})}(window.jQuery);!function($){"use strict";var Button=function(element,options){this.$element=$(element)
this.options=$.extend({},$.fn.button.defaults,options)}
Button.prototype.setState=function(state){var d='disabled',$el=this.$element,data=$el.data(),val=$el.is('input')?'val':'html'
state=state+'Text'
data.resetText||$el.data('resetText',$el[val]())
$el[val](data[state]||this.options[state])
setTimeout(function(){state=='loadingText'?$el.addClass(d).attr(d,d):$el.removeClass(d).removeAttr(d)},0)}
Button.prototype.toggle=function(){var $parent=this.$element.closest('[data-toggle="buttons-radio"]')
$parent&&$parent.find('.active').removeClass('active')
this.$element.toggleClass('active')}
var old=$.fn.button
$.fn.button=function(option){return this.each(function(){var $this=$(this),data=$this.data('button'),options=typeof option=='object'&&option
if(!data)$this.data('button',(data=new Button(this,options)))
if(option=='toggle')data.toggle()
else if(option)data.setState(option)})}
$.fn.button.defaults={loadingText:'loading...'}
$.fn.button.Constructor=Button
$.fn.button.noConflict=function(){$.fn.button=old
return this}
$(document).on('click.button.data-api','[data-toggle^=button]',function(e){var $btn=$(e.target)
if(!$btn.hasClass('btn'))$btn=$btn.closest('.btn')
$btn.button('toggle')})}(window.jQuery);!function($){"use strict";var bUiSlCt=function(element,options,e){if(e){e.stopPropagation();e.preventDefault();}
this.$element=$(element);this.$newElement=null;this.button=null;this.options=$.extend({},$.fn.bUiSlCt.defaults,this.$element.data(),typeof options=='object'&&options);if(this.options.title==null)
this.options.title=this.$element.attr('title');this.val=bUiSlCt.prototype.val;this.render=bUiSlCt.prototype.render;this.refresh=bUiSlCt.prototype.refresh;this.selectAll=bUiSlCt.prototype.selectAll;this.deselectAll=bUiSlCt.prototype.deselectAll;this.init();};bUiSlCt.prototype={constructor:bUiSlCt,init:function(e){if(!this.options.container){this.$element.hide();}else{this.$element.css('visibility','hidden');};this.multiple=this.$element.prop('multiple');var id=this.$element.attr('id');this.$newElement=this.createView()
this.$element.after(this.$newElement);if(this.options.container){this.selectPosition();}
this.button=this.$newElement.find('> button');if(id!==undefined){var _this=this;this.button.attr('data-id',id);$('label[for="'+id+'"]').click(function(){_this.button.focus();})}
if(this.$element.attr('class')){this.$newElement.addClass(this.$element.attr('class').replace(/bUiSlCt/gi,''));}
if(this.multiple){this.$newElement.addClass('show-tick multiple');}
this.button.addClass(this.options.style);this.checkDisabled();this.checkTabIndex();this.clickListener();this.render();this.setSize();},createDropdown:function(){var drop="<div class='bUi-sLcT dropdown'>"+"<button type='button' class='btn dropdown-toggle' data-toggle='dropdown'>"+"<span class='filter-option pLlT dSpL'></span>&nbsp;"+"<i aria-hidden='true' class='bUi-iCn-cRt-tB-12 pLrT dSpL'></i>"+"</button>"+"<ul class='dropdown-menu' role='menu'>"+"</ul>"+"</div>";return $(drop);},createView:function(){var $drop=this.createDropdown();var $li=this.createLi();$drop.find('ul').append($li);return $drop;},reloadLi:function(){this.destroyLi();var $li=this.createLi();this.$newElement.find('ul').append($li);},destroyLi:function(){this.$newElement.find('li').remove();},createLi:function(){var _this=this;var _liA=[];var _liHtml='';this.$element.find('option').each(function(index){var $this=$(this);var optionClass=$this.attr("class")||'';var text=$this.text();var subtext=$this.data('subtext')!==undefined?'<small class="muted">'+$this.data('subtext')+'</small>':'';var icon=$this.data('icon')!==undefined?'<i class="'+$this.data('icon')+' mRr5 "></i> ':'';if(icon!==''&&($this.is(':disabled')||$this.parent().is(':disabled'))){icon='<span>'+icon+'</span>';}
var _location=$this.data('location')!==undefined?$this.data('location'):'';text=icon+'<span class="text">'+text+subtext+'</span>';if(_this.options.hideDisabled&&($this.is(':disabled')||$this.parent().is(':disabled'))){_liA.push('<a style="min-height: 0; padding: 0"></a>');}else if($this.parent().is('optgroup')&&$this.data('divider')!=true){if($this.index()==0){var label=$this.parent().attr('label');var labelSubtext=$this.parent().data('subtext')!==undefined?'<small class="muted">'+$this.parent().data('subtext')+'</small>':'';var labelIcon=$this.parent().data('icon')?'<i class="'+$this.parent().data('icon')+'"></i> ':'';label=labelIcon+'<span class="text">'+label+labelSubtext+'</span>';if($this[0].index!=0){_liA.push('<div class="divider"></div>'+'<span class="nav-header">'+label+'</span>'+
_this.createA(text,"opt "+optionClass,_location));}else{_liA.push('<span class="nav-header">'+label+'</span>'+
_this.createA(text,"opt "+optionClass,_location));}}else{_liA.push(_this.createA(text,"opt "+optionClass,_location));}}else if($this.data('divider')==true){_liA.push('<div class="div-contain"><div class="divider"></div></div>');}else if($(this).data('hidden')==true){_liA.push('');}else{_liA.push(_this.createA(text,optionClass,_location));}});$.each(_liA,function(i,item){_liHtml+="<li rel="+i+">"+item+"</li>";});if(!this.multiple&&this.$element.find('option:selected').length==0&&!_this.options.title){this.$element.find('option').eq(0).prop('selected',true).attr('selected','selected');}
return $(_liHtml);},createA:function(text,classes,location){return'<a tabindex="0" href="'+location+'" class="'+classes+'">'+
text+'<i class="bUi-iCn-oK-16 lH1 check-mark" aria-hidden="true"></i>'+'</a>';},render:function(){var _this=this;this.$element.find('option').each(function(index){_this.setDisabled(index,$(this).is(':disabled')||$(this).parent().is(':disabled'));_this.setSelected(index,$(this).is(':selected'));});var selectedItems=this.$element.find('option:selected').map(function(index,value){var subtext;if(_this.options.showSubtext&&$(this).attr('data-subtext')&&!_this.multiple){subtext=' <small class="muted">'+$(this).data('subtext')+'</small>';}else{subtext='';}
if($(this).attr('title')!=undefined){return $(this).attr('title');}else{return $(this).text()+subtext;}}).toArray();var title=!this.multiple?selectedItems[0]:selectedItems.join(", "),separator=_this.options.separatorText||_this.options.defaultSeparatorText,selected=_this.options.selectedText||_this.options.defaultSelectedText;if(_this.multiple&&_this.options.selectedTextFormat.indexOf('count')>-1){var max=_this.options.selectedTextFormat.split(">");var notDisabled=this.options.hideDisabled?':not([disabled])':'';if((max.length>1&&selectedItems.length>max[1])||(max.length==1&&selectedItems.length>=2)){title=_this.options.countSelectedText.replace('{0}',selectedItems.length).replace('{1}',this.$element.find('option:not([data-divider="true"]):not([data-hidden="true"])'+notDisabled).length);}}
if(!title){title=_this.options.title!=undefined?_this.options.title:_this.options.noneSelectedText;}
var subtext;if(this.options.showSubtext&&this.$element.find('option:selected').attr('data-subtext')){subtext=' <small class="muted">'+this.$element.find('option:selected').data('subtext')+'</small>';}else{subtext='';}
var icon=this.$element.find('option:selected').data('icon')||'';if(icon.length){icon='<i class="'+icon+'"></i> ';}
_this.$newElement.find('.filter-option').html(icon+title+subtext);},setSize:function(){if(this.options.container){this.$newElement.toggle(this.$element.parent().is(':visible'));}
var _this=this;var menu=this.$newElement.find('.dropdown-menu');var menuA=menu.find('li > a');var liHeight=this.$newElement.addClass('open').find('.dropdown-menu li > a').outerHeight();this.$newElement.removeClass('open');var divHeight=menu.find('li .divider').outerHeight(true);var selectOffset_top=this.$newElement.offset().top;var selectHeight=this.$newElement.outerHeight();var menuPadding=parseInt(menu.css('padding-top'))+parseInt(menu.css('padding-bottom'))+parseInt(menu.css('border-top-width'))+parseInt(menu.css('border-bottom-width'));var notDisabled=this.options.hideDisabled?':not(.disabled)':'';var menuHeight;if(this.options.size=='auto'){var getSize=function(){var selectOffset_top_scroll=selectOffset_top-$(window).scrollTop();var windowHeight=window.innerHeight;var menuExtras=menuPadding+parseInt(menu.css('margin-top'))+parseInt(menu.css('margin-bottom'))+2;var selectOffset_bot=windowHeight-selectOffset_top_scroll-selectHeight-menuExtras;var minHeight;menuHeight=selectOffset_bot;if(_this.$newElement.hasClass('dropup')){menuHeight=selectOffset_top_scroll-menuExtras;}
minHeight=0;menu.css({'max-height':menuHeight+'px','overflow-y':'auto','min-height':minHeight+'px'});}
getSize();$(window).resize(getSize);$(window).scroll(getSize);}else if(this.options.size&&this.options.size!='auto'&&menu.find('li'+notDisabled).length>this.options.size){var optIndex=menu.find("li"+notDisabled+" > *").filter(':not(.div-contain)').slice(0,this.options.size).last().parent().index();var divLength=menu.find("li").slice(0,optIndex+1).find('.div-contain').length;menuHeight=25*this.options.size;menu.css({'max-height':menuHeight+'px','overflow-y':'auto'});}
if(this.options.width=='auto'){this.$newElement.find('.dropdown-menu').css('min-width','0');var ulWidth=this.$newElement.find('.dropdown-menu').css('width');this.$newElement.css('width',ulWidth);if(this.options.container){this.$element.css('width',ulWidth);}}else if(this.options.width){if(this.options.container){this.$element.css('width',this.options.width);this.$newElement.width(this.$element.outerWidth());}else{this.$newElement.css('width',this.options.width);}}else if(this.options.container){this.$newElement.width(this.$element.outerWidth());}},selectPosition:function(){var containerOffset=$(this.options.container).offset();var eltOffset=this.$element.offset();if(containerOffset&&eltOffset){var selectElementTop=eltOffset.top-containerOffset.top;var selectElementLeft=eltOffset.left-containerOffset.left;this.$newElement.appendTo(this.options.container);this.$newElement.css({'position':'absolute','top':selectElementTop+'px','left':selectElementLeft+'px'});}},refresh:function(){this.reloadLi();this.render();this.setSize();this.checkDisabled();if(this.options.container){this.selectPosition();}},setSelected:function(index,selected){if(selected){this.$newElement.find('li').eq(index).addClass('selected');}else{this.$newElement.find('li').eq(index).removeClass('selected');}},setDisabled:function(index,disabled){if(disabled){this.$newElement.find('li').eq(index).addClass('disabled').find('a').attr('href','#').attr('tabindex',-1);}else{this.$newElement.find('li').eq(index).removeClass('disabled').find('a').attr('tabindex',0);}},isDisabled:function(){return this.$element.is(':disabled')||this.$element.attr('readonly');},checkDisabled:function(){if(this.isDisabled()){this.button.addClass('disabled');this.button.click(function(e){e.preventDefault();});this.button.attr('tabindex','-1');}else if(!this.isDisabled()&&this.button.hasClass('disabled')){this.button.removeClass('disabled');this.button.click(function(){return true;});this.button.removeAttr('tabindex');}},checkTabIndex:function(){if(this.$element.is('[tabindex]')){var tabindex=this.$element.attr("tabindex");this.button.attr('tabindex',tabindex);}},clickListener:function(){var _this=this;$('body').on('touchstart.dropdown','.dropdown-menu',function(e){e.stopPropagation();});this.$element.each(function(index){if(!$(this).data('link')==true){_this.$newElement.on('click','li a',function(e){var clickedIndex=$(this).parent().index(),$this=$(this).parent(),$select=$this.parents('.bUi-sLcT'),prevValue=_this.$element.val();if(_this.multiple){e.stopPropagation();}
e.preventDefault();if(_this.$element.not(':disabled')&&!$(this).parent().hasClass('disabled')){if(!_this.multiple){_this.$element.find('option').prop('selected',false);_this.$element.find('option').eq(clickedIndex).prop('selected',true);}
else{var selected=_this.$element.find('option').eq(clickedIndex).prop('selected');if(selected){_this.$element.find('option').eq(clickedIndex).prop('selected',false);}else{_this.$element.find('option').eq(clickedIndex).prop('selected',true);}}
$select.find('button').focus();if(prevValue!=_this.$element.val()){_this.$element.trigger('change');}
_this.render();}});}})
this.$newElement.on('click','li.disabled a, li span.nav-header, li .div-contain',function(e){e.preventDefault();e.stopPropagation();var $select=$(this).parent().parents('.bUi-sLcT');$select.find('button').focus();});this.$element.on('change',function(e){_this.render();});},val:function(value){if(value!=undefined){this.$element.val(value);this.$element.trigger('change');return this.$element;}else{return this.$element.val();}},selectAll:function(){this.$element.find('option').prop('selected',true).attr('selected','selected');this.render();},deselectAll:function(){this.$element.find('option').prop('selected',false).removeAttr('selected');this.render();},keydown:function(e){var $this,$items,$parent,index,next,first,last,prev,nextPrev
$this=$(this);$parent=$this.parent();$items=$('[role=menu] li:not(.divider):visible a',$parent);if(!$items.length)return;if(/(38|40)/.test(e.keyCode)){index=$items.index($items.filter(':focus'));first=$items.parent(':not(.disabled)').first().index();last=$items.parent(':not(.disabled)').last().index();next=$items.eq(index).parent().nextAll(':not(.disabled)').eq(0).index();prev=$items.eq(index).parent().prevAll(':not(.disabled)').eq(0).index();nextPrev=$items.eq(next).parent().prevAll(':not(.disabled)').eq(0).index();if(e.keyCode==38){if(index!=nextPrev&&index>prev)index=prev;if(index<first)index=first;}
if(e.keyCode==40){if(index!=nextPrev&&index<next)index=next;if(index>last)index=last;}
$items.eq(index).focus()}else{var keyCodeMap={48:"0",49:"1",50:"2",51:"3",52:"4",53:"5",54:"6",55:"7",56:"8",57:"9",59:";",65:"a",66:"b",67:"c",68:"d",69:"e",70:"f",71:"g",72:"h",73:"i",74:"j",75:"k",76:"l",77:"m",78:"n",79:"o",80:"p",81:"q",82:"r",83:"s",84:"t",85:"u",86:"v",87:"w",88:"x",89:"y",90:"z",96:"0",97:"1",98:"2",99:"3",100:"4",101:"5",102:"6",103:"7",104:"8",105:"9"}
var keyIndex=[];$items.each(function(){if($(this).parent().is(':not(.disabled)')){if($.trim($(this).text().toLowerCase()).substring(0,1)==keyCodeMap[e.keyCode]){keyIndex.push($(this).parent().index());}}});var count=$(document).data('keycount');count++;$(document).data('keycount',count);var prevKey=$.trim($(':focus').text().toLowerCase()).substring(0,1);if(prevKey!=keyCodeMap[e.keyCode]){count=1;$(document).data('keycount',count);}else if(count>=keyIndex.length){$(document).data('keycount',0);}
$items.eq(keyIndex[count-1]).focus();}
if(/(13)/.test(e.keyCode)){$(':focus').click();$parent.addClass('open');$(document).data('keycount',0);}}};$.fn.bUiSlCt=function(option,event){var args=arguments;var value;var chain=this.each(function(){if($(this).is('select')){var $this=$(this),data=$this.data('bUiSlCt'),options=typeof option=='object'&&option;if(!data){$this.data('bUiSlCt',(data=new bUiSlCt(this,options,event)));}else if(options){for(var i in options){data.options[i]=options[i];}}
if(typeof option=='string'){var property=option;if(data[property]instanceof Function){[].shift.apply(args);value=data[property].apply(data,args);}else{value=data.options[property];}}}});if(value!=undefined){return value;}else{return chain;}};$.fn.bUiSlCt.defaults={style:null,size:'auto',title:null,selectedTextFormat:'values',noneSelectedText:'Nothing selected',countSelectedText:'{0} of {1} selected',width:null,container:false,hideDisabled:false,showSubtext:false}
$(document).data('keycount',0).on('keydown','[data-toggle=dropdown], [role=menu]',bUiSlCt.prototype.keydown)}(window.jQuery);!function($){"use strict";var toggle='[data-toggle=dropdown]',Dropdown=function(element){var $el=$(element).on('click.dropdown.data-api',this.toggle)
$('html').on('click.dropdown.data-api',function(){$el.parent().removeClass('open')})}
Dropdown.prototype={constructor:Dropdown,toggle:function(e){var $this=$(this),$parent,isActive
if($this.is('.disabled, :disabled'))return
$parent=getParent($this)
isActive=$parent.hasClass('open')
clearMenus()
if(!isActive){if('ontouchstart'in document.documentElement){$('<div class="dropdown-backdrop"/>').insertBefore($(this)).on('click',clearMenus)}
$parent.toggleClass('open')}
$this.focus()
return false},keydown:function(e){var $this,$items,$active,$parent,isActive,index
if(!/(38|40|27)/.test(e.keyCode))return
$this=$(this)
e.preventDefault()
e.stopPropagation()
if($this.is('.disabled, :disabled'))return
$parent=getParent($this)
isActive=$parent.hasClass('open')
if(!isActive||(isActive&&e.keyCode==27)){if(e.which==27)$parent.find(toggle).focus()
return $this.click()}
$items=$('[role=menu] li:not(.divider):visible a',$parent)
if(!$items.length)return
index=$items.index($items.filter(':focus'))
if(e.keyCode==38&&index>0)index--
if(e.keyCode==40&&index<$items.length-1)index++
if(!~index)index=0
$items.eq(index).focus()}}
function clearMenus(){$('.dropdown-backdrop').remove()
$(toggle).each(function(){getParent($(this)).removeClass('open')})}
function getParent($this){var selector=$this.attr('data-target'),$parent
if(!selector){selector=$this.attr('href')
selector=selector&&/#/.test(selector)&&selector.replace(/.*(?=#[^\s]*$)/,'')}
$parent=selector&&$(selector)
if(!$parent||!$parent.length)$parent=$this.parent()
return $parent}
var old=$.fn.dropdown
$.fn.dropdown=function(option){return this.each(function(){var $this=$(this),data=$this.data('dropdown')
if(!data)$this.data('dropdown',(data=new Dropdown(this)))
if(typeof option=='string')data[option].call($this)})}
$.fn.dropdown.Constructor=Dropdown
$.fn.dropdown.noConflict=function(){$.fn.dropdown=old
return this}
$(document).on('click.dropdown.data-api',clearMenus).on('click.dropdown.data-api','.dropdown form, .radio',function(e){e.stopPropagation()}).on('click.dropdown.data-api',toggle,Dropdown.prototype.toggle).on('keydown.dropdown.data-api',toggle+', [role=menu]',Dropdown.prototype.keydown)}(window.jQuery);!function($){"use strict";var Tooltip=function(element,options){this.init('tooltip',element,options)}
Tooltip.prototype={constructor:Tooltip,init:function(type,element,options){var eventIn,eventOut,triggers,trigger,i
this.type=type
this.$element=$(element)
this.options=this.getOptions(options)
this.enabled=true
triggers=this.options.trigger.split(' ')
for(i=triggers.length;i--;){trigger=triggers[i]
if(trigger=='click'){this.$element.on('click.'+this.type,this.options.selector,$.proxy(this.toggle,this))}else if(trigger!='manual'){eventIn=trigger=='hover'?'mouseenter':'focus'
eventOut=trigger=='hover'?'mouseleave':'blur'
this.$element.on(eventIn+'.'+this.type,this.options.selector,$.proxy(this.enter,this))
this.$element.on(eventOut+'.'+this.type,this.options.selector,$.proxy(this.leave,this))}}
this.options.selector?(this._options=$.extend({},this.options,{trigger:'manual',selector:''})):this.fixTitle()},getOptions:function(options){options=$.extend({},$.fn[this.type].defaults,this.$element.data(),options)
if(options.delay&&typeof options.delay=='number'){options.delay={show:options.delay,hide:options.delay}}
return options},enter:function(e){var defaults=$.fn[this.type].defaults,options={},self
this._options&&$.each(this._options,function(key,value){if(defaults[key]!=value)options[key]=value},this)
self=$(e.currentTarget)[this.type](options).data(this.type)
if(!self.options.delay||!self.options.delay.show)return self.show()
clearTimeout(this.timeout)
self.hoverState='in'
this.timeout=setTimeout(function(){if(self.hoverState=='in')self.show()},self.options.delay.show)},leave:function(e){var self=$(e.currentTarget)[this.type](this._options).data(this.type)
if(this.timeout)clearTimeout(this.timeout)
if(!self.options.delay||!self.options.delay.hide)return self.hide()
self.hoverState='out'
this.timeout=setTimeout(function(){if(self.hoverState=='out')self.hide()},self.options.delay.hide)},show:function(){var $tip,pos,actualWidth,actualHeight,placement,tp,e=$.Event('show')
if(this.hasContent()&&this.enabled){this.$element.trigger(e)
if(e.isDefaultPrevented())return
$tip=this.tip()
this.setContent()
if(this.options.animation){$tip.addClass('fade')}
if(this.options.sLanimation){$tip.addClass('sLd')}
placement=typeof this.options.placement=='function'?this.options.placement.call(this,$tip[0],this.$element[0]):this.options.placement
$tip.detach().css({top:0,left:0,display:'block'})
this.options.container?$tip.appendTo(this.options.container):$tip.insertAfter(this.$element)
pos=this.getPosition()
actualWidth=$tip[0].offsetWidth
actualHeight=$tip[0].offsetHeight
switch(placement){case'bottom':tp={top:pos.top+pos.height,left:pos.left+pos.width/2-actualWidth/2}
break
case'top':tp={top:pos.top-actualHeight,left:pos.left+pos.width/2-actualWidth/2}
break
case'left':tp={top:pos.top+pos.height/2-actualHeight/2,left:pos.left-actualWidth}
break
case'right':tp={top:pos.top+pos.height/2-actualHeight/2,left:pos.left+pos.width}
break}
this.applyPlacement(tp,placement)
this.$element.trigger('shown');if(this.options.eNcL==false)$tip.find('.close').remove();}},applyPlacement:function(offset,placement){var $tip=this.tip(),width=$tip[0].offsetWidth,height=$tip[0].offsetHeight,actualWidth,actualHeight,delta,replace
$tip.offset(offset).addClass(placement).addClass('in')
actualWidth=$tip[0].offsetWidth
actualHeight=$tip[0].offsetHeight
if(placement=='top'&&actualHeight!=height){offset.top=offset.top+height-actualHeight
replace=true}
if(placement=='bottom'||placement=='top'){delta=0
if(offset.left<0){delta=offset.left*-2
offset.left=0
$tip.offset(offset)
actualWidth=$tip[0].offsetWidth
actualHeight=$tip[0].offsetHeight}
this.replaceArrow(delta-width+actualWidth,actualWidth,'left')}else{this.replaceArrow(actualHeight-height,actualHeight,'top')}
if(replace)$tip.offset(offset)},replaceArrow:function(delta,dimension,position){this.arrow().css(position,delta?(50*(1-delta/dimension)+"%"):'')},setContent:function(){var $tip=this.tip(),title=this.getTitle()
$tip.find('.tooltip-inner')[this.options.html?'html':'text'](title)
$tip.removeClass('fade in top bottom left right')},hide:function(){var that=this,$tip=this.tip(),e=$.Event('hide')
this.$element.trigger(e)
if(e.isDefaultPrevented())return
$tip.removeClass('in')
function removeWithAnimation(){var timeout=setTimeout(function(){$tip.off($.support.transition.end).detach()},500)
$tip.one($.support.transition.end,function(){clearTimeout(timeout)
$tip.detach()})}
$.support.transition&&this.$tip.hasClass('fade')?removeWithAnimation():$tip.detach()
this.$element.trigger('hidden')
return this},fixTitle:function(){var $e=this.$element
if($e.attr('title')||typeof($e.attr('data-original-title'))!='string'){$e.attr('data-original-title',$e.attr('title')||'').attr('title','')}},hasContent:function(){return this.getTitle()},getPosition:function(){var el=this.$element[0]
return $.extend({},(typeof el.getBoundingClientRect=='function')?el.getBoundingClientRect():{width:el.offsetWidth,height:el.offsetHeight},this.$element.offset())},getTitle:function(){var title,$e=this.$element,o=this.options
title=$e.attr('data-original-title')||(typeof o.title=='function'?o.title.call($e[0]):o.title)
return title},tip:function(){return this.$tip=this.$tip||$(this.options.template)},arrow:function(){return this.$arrow=this.$arrow||this.tip().find(".tooltip-arrow")},validate:function(){if(!this.$element[0].parentNode){this.hide()
this.$element=null
this.options=null}},enable:function(){this.enabled=true},disable:function(){this.enabled=false},toggleEnabled:function(){this.enabled=!this.enabled},toggle:function(e){var self=e?$(e.currentTarget)[this.type](this._options).data(this.type):this
self.tip().hasClass('in')?self.hide():self.show();if(self.options.eNcL==true){var $tip=self.tip();var cLeL=$tip.find('.close');$(cLeL).click(function(){self.hide();})}},destroy:function(){this.hide().$element.off('.'+this.type).removeData(this.type)}}
var old=$.fn.tooltip
$.fn.tooltip=function(option){return this.each(function(){var $this=$(this),data=$this.data('tooltip'),options=typeof option=='object'&&option
if(!data)$this.data('tooltip',(data=new Tooltip(this,options)))
if(typeof option=='string')data[option]()})}
$.fn.tooltip.Constructor=Tooltip
$.fn.tooltip.defaults={animation:true,sLanimation:true,placement:'top',selector:false,template:'<div class="tooltip"><div class="tooltip-arrow"></div><div class="tooltip-inner"></div></div>',trigger:'hover focus',title:'',delay:0,html:false,container:false,eNcL:false}
$.fn.tooltip.noConflict=function(){$.fn.tooltip=old
return this}}(window.jQuery);+function($){"use strict";var Modal=function(element,options){this.options=options
this.$element=$(element).on('click.dismiss.modal','[data-dismiss="modal"]',$.proxy(this.hide,this))
this.$backdrop=this.isShown=null
if(this.options.remote)this.$element.find('.modal-body').load(this.options.remote)}
Modal.DEFAULTS={backdrop:true,keyboard:true,show:true,remote:true}
Modal.prototype.toggle=function(){return this[!this.isShown?'show':'hide']()}
Modal.prototype.show=function(){var that=this
var e=$.Event('show.bs.modal')
this.$element.trigger(e)
if(this.isShown||e.isDefaultPrevented())return
this.isShown=true
this.escape()
this.backdrop(function(){var transition=$.support.transition&&that.$element.hasClass('fade')
if(!that.$element.parent().length){that.$element.appendTo(document.body)}
that.$element.show()
if(transition){that.$element[0].offsetWidth}
that.$element.addClass('in').attr('aria-hidden',false)
that.enforceFocus()
transition?that.$element.one($.support.transition.end,function(){that.$element.focus().trigger('shown.bs.modal')}).emulateTransitionEnd(300):that.$element.focus().trigger('shown.bs.modal')})}
Modal.prototype.hide=function(e){if(e)e.preventDefault()
e=$.Event('hide.bs.modal')
this.$element.trigger(e)
if(!this.isShown||e.isDefaultPrevented())return
this.isShown=false
this.escape()
$(document).off('focusin.bs.modal')
this.$element.removeClass('in').attr('aria-hidden',true)
$.support.transition&&this.$element.hasClass('fade')?this.$element.one($.support.transition.end,$.proxy(this.hideModal,this)).emulateTransitionEnd(300):this.hideModal()}
Modal.prototype.enforceFocus=function(){$(document).off('focusin.bs.modal').on('focusin.bs.modal',$.proxy(function(e){if(this.$element[0]!==e.target&&!this.$element.has(e.target).length){this.$element.focus()}},this))}
Modal.prototype.escape=function(){if(this.isShown&&this.options.keyboard){this.$element.on('keyup.dismiss.bs.modal',$.proxy(function(e){e.which==27&&this.hide()},this))}else if(!this.isShown){this.$element.off('keyup.dismiss.bs.modal')}}
Modal.prototype.hideModal=function(){var that=this
this.$element.hide()
this.backdrop(function(){that.removeBackdrop()
that.$element.trigger('hidden.bs.modal')})}
Modal.prototype.removeBackdrop=function(){this.$backdrop&&this.$backdrop.remove()
this.$backdrop=null}
Modal.prototype.backdrop=function(callback){var that=this
var animate=this.$element.hasClass('fade')?'fade':''
if(this.isShown&&this.options.backdrop){var doAnimate=$.support.transition&&animate
this.$backdrop=$('<div class="modal-backdrop '+animate+'" />').appendTo(document.body)
this.$element.on('click',$.proxy(function(e){if(e.target!==e.currentTarget)return
this.options.backdrop=='static'?this.$element[0].focus.call(this.$element[0]):this.hide.call(this)},this))
if(doAnimate)this.$backdrop[0].offsetWidth
this.$backdrop.addClass('in')
if(!callback)return
doAnimate?this.$backdrop.one($.support.transition.end,callback).emulateTransitionEnd(150):callback()}else if(!this.isShown&&this.$backdrop){this.$backdrop.removeClass('in')
$.support.transition&&this.$element.hasClass('fade')?this.$backdrop.one($.support.transition.end,callback).emulateTransitionEnd(150):callback()}else if(callback){callback()}}
var old=$.fn.modal
$.fn.modal=function(option){return this.each(function(){var $this=$(this)
var data=$this.data('bs.modal')
var options=$.extend({},Modal.DEFAULTS,$this.data(),typeof option=='object'&&option)
if(!data)$this.data('bs.modal',(data=new Modal(this,options)))
if(typeof option=='string')data[option]()
else if(options.show)data.show()})}
$.fn.modal.Constructor=Modal
$.fn.modal.noConflict=function(){$.fn.modal=old
return this}
$(document).on('click.bs.modal.data-api','[data-toggle="modal"]',function(e){var $this=$(this)
var href=$this.attr('href')
var $target=$($this.attr('data-target')||(href&&href.replace(/.*(?=#[^\s]+$)/,'')))
var option=$target.data('modal')?'toggle':$.extend({remote:!/#/.test(href)&&href},$target.data(),$this.data())
e.preventDefault()
$target.modal(option).one('hide',function(){$this.is(':visible')&&$this.focus()})})
$(function(){var $body=$(document.body).on('shown.bs.modal','.modal',function(){$body.addClass('modal-open')}).on('hidden.bs.modal','.modal',function(){$body.removeClass('modal-open')})})}(window.jQuery);!function($){"use strict";var Popover=function(element,options){this.init('popover',element,options)}
Popover.prototype=$.extend({},$.fn.tooltip.Constructor.prototype,{constructor:Popover,setContent:function(){var $tip=this.tip(),title=this.getTitle(),content=this.getContent()
$tip.find('.popover-title')[this.options.html?'html':'text'](title)
$tip.find('.popover-content')[this.options.html?'html':'text'](content)
$tip.removeClass('fade top bottom left right in')},hasContent:function(){return this.getTitle()||this.getContent()},getContent:function(){var content,$e=this.$element,o=this.options
content=(typeof o.content=='function'?o.content.call($e[0]):o.content)||$e.attr('data-content')
if(typeof this.options.external!=='undefined'&&this.options.external!==null){content=$(this.options.external).html();}
return content},tip:function(){if(!this.$tip){this.$tip=$(this.options.template)}
return this.$tip},destroy:function(){this.hide().$element.off('.'+this.type).removeData(this.type)}})
var old=$.fn.popover
$.fn.popover=function(option){return this.each(function(){var $this=$(this),data=$this.data('popover'),options=typeof option=='object'&&option
if(!data)$this.data('popover',(data=new Popover(this,options)))
if(typeof option=='string')data[option]()})}
$.fn.popover.Constructor=Popover
$.fn.popover.defaults=$.extend({},$.fn.tooltip.defaults,{placement:'right',trigger:'click',content:'',template:'<div class="popover"><div class="arrow"></div><div class="close">&times;</div><h3 class="popover-title"></h3><div class="popover-content"></div></div>',eNcL:true})
$.fn.popover.noConflict=function(){$.fn.popover=old
return this}}(window.jQuery);!function($){"use strict";$.fn['bootstrapSwitch']=function(method){var methods={init:function(){return this.each(function(){var $element=$(this),$div,$switchLeft,$switchRight,$label,myClasses="",classes=$element.attr('class'),color,moving,onLabel="ON",offLabel="OFF",icon=false;$.each(['switch-mini','switch-small','switch-large'],function(i,el){if(classes.indexOf(el)>=0)
myClasses=el;});$element.addClass('has-switch');if($element.data('on')!==undefined)
color="switch-"+$element.data('on');if($element.data('on-label')!==undefined)
onLabel=$element.data('on-label');if($element.data('off-label')!==undefined)
offLabel=$element.data('off-label');if($element.data('icon')!==undefined)
icon=$element.data('icon');$switchLeft=$('<span>').addClass("switch-left").addClass(myClasses).addClass(color).html(onLabel);color='';if($element.data('off')!==undefined)
color="switch-"+$element.data('off');$switchRight=$('<span>').addClass("switch-right").addClass(myClasses).addClass(color).html(offLabel);$label=$('<label>').html("&nbsp;").addClass(myClasses).attr('for',$element.find('input').attr('id'));if(icon){$label.html('<i class="'+icon+'"></i>');}
$div=$element.find(':checkbox').wrap($('<div>')).parent().data('animated',false);if($element.data('animated')!==false)
$div.addClass('switch-animate').data('animated',true);$div.append($switchLeft).append($label).append($switchRight);$element.find('>div').addClass($element.find('input').is(':checked')?'switch-on':'switch-off');if($element.find('input').is(':disabled'))
$(this).addClass('deactivate');var changeStatus=function($this){$this.siblings('label').trigger('mousedown').trigger('mouseup').trigger('click');};$element.on('keydown',function(e){if(e.keyCode===32){e.stopImmediatePropagation();e.preventDefault();changeStatus($(e.target).find('span:first'));}});$switchLeft.on('click',function(e){changeStatus($(this));});$switchRight.on('click',function(e){changeStatus($(this));});$element.find('input').on('change',function(e){var $this=$(this),$element=$this.parent(),thisState=$this.is(':checked'),state=$element.is('.switch-off');e.preventDefault();$element.css('left','');if(state===thisState){if(thisState)
$element.removeClass('switch-off').addClass('switch-on');else $element.removeClass('switch-on').addClass('switch-off');if($element.data('animated')!==false)
$element.addClass("switch-animate");$element.parent().trigger('switch-change',{'el':$this,'value':thisState})}});$element.find('label').on('mousedown touchstart',function(e){var $this=$(this);moving=false;e.preventDefault();e.stopImmediatePropagation();$this.closest('div').removeClass('switch-animate');if($this.closest('.has-switch').is('.deactivate'))
$this.unbind('click');else{$this.on('mousemove touchmove',function(e){var $element=$(this).closest('.switch'),relativeX=(e.pageX||e.originalEvent.targetTouches[0].pageX)-$element.offset().left,percent=(relativeX/$element.width())*100,left=25,right=75;moving=true;if(percent<left)
percent=left;else if(percent>right)
percent=right;$element.find('>div').css('left',(percent-right)+"%")});$this.on('click touchend',function(e){var $this=$(this),$target=$(e.target),$myCheckBox=$target.siblings('input');e.stopImmediatePropagation();e.preventDefault();$this.unbind('mouseleave');if(moving)
$myCheckBox.prop('checked',!(parseInt($this.parent().css('left'))<-25));else $myCheckBox.prop("checked",!$myCheckBox.is(":checked"));moving=false;$myCheckBox.trigger('change');});$this.on('mouseleave',function(e){var $this=$(this),$myCheckBox=$this.siblings('input');e.preventDefault();e.stopImmediatePropagation();$this.unbind('mouseleave');$this.trigger('mouseup');$myCheckBox.prop('checked',!(parseInt($this.parent().css('left'))<-25)).trigger('change');});$this.on('mouseup',function(e){e.stopImmediatePropagation();e.preventDefault();$(this).unbind('mousemove');});}});});},toggleActivation:function(){$(this).toggleClass('deactivate');},isActive:function(){return!$(this).hasClass('deactivate');},setActive:function(active){if(active)
$(this).removeClass('deactivate');else $(this).addClass('deactivate');},toggleState:function(skipOnChange){var $input=$(this).find('input:checkbox');$input.prop('checked',!$input.is(':checked')).trigger('change',skipOnChange);},setState:function(value,skipOnChange){$(this).find('input:checkbox').prop('checked',value).trigger('change',skipOnChange);},status:function(){return $(this).find('input:checkbox').is(':checked');},destroy:function(){var $div=$(this).find('div'),$checkbox;$div.find(':not(input:checkbox)').remove();$checkbox=$div.children();$checkbox.unwrap().unwrap();$checkbox.unbind('change');return $checkbox;}};if(methods[method])
return methods[method].apply(this,Array.prototype.slice.call(arguments,1));else if(typeof method==='object'||!method)
return methods.init.apply(this,arguments);else
$.error('Method '+method+' does not exist!');};}(jQuery);$(function(){$('.switch')['bootstrapSwitch']();});!function($){"use strict";var Typeahead=function(element,options){this.$element=$(element);this.options=$.extend(true,{},$.fn.typeahead.defaults,options);this.$menu=$(this.options.menu).appendTo('body');this.shown=false;this.eventSupported=this.options.eventSupported||this.eventSupported;this.grepper=this.options.grepper||this.grepper;this.highlighter=this.options.highlighter||this.highlighter;this.lookup=this.options.lookup||this.lookup;this.matcher=this.options.matcher||this.matcher;this.render=this.options.render||this.render;this.select=this.options.select||this.select;this.sorter=this.options.sorter||this.sorter;this.source=this.options.source||this.source;if(!this.source.length){var ajax=this.options.ajax;if(typeof ajax==='string'){this.ajax=$.extend({},$.fn.typeahead.defaults.ajax,{url:ajax});}else{this.ajax=$.extend({},$.fn.typeahead.defaults.ajax,ajax);}
if(!this.ajax.url){this.ajax=null;}}
this.listen();}
Typeahead.prototype={constructor:Typeahead,eventSupported:function(eventName){var isSupported=(eventName in this.$element);if(!isSupported){this.$element.setAttribute(eventName,'return;');isSupported=typeof this.$element[eventName]==='function';}
return isSupported;},ajaxer:function(){var that=this,query=that.$element.val();if(query===that.query){return that;}
that.query=query;if(that.ajax.timerId){clearTimeout(that.ajax.timerId);that.ajax.timerId=null;}
if(!query||query.length<that.ajax.triggerLength){if(that.ajax.xhr){that.ajax.xhr.abort();that.ajax.xhr=null;that.ajaxToggleLoadClass(false);}
return that.shown?that.hide():that;}
that.ajax.timerId=setTimeout(function(){$.proxy(that.ajaxExecute(query),that)},that.ajax.timeout);return that;},ajaxExecute:function(query){this.ajaxToggleLoadClass(true);if(this.ajax.xhr)this.ajax.xhr.abort();var params=this.ajax.preDispatch?this.ajax.preDispatch(query):{query:query};var jAjax=(this.ajax.method==="post")?$.post:$.get;this.ajax.xhr=jAjax(this.ajax.url,params,$.proxy(this.ajaxLookup,this));this.ajax.timerId=null;},ajaxLookup:function(data){var items;this.ajaxToggleLoadClass(false);if(!this.ajax.xhr)return;if(this.ajax.preProcess){data=this.ajax.preProcess(data);}
this.ajax.data=data;items=this.grepper(this.ajax.data);if(!items||!items.length){return this.shown?this.hide():this;}
this.ajax.xhr=null;return this.render(items.slice(0,this.options.items)).show();},ajaxToggleLoadClass:function(enable){if(!this.ajax.loadingClass)return;this.$element.toggleClass(this.ajax.loadingClass,enable);},lookup:function(event){var that=this,items;if(that.ajax){that.ajaxer();}
else{that.query=that.$element.val();if(!that.query){return that.shown?that.hide():that;}
items=that.grepper(that.source);if(!items||!items.length){return that.shown?that.hide():that;}
return that.render(items.slice(0,that.options.items)).show();}},grepper:function(data){var that=this,items;if(data&&data.length&&!data[0].hasOwnProperty(that.options.display)){return null;}
items=$.grep(data,function(item){return that.matcher(item[that.options.display],item);});return this.sorter(items);},matcher:function(item){return~item.toLowerCase().indexOf(this.query.toLowerCase());},sorter:function(items){var that=this,beginswith=[],caseSensitive=[],caseInsensitive=[],item;while(item=items.shift()){if(!item[that.options.display].toLowerCase().indexOf(this.query.toLowerCase())){beginswith.push(item);}
else if(~item[that.options.display].indexOf(this.query)){caseSensitive.push(item);}
else{caseInsensitive.push(item);}}
return beginswith.concat(caseSensitive,caseInsensitive);},show:function(){var pos=$.extend({},this.$element.offset(),{height:this.$element[0].offsetHeight});this.$menu.css({top:pos.top+pos.height,left:pos.left});this.$menu.show();this.shown=true;return this;},hide:function(){this.$menu.hide();this.shown=false;return this;},highlighter:function(item){var query=this.query.replace(/[\-\[\]{}()*+?.,\\\^$|#\s]/g,'\\$&');return item.replace(new RegExp('('+query+')','ig'),function($1,match){return'<strong>'+match+'</strong>';});},render:function(items){var that=this;items=$(items).map(function(i,item){i=$(that.options.item).attr('data-value',item[that.options.val]);i.find('a').html(that.highlighter(item[that.options.display],item));return i[0];});this.$menu.html(items);return this;},select:function(){var $selectedItem=this.$menu.find('.active');this.$element.val($selectedItem.text()).change();this.options.itemSelected($selectedItem,$selectedItem.attr('data-value'),$selectedItem.text());return this.hide();},next:function(event){var active=this.$menu.find('.active').removeClass('active');var next=active.next();if(!next.length){next=$(this.$menu.find('li')[0]);}
next.addClass('active');},prev:function(event){var active=this.$menu.find('.active').removeClass('active');var prev=active.prev();if(!prev.length){prev=this.$menu.find('li').last();}
prev.addClass('active');},listen:function(){this.$element.on('blur',$.proxy(this.blur,this)).on('keyup',$.proxy(this.keyup,this));if(this.eventSupported('keydown')){this.$element.on('keydown',$.proxy(this.keypress,this));}else{this.$element.on('keypress',$.proxy(this.keypress,this));}
this.$menu.on('click',$.proxy(this.click,this)).on('mouseenter','li',$.proxy(this.mouseenter,this)).on('mouseleave','li',$.proxy(this.mouseleave,this));},keyup:function(e){e.stopPropagation();e.preventDefault();var $thiss=this;switch(e.keyCode){case 40:case 38:break;case 9:case 13:if(!this.shown){return;}
if(this.$menu.find('li').hasClass('active')){this.select();}else{this.hide();}
break;case 27:this.hide();break;default:this.lookup();}},keypress:function(e){e.stopPropagation();if(!this.shown){return;}
switch(e.keyCode){case 9:case 13:case 27:e.preventDefault();break;case 38:e.preventDefault();this.prev();break;case 40:e.preventDefault();this.next();break;}},blur:function(e){var that=this;e.stopPropagation();e.preventDefault();setTimeout(function(){if(!that.$menu.is(':focus')){that.hide();}},150)},click:function(e){e.stopPropagation();e.preventDefault();this.select();},mouseenter:function(e){this.$menu.find('.active').removeClass('active');$(e.currentTarget).addClass('active');},mouseleave:function(e){this.$menu.find('.active').removeClass('active');}}
$.fn.typeahead=function(option){return this.each(function(){var $this=$(this),data=$this.data('typeahead'),options=typeof option==='object'&&option;if(!data){$this.data('typeahead',(data=new Typeahead(this,options)));}
if(typeof option==='string'){data[option]();}});}
$.fn.typeahead.defaults={source:[],items:8,menu:'<ul class="typeahead dropdown-menu"></ul>',item:'<li><a href="#"></a></li>',display:'name',val:'id',itemSelected:function(){},ajax:{url:null,timeout:300,method:'post',triggerLength:3,loadingClass:null,displayField:null,preDispatch:null,preProcess:null}}
$.fn.typeahead.Constructor=Typeahead;$(function(){$('body').on('focus.typeahead.data-api','[data-provide="typeahead"]',function(e){var $this=$(this);if($this.data('typeahead')){return;}
e.preventDefault();$this.typeahead($this.data());})});}(window.jQuery);(function($){var delimiter=new Array();var tags_callbacks=new Array();$.fn.doAutosize=function(o){var minWidth=$(this).data('minwidth'),maxWidth=$(this).data('maxwidth'),val='',input=$(this),testSubject=$('#'+$(this).data('tester_id'));if(val===(val=input.val())){return;}
var escaped=val.replace(/&/g,'&amp;').replace(/\s/g,' ').replace(/</g,'&lt;').replace(/>/g,'&gt;');testSubject.html(escaped);var testerWidth=testSubject.width(),newWidth=(testerWidth+o.comfortZone)>=minWidth?testerWidth+o.comfortZone:minWidth,currentWidth=input.width(),isValidWidthChange=(newWidth<currentWidth&&newWidth>=minWidth)||(newWidth>minWidth&&newWidth<maxWidth);if(isValidWidthChange){input.width(newWidth);}};$.fn.resetAutosize=function(options){var minWidth=$(this).data('minwidth')||options.minInputWidth||$(this).width(),maxWidth=$(this).data('maxwidth')||options.maxInputWidth||($(this).closest('.tagsinput').width()-options.inputPadding),val='',input=$(this),testSubject=$('<tester/>').css({position:'absolute',top:-9999,left:-9999,width:'auto',fontSize:input.css('fontSize'),fontFamily:input.css('fontFamily'),fontWeight:input.css('fontWeight'),letterSpacing:input.css('letterSpacing'),whiteSpace:'nowrap'}),testerId=$(this).attr('id')+'_autosize_tester';if(!$('#'+testerId).length>0){testSubject.attr('id',testerId);testSubject.appendTo('body');}
input.data('minwidth',minWidth);input.data('maxwidth',maxWidth);input.data('tester_id',testerId);input.css('width',minWidth);};$.fn.addTag=function(value,options){options=jQuery.extend({focus:false,callback:true},options);this.each(function(){var id=$(this).attr('id');var tagslist=$(this).val().split(delimiter[id]);if(tagslist[0]==''){tagslist=new Array();}
value=jQuery.trim(value);if(options.unique){var skipTag=$(this).tagExist(value);if(skipTag==true){$('#'+id+'_tag').addClass('not_valid');}}else{var skipTag=false;}
if(value!=''&&skipTag!=true){$('<span>').addClass('tag').append($('<span>').text(value).append('&nbsp;&nbsp;'),$('<a class="tagsinput-remove-link" title="Remove tag" text=""><i class="bUi-iCn-rMv-16 fS12" aria-hidden="true"></i></a>').click(function(){return $('#'+id).removeTag(escape(value));})).insertBefore('#'+id+'_addTag');tagslist.push(value);$('#'+id+'_tag').val('');if(options.focus){$('#'+id+'_tag').focus();}else{$('#'+id+'_tag').blur();}
$.fn.tagsInput.updateTagsField(this,tagslist);if(options.callback&&tags_callbacks[id]&&tags_callbacks[id]['onAddTag']){var f=tags_callbacks[id]['onAddTag'];f.call(this,value);}
if(tags_callbacks[id]&&tags_callbacks[id]['onChange'])
{var i=tagslist.length;var f=tags_callbacks[id]['onChange'];f.call(this,$(this),tagslist[i-1]);}}});return false;};$.fn.removeTag=function(value){value=unescape(value);this.each(function(){var id=$(this).attr('id');var old=$(this).val().split(delimiter[id]);$('#'+id+'_tagsinput .tag').remove();str='';for(i=0;i<old.length;i++){if(old[i]!=value){str=str+delimiter[id]+old[i];}}
$.fn.tagsInput.importTags(this,str);if(tags_callbacks[id]&&tags_callbacks[id]['onRemoveTag']){var f=tags_callbacks[id]['onRemoveTag'];f.call(this,value);}});return false;};$.fn.tagExist=function(val){var id=$(this).attr('id');var tagslist=$(this).val().split(delimiter[id]);return(jQuery.inArray(val,tagslist)>=0);};$.fn.importTags=function(str){id=$(this).attr('id');$('#'+id+'_tagsinput .tag').remove();$.fn.tagsInput.importTags(this,str);}
$.fn.tagsInput=function(options){var settings=jQuery.extend({interactive:true,defaultText:'',minChars:0,width:'',height:'',autocomplete:{selectFirst:false},'hide':true,'delimiter':',','unique':true,removeWithBackspace:true,placeholderColor:'#666666',autosize:true,comfortZone:20,inputPadding:6*2},options);this.each(function(){if(settings.hide){$(this).hide();}
var id=$(this).attr('id');if(!id||delimiter[$(this).attr('id')]){id=$(this).attr('id','tags'+new Date().getTime()).attr('id');}
var data=jQuery.extend({pid:id,real_input:'#'+id,holder:'#'+id+'_tagsinput',input_wrapper:'#'+id+'_addTag',fake_input:'#'+id+'_tag'},settings);delimiter[id]=data.delimiter;if(settings.onAddTag||settings.onRemoveTag||settings.onChange){tags_callbacks[id]=new Array();tags_callbacks[id]['onAddTag']=settings.onAddTag;tags_callbacks[id]['onRemoveTag']=settings.onRemoveTag;tags_callbacks[id]['onChange']=settings.onChange;}
var containerClass=$('#'+id).attr('class').replace('tagsinput','');var markup='<div id="'+id+'_tagsinput" class="tagsinput '+containerClass+'"><div class="tagsinput-add-container" id="'+id+'_addTag"><div class="tagsinput-add"><i class="bUi-iCn-pLs-16" aria-hidden="true"></i></div>';if(settings.interactive){markup=markup+'<input id="'+id+'_tag" class="tagInput" value="" data-default="'+settings.defaultText+'" />';}
markup=markup+'</div></div>';$(markup).insertAfter(this);var $tagInput=$('.tagInput');var $tagsinput=$('.tagsinput');$tagInput.focus(function(){$tagsinput.addClass('focus');})
$tagInput.blur(function(){$tagsinput.removeClass('focus');})
$(data.holder).css('width',settings.width);$(data.holder).css('min-height',settings.height);$(data.holder).css('height','100%');if($(data.real_input).val()!=''){$.fn.tagsInput.importTags($(data.real_input),$(data.real_input).val());}
if(settings.interactive){$(data.fake_input).val($(data.fake_input).attr('data-default'));$(data.fake_input).css('color',settings.placeholderColor);$(data.fake_input).resetAutosize(settings);$(data.holder).bind('click',data,function(event){$(event.data.fake_input).focus();});$(data.fake_input).bind('focus',data,function(event){if($(event.data.fake_input).val()==$(event.data.fake_input).attr('data-default')){$(event.data.fake_input).val('');}
$(event.data.fake_input).css('color','#000000');});if(settings.autocomplete_url!=undefined){autocomplete_options={source:settings.autocomplete_url};for(attrname in settings.autocomplete){autocomplete_options[attrname]=settings.autocomplete[attrname];}
if(jQuery.Autocompleter!==undefined){$(data.fake_input).autocomplete(settings.autocomplete_url,settings.autocomplete);$(data.fake_input).bind('result',data,function(event,data,formatted){if(data){$('#'+id).addTag(data[0]+"",{focus:true,unique:(settings.unique)});}});}else if(jQuery.ui.autocomplete!==undefined){$(data.fake_input).autocomplete(autocomplete_options);$(data.fake_input).bind('autocompleteselect',data,function(event,ui){$(event.data.real_input).addTag(ui.item.value,{focus:true,unique:(settings.unique)});return false;});}}else{$(data.fake_input).bind('blur',data,function(event){var d=$(this).attr('data-default');if($(event.data.fake_input).val()!=''&&$(event.data.fake_input).val()!=d){if((event.data.minChars<=$(event.data.fake_input).val().length)&&(!event.data.maxChars||(event.data.maxChars>=$(event.data.fake_input).val().length)))
$(event.data.real_input).addTag($(event.data.fake_input).val(),{focus:true,unique:(settings.unique)});}else{$(event.data.fake_input).val($(event.data.fake_input).attr('data-default'));$(event.data.fake_input).css('color',settings.placeholderColor);}
return false;});}
$(data.fake_input).bind('keypress',data,function(event){if(event.which==event.data.delimiter.charCodeAt(0)||event.which==13){event.preventDefault();if((event.data.minChars<=$(event.data.fake_input).val().length)&&(!event.data.maxChars||(event.data.maxChars>=$(event.data.fake_input).val().length)))
$(event.data.real_input).addTag($(event.data.fake_input).val(),{focus:true,unique:(settings.unique)});$(event.data.fake_input).resetAutosize(settings);return false;}else if(event.data.autosize){$(event.data.fake_input).doAutosize(settings);}});data.removeWithBackspace&&$(data.fake_input).bind('keydown',function(event)
{if(event.keyCode==8&&$(this).val()=='')
{event.preventDefault();var last_tag=$(this).closest('.tagsinput').find('.tag:last').text();var id=$(this).attr('id').replace(/_tag$/,'');last_tag=last_tag.replace(/[\s\u00a0]+x$/,'');$('#'+id).removeTag(escape(last_tag));$(this).trigger('focus');}});$(data.fake_input).blur();if(data.unique){$(data.fake_input).keydown(function(event){if(event.keyCode==8||String.fromCharCode(event.which).match(/\w+|[áéíóúÁÉÍÓÚñÑ,/]+/)){$(this).removeClass('not_valid');}});}}});return this;};$.fn.tagsInput.updateTagsField=function(obj,tagslist){var id=$(obj).attr('id');$(obj).val(tagslist.join(delimiter[id]));};$.fn.tagsInput.importTags=function(obj,val){$(obj).val('');var id=$(obj).attr('id');var tags=val.split(delimiter[id]);for(i=0;i<tags.length;i++){$(obj).addTag(tags[i],{focus:false,callback:false});}
if(tags_callbacks[id]&&tags_callbacks[id]['onChange'])
{var f=tags_callbacks[id]['onChange'];f.call(obj,obj,tags[i]);}};})(jQuery);;$.fn.bMalign=function(options){"use strict";var defaults={leftStyle:"position:absolute;padding-left:0px;right:auto;",rightStyle:"position:absolute;padding-left:12px;right:0px;",marginBottom:30};var settings=$.extend(true,{},defaults,options),el=$(this),$children=el.children(),contHeight=el.outerHeight(),w=$(window).width(),bmAlignOn=false,len=$children.length,t1,t2,i;var plugin={init:function(){this.build();this.resizeWindow();},build:function(){var i;if(w<980&&w>480){el.css({'position':'relative','height':contHeight});bmAlignOn=true;t1=$children.eq(0).outerHeight();t2=$children.eq(1).outerHeight();for(i=2;i<len;i++){if(t1>t2){$children.eq(i).css("cssText",settings.rightStyle);$children.eq(i).css("top",t2+'px');t2+=$children.eq(i).outerHeight();}
else{$children.eq(i).css("cssText",settings.leftStyle);$children.eq(i).css("top",t1+'px');t1+=$children.eq(i).outerHeight();}}
t1>t2?contHeight=t1:contHeight=t2;el.css('height',contHeight+settings.marginBottom+'px');}},resizeWindow:function(){var $this=this
$(window).on('resize',function(){w=$(window).width();$this.build();$this.destroy();});},destroy:function(){if(bmAlignOn&&(w>=980||w<=480)){el.add($children).removeAttr('style');bmAlignOn=false;}}};plugin.init();return this;};var isTouch=/Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(navigator.userAgent);var site=$('#site');function enableTouch(){if(isTouch){var site=$('#site');var distance,swipeThreshold=10,startCoords={},endCoords={};$('.sub_headder').bind('touchstart',function(e){$('.sub_headder').addClass('touchNav');endCoords=e.originalEvent.targetTouches[0];startCoords.pageX=e.originalEvent.targetTouches[0].pageX;$('.touchNav').bind('touchmove',function(e){e.preventDefault();e.stopPropagation();endCoords=e.originalEvent.targetTouches[0];});return false;}).bind('click touchend',function(e){e.preventDefault();e.stopPropagation();distance=endCoords.pageX-startCoords.pageX;if(distance>=swipeThreshold){$("#mast-head").css('display','block');site.addClass('translate');}
else if(distance<=-swipeThreshold){if(site.hasClass('translate')){site.removeClass('translate');setTimeout(function(){$("#mast-head").css('display','none');},350);}}
$('.touchNav').off('touchmove').removeClass('touch');});}};function setnavHeight(){if(isTouch){var navbarHeight=$(window).height();$('.navbar').css('height',navbarHeight);}};$(document).ready(function(e){var site=$('#site');setnavHeight();$(window).on('orientationchange',function(event){setnavHeight()});enableTouch();$('.btn-navbar').on('click touchend',function(){if(site.hasClass('translate')){site.removeClass('translate');setTimeout(function(){$("#mast-head").css('display','none');},350);}else{$("#mast-head").css('display','block');site.addClass('translate');}});$(window).on("resize orientationchange",function(){if($(window).width()>979){$("#mast-head").css('display','block');site.removeClass('translate');}else if(!site.hasClass('translate')){$("#mast-head").css('display','none');}});});;$.fn.changeText=function(options){"use strict";var defaults=$.extend({dT:'Follow Question',fT:'Following',sT:'Unfollow',icon:true,aCl:'bUi-iCn-oK-16',bCl:'bUi-iCn-rMv-12'},options);var settings=$.extend(true,{},defaults,options),cL=false,w;$(this).each(function(index,element){$(this).on('click',function(){if(cL==false){$(this).text(settings.fT);if(settings.icon==true){$(this).find('[class^="bUi-iCn-"]').remove();$(this).prepend('<i class="'+settings.aCl+' mRr5 fS12" aria-hidden="true"></i>')}
w=$(this).width();$(this).css({'transition':'none','width':w});cL=true;}
else{$(this).css('width','auto');$(this).text(settings.dT);if(settings.icon==true){$(this).find('[class^="bUi-iCn-"]').remove();}
cL=false;}});$(this).on('mouseover',function(){if(cL==true){$(this).text(settings.sT);if(settings.icon==true){$(this).find('[class^="bUi-iCn-"]').remove();$(this).prepend('<i class="'+settings.bCl+' mRr5 fS11" aria-hidden="true"></i>')}}})
$(this).on('mouseout',function(){if(cL==true){$(this).text(settings.fT);if(settings.icon==true){$(this).find('[class^="bUi-iCn-"]').remove();$(this).prepend('<i class="'+settings.aCl+' mRr5 fS12" aria-hidden="true"></i>')}}})});return this;};;$.fn.moreNav=function(options){"use strict";var defaults=$.extend({html:'<li id="more" class="dropdown">\
                	<div class="rLvE">\
						<a href="#" class="dropdown-toggle">More<b class="caret"></b></a>\
                        <ul class="dropdown-menu pLrT more"></ul>\
				</div>',maxWidth:1200,minWidth:980},options);var settings=$.extend(true,{},defaults,options),$this=$(this),w,mW,flag=false,des=false,newW=settings.maxWidth,dRcHw=0;var plugin={init:function(){plugin.resizeWindow();$(window).on('resize',function(){setTimeout(function(){plugin.resizeWindow()},350);});},resizeWindow:function(){w=$(window).width();mW=$this.width();if((w>=settings.maxWidth)&&(mW>settings.maxWidth)){plugin.build();}
else if(w<=mW){plugin.build();}
else if((w>settings.minWidth&&w<mW)&&(des==true&&flag==false)){plugin.build();}
else if((newW+dRcHw)<=mW){plugin.rebuild();};if(w<settings.minWidth)
plugin.destroy();},build:function(){var lEn=$this.children().length;var lW=100,mN=0,oVcH;for(var i=0;i<lEn-1;i++){lW+=$this.children().eq(i).width();if(lW>=mW||lW>=settings.maxWidth)
break;mN=i;}
mN=mN-1;oVcH=$this.children().eq(mN).nextUntil($this.children().eq(lEn-1));if(flag==false){var lCh=$this.children().eq(lEn-1);$this.children().eq(lEn-1).after(settings.html);$this.find('.more').html(lCh)
flag=true;}
dRcHw=$this.children().eq(lEn-2).outerWidth();$this.find('.more').prepend(oVcH);newW=$this.width();},rebuild:function(){if($this.find('.more').children().length>1){var lEn=$this.children().length;var dRfC=$this.find('.more').children().eq(0);$this.children().eq(lEn-1).before(dRfC);newW=newW+dRcHw;}
else{plugin.destroy();newW=$this.width();}},destroy:function(){if(flag==true){var addedCh=$this.find('.more').children();$this.append(addedCh);$this.find('#more').remove();des=true;flag=false;}}};plugin.init();return this;};$.fn.doThis=function(func){this.length&&func.apply(this);return this;}
$.fn.addCl=function(cl){$(this).click(function(){$(this).parent().addClass(cl);})
return this;}
$.fn.setrSpVWidth=function(w){$(this).each(function(index,element){var fLxcOnTWidth=$(this).width();$(this).find('img').css('width',fLxcOnTWidth+1+w);});return this;}
$.fn.fLxVideoWidth=function(w,h){$(this).each(function(index,element){var r=w/h;var fLxVideoW=$(this).width();var height=fLxVideoW/r;$(this).find('iframe').css({'width':fLxVideoW+1,'height':height});});return this;}
$.fn.setfTrDtXtHeight=function(){$(this).each(function(){if($(this).hasClass('aDpTv')&&!$(this).hasClass('tXt-oTsD')){aDpTvHeight=$(this).height();$(this).find('.fTrD-tXt').css('height',aDpTvHeight);}})
return this;}
$.fn.setrSpVHeight=function(mDaLt){var w=$(window).width();$(this).each(function(index,element){var fLxcOnTWidth=$(this).height();$(this).find('img').css('height',fLxcOnTWidth+1);});return this;}
$.fn.classToggle=function(){$(this).click(function(){$(this).toggleClass('active');})
return this;}
$.fn.classTogglep=function(){$(this).click(function(){$(this).parent().toggleClass('active');})
return this;}
$.fn.iconToggle=function(){$(this).each(function(index,element){var cLlT=$(this).find('[class^="bUi-iCn-"]:last').attr('class').split(/\s+/),oC,nC=$(this).attr('data-toggle-icon');for(var i=0;i<cLlT.length;i++){if(cLlT[i].match(/bUi-iCn-/i)){oC=cLlT[i];}};var oB=$(this).find('[class^="bUi-iCn-"]:last');$(this).click(function(){oB.toggleClass(oC);if(oB.hasClass(oC))
oB.removeClass(nC);else
oB.addClass(nC);})});return this;}
$.fn.collapseM480=function(){var w=$(window).width();var el=$(this).attr('data-target');if(w<=480){if($(el).hasClass('in'))$(el).removeClass('in');}
else{if(!$(el).hasClass('in'))$(el).addClass('in');$(el).removeAttr('style');}
return this;}
$.fn.fold=function(){var w=$(window).width();el=$(this).parent().find('.fLdED');if(w<=480){if(el.height()>200)el.addClass('on',300);}
else el.removeClass("on",300);$(window).on("resize orientationchange",(function(){w=$(window).width();if(w<=480){if(el.height()>200)el.addClass('on',300);}
else el.removeClass('on',300);}))
$(this).click(function(){el.toggleClass('on',300);if(!el.hasClass('on'))$(this).find('a').html('Read Less <i class="bUi-iCn-aNg-t-12" aria-hidden="true"></i>');else $(this).find('a').html('Read More <i class="bUi-iCn-aNg-b-12" aria-hidden="true"></i>')})
return this;}
$.fn.autoFocus=function(){$(this).focus(function(){$(this).closest('form').addClass('hS-fCs');})
return this;}
$.fn.autoExpand=function(){var $ta=this,$clone,timer=null,mh=70;function resize(){var h=$clone.val($ta.val()+'\n').get(0).scrollHeight;$ta.css('height',(h<mh)?'':h+18);};function onkeydown(event){this.scrollTop=0;clearTimeout(timer);timer=setTimeout(resize,50);};if($clone)$clone.remove();$clone=$ta.clone().removeAttr('id').removeAttr('name').css({padding:0,margin:0}).addClass('cLn').attr('tabindex','-1').insertAfter($ta);$ta.css('overflow','hidden').off('keydown.expand').on('keydown.expand',onkeydown);return $ta;};$(function(){$("[data-toggle='switch']").doThis(function(){this.wrap('<div class="switch" />').parent().bootstrapSwitch();});$(".tagsinput").doThis(function(){this.tagsInput();;});$("[data-toggle='popover']").doThis(function(){this.popover();});$('.sD-bR').bMalign();$('#moreNav').moreNav();$('[data-toggle-class]').doThis(function(){this.classToggle();});$('[data-toggle-class-p]').doThis(function(){this.classTogglep();});$('.fLd-bTn').doThis(function(){this.fold();});$('[data-expand="true"]').doThis(function(){this.autoExpand();});$('[data-focus="true"]').doThis(function(){this.autoFocus();});$('.bM-sLt').doThis(function(){this.bUiSlCt();});$('.uSr-aCnT-sLt').doThis(function(){this.bUiSlCt({style:'btn-light vP'});});$('.bUiSlCt').doThis(function(){this.bUiSlCt({style:''});});$('.bUiSlCt-wHt').doThis(function(){this.bUiSlCt({style:'btn-light'});});$('.bUiSlCtbtn-light').doThis(function(){this.bUiSlCt({style:'btn-light btn-small pLrT'});});$('.discussion').doThis(function(){this.bUiSlCt({style:'btn-light vP pLlTp w100pP h38p tEx-aLl'});});$('.bTn-lT-sLcT').doThis(function(){this.bUiSlCt({style:'btn-light w100P h40 tXt-lT bXShD0'});});$('.bUiSlCtbtn-link').doThis(function(){this.bUiSlCt({style:'btn-link'});});$('.sLcFlTr').doThis(function(){this.bUiSlCt({style:'btn-link, w100P tXt-lT fS11 fW-bLd'});});$('.tBlbUiSlCtbtn-light').doThis(function(){this.bUiSlCt({style:'btn-light btn-small'});});$('[data-toggle-icon]').doThis(function(){this.iconToggle();});$('.browse').doThis(function(){this.collapseM480();});$('.sHw-sRcH').doThis(function(){this.addCl('eXpD');});$('#fLw_btn').doThis(function(){this.changeText();});$('.fLxiMgW').setrSpVWidth(0);$('.fLxiMgW30').setrSpVWidth(30);$('.fLxiMgH').setrSpVHeight('mDa-lT');$('.fLxVdO').doThis(function(){this.fLxVideoWidth(560,315);});$('.fTrD-bL').setfTrDtXtHeight();$(window).load(function(){$('.sD-bR').bMalign();});$(window).on("resize orientationchange",(function(){$('.fLxiMgW').setrSpVWidth(0);$('.fLxiMgW30').setrSpVWidth(30);$('.fLxiMgH').setrSpVHeight('mDa-lT');$('.fLxVdO').doThis(function(){this.fLxVideoWidth(560,315);});$('.fTrD-bL').setfTrDtXtHeight();$('.browse').doThis(function(){this.collapseM480();});$('.fTrDfLxiMgH').setrSpVHeight('fTrD-bL');}))
var views=$('#media-toggle');var figureItems=$('.main').find('.modulesBrowseData');var thumbnaiItem=$('.modulesBrowseData').find('.mDa-oT');function setGridColumn(){$('.mDa-gD').each(function(index,element){if(!$(this).hasClass('dSgDwDt')){var gridColumnWidth=$(this).find('.mDa').width();$(this).find('.mDa .mDa-oT').css({'width':''+gridColumnWidth+'','height':'auto'});}});}
views.on('click','.c-lT',function(){views.find('.btn').removeClass('active');$(this).addClass('active');figureItems.removeClass('mDa-gD mDa-oT-tP').addClass('mDa-lT mDa-oT-lT');if(figureItems.children('li').hasClass('mDa-gRp')){figureItems.find('.mDa-gRp > ul').removeClass('pDfX')}
else{figureItems.removeClass('pDfX');}
thumbnaiItem.css('width','auto');$('.fLxiMgH').setrSpVHeight('mDa-lT');$('.fLxiMgW').setrSpVWidth(0);$('.fLxiMgW30').setrSpVWidth(30);});views.on('click','.c-gD',function(){views.find('.btn').removeClass('active');$(this).addClass('active');figureItems.removeClass('mDa-lT mDa-oT-lT').addClass('mDa-gD mDa-oT-tP');if(figureItems.children('li').hasClass('mDa-gRp')){figureItems.find('.mDa-gRp > ul').addClass('pDfX')}
else{figureItems.addClass('pDfX');}
$('.fLxiMgH').setrSpVHeight('mDa-lT');$('.fLxiMgW').setrSpVWidth(0);$('.fLxiMgW30').setrSpVWidth(30);setGridColumn();});setGridColumn();$(window).on("resize orientationchange",(function(){setGridColumn();}))});(function($,document,window){var
defaults={transition:"elastic",speed:300,width:false,initialWidth:"600",innerWidth:false,maxWidth:false,height:false,initialHeight:"450",innerHeight:false,maxHeight:false,scalePhotos:true,scrolling:false,inline:false,html:false,iframe:false,fastIframe:true,photo:false,href:false,title:false,rel:false,opacity:0.6,preloading:true,current:"image {current} of {total}",previous:"previous",next:"next",close:"close",open:false,returnFocus:true,reposition:true,loop:true,slideshow:false,slideshowAuto:true,slideshowSpeed:2500,slideshowStart:"start slideshow",slideshowStop:"stop slideshow",onOpen:false,onLoad:false,onComplete:false,onCleanup:false,onClosed:false,overlayClose:false,escKey:false,arrowKey:true,top:false,bottom:false,left:false,right:false,fixed:false,data:undefined},colorbox='colorbox',prefix='bm',boxElement=prefix+'Element',event_open=prefix+'_open',event_load=prefix+'_load',event_complete=prefix+'_complete',event_cleanup=prefix+'_cleanup',event_closed=prefix+'_closed',event_purge=prefix+'_purge',isIE=!$.support.opacity&&!$.support.style,isIE6=isIE&&!window.XMLHttpRequest,event_ie6=prefix+'_IE6',$overlay,$box,$wrap,$content,$topBorder,$leftBorder,$rightBorder,$bottomBorder,$related,$window,$loaded,$loadingBay,$loadingOverlay,$title,$current,$slideshow,$next,$prev,$close,$groupControls,settings,interfaceHeight,interfaceWidth,loadedHeight,loadedWidth,element,index,photo,open,active,closing,loadingTimer,publicMethod,div="div",init;function $tag(tag,id,css){var element=document.createElement(tag);if(id){element.id=prefix+id;}
if(css){element.style.cssText=css;}
return $(element);}
function getIndex(increment){var
max=$related.length,newIndex=(index+increment)%max;return(newIndex<0)?max+newIndex:newIndex;}
function setSize(size,dimension){return Math.round((/%/.test(size)?((dimension==='x'?$window.width():$window.height())/100):1)*parseInt(size,10));}
function isImage(url){return settings.photo||/\.(gif|png|jpe?g|bmp|ico)((#|\?).*)?$/i.test(url);}
function makeSettings(){var i;settings=$.extend({},$.data(element,colorbox));for(i in settings){if($.isFunction(settings[i])&&i.slice(0,2)!=='on'){settings[i]=settings[i].call(element);}}
settings.rel=settings.rel||element.rel||'nofollow';settings.href=settings.href||$(element).attr('href');settings.title=settings.title||element.title;if(typeof settings.href==="string"){settings.href=$.trim(settings.href);}}
function trigger(event,callback){$.event.trigger(event);if(callback){callback.call(element);}}
function slideshow(){var
timeOut,className=prefix+"Slideshow_",click="click."+prefix,start,stop,clear;if(settings.slideshow&&$related[1]){start=function(){$slideshow.text(settings.slideshowStop).unbind(click).bind(event_complete,function(){if(settings.loop||$related[index+1]){timeOut=setTimeout(publicMethod.next,settings.slideshowSpeed);}}).bind(event_load,function(){clearTimeout(timeOut);}).one(click+' '+event_cleanup,stop);$box.removeClass(className+"off").addClass(className+"on");timeOut=setTimeout(publicMethod.next,settings.slideshowSpeed);};stop=function(){clearTimeout(timeOut);$slideshow.text(settings.slideshowStart).unbind([event_complete,event_load,event_cleanup,click].join(' ')).one(click,function(){publicMethod.next();start();});$box.removeClass(className+"on").addClass(className+"off");};if(settings.slideshowAuto){start();}else{stop();}}else{$box.removeClass(className+"off "+className+"on");}}
function launch(target){if(!closing){element=target;makeSettings();$related=$(element);index=0;if(settings.rel!=='nofollow'){$related=$('.'+boxElement).filter(function(){var relRelated=$.data(this,colorbox).rel||this.rel;return(relRelated===settings.rel);});index=$related.index(element);if(index===-1){$related=$related.add(element);index=$related.length-1;}}
if(!open){open=active=true;$box.show();if(settings.returnFocus){$(element).blur().one(event_closed,function(){$(this).focus();});}
$overlay.css({"opacity":+settings.opacity,"cursor":settings.overlayClose?"pointer":"auto"}).show();settings.w=setSize(settings.initialWidth,'x');settings.h=setSize(settings.initialHeight,'y');publicMethod.position();if(isIE6){$window.bind('resize.'+event_ie6+' scroll.'+event_ie6,function(){$overlay.css({width:$window.width(),height:$window.height(),top:$window.scrollTop(),left:$window.scrollLeft()});}).trigger('resize.'+event_ie6);}
trigger(event_open,settings.onOpen);$groupControls.add($title).hide();$close.html(settings.close).show();}
publicMethod.load(true);}}
function appendHTML(){if(!$box&&document.body){init=false;$window=$(window);$box=$tag(div).attr({id:colorbox,'class':isIE?prefix+(isIE6?'IE6':'IE'):''}).hide();$overlay=$tag(div,"Overlay",isIE6?'position:absolute':'').hide();$wrap=$tag(div,"Wrapper");$content=$tag(div,"Content").append($loaded=$tag(div,"LoadedContent",'width:0; height:0; overflow:hidden'),$loadingOverlay=$tag(div,"LoadingOverlay").add($tag(div,"LoadingGraphic")),$title=$tag(div,"Title"),$current=$tag(div,"Current"),$next=$tag(div,"Next"),$prev=$tag(div,"Previous"),$slideshow=$tag(div,"Slideshow").bind(event_open,slideshow),$close=$tag(div,"Close").addClass("tttxt"));$wrap.append($tag(div).append($tag(div,"TopLeft"),$topBorder=$tag(div,"TopCenter"),$tag(div,"TopRight")),$tag(div,false,'clear:left').append($leftBorder=$tag(div,"MiddleLeft"),$content,$rightBorder=$tag(div,"MiddleRight")),$tag(div,false,'clear:left').append($tag(div,"BottomLeft"),$bottomBorder=$tag(div,"BottomCenter"),$tag(div,"BottomRight"))).find('div div').css({'float':'left'});$loadingBay=$tag(div,false,'position:absolute; width:9999px; visibility:hidden; display:none');$groupControls=$next.add($prev).add($current).add($slideshow);$(document.body).append($overlay,$box.append($wrap,$loadingBay));}}
function addBindings(){if($box){if(!init){init=true;interfaceHeight=$topBorder.height()+$bottomBorder.height()+$content.outerHeight(true)-$content.height();interfaceWidth=$leftBorder.width()+$rightBorder.width()+$content.outerWidth(true)-$content.width();loadedHeight=$loaded.outerHeight(true);loadedWidth=$loaded.outerWidth(true);$box.css({"padding-bottom":interfaceHeight,"padding-right":interfaceWidth});$next.click(function(){publicMethod.next();});$prev.click(function(){publicMethod.prev();});$close.click(function(){publicMethod.close();});$overlay.click(function(){if(settings.overlayClose){publicMethod.close();}});$(document).bind('keydown.'+prefix,function(e){var key=e.keyCode;if(open&&settings.escKey&&key===27){e.preventDefault();publicMethod.close();}
if(open&&settings.arrowKey&&$related[1]){if(key===37){e.preventDefault();$prev.click();}else if(key===39){e.preventDefault();$next.click();}}});$('.'+boxElement,document).live('click',function(e){if(!(e.which>1||e.shiftKey||e.altKey||e.metaKey)){e.preventDefault();launch(this);}});}
return true;}
return false;}
if($.colorbox){return;}
$(appendHTML);publicMethod=$.fn[colorbox]=$[colorbox]=function(options,callback){var $this=this;options=options||{};appendHTML();if(addBindings()){if(!$this[0]){if($this.selector){return $this;}
$this=$('<a/>');options.open=true;}
if(callback){options.onComplete=callback;}
$this.each(function(){$.data(this,colorbox,$.extend({},$.data(this,colorbox)||defaults,options));}).addClass(boxElement);if(($.isFunction(options.open)&&options.open.call($this))||options.open){launch($this[0]);}}
return $this;};publicMethod.position=function(speed,loadedCallback){var
top=0,left=0,offset=$box.offset(),scrollTop=$window.scrollTop(),scrollLeft=$window.scrollLeft();$window.unbind('resize.'+prefix);$box.css({top:-9e4,left:-9e4});if(settings.fixed&&!isIE6){offset.top-=scrollTop;offset.left-=scrollLeft;$box.css({position:'fixed'});}else{top=scrollTop;left=scrollLeft;$box.css({position:'absolute'});}
if(settings.right!==false){left+=Math.max($window.width()-settings.w-loadedWidth-interfaceWidth-setSize(settings.right,'x'),0);}else if(settings.left!==false){left+=setSize(settings.left,'x');}else{left+=Math.round(Math.max($window.width()-settings.w-loadedWidth-interfaceWidth,0)/2);}
if(settings.bottom!==false){top+=Math.max($window.height()-settings.h-loadedHeight-interfaceHeight-setSize(settings.bottom,'y'),0);}else if(settings.top!==false){top+=setSize(settings.top,'y');}else{top=Math.round(Math.max($window.height()-settings.h-loadedHeight-interfaceHeight,0)/2);}
$box.css({top:offset.top,left:offset.left});speed=($box.width()===settings.w+loadedWidth&&$box.height()===settings.h+loadedHeight)?0:speed||0;$wrap[0].style.width=$wrap[0].style.height="9999px";function modalDimensions(that){$topBorder[0].style.width=$bottomBorder[0].style.width=$content[0].style.width=that.style.width;$content[0].style.height=$leftBorder[0].style.height=$rightBorder[0].style.height=that.style.height;}
$box.dequeue().animate({width:settings.w+loadedWidth,height:settings.h+loadedHeight,top:top,left:left},{duration:speed,complete:function(){modalDimensions(this);active=false;$wrap[0].style.width=(settings.w+loadedWidth+interfaceWidth)+"px";$wrap[0].style.height=(settings.h+loadedHeight+interfaceHeight)+"px";if(settings.reposition){setTimeout(function(){$window.bind('resize.'+prefix,publicMethod.position);},1);}
if(loadedCallback){loadedCallback();}},step:function(){modalDimensions(this);}});};publicMethod.resize=function(options){if(open){options=options||{};if(options.width){settings.w=setSize(options.width,'x')-loadedWidth-interfaceWidth;}
if(options.innerWidth){settings.w=setSize(options.innerWidth,'x');}
$loaded.css({width:settings.w});if(options.height){settings.h=setSize(options.height,'y')-loadedHeight-interfaceHeight;}
if(options.innerHeight){settings.h=setSize(options.innerHeight,'y');}
if(!options.innerHeight&&!options.height){$loaded.css({height:"auto"});settings.h=$loaded.height();}
$loaded.css({height:settings.h});publicMethod.position(settings.transition==="none"?0:0);}};publicMethod.prep=function(object){if(!open){return;}
var callback,speed=settings.transition==="none"?0:settings.speed;$loaded.remove();$loaded=$tag(div,'LoadedContent').append(object);function getWidth(){settings.w=settings.w||$loaded.width();settings.w=settings.mw&&settings.mw<settings.w?settings.mw:settings.w;return settings.w;}
function getHeight(){settings.h=settings.h||$loaded.height();settings.h=settings.mh&&settings.mh<settings.h?settings.mh:settings.h;return settings.h;}
$loaded.hide().appendTo($loadingBay.show()).css({width:getWidth(),overflow:settings.scrolling?'auto':'hidden'}).css({height:getHeight()}).prependTo($content);$loadingBay.hide();$(photo).css({'float':'none'});if(isIE6){$('select').not($box.find('select')).filter(function(){return this.style.visibility!=='hidden';}).css({'visibility':'hidden'}).one(event_cleanup,function(){this.style.visibility='inherit';});}
callback=function(){var preload,i,total=$related.length,iframe,frameBorder='frameBorder',allowTransparency='allowTransparency',complete,src,img;if(!open){return;}
function removeFilter(){if(isIE){$box[0].style.removeAttribute('filter');}}
complete=function(){clearTimeout(loadingTimer);$loadingOverlay.hide();trigger(event_complete,settings.onComplete);};if(isIE){if(photo){$loaded.fadeIn(100);}}
$title.html(settings.title).add($loaded).show();if(total>1){if(typeof settings.current==="string"){$current.html(settings.current.replace('{current}',index+1).replace('{total}',total)).show();}
$next[(settings.loop||index<total-1)?"show":"hide"]().html(settings.next);$prev[(settings.loop||index)?"show":"hide"]().html(settings.previous);if(settings.slideshow){$slideshow.show();}
if(settings.preloading){preload=[getIndex(-1),getIndex(1)];while(i=$related[preload.pop()]){src=$.data(i,colorbox).href||i.href;if($.isFunction(src)){src=src.call(i);}
if(isImage(src)){img=new Image();img.src=src;}}}}else{$groupControls.hide();}
if(settings.iframe){iframe=$tag('iframe')[0];if(frameBorder in iframe){iframe[frameBorder]=0;}
if(allowTransparency in iframe){iframe[allowTransparency]="true";}
iframe.name=prefix+(+new Date());if(settings.fastIframe){complete();}else{$(iframe).one('load',complete);}
iframe.src=settings.href;if(!settings.scrolling){iframe.scrolling="no";}
$(iframe).addClass(prefix+'Iframe').appendTo($loaded).one(event_purge,function(){iframe.src="//about:blank";});}else{complete();}
if(settings.transition==='fade'){$box.fadeTo(speed,1,removeFilter);}else{removeFilter();}};if(settings.transition==='fade'){$box.fadeTo(speed,0,function(){publicMethod.position(0,callback);});}else{publicMethod.position(speed,callback);}};publicMethod.load=function(launched){var href,setResize,prep=publicMethod.prep;active=true;photo=false;element=$related[index];if(!launched){makeSettings();}
trigger(event_purge);trigger(event_load,settings.onLoad);settings.h=settings.height?setSize(settings.height,'y')-loadedHeight-interfaceHeight:settings.innerHeight&&setSize(settings.innerHeight,'y');settings.w=settings.width?setSize(settings.width,'x')-loadedWidth-interfaceWidth:settings.innerWidth&&setSize(settings.innerWidth,'x');settings.mw=settings.w;settings.mh=settings.h;if(settings.maxWidth){settings.mw=setSize(settings.maxWidth,'x')-loadedWidth-interfaceWidth;settings.mw=settings.w&&settings.w<settings.mw?settings.w:settings.mw;}
if(settings.maxHeight){settings.mh=setSize(settings.maxHeight,'y')-loadedHeight-interfaceHeight;settings.mh=settings.h&&settings.h<settings.mh?settings.h:settings.mh;}
href=settings.href;loadingTimer=setTimeout(function(){$loadingOverlay.show();},100);if(settings.inline){$tag(div).hide().insertBefore($(href)[0]).one(event_purge,function(){$(this).replaceWith($loaded.children());});prep($(href));}else if(settings.iframe){prep(" ");}else if(settings.html){prep(settings.html);}else if(isImage(href)){$(photo=new Image()).addClass(prefix+'Photo').error(function(){settings.title=false;prep($tag(div,'Error').text('This image could not be loaded'));}).load(function(){var percent;photo.onload=null;if(settings.scalePhotos){setResize=function(){photo.height-=photo.height*percent;photo.width-=photo.width*percent;};if(settings.mw&&photo.width>settings.mw){percent=(photo.width-settings.mw)/photo.width;setResize();}
if(settings.mh&&photo.height>settings.mh){percent=(photo.height-settings.mh)/photo.height;setResize();}}
if(settings.h){photo.style.marginTop=Math.max(settings.h-photo.height,0)/2+'px';}
if($related[1]&&(settings.loop||$related[index+1])){photo.style.cursor='pointer';photo.onclick=function(){publicMethod.next();};}
if(isIE){photo.style.msInterpolationMode='bicubic';}
setTimeout(function(){prep(photo);},1);});setTimeout(function(){photo.src=href;},1);}else if(href){$loadingBay.load(href,settings.data,function(data,status,xhr){prep(status==='error'?$tag(div,'Error').text('Request unsuccessful: '+xhr.statusText):$(this).contents());});}};publicMethod.next=function(){if(!active&&$related[1]&&(settings.loop||$related[index+1])){index=getIndex(1);publicMethod.load();}};publicMethod.prev=function(){if(!active&&$related[1]&&(settings.loop||index)){index=getIndex(-1);publicMethod.load();}};publicMethod.close=function(){if(open&&!closing){closing=true;open=false;trigger(event_cleanup,settings.onCleanup);$window.unbind('.'+prefix+' .'+event_ie6);$overlay.fadeTo(200,0);$box.stop().fadeTo(300,0,function(){$box.add($overlay).css({'opacity':1,cursor:'auto'}).hide();trigger(event_purge);$loaded.remove();setTimeout(function(){closing=false;trigger(event_closed,settings.onClosed);},1);});}};publicMethod.remove=function(){$([]).add($box).add($overlay).remove();$box=null;$('.'+boxElement).removeData(colorbox).removeClass(boxElement).die();};publicMethod.element=function(){return $(element);};publicMethod.settings=defaults;}(jQuery,document,this));(function(){var global=this;if(global.postscribe){return;}
var DEBUG=true;var DEBUG_CHUNK=false;var slice=Array.prototype.slice;function doNothing(){}
function isFunction(x){return"function"===typeof x;}
function each(arr,fn,_this){var i,len=(arr&&arr.length)||0;for(i=0;i<len;i++){fn.call(_this,arr[i],i);}}
function eachKey(obj,fn,_this){var key;for(key in obj){if(obj.hasOwnProperty(key)){fn.call(_this,key,obj[key]);}}}
function set(obj,props){eachKey(props,function(key,value){obj[key]=value;});return obj;}
function defaults(options,_defaults){options=options||{};eachKey(_defaults,function(key,val){if(options[key]==null){options[key]=val;}});return options;}
function toArray(obj){try{return slice.call(obj);}catch(e){var ret=[];each(obj,function(val){ret.push(val);});return ret;}}
function isScript(tok){return(/^script$/i).test(tok.tagName);}
var WriteStream=(function(){var BASEATTR='data-ps-';function data(el,name,value){var attr=BASEATTR+name;if(arguments.length===2){var val=el.getAttribute(attr);return val==null?val:String(val);}else if(value!=null&&value!==''){el.setAttribute(attr,value);}else{el.removeAttribute(attr);}}
function WriteStream(root,options){var doc=root.ownerDocument;set(this,{root:root,options:options,win:doc.defaultView||doc.parentWindow,doc:doc,parser:global.htmlParser('',{autoFix:true}),actuals:[root],proxyHistory:'',proxyRoot:doc.createElement(root.nodeName),scriptStack:[],writeQueue:[]});data(this.proxyRoot,'proxyof',0);}
WriteStream.prototype.write=function(){[].push.apply(this.writeQueue,arguments);var arg;while(!this.deferredRemote&&this.writeQueue.length){arg=this.writeQueue.shift();if(isFunction(arg)){this.callFunction(arg);}else{this.writeImpl(arg);}}};WriteStream.prototype.callFunction=function(fn){var tok={type:"function",value:fn.name||fn.toString()};this.onScriptStart(tok);fn.call(this.win,this.doc);this.onScriptDone(tok);};WriteStream.prototype.writeImpl=function(html){this.parser.append(html);var tok,tokens=[];while((tok=this.parser.readToken())&&!isScript(tok)){tokens.push(tok);}
this.writeStaticTokens(tokens);if(tok){this.handleScriptToken(tok);}};WriteStream.prototype.writeStaticTokens=function(tokens){var chunk=this.buildChunk(tokens);if(!chunk.actual){return;}
chunk.html=this.proxyHistory+chunk.actual;this.proxyHistory+=chunk.proxy;this.proxyRoot.innerHTML=chunk.html;if(DEBUG_CHUNK){chunk.proxyInnerHTML=this.proxyRoot.innerHTML;}
this.walkChunk();if(DEBUG_CHUNK){chunk.actualInnerHTML=this.root.innerHTML;}
return chunk;};WriteStream.prototype.buildChunk=function(tokens){var nextId=this.actuals.length,raw=[],actual=[],proxy=[];each(tokens,function(tok){raw.push(tok.text);if(tok.attrs){if(!(/^noscript$/i).test(tok.tagName)){var id=nextId++;actual.push(tok.text.replace(/(\/?>)/,' '+BASEATTR+'id='+id+' $1'));if(tok.attrs.id!=="ps-script"){proxy.push(tok.type==='atomicTag'?'':'<'+tok.tagName+' '+BASEATTR+'proxyof='+id+(tok.unary?'/>':'>'));}}}else{actual.push(tok.text);proxy.push(tok.type==='endTag'?tok.text:'');}});return{tokens:tokens,raw:raw.join(''),actual:actual.join(''),proxy:proxy.join('')};};WriteStream.prototype.walkChunk=function(){var node,stack=[this.proxyRoot];while((node=stack.shift())!=null){var isElement=node.nodeType===1;var isProxy=isElement&&data(node,'proxyof');if(!isProxy){if(isElement){this.actuals[data(node,'id')]=node;data(node,'id',null);}
var parentIsProxyOf=node.parentNode&&data(node.parentNode,'proxyof');if(parentIsProxyOf){this.actuals[parentIsProxyOf].appendChild(node);}}
stack.unshift.apply(stack,toArray(node.childNodes));}};WriteStream.prototype.handleScriptToken=function(tok){var remainder=this.parser.clear();if(remainder){this.writeQueue.unshift(remainder);}
tok.src=tok.attrs.src||tok.attrs.SRC;if(tok.src&&this.scriptStack.length){this.deferredRemote=tok;}else{this.onScriptStart(tok);}
var _this=this;this.writeScriptToken(tok,function(){_this.onScriptDone(tok);});};WriteStream.prototype.onScriptStart=function(tok){tok.outerWrites=this.writeQueue;this.writeQueue=[];this.scriptStack.unshift(tok);};WriteStream.prototype.onScriptDone=function(tok){if(tok!==this.scriptStack[0]){this.options.error({message:"Bad script nesting or script finished twice"});return;}
this.scriptStack.shift();this.write.apply(this,tok.outerWrites);if(!this.scriptStack.length&&this.deferredRemote){this.onScriptStart(this.deferredRemote);this.deferredRemote=null;}};WriteStream.prototype.writeScriptToken=function(tok,done){var el=this.buildScript(tok);if(tok.src){el.src=tok.src;this.scriptLoadHandler(el,done);}
try{this.insertScript(el);if(!tok.src){done();}}catch(e){this.options.error(e);done();}};WriteStream.prototype.buildScript=function(tok){var el=this.doc.createElement(tok.tagName);eachKey(tok.attrs,function(name,value){el.setAttribute(name,value);});if(tok.content){el.text=tok.content;}
return el;};WriteStream.prototype.insertScript=function(el){this.writeImpl('<span id="ps-script"/>');var cursor=this.doc.getElementById("ps-script");cursor.parentNode.replaceChild(el,cursor);};WriteStream.prototype.scriptLoadHandler=function(el,done){function cleanup(){el=el.onload=el.onreadystatechange=el.onerror=null;done();}
var error=this.options.error;set(el,{onload:function(){cleanup();},onreadystatechange:function(){if(/^(loaded|complete)$/.test(el.readyState)){cleanup();}},onerror:function(){error({message:'remote script failed '+el.src});cleanup();}});};return WriteStream;}());var postscribe=(function(){var nextId=0;var queue=[];var active=null;function nextStream(){var args=queue.shift();if(args){args.stream=runStream.apply(null,args);}}
function runStream(el,html,options){active=new WriteStream(el,options);active.id=nextId++;active.name=options.name||active.id;postscribe.streams[active.name]=active;var doc=el.ownerDocument;var stash={write:doc.write,writeln:doc.writeln};function write(str){str=options.beforeWrite(str);active.write(str);options.afterWrite(str);}
set(doc,{write:write,writeln:function(str){write(str+'\n');}});var oldOnError=active.win.onerror||doNothing;active.win.onerror=function(msg,url,line){options.error({msg:msg+' - '+url+':'+line});oldOnError.apply(active.win,arguments);};active.write(html,function streamDone(){set(doc,stash);active.win.onerror=oldOnError;options.done();active=null;nextStream();});return active;}
function postscribe(el,html,options){if(isFunction(options)){options={done:options};}
options=defaults(options,{done:doNothing,error:function(e){throw e;},beforeWrite:function(str){return str;},afterWrite:doNothing});el=(/^#/).test(el)?global.document.getElementById(el.substr(1)):el.jquery?el[0]:el;var args=[el,html,options];el.postscribe={cancel:function(){if(args.stream){args.stream.abort();}else{args[1]=doNothing;}}};queue.push(args);if(!active){nextStream();}
return el.postscribe;}
return set(postscribe,{streams:{},queue:queue,WriteStream:WriteStream});}());global.postscribe=postscribe;}());(function(){var supports=(function(){var supports={};var html;var work=this.document.createElement('div');html="<P><I></P></I>";work.innerHTML=html;supports.tagSoup=work.innerHTML!==html;work.innerHTML="<P><i><P></P></i></P>";supports.selfClose=work.childNodes.length===2;return supports;})();var startTag=/^<([\-A-Za-z0-9_]+)((?:\s+[\w\-]+(?:\s*=\s*(?:(?:"[^"]*")|(?:'[^']*')|[^>\s]+))?)*)\s*(\/?)>/;var endTag=/^<\/([\-A-Za-z0-9_]+)[^>]*>/;var attr=/([\-A-Za-z0-9_]+)(?:\s*=\s*(?:(?:"((?:\\.|[^"])*)")|(?:'((?:\\.|[^'])*)')|([^>\s]+)))?/g;var fillAttr=/^(checked|compact|declare|defer|disabled|ismap|multiple|nohref|noresize|noshade|nowrap|readonly|selected)$/i;var DEBUG=false;function htmlParser(stream,options){stream=stream||'';options=options||{};for(var key in supports){if(supports.hasOwnProperty(key)){if(options.autoFix){options['fix_'+key]=true;}
options.fix=options.fix||options['fix_'+key];}}
var stack=[];var append=function(str){stream+=str;};var prepend=function(str){stream=str+stream;};var detect={comment:/^<!--/,endTag:/^<\//,atomicTag:/^<\s*(script|style|noscript)[\s>]/i,startTag:/^</,chars:/^[^<]/};var reader={comment:function(){var index=stream.indexOf("-->");if(index>=0){return{content:stream.substr(4,index),length:index+3};}},endTag:function(){var match=stream.match(endTag);if(match){return{tagName:match[1],length:match[0].length};}},atomicTag:function(){var start=reader.startTag();if(start){var rest=stream.slice(start.length);if(rest.match(new RegExp("<\/\\s*"+start.tagName+"\\s*>","i"))){var match=rest.match(new RegExp("([\\s\\S]*?)<\/\\s*"+start.tagName+"\\s*>","i"));if(match){return{tagName:start.tagName,attrs:start.attrs,content:match[1],length:match[0].length+start.length};}}}},startTag:function(){var match=stream.match(startTag);if(match){var attrs={};match[2].replace(attr,function(match,name){var value=arguments[2]||arguments[3]||arguments[4]||fillAttr.test(name)&&name||null;attrs[name]=value;});return{tagName:match[1],attrs:attrs,unary:!!match[3],length:match[0].length};}},chars:function(){var index=stream.indexOf("<");return{length:index>=0?index:stream.length};}};var readToken=function(){for(var type in detect){if(detect[type].test(stream)){if(DEBUG){console.log('suspected '+type);}
var token=reader[type]();if(token){if(DEBUG){console.log('parsed '+type,token);}
token.type=token.type||type;token.text=stream.substr(0,token.length);stream=stream.slice(token.length);return token;}
return null;}}};var readTokens=function(handlers){var tok;while(tok=readToken()){if(handlers[tok.type]&&handlers[tok.type](tok)===false){return;}}};var clear=function(){var rest=stream;stream='';return rest;};var rest=function(){return stream;};if(options.fix){(function(){var EMPTY=/^(AREA|BASE|BASEFONT|BR|COL|FRAME|HR|IMG|INPUT|ISINDEX|LINK|META|PARAM|EMBED)$/i;var CLOSESELF=/^(COLGROUP|DD|DT|LI|OPTIONS|P|TD|TFOOT|TH|THEAD|TR)$/i;var stack=[];stack.last=function(){return this[this.length-1];};stack.lastTagNameEq=function(tagName){var last=this.last();return last&&last.tagName&&last.tagName.toUpperCase()===tagName.toUpperCase();};stack.containsTagName=function(tagName){for(var i=0,tok;tok=this[i];i++){if(tok.tagName===tagName){return true;}}
return false;};var correct=function(tok){if(tok&&tok.type==='startTag'){tok.unary=EMPTY.test(tok.tagName)||tok.unary;}
return tok;};var readTokenImpl=readToken;var peekToken=function(){var tmp=stream;var tok=correct(readTokenImpl());stream=tmp;return tok;};var closeLast=function(){var tok=stack.pop();prepend('</'+tok.tagName+'>');};var handlers={startTag:function(tok){var tagName=tok.tagName;if(tagName.toUpperCase()==='TR'&&stack.lastTagNameEq('TABLE')){prepend('<TBODY>');prepareNextToken();}else if(options.fix_selfClose&&CLOSESELF.test(tagName)&&stack.containsTagName(tagName)){if(stack.lastTagNameEq(tagName)){closeLast();}else{prepend('</'+tok.tagName+'>');prepareNextToken();}}else if(!tok.unary){stack.push(tok);}},endTag:function(tok){var last=stack.last();if(last){if(options.fix_tagSoup&&!stack.lastTagNameEq(tok.tagName)){closeLast();}else{stack.pop();}}else if(options.fix_tagSoup){skipToken();}}};var skipToken=function(){readTokenImpl();prepareNextToken();};var prepareNextToken=function(){var tok=peekToken();if(tok&&handlers[tok.type]){handlers[tok.type](tok);}};readToken=function(){prepareNextToken();return correct(readTokenImpl());};})();}
return{append:append,readToken:readToken,readTokens:readTokens,clear:clear,rest:rest,stack:stack};}
htmlParser.supports=supports;htmlParser.tokenToString=function(tok){var handler={comment:function(tok){return'<--'+tok.content+'-->';},endTag:function(tok){return'</'+tok.tagName+'>';},atomicTag:function(tok){console.log(tok);return handler.startTag(tok)+
tok.content+
handler.endTag(tok);},startTag:function(tok){var str='<'+tok.tagName;for(var key in tok.attrs){var val=tok.attrs[key];str+=' '+key+'="'+(val?val.replace(/(^|[^\\])"/g,'$1\\\"'):'')+'"';}
return str+(tok.unary?'/>':'>');},chars:function(tok){return tok.text;}};return handler[tok.type](tok);};htmlParser.escapeAttributes=function(attrs){var escapedAttrs={};for(var name in attrs){var value=attrs[name];escapedAttrs[name]=value&&value.replace(/(^|[^\\])"/g,'$1\\\"');}
return escapedAttrs;};for(var key in supports){htmlParser.browserHasFlaw=htmlParser.browserHasFlaw||(!supports[key])&&key;}
this.htmlParser=htmlParser;})();$(document).ready(function(){dataString='url='+$(location).attr('href');setTimeout(function(){try{update_banner_views()}
catch(e){}},10000);try{$.ajax({type:"GET",url:"/banners/ajax-get-banner/",data:dataString,dataType:'JSON',success:function(data){if(data.right_banner_html){try{if(typeof data.right_banner_html!='undefined'){postscribe('#banner_placement_right',data.right_banner_html);$('#banner_placement_right').show();}}
catch(e){}}else{$('#banner_placement_right').remove()}}});}
catch(e){}
try{$.ajax({type:"GET",url:"/banners/ajax-get-top-banner/",data:dataString,dataType:'JSON',success:function(data){try{if(typeof data.top_banner_html!='undefined'){postscribe('#banner_placement_top',data.top_banner_html);$('#banner_placement_top').show();}}
catch(e){}}});}
catch(e){}
try{$.ajax({type:"GET",url:"/banners/ajax-get-bottom-banner/",data:dataString,dataType:'JSON',success:function(data){try{if(typeof data.bottom_banner_html!='undefined'){postscribe('#banner_placement_bottom',data.bottom_banner_html);$('#banner_placement_bottom').show();}}
catch(e){}}});}
catch(e){}});function update_banner_views(){var senddata='';var bannerids=[];$('.ds_banner_ids').each(function(){bannerids.push($(this).val());});senddata='bannerids='+bannerids;$.ajax({type:"GET",url:"/banners/ajax-update-views/",data:senddata,success:function(response){if(response==1){return true;}
else{return false;}}});}
function update_banner_clicks(bid){senddata='bid='+bid;$.ajax({type:"GET",url:"/banners/ajax-update-clicks/",data:senddata,success:function(response){if(response==1){return true;}
else{return false;}}});}