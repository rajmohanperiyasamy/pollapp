import time
import HTMLParser
import datetime,time
import urllib2
from time import strptime
from xml.etree import ElementTree 

from xml.dom import minidom
from xml.dom.minidom import Node,parse,parseString

import getsettings
from domains import *
from django.contrib.auth import get_user_model
User = get_user_model()
from django.template.defaultfilters import slugify

from django.db import connection


from common.getunique import getUniqueValue
from hotels.models import Category,ApiSettings,Amenities,HotelDetails,Hotels,HotelImages,RoomAmenities,HotelRoomDetails

html_parser= HTMLParser.HTMLParser()
  


AMINITY_MASK={'1':'Business Center','2':'Fitness Center','4':'Hot Tub On-site','8':'Internet Access Available','16':'Kids Activities','32':'Kitchen or Kitchenette',
             '64':'Pets Allowed','128':'Pool','256':'Restaurant On-site','512':'Spa On-site','1024':'Whirlpool Bath Available','2048':'Breakfast','4096':'Babysitting',
             '8192':'Jacuzzi','16384':'Parking','32768':'Room Service','65536':' Accessible Path of Travel','131072':'Accessible Bathroom','262144':'Roll-in Shower',
             '524288':'Handicapped Parking','1048576':'In-room Accessibility','2097152':'Accessibility Equipment for the Deaf','4194304':'Braille or Raised Signage',
             '8388608':'Free Airport Shuttle','16777216':'Indoor Pool','33554432':'Outdoor Pool','67108864':'Extended Parking','134217728':'Free Parking'}

