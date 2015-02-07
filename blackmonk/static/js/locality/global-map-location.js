$.fn.setrSpVHeight = function(mDaLt){
    var w = $(window).width();
    $(this).each(function(index, element) {
        var fLxcOnTWidth =    $(this).height();
        $(this).find('img').css('height',fLxcOnTWidth+1); 
    });    
    return this;
}
$.fn.setrSpVWidth = function(w){
    $(this).each(function(index, element) {
        var fLxcOnTWidth =    $(this).width();
        $(this).find('img').css('width',fLxcOnTWidth+1+w);    
    });
    return this;
}

var media, orientation;
var image = "/static/themes/img/icons/map-pointer.png";
var simage = "/static/themes/img/icons/a-small.png";
var counter=0;
var MarkerList = [];
var map;
var zoom = 9;
var infoWindows = [];
var markerBounds = [];   

/*
var rendererOptions = {
          draggable: true,
          suppressMarkers: true
        };

var directionsDisplay = new google.maps.DirectionsRenderer(rendererOptions);
var directionsService = new google.maps.DirectionsService(); 
*/

var directionsDisplay;
var directionsService;

$(document).ready(function (e) {
    var $mapWrap = $('#site-map-wrapper');
    $(window).width() >= 768 ? media = 'desktop' : media = 'phone';

    if(window.innerHeight < window.innerWidth){
        orientation = 'landscape';
    }else{
        orientation = 'potrate';
    }

    $('.fLxiMgH').setrSpVHeight('mDa-lT');
    
    try{
        $('#id_travel_mode_ul li a').click(function(){
            $('#gmap_travel_mode').val($(this).attr('data-value'));
            calcRoute();
        });
    }
    catch(e){}    
    
    media === 'desktop' ? zoom = 11 : zoom = 8;
                                
    $( window ).on( "orientationchange", function( event ) {
        if(window.innerHeight < window.innerWidth){
            orientation = 'landscape';
        }else{
            orientation = 'potrate';
        }
        if(orientation === 'landscape'){
            if ($('#site-map-wrapper').hasClass('hasResult')) {
                $('#site-map-wrapper').removeClass('hasResult');
            }     
        }else{
            if (!$('#site-map-wrapper').hasClass('hasResult')) {
                $('#site-map-wrapper').addClass('hasResult');
            } 
        }
        window.setTimeout(function() {
          map.panTo(berlin);
        }, 1000);
    });  
    
    var mastHead = $('#site-map-wrapper').find('#mast-head');
    mastHead.mouseover(function () {
        $('#site-map-wrapper').addClass('translate');
    });
    mastHead.mouseleave(function () {
        $('#site-map-wrapper').removeClass('translate');
    });

    setTimeout(function () {
        $('#site-map-wrapper').addClass('scale');
    }, 200);
    
    //google.maps.event.addDomListener($('#cLmAp'), 'click', );
});

function load_global_map(map_id,lat,lng,loc_zoom,markers,globalzoom){
    if(globalzoom){zoom=loc_zoom;}                                                                       
    //media === 'desktop' ? zoom = 9 : zoom = 8;     
    var latlng = new google.maps.LatLng(lat,lng);                              
    var mapOptions = {
        zoom: zoom,
        center:latlng,
        mapTypeControl: false,
        mapTypeControlOptions: {
            style: google.maps.MapTypeControlStyle.HORIZONTAL_BAR,
            position: google.maps.ControlPosition.BOTTOM_CENTER
        },
        panControl: false,
        panControlOptions: {
            position: google.maps.ControlPosition.TOP_RIGHT
        },
        zoomControl: true,
        zoomControlOptions: {
            style: google.maps.ZoomControlStyle.SMALL,
            position: google.maps.ControlPosition.TOP_RIGHT
        },
        scaleControl: false,
        scaleControlOptions: {
            position: google.maps.ControlPosition.TOP_LEFT
        },
        streetViewControl: true,
        streetViewControlOptions: {
            position: google.maps.ControlPosition.TOP_RIGHT
        }
      };
    
      map = new google.maps.Map(document.getElementById(map_id), mapOptions);
      var thePanorama = map.getStreetView();
        google.maps.event.addListener(thePanorama, 'visible_changed', function () {
            if (thePanorama.getVisible()) {
                if ($('#site-map-wrapper').hasClass('hasResult')) {
                    $('#site-map-wrapper').removeClass('hasResult');
                }
                if (!$('#site-map-wrapper').hasClass('hasStreet')) {
                    $('#site-map-wrapper').addClass('hasStreet');
                }
    
            } else {
                if (!$('#site-map-wrapper').hasClass('hasResult') && media === 'desktop') {
                    $('#site-map-wrapper').addClass('hasResult');
                }else if(!$('#site-map-wrapper').hasClass('hasResult') && media === 'phone' && orientation === 'potrate') {
                    $('#site-map-wrapper').addClass('hasResult');
                }
                if ($('#site-map-wrapper').hasClass('hasStreet')) {
                    $('#site-map-wrapper').removeClass('hasStreet');
                }
    
            }
    
        });
    
    for (var i = 0; i < markers.length; i++) {
        setTimeout(function() {
          create_marker_with_animation();
        }, i*200);
     }
                                                       
}

