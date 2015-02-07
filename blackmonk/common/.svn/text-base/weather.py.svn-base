import time,datetime,urllib2
from xml.dom import minidom

from django.shortcuts import render_to_response
from django.template import RequestContext

from django.conf import settings

def getText(nodelist):
   rc = ""
   for node in nodelist:
       if node.nodeType == node.TEXT_NODE:
           rc = rc + node.data
   return rc    
    
def get_weather_date(cdate):
    str=cdate
    year=int(str[:4])
    month=int(str[5:7])
    day=int(str[8:10])
    hour=int(str[11:13])
    minute=int(str[14:16])
    new_date = datetime.datetime(year,month,day,hour,minute)
    return new_date

def get_weather_network(request,wx_api_obj,template='default/common/weather-network.html'):
    import socket
    data={}
    url = wx_api_obj.weather_xml
    w_unit = wx_api_obj.weather_unit
    
    try:
        timeout = 3
        socket.setdefaulttimeout(timeout)
        dom = minidom.parse(urllib2.urlopen(url))
    except:
        data['error']=True
        return render_to_response(template,data,context_instance=RequestContext(request))
    
    short_term_forcast=[]
    long_term_forcast=[]
    weather_links=[]
    for node in dom.getElementsByTagName("SITE"):
        current_condition_list=node.getElementsByTagName("OBS")
        '''Current Weather '''
        for list in current_condition_list:
            try:
                cw_date=get_weather_date(list.getAttribute('DATE'))
            except:
                cw_date=list.getAttribute('DATE')[:16]
            data={'wdate':cw_date,'station':list.getAttribute('STATION'),'forcast':list.getAttribute('FORECAST_TEXT_EN'),'temperature':list.getAttribute('TEMPERATURE'),
                                     'feels':list.getAttribute('FEELS_LIKE'),'wind_speed':list.getAttribute('WIND_SPEED'),'wind_dir':list.getAttribute('WIND_DIR_EN'),'humidity':list.getAttribute('REL_HUMIDITY'),
                                     'pressure':list.getAttribute('PRESSURE'),'pressure_trend':list.getAttribute('PRESSURE_TREND'),'cur_weather_icon':settings.STATIC_URL+'images/weather/wn/'+list.getAttribute('ICON')+'.jpg'}            
        '''Almanac '''
        for alm in node.getElementsByTagName("ALM"):
            almanac={'alm_date':alm.getAttribute('DATE'),'alm_nor_low':alm.getAttribute('NORMAL_LOW'),'alm_nor_high':alm.getAttribute('NORMAL_HIGH'),'alm_record_low':alm.getAttribute('RECORD_LOW'),
                  'alm_record_low_year':alm.getAttribute('RECORD_LOW_YEAR'),'alm_record_high':alm.getAttribute('RECORD_HIGH'),'alm_record_high_year':alm.getAttribute('RECORD_HIGH_YEAR'),
                  'alm_sunrise':alm.getAttribute('SUNRISE_EN'),'alm_sunset':alm.getAttribute('SUNSET_EN')}
        
        '''Short Term Forecast '''    
        s_dates = []
        s_name_in =[]
        s_forcast = []
        s_temp = []
        s_pop = []
        s_wind = []
        s_icon = []    
        
        for sf in node.getElementsByTagName("PERIOD"):
             s_dates.append(sf.getAttribute('DATE'))
             s_name_in.append(sf.getAttribute('NAME_EN'))
             s_forcast.append(sf.getAttribute('FORECAST_TEXT_EN'))
             s_temp.append(sf.getAttribute('TEMPERATURE'))
             s_wind.append(sf.getAttribute('WIND_DIR_EN') + " "+sf.getAttribute('WIND_SPEED'))
             s_pop.append(sf.getAttribute('POP'))
             s_icon.append(settings.STATIC_URL+'images/weather/wn/'+sf.getAttribute('ICON')+'.jpg')
        
        short_term_forcast={'sf_date':s_dates,'name_in':s_name_in,'forcast':s_forcast,'temp':s_temp,'pop':s_pop,
                                        'wind':s_wind,'icon':s_icon}
        '''Long Term Forecast '''  
        l_dates = []
        l_name_in =[]
        l_forcast = []
        l_hightemp = []
        l_lowtemp = []
        l_pop = []
        l_icon = []  
        
        for lf in node.getElementsByTagName("WEEKDAY"):
            l_dates.append(lf.getAttribute('DATE'))
            f_dates=lf.getAttribute('NAME_EN').split(',')
            l_name_in.append({'day':f_dates[0],'date':f_dates[1]})
            l_forcast.append(lf.getAttribute('FORECAST_TEXT'))
            l_hightemp.append(lf.getAttribute('HIGH_TEMP'))
            l_lowtemp.append(lf.getAttribute('LOW_TEMP'))
            l_pop.append(lf.getAttribute('POP'))
            l_icon.append(settings.STATIC_URL+'images/weather/wn/'+lf.getAttribute('ICON')+'.jpg')
               
        long_term_forcast={'lf_date':l_dates,'lf_name_in':l_name_in,'lf_forcast':l_forcast,'lf_high_temp':l_hightemp,'lf_low_temp':l_lowtemp,
                            'lf_pop':l_pop,'lf_icon':l_icon}
        
        '''Weather Forecast Links'''
        for link in node.getElementsByTagName('LINK'):
            weather_links.append({'link_name':link.getAttribute('name_en'),'link_url':link.getAttribute('URL_EN')})  
    
    data['short_term_forcast']=short_term_forcast
    data['long_term_forcast']=long_term_forcast
    data['almanac']=almanac
    data['weather_links']=weather_links
    data['wx_api_obj'] = wx_api_obj
    socket.setdefaulttimeout(30)
    return render_to_response(template,data,context_instance=RequestContext(request)) 