def __fetch_details(api_settings):
    #Working Code Live
    url = 'http://api.ean.com/ean-services/rs/hotel/v3/list?type=xml&apiKey=%s&cid=%s&locale=en_US&city=%s&minorRev=12'%(api_settings.api_key,api_settings.customer_id,urllib2.quote(api_settings.city))
    request = urllib2.Request(url, headers={"Accept" : "application/xml"})
    xml = urllib2.urlopen(request)
    tree = ElementTree.parse(xml)
    rootElem = tree.getroot()
    hotel_list = rootElem.find('HotelList').findall("HotelSummary")  
    
    
    """
    tree = ElementTree.parse('sample-list.xml')
    rootElem = tree.getroot()
    hotel_list = rootElem.find('HotelList').findall("HotelSummary") 
    """
    
    for hotel in hotel_list:
        
        try:
            hotel_obj = Hotels.objects.get(hotelid = hotel.findtext("hotelId"))
        except:
            hotel_obj = Hotels(hotelid = hotel.findtext("hotelId"))
        hotel_obj.created_by = admin
      
        hotel_obj.name = hotel.findtext("name")
        hotel_obj.slug = getUniqueValue(Hotels,slugify(hotel_obj.name),instance_pk=hotel_obj.id)
        hotel_obj.created_by = admin
        hotel_obj.address = hotel.findtext("address1")
        hotel_obj.city = hotel.findtext("city")
        hotel_obj.state_province_code = hotel.findtext("stateProvinceCode")
        hotel_obj.postal_code = hotel.findtext("postalCode")
        hotel_obj.country_code = hotel.findtext("countryCode")
        hotel_obj.airport_code = hotel.findtext("airportCode")
        hotel_obj.hotel_rating = hotel.findtext("hotelRating")
        
        try:hotel_obj.confidence_rating = hotel.findtext("confidenceRating")
        except:pass
        try:hotel_obj.tripadvisor_rating = hotel.findtext("tripAdvisorRating")
        except:pass
        try:hotel_obj.tripadvisor_review_count = hotel.findtext("tripAdvisorReviewCount")
        except:pass
        try:hotel_obj.tripadvisor_rating_url = hotel.findtext("tripAdvisorRatingUrl")
        except:pass
        try:hotel_obj.currency_code = hotel.findtext("rateCurrencyCode")
        except:pass
        try:hotel_obj.short_description = html_parser.unescape(hotel.findtext("shortDescription"))
        except:hotel_obj.short_description = hotel.findtext("shortDescription")
        hotel_obj.deeplink = hotel.findtext("deepLink")
        hotel_obj.save() 
           
    hotels = Hotels.objects.all().order_by('id')
    
    for hotel in hotels:
        time.sleep(1)
        
        url = "http://api.ean.com/ean-services/rs/hotel/v3/info?minorRev=12&cid=%s&apiKey=%s&locale=en_US&city=%s&xml=<HotelInformationRequest><hotelId>%s</hotelId></HotelInformationRequest>"%(api_settings.customer_id,api_settings.api_key,urllib2.quote(api_settings.city),hotel.hotelid)
        request = urllib2.Request(url, headers={"Accept" : "application/xml"})
        xml = urllib2.urlopen(request)
        tree = ElementTree.parse(xml)
        rootElem = tree.getroot()
        
        for summary in rootElem.findall("HotelSummary"):
            try:
                hotel_obj=Hotels.objects.get(hotelid=summary.findtext("hotelId"))
                hotel_obj.highrate = summary.findtext("highRate")
                hotel_obj.lowrate = summary.findtext("lowRate")
                try:hotel_obj.latitude = summary.findtext("latitude")
                except:pass
                try:hotel_obj.longitude = summary.findtext("longitude")
                except:pass
                hotel_obj.is_active = True
                hotel_obj.save()
                
                try:categories=summary.findtext("propertyCategory").split(',')
                except:categories=summary.findtext("propertyCategory")
                
                hotel_obj.category.clear()
                for cat in categories:
                    try:
                        category_obj=Category.objects.get(catid=int(cat))
                        hotel_obj.category.add(category_obj)
                    except:pass
            except:pass    
        
        for details in rootElem.findall("HotelDetails"):
            try:
                hotel_detail_obj = HotelDetails.objects.get(id=hotel_obj.details.id)
            except:
                hotel_detail_obj = HotelDetails()
                
            hotel_detail_obj.number_of_rooms = details.findtext("numberOfRooms")
            hotel_detail_obj.number_of_floors = details.findtext("numberOfFloors")
            hotel_detail_obj.checkin_time = details.findtext("checkInTime")
            hotel_detail_obj.checkout_time = details.findtext("checkOutTime")
            
            try:hotel_detail_obj.property_information = html_parser.unescape(details.findtext("propertyInformation"))
            except:hotel_detail_obj.property_information = details.findtext("propertyInformation")
            
            try:hotel_detail_obj.area_information = html_parser.unescape(details.findtext("areaInformation"))
            except:hotel_detail_obj.area_information = details.findtext("areaInformation")
            
            try:hotel_detail_obj.property_description = html_parser.unescape(details.findtext("propertyDescription"))
            except:hotel_detail_obj.property_description = details.findtext("propertyDescription")
            
            try:hotel_detail_obj.hotel_policy = html_parser.unescape(details.findtext("hotelPolicy"))
            except:hotel_detail_obj.hotel_policy = details.findtext("hotelPolicy")
            
            try:hotel_detail_obj.room_information = html_parser.unescape(details.findtext("roomInformation"))
            except:hotel_detail_obj.room_information = details.findtext("roomInformation")
            
            try:hotel_detail_obj.driving_directions = html_parser.unescape(details.findtext("drivingDirections"))
            except:hotel_detail_obj.driving_directions = details.findtext("drivingDirections")
            
            try:hotel_detail_obj.checkin_instructions = html_parser.unescape(details.findtext("checkInInstructions"))
            except:hotel_detail_obj.checkin_instructions = details.findtext("checkInInstructions")
            
            hotel_detail_obj.save()
            hotel_obj.details = hotel_detail_obj
            
            hotel_obj.save()
            
        for roominfo in rootElem.find("RoomTypes").findall("RoomType"):
            room_obj = HotelRoomDetails(hotel=hotel_obj)
            room_obj.type = roominfo.findtext("description")
            room_obj.description = roominfo.findtext("descriptionLong")
            room_obj.save()
            
            try:
                for room_amenity in roominfo.find("roomAmenities").findall("RoomAmenity"):
                    try:amenity = room_amenity.findtext("amenity")
                    except:amenity=False
                    if amenity:
                        try:
                            room_amenity_obj = RoomAmenities.objects.get(name__iexact=amenity)
                        except:
                            room_amenity_obj = RoomAmenities(name=amenity)
                            room_amenity_obj.save()    
                        room_obj.amenities.add(room_amenity_obj)
            except:pass
            
        try:
            for hotel_amnts in rootElem.find("PropertyAmenities").findall("PropertyAmenity"):
                
                try:hotelamenity = hotel_amnts.findtext("amenity")
                except:hotelamenity=False
                if hotelamenity:
                    try:
                        hotel_amenity_obj = Amenities.objects.get(name__iexact=hotelamenity)
                    except:
                        hotel_amenity_obj = Amenities(name=hotelamenity)
                        hotel_amenity_obj.save()
                    hotel_obj.amenities.add(hotel_amenity_obj)     
        except:pass
        
        try:
            for hotel_image in rootElem.find("HotelImages").findall("HotelImage"):
                hotel_image_obj = HotelImages(hotel=hotel_obj)
                hotel_image_obj.imageid = hotel_image.findtext("hotelImageId")
                try:hotel_image_obj.caption = hotel_image.findtext("caption")
                except:pass
                hotel_image_obj.image_big = hotel_image.findtext("url")
                hotel_image_obj.image_thumbnail = hotel_image.findtext("thumbnailUrl")
                hotel_image_obj.save()
        except:pass        
for domain_name in SCHEMATA_DOMAINS:
    connection.set_schemata_domain(domain_name)    
    try:
        api_settings = ApiSettings.objects.all()[:1][0]
    except:
        continue
     
    ''' Deleting Hotel Amenities,Images etc... '''
    Amenities.objects.all().delete()    
    HotelImages.objects.all().delete()    
    RoomAmenities.objects.all().delete()    
    HotelRoomDetails.objects.all().delete()  
    __fetch_details(api_settings)