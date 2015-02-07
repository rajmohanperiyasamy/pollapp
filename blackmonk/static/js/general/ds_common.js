$(document).ready(function(){
	
//Just add this class to any anchor tag for preventing it from refreshing the page, it is similar to return false
//Caution this wont work for the newly imported content using ajax
	$('.click_pvnt').click(function(event){
		event.preventDefault();
	});

//Featured Slider code begin autoscroll function call
	/*if ($('#call_from').val() != 'movie_index'){*/
		window.setTimeout("next_nav(1)",4000);
	/*}*/
	$('.whole_slider_wrapper').mouseover(function() {
		clearTimeout(auto);
	});
	$('.whole_slider_wrapper').mouseout(function() {
		/*if ($('#call_from').val() != 'movie_index') {*/
			auto = setTimeout("next_nav(1)", 4000);
		/*}*/
	});

//Adding class 'active' to the li on clicking directly to any of the five navigation numbers
$('.nav').click(function(){
    $('.nav').removeClass('active');
    $(this).addClass('active');
    show_ftrd(0);
});

//Moving the activate class to the right of the navigation,jumbing to "1" if reaches at the end "5" 
$('div.next').click(function(){
    next_nav(0);
});

//Moving the activate class to the left of the navigation,jumbing to "5" if reaches at the end "1"
$('div.prev').click(function(){
    $('ul#ftrd_nav_ul li.active').addClass('p');
    if ($('ul#ftrd_nav_ul li.active').hasClass('first_li')) {
        $('ul#ftrd_nav_ul li.last_li').addClass('active');
    }
    else {
        $('ul#ftrd_nav_ul li.active').prev('li').addClass('active');
    }
    $('ul#ftrd_nav_ul li.p').removeClass('active');
    $('ul#ftrd_nav_ul li.nav').removeClass('p');
    show_ftrd(0);
});

//Featured Slider end

//Accordium code begin
	$('ul.accordian9 li:first').addClass('first_accdn');
	
	//Got to top scroll
	$('.top_link99').click(function(){
		$('html, body').animate({scrollTop:'0'}, 500);
	});
	
	//Calling Accordium when Accordium side tab is clicked
	$('.call_acdn').click(function(){
		id=$(this).attr('id');
		accordium("li."+id+" "+"a.bar_title");
	});
	
	//Calling Accordium when Accordium tab is clicked
	$('a.bar_title').click(function(){
		accordium(this);
	});	
	
//Accordium code end

//Auto opening accordium
	var loc_url = String(window.location);
	var show = loc_url.substring(loc_url.indexOf('#')+1,loc_url.length);
	//var show = loc_url.split(".html#"); //This too works fine
		if(show == "trailer") {
			var id = $(".trailor").attr('id');
			show_trailer(id);
		}
		else if (show == "user-reviews") {
			accordium('#user-reviews a.bar_title');
		}
		else if (show == "critic-reviews") {
			accordium('#critic-reviews a.bar_title');
		}
		else if (show == "map") {
			accordium('.map_accdn a.bar_title');
		}
		else if (show == "comments") {
			accordium('.comments_accdn a.bar_title');
		}
		else if (show == "events") {
			accordium('.events_accdn a.bar_title');
		}
		else if (show == "photos"){
			accordium('#movie_photos a.bar_title');
		}
		

//Ajax date wise content retrieving begin
$('#days ul li a').click(function(){
			var all_ids=[];
			var retrieve_events = $('#as_retrieve_events').val();
            if($(this).hasClass('nav_arrow')){
                exit();
            }
			$('.ecat_id').each(function(){
				all_ids.push($(this).val());
			});
            $('#days li a').removeClass('on');
            $("#loading").show();
            $('#event_list').hide();
            $(this).addClass("on");
            $.ajax({
               type: "GET",
               url: "/events/eventlistretrieve/",
               data:"date="+$(this).attr('name')+"&eids="+all_ids+"&retrieve_events="+retrieve_events,
               success: function(html_from_server)
               {   
                    $('#event_list').empty().html(html_from_server);
                    $("#loading").hide();
                    $('#event_list').fadeIn(300);                   
               }
         });
    });

$('#tab2').click(function()
{ 
	$("#tab2").addClass("on"); 
	$('#tab1').removeClass("on");
	$('#tab1_content').hide();																	 
	$('#tab2_content').fadeIn("slow");
});
$('#tab1').click(function()
{ 
	$("#tab1").addClass("on");
	$('#tab2').removeClass("on");
	$('#tab2_content').hide();
	$('#tab1_content').fadeIn("slow");
});
  
//Ajax date wise content retrieving  end

//Description expanding and contracting begin
	var str_len = $('#synopsis').text().length;
	if(str_len<565){
		$('#synopsis').css('height','100%');
		$('.toggle').remove();
	}
	//Expanding and Contracting "Synopsis" 
	$('a.toggle').click(function(){
		var hgt=$('#synopsis').css('height');		
		$('#synopsis').css('overflow','hidden');
		$('#synopsis').css('height','100%');
		var syp_hgt=$('#synopsis').height();
		$('#synopsis').css('height',hgt);
		$('#synopsis').css('overflow','visible');		
		
		if(hgt=="99px"){
			$('#synopsis').animate({
				'height': syp_hgt+'px'
			},300,function(){
				$('a.toggle').empty().html('(less)');
			})
		}
		else{
			$('#synopsis').animate({
				'height':'99px'
			},300,function(){
				$('a.toggle').empty().html('(more)');
			})
		}
		
	});

//Description expanding and contracting end

//Book marking script code begin
		// add a "rel" attrib if Opera 7+
	    if(window.opera) {
	        if ($("a.jqbookmark").attr("rel") != ""){ // don't overwrite the rel attrib if already set
	            $("a.jqbookmark").attr("rel","sidebar");
	        }
	    }
	 
	    $("a.jqbookmark").click(function(){
			
			if($(this).attr('href')=='#' || $(this).attr('href')=='' ){
				var url = window.location;	
			}
			if($(this).attr('title') == 'Add To Bookmarks' || $(this).attr('title') == 'Add To Favourite'){
				var title = document.title;
			}
	 
	        if (window.sidebar) { // Mozilla Firefox Bookmark
	            window.sidebar.addPanel(title, url,"");
	        } else if( window.external ) { // IE Favorite
	            window.external.AddFavorite( url, title);
	        } else if(window.opera) { // Opera 7+
	            return false; // do nothing - the rel="sidebar" should do the trick
	        } else { // for Safari, Konq etc - browsers who do not support bookmarking scripts (that i could find anyway)
	             alert('Unfortunately, this browser does not support the requested action,'
	             + ' please bookmark this page manually.');
	        }
	 
	    });
		
//Bookmarting script code end

//Small photo gallery shared by classifieds and business
$('.thumb_img').click(function(){
		$('.thumb_img').parent().removeClass('selected');
		$('.loader_16').show();
		$("#full_imgs").animate({
					opacity:'0.5'
					},300);
		$(this).parent().addClass('selected');
		var img_src = $(this).attr('src');
		if ($('#call_from').val() == 're_property_detail') {
			var full_img_src = img_src.replace("Ti.jpg", "478x10000.jpg");
		}
		else {
			var full_img_src = img_src.replace("75x75.jpg", "284x213.jpg");
		}
		$("#full_imgs").attr("src", full_img_src).load(function(){
					$('.loader_16').hide();
					$("#full_imgs").animate({
					opacity:'1'
					},300,function(){
						$("#full_imgs").stop();
					});				
		});
		
	});

//Fixing the accordium map bug ,loading the map only when accordium gets visible	
$('.load_map').click(function(){
		setTimeout('load_accdn_map()',302);
	});

//Global search validation code begin

$('.search_ex input').each(function(index) {
	var search_val = $(this).val();
    var str = jQuery.trim(search_val)
	if (str.length != 0) {
		var tips_id = get_tips_class(this);
		$(tips_id).hide();
	}
  });

$('.search_ex input').click(function(){
	var tips_id = get_tips_class(this);
	$(tips_id).addClass('focus');
});

$('.search_ex input').keyup(function(){
	$(this).css('border-color','');
	var tips_id = get_tips_class(this);
	$(tips_id).hide();
});

$('.search_ex input').blur(function(){
	var str = jQuery.trim($(this).val());		
	if (str.length == 0) {
			var tips_id = get_tips_class(this);
			$(tips_id).removeClass('has_text focus');
			$(tips_id).show();
		}		
});

$('.tips').click(function(){
	var id = $(this).attr('id');
	var input_class = "."+id+"_input";
	$(input_class).focus();
	$(this).addClass('focus');
	
});

$('.single_submit').click(function(){
		var input_id =  $(this).attr('name');
		var search_val = $('#'+input_id).val();
		var str = jQuery.trim(search_val);		
		if (str.length == 0) {
			$('#'+input_id).css('border-color','red');	
			$('#'+input_id).focus();
			return false;
		}		
});

//Global search validation code end

// Tell a friend or Respond to code begin

//On calling the respond , making all the fields empty
	$('.respond_clr').click(function(){
		$('#respond_form [type="text"]').val('');
		$('#msg').val('');
		$('.tellfriend input').css('border-color','#069');
		$('.tellfriend textarea').css('border-color','#069');
	});
	$('#respond_form [type="text"]').keyup(function(){
		$(this).css('border-color','#069');
	});
	$('.tellfriend textarea').keyup(function(){
		$(this).css('border-color','#069');
	});
	
//Assigning the "#respond_hashkey" hidden input box with the comment hash key value only at the first loading of the page
var exec_this = $('#as_exec_respond').val();
if (exec_this == 'yes' || exec_this == 'yes2') {  
	$('#respond_hashkey').val($('#id_hashkey').val());
	
	$('.respond_submit').click(function(){
		$('.tellfriend input').css('border-color','green');
		$('.tellfriend textarea').css('border-color','green');
	});
	
	$('#from_name').keyup(function(){
		$('#keyup_name').text($(this).val());
	});
	$('#from_name').click(function(){
		$('#keyup_name').text($(this).val());
	});
	
	$("#respond_form").submit(function(event){
			event.preventDefault();
			var tell_friend_submit = true;
			
			//validate all the text boxes
			$("#respond_form [type = 'text']").each(function(i) {
			
				var val = $(this).val();
				var str = jQuery.trim(val);
				if (str.length == 0) {
					$(this).css('border-color','red').focus();
					
					tell_friend_submit = false;
				}
				else{
					$(this).css('border-color','green');
				}
				
				
				if($(this).attr('name') == 'to_email'){
					if (!(/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test($(this).val()))) {
						$(this).css('border-color','red').focus();
						tell_friend_submit = false;
					}
					else{
						$(this).css('border-color','green');
					}
				}
			
			});
			
			//validate the message box
			var val = $('#msg').val();
			var str = jQuery.trim(val);
			
			if (str.length == 0){
				$('#msg').css('border-color','red').focus();
				tell_friend_submit = false;
			}
			else{
				$('#msg').css('border-color','green');
			}
			
			if (tell_friend_submit) {
				//On submit , hiding the submit button & showing the status msg
				$('.respond_submit').hide();
				$('#respondstatus').removeAttr('class').addClass('msg_sending').text('Message sending , please wait...');
				$('#respondstatus').show();
				
				//Data sending to the server
				var postdata = "from_name=" + $('#from_name').val();
				postdata += '&to_name=' + $('#to_name').val();
				postdata += '&to_email=' + $('#to_email').val();
				postdata += '&msg=' + $('#msg').val();
				//postdata += '&Captcha_value=' + $('#Captcha_value').val();
				//postdata += '&hash-key=' + $('#respond_hashkey').val();
				postdata += '&content_id=' + $('#content_id').val();
				postdata += '&share=' + exec_this;
				
				//Ajax 
				$.ajax({
					type: "POST",
					url: $('#respond_form').attr('action'),
					dataType: 'json',
					data: postdata,
					success: function(html_from_server){
						//Assiging the new hash key to the hidden field "#respond_hashkey"
						$('#respond_hashkey').val(html_from_server.hash);
						
						if (html_from_server.success == "1") {
						
							//If success then staus msg in green
							$('#respondstatus').removeAttr('class').addClass('flash_success_alert').text('Thank You!! Your message has been sent.');
							
							//Clearing all the input fields
							$('#respond_form [type="text"]').val('');
							$('#msg').val('');
							$('.tellfriend input').css('border-color', '#069');
							$('.tellfriend textarea').css('border-color', '#069');
							
							//Closing lightbox,loading new captcha image,removing status msg,showing submit button
							window.setTimeout("$('#respondstatus').fadeOut(300)", 4000);
							window.setTimeout("hide_lightbox()", 5000);
							window.setTimeout("$('.respond_submit').show();", 6000);
							$('#respond_catcha_img').attr('src', '/site_media/images/captcha/' + html_from_server.image).load();
						}
						else 
							if (html_from_server.success == "0") {
								$('#respondstatus').removeAttr('class').addClass('flash_error_alert');
								$('#Captcha_value').val('');
								//if error then showing status msg in red
								//if wrong image key inside if or inside else loop
								if (html_from_server.captcha == "0") {
									$('#respondstatus').text('Wrong Image key! Please re-enter the text in the image');
									$('#Captcha_value').css('border-color', 'red').focus();
								}
								else {
									$('#respondstatus').text('Sorry, we were unable to send this message, please try again later.');
								}
								//removing status msg,show submit,load new captcha image
								window.setTimeout("$('#respondstatus').fadeOut(200)", 3000);
								if ($.browser.msie) {
									$('.respond_submit').show();
								}
								else {
									window.setTimeout("$('.respond_submit').fadeIn(200)", 4000);
								}
								$('#respond_catcha_img').attr('src', '/site_media/images/captcha/' + html_from_server.image).load();
							}
					}
				});
			}
	});
}

// Tell a friend or Respond to code end






//NewsLetter Code Start
// News letter validation

$('#header_subscribe_email_notext').click(function(){
	if ($('#newsletter_signup').css('display') == 'block') {
		$('#news_letter_status').removeAttr('class').text('');
		$('#newsletter_signup').hide(300,function(){
			$('#as_news_letter_li').removeClass('onPp');
		});
		$('.as_news_submit').show();
	}
	else {
		$('#as_news_letter_li').addClass('onPp');
		$('#newsletter_signup').show(300);
	}
});

$('.as_news_letter').click(function(){
		$('#newsletter input').val('').css('border-color', '#069');
		$('.as_news_isNaN').html('(Eg:4034757903)').css('color', '');
		$('.as_news_isemail').html('(Eg:yourname@domain.com)').css('color', '');
});

$('#to_news_number').keyup(function(){
	validate_news_letter_number();
});

$('#to_news_email').keyup(function(){
	$('input#to_news_email').css('border-color', '');
	$('.as_news_isemail').html('(Eg:yourname@domain.com)').css('color', '');
});

// News letter validation end






//sms validation begin

$('#sms_form').submit(function(event){ event.preventDefault(); });

$('.sms_this').click(function(){
	$('#sms_form input').val('').css('border-color','#069');
	$('.as_isNaN').html('(Eg:9886098860)').css('color', '');
});

$('#to_number').keyup(function(){
		var number = $("#to_number").val();
		if (isNaN($("#to_number").val())|| number.search(/\.+/) != -1 ) {
		$('input#to_number').css('border-color', 'red');
		$('.as_isNaN').html('(Invalid Mobile Number)').css('color', 'red');
		$("#to_number").focus();
	}
	else {
		$('input#to_number').css('border-color', '');
		if ($("#to_number").val().length > 1) {
			$('.as_isNaN').html('(Eg:9886098860)').css('color', '');
		}
		else {
			$('.as_isNaN').html('(Eg:9886098860)').css('color', '');
		}
	}
});

//sms validation end
	
});

