from django.template.loader import render_to_string
from django.http import HttpResponse
import simplejson
from common.templatetags.ds_utils import get_msg_class_name

def success_response_to_restaurant_module(append_data,data,template,MSG):
    """
    HTML TO APPEND IN LISTING PAGE AND DISPLAY IN LIGHTBOX AFTER ADDING/UPDATING AN Meal type and Cuisine
    """
    print ",,,,,,,,,,,,,,", append_data['label']
    lightbox_html=render_to_string(template,data)
    append_html=render_to_string('admin/portal/common/append_module_list.html',append_data)
    send_data={'append_html':append_html, 'lightbox_html':lightbox_html,'status':True,'msg':str(MSG['CUS']),'mtype':get_msg_class_name('s'),'id':append_data['cat'].id}
    return HttpResponse(simplejson.dumps(send_data))