function create_marker_with_animation(){
    
    var marker = new google.maps.Marker({
                map: map,
                position: new google.maps.LatLng(markers[counter].lat,markers[counter].lng),
                icon: markers[counter].icon,
                animation: google.maps.Animation.DROP
            });
          
        var infowindow = new google.maps.InfoWindow({
            content: markers[counter].content_info,
            maxWidth: 330
        });
        
        infoWindows.push(infowindow); 
        MarkerList.push(marker); 
        
        markerBounds.push(new google.maps.LatLng(markers[counter].lat,markers[counter].lng));
            
        google.maps.event.addListener(marker, 'click', function () {
            close_all_infowindows();                                                         
            infowindow.open(map, this);
            $('.fLxiMgH').setrSpVHeight('mDa-lT');
            try{
                $('#site-map-wrapper .sTr-rT-rD').raty({
                    readOnly: true, 
                    score: function() {return $(this).attr('data-rating');},
                    size: 16
                });
            }
            catch(e){}
            
            setTimeout(function () {
                $('.map-info').addClass('on');
            }, 50);

        });
    
       counter++;
}

function show_info_window(id){
   close_all_infowindows();   
   google.maps.event.trigger(MarkerList[id], 'click');
}

function close_all_infowindows() {
  for (var i=0;i<infoWindows.length;i++) {
     infoWindows[i].close();
  }
}

var loaded = true;
function loadMore()
{
  load_more_contents();       
  $('#id_result_div').on('scroll', bindScroll);
}

function bindScroll(){
    if($('#id_result_div').scrollTop() + $('#id_result_div').innerHeight()>=$('#id_result_div')[0].scrollHeight && loaded)
    {
      loaded = false;
      $('#id_result_div').off('scroll');
      loadMore();
    }                   
}

$('#id_result_div').scroll(bindScroll);

function load_more_contents(){
    var dataString='';                          
    var fl_counter = parseInt($("#id_content_ul:first > li").last().val()) + 1;
    dataString+='page='+$('#page_number').val()+'&fl_counter='+fl_counter;
    if($('#id_search_status').val()=='true'){dataString+='&search=true'+'&q='+$('#id_q').val();}
    
    $('#id_loading_txt').show();
    
    $.ajax({
    type: "GET",
    url: $('#load_more_url').val(),
    data: dataString,
    dataType:'JSON',
    success: function(data){
            loaded = true;
            $('#id_loading_txt').hide();
            if(data.status)
            {
                $('#id_content_ul').append(data.html);
                $('#page_number').val(data.page_number);
                $('#id_fl_counter').val(data.fl_counter);
                $('.fLxiMgH').setrSpVHeight('mDa-lT');
            }
            else
            {
                alert('No results found....');
             }
        }
    });
}




function remove_all_markers() {
    while(MarkerList.length){
        MarkerList.pop().setMap(null);
    }
}