//All function defnitions

//Send sms begin
function send_sms(msg,number,module_id){
	var input_number = $("#to_number").val();
	if (isNaN(input_number) || $.trim(input_number).length < 10 ) {
			$('input#to_number').css('border-color', 'red');
			$('.as_isNaN').html('(Invalid Mobile Number)').css('color', 'red');
			$("#to_number").focus();
			return false;
		}
	$('.as_sms_submit').hide();
	$('.as_sms_theatre_submit').hide();
	$('#sms_status').show();
	setTimeout('lightbox()',4000);
	setTimeout('$("#sms_status").hide();$(".as_sms_submit").show();$(".as_sms_theatre_submit").show();',4000);
	$.get("/sms/", {msg: msg,mobile_number: number,module_id: module_id}, function(data){
		if(data=='1'){
			//alert('success');
		}
	});
}
//Send sms end


//Global search validation code begin

function get_tips_class(clicked){
	var input_class = String($(clicked).attr('class'));
	var tips_class =  input_class.split('_input');
	return '#'+tips_class[0];
}

//Global search validation code end

//Accordium begin
//Accordium remove class "close" and add class "open" to the bar
function rmClose_addOpen(id){
	$(id).removeClass('close');
	$(id).addClass('open');
}

//Accordium remove class "close" and add class "open" to the bar
function rmOpen_addClose(id){
	$(id).removeClass('open');
	$(id).addClass('close');
}