def get_weather_online(request,wx_api_obj,template='default/common/world-weather.html'):
    import socket
    data={}
    url = wx_api_obj.weather_xml
    w_unit = wx_api_obj.weather_unit
    
    try:
        timeout = 3
        socket.setdefaulttimeout(timeout)
        dom = minidom.parse(urllib2.urlopen(url))
    except:
        data['error']=True
        return render_to_response(template,data,context_instance=RequestContext(request))
    
    current_conditions=[]        
    #long_term_forcast=[]
    for node in dom.getElementsByTagName("data"):
        '''Current Weather '''
        for cc in dom.getElementsByTagName("current_condition"):
            current_wthr_image=cc.getElementsByTagName('weatherIconUrl')[0].childNodes
            for img in current_wthr_image:
                cw_image = img.data
            if w_unit == 'cel':
                cw_temp = getText(cc.getElementsByTagName('temp_C')[0].childNodes)
            else:
                cw_temp = getText(cc.getElementsByTagName('temp_F')[0].childNodes)
            current_conditions={'cw_ob_time':getText(cc.getElementsByTagName('observation_time')[0].childNodes),
                                'cw_temp':cw_temp,
                                'cw_image':cw_image,
                                'cw_desc':cc.getElementsByTagName('weatherDesc')[0].childNodes[0].data,
                                'cw_wind_speed':getText(cc.getElementsByTagName('windspeedKmph')[0].childNodes),
                                'cw_wind_speed_miles':getText(cc.getElementsByTagName('windspeedMiles')[0].childNodes),
                                'cw_wind_dir':getText(cc.getElementsByTagName('winddir16Point')[0].childNodes),
                                'cw_humidity':getText(cc.getElementsByTagName('humidity')[0].childNodes),
                                'cw_pressure':getText(cc.getElementsByTagName('pressure')[0].childNodes),
                                'cw_cloudcover':getText(cc.getElementsByTagName('cloudcover')[0].childNodes),
                                'cw_date':datetime.datetime.now()}
        
        """    
        l_dates = []
        l_desc =[]
        l_wind_speed = []
        l_wind_speed_miles = []
        l_wind_dir = []
        l_hightemp = []
        l_lowtemp = []
        l_icon = []
        
        
        for ltwc in dom.getElementsByTagName("weather"):
            l_dates.append(getText(ltwc.getElementsByTagName('date')[0].childNodes))
            if w_unit == 'cel':
                l_hightemp.append(getText(ltwc.getElementsByTagName('tempMaxC')[0].childNodes))
                l_lowtemp.append(getText(ltwc.getElementsByTagName('tempMinC')[0].childNodes))
            else:
                l_hightemp.append(getText(ltwc.getElementsByTagName('tempMaxF')[0].childNodes))
                l_lowtemp.append(getText(ltwc.getElementsByTagName('tempMinF')[0].childNodes))
            l_wind_speed.append(getText(ltwc.getElementsByTagName('winddirection')[0].childNodes) + " " + getText(ltwc.getElementsByTagName('windspeedKmph')[0].childNodes))
            l_wind_speed_miles.append(getText(ltwc.getElementsByTagName('winddirection')[0].childNodes) + " " + getText(ltwc.getElementsByTagName('windspeedMiles')[0].childNodes))
            l_wind_dir.append(getText(ltwc.getElementsByTagName('winddirection')[0].childNodes))
            l_desc.append(ltwc.getElementsByTagName('weatherDesc')[0].childNodes[0].data)
            l_icon.append(ltwc.getElementsByTagName('weatherIconUrl')[0].childNodes[0].data)
            
        long_term_forcast={'lwc_date':l_dates,'lwc_desc':l_desc,'lwc_high_temp':l_hightemp,'lwc_low_temp':l_lowtemp,
                            'lwc_wind_speed':l_wind_speed,'lwc_wind_speed_miles':l_wind_speed_miles,'lwc_wind_dir':l_wind_dir,'lwc_icon':l_icon}  
        """    
        
        long_term_weather_info = []
        for node in dom.getElementsByTagName("weather"):
            if w_unit == 'cel':
                hight_temp = getText(node.getElementsByTagName('tempMaxC')[0].childNodes)
                low_temp = getText(node.getElementsByTagName('tempMinC')[0].childNodes)
            else:
                hight_temp = getText(node.getElementsByTagName('tempMaxF')[0].childNodes)
                low_temp = getText(node.getElementsByTagName('tempMinF')[0].childNodes)
            
            long_term_weather_info.append({'date':getText(node.getElementsByTagName('date')[0].childNodes), 'high_temp':hight_temp, 'low_temp':low_temp,
                                          'wind_in_kmph':getText(node.getElementsByTagName('winddirection')[0].childNodes) + " " + getText(node.getElementsByTagName('windspeedKmph')[0].childNodes),
                                          'wind_in_mph':getText(node.getElementsByTagName('winddirection')[0].childNodes) + " " + getText(node.getElementsByTagName('windspeedMiles')[0].childNodes),
                                          'wind_direction':getText(node.getElementsByTagName('winddirection')[0].childNodes),
                                          'weather_desc': node.getElementsByTagName('weatherDesc')[0].childNodes[0].data,
                                          'weather_icon':node.getElementsByTagName('weatherIconUrl')[0].childNodes[0].data
                                          
                                          })
        
    data['current_conditions']=current_conditions
    data['wx_api_obj'] = wx_api_obj
    #data['long_term_forcast'] = long_term_forcast
    data['long_term_weather_info'] = long_term_weather_info
    socket.setdefaulttimeout(30)
    return render_to_response(template,data,context_instance=RequestContext(request))