function calcRoute() {
    var selectedMode = document.getElementById("gmap_travel_mode").value;
    directionsDisplay.setMap(map);
    directionsDisplay.setPanel(document.getElementById('directions-panel'));
    var dir_icons = {start: new google.maps.MarkerImage(dir_icon_start),
                 end: new google.maps.MarkerImage(dir_icon_end)
             };

    var start = $('#directionFrom').val();
    var end = $('#directionTo').val();
    
    var request = {
        origin:start, 
        destination:end,
        //travelMode: google.maps.DirectionsTravelMode.DRIVING
        travelMode: google.maps.DirectionsTravelMode[selectedMode]
    };
    directionsService.route(request, function(response, status) {
      if (status == google.maps.DirectionsStatus.OK) {
        remove_all_markers();   
        $('#directions-panel').empty();
        var leg = response.routes[ 0 ].legs[ 0 ];
        makeMarker(leg.start_location, dir_icons.start, leg.start_address);
        makeMarker(leg.end_location, dir_icons.end, leg.end_address);
        directionsDisplay.setDirections(response);
      }
      else{alert("Sorry !! locations specified in the requests's origin, destination, or waypoints could not be geocoded.")}                                                           
    });
  }

function makeMarker(position, icon, title) {
    marker=new google.maps.Marker({
     position: position,
     map: map,
     icon: icon,
     title: title
    });
                                            
    var Dirinfowindow = new google.maps.InfoWindow({
            content: title,
            maxWidth: 330
    });                                       
    
    google.maps.event.addListener(marker, 'click', function () {
            Dirinfowindow.open(map, this);
    });                                        
    MarkerList.push(marker);                                         
    return marker;                                         
                                            
}

function initialize_places_auto_complete(lat, lon, cc_code){
    
    var rendererOptions = {
          draggable: true,
          suppressMarkers: true
        };

    directionsDisplay = new google.maps.DirectionsRenderer(rendererOptions);
    directionsService = new google.maps.DirectionsService(); 
    
    var options = {
      bounds: map,
      types: ['geocode'],
      componentRestrictions: {country: cc_code}
    };
    var input_one = document.getElementById('directionFrom');
    var autocomplete_one = new google.maps.places.Autocomplete(input_one,options);
}

function init_get_direction(aid,objid,src,ajx_url){
   if($('#site-map-wrapper').hasClass('scale')){$('#site-map-wrapper').removeClass('scale');}
   $('#site-map-wrapper').addClass('on');  
   var dataString='aid='+aid+'&objid='+objid+'&src='+src;
   $.ajax({
    type: "GET",
    url: ajx_url,
    data: dataString,
    dataType:'JSON',
    success: function(data){
              
            if(data.status){                
                /**/
                $('#site-map-wrapper').empty().append(data.html);  
                setTimeout(function () {
                    $('#site-map-wrapper').addClass('scale');
                }, 200);
                setTimeout(function () {
                    $('#site-map-wrapper').addClass('hasResult');
                }, 1000);   
                $('#directionFrom').focus();
                /**/
                
                try{
                    $('#id_travel_mode_ul li a').on('click', function()
                    {
                        $('#gmap_travel_mode').val($(this).attr('data-value'));
                        calcRoute();
                    });
                }
                catch(e){}
                
                update_navigation_bar();
            }
            else{
                 alert(gettext('Sorry there is a problem! Your action cannot be performed, Please try later'));
                 $('#site-map-wrapper').removeClass('on scale opacity hasResult');
            }    
            init_close_lb();
        }
    });
}

function init_close_lb(){
    $('.close').on('click',function () {
        $('#site-map-wrapper').addClass('opacity');
        setTimeout(function () {
            $('#site-map-wrapper').removeClass('on scale opacity hasResult');
            $('#site-map-wrapper').empty();
        }, 250);
        counter=0;   
        MarkerList = [];
        infoWindows = [];
        markerBounds = [];  
        map = null;       
    });                     
}

function update_navigation_bar(){
    var mastHead = $('#site-map-wrapper').find('#mast-head');                             
    mastHead.on('mouseover', function()
    {
        $('#site-map-wrapper').addClass('translate');
    });  
    mastHead.on('mouseleave', function()
    {
        $('#site-map-wrapper').removeClass('translate');
    });                                                          
}

function check_enter_key_hit(event){
   if(event.keyCode == 13){
        calcRoute();
    } 
   else{return false;}                                                                 
}