//Accordium action
function accordium(id){
	if($('#call_from').val()=='classifieds' || $('#stop_accdn').val() == "yes"){
		return
	}
	rmOpen_addClose('a.bar_title');
	var dis = $(id).next('div').css('display');
	//$('.acdn_content').slideUp(300);
	$('.acdn_content').hide();
	if (dis == "block") {
		rmOpen_addClose(id);
		//$(id).next('div').slideUp(300);
		$(id).next('div').hide();
	}
	else {
    	try{
        	var target_offset = $('.first_accdn').offset().top;
            $('html, body').animate({scrollTop:target_offset-10}, 1000);
            rmClose_addOpen(id)
            $(id).next('div').slideDown(300);
            $('#as_open_showtimeaccdn').val('no');
    	}
        catch(e){}
	}
}
//Accordium end

//The sliding function shared by classifed detail , classified list , business
function ds_slide(clicked,slide_elmnt,down_status,up_status){
	if ($(clicked).hasClass('down')) {
		slidedown(clicked,slide_elmnt,down_status);
		return
	}
	if ($(clicked).hasClass('up')) {
		slideup(clicked,slide_elmnt,up_status);
	}
	
}


//function slideup
function slideup(clicked,slide_div,up_status){
	$(slide_div).slideUp(300);
	//For q&a qa_details.html
	$(clicked).html(up_status);
	$(clicked).removeClass('up');
	$(clicked).addClass('down');
}

//function slidedown
function slidedown(clicked,slide_div,down_status){
	$(slide_div).slideDown(300);
	$(clicked).html(down_status);
	$(clicked).removeClass('down');
	$(clicked).addClass('up');
}

//Featured Slider code begin
function next_nav(flag){
	$('ul#ftrd_nav_ul li.active').addClass('p');
	if ($('ul#ftrd_nav_ul li.active').hasClass('last_li')) {
		$('ul#ftrd_nav_ul li.first_li').addClass('active');
	}
	else {
		$('ul#ftrd_nav_ul li.active').next('li').addClass('active');
	}
	$('ul#ftrd_nav_ul li.p').removeClass('active');
	$('ul#ftrd_nav_ul li.nav').removeClass('p');
	show_ftrd(flag);
}


//Function which displays the featured contents
function show_ftrd(flag){
    var id = $('ul#ftrd_nav_ul li.active a').attr('name');
    $('.featured_content_div').hide();
    $('#' + id).fadeIn(1000);
	if (flag==1) {
		/*if ($('#call_from').val() != 'movie_index'){*/
		auto = setTimeout("next_nav(1)", 6000);
		/*}*/
	}
}
//Featured Slider code end

//Lightbox ie hack
function restore(){
	var lb_auto = setTimeout("make_default()",200);
}

function make_default(){
	$('.lightbox_background').css('background-color','transparent');
	$('.lightbox_content_holder').css({
		'padding':'16px',
		'background-color':'white'
		});
}

function change_url_parm(value){
    $(".bm_pgntn_anchr").each(function(){
		$(this).attr("href", function(i,origValue){
            return origValue.replace(/(view=)[a-z]+/ig,'view='+value); 
        });
	});

   try{$('#id_sort_sb').attr('data-view',value);}
   catch(e){}
}

