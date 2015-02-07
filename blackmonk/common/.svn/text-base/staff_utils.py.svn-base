from django.utils import simplejson
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template import RequestContext

from common.templatetags.ds_utils import get_msg_class_name

def success_response_to_save_category(append_data,data,template,MSG):
    """
    HTML TO APPEND IN LISTING PAGE AND DISPLAY IN LIGHTBOX AFTER ADDING/UPDATING AN CATEGORY
    """
    lightbox_html=render_to_string(template,data)
    append_html=render_to_string('admin/portal/common/append_category_list.html',append_data)
    send_data={'append_html':append_html, 'lightbox_html':lightbox_html,'status':True,'msg':str(MSG['CUS']),'mtype':get_msg_class_name('s'),'id':append_data['cat'].id}
    return HttpResponse(simplejson.dumps(send_data))

def success_response_to_save_parent_category(append_data,data,template,MSG,parent):
    """
        HTML TO APPEND IN LISTING PAGE AND DISPLAY IN LIGHTBOX AFTER AJAX ADDING/UPDATING AN CATEGORY/Parent Category
    """
    lightbox_html=render_to_string(template,data)
    if not parent:
        append_html=render_to_string('admin/portal/common/append_parent_category_list.html',append_data)
    else:
        append_html=render_to_string('admin/portal/common/append_sub_category_list.html',append_data)
    if parent:parent=1
    else:parent=0
    send_data={'append_html':append_html,'parent':parent,'lightbox_html':lightbox_html,'status':1,'msg':str(MSG['CUS']),'mtype':get_msg_class_name('s'),'id':append_data['cat'].id}
    if parent:
        try:send_data['parent_id']=append_data['cat'].parent.id
        except:send_data['parent_id']=append_data['cat'].parent_cat.id
    else:send_data['parent_id']=None
    return HttpResponse(simplejson.dumps(send_data))


def error_response(request,data,template,MSG):
    """
    ERROR STAFF ADD VENUE
    """
    lightbox_html=render_to_string(template,data,context_instance=RequestContext(request))
    send_data={'lightbox_html':lightbox_html,'status':0,'msg':str(MSG['OOPS']),'mtype':get_msg_class_name('e')}
    return HttpResponse(simplejson.dumps(send_data))
   
def response_delete_category(request,model,MSG):
    """
    DELETE CATEGORY COMMON METHOD FOR CATEGORY
    """
    try:
        try:id=request.GET['id'].split(',')
        except:id=request.GET['id']
        cat = model.objects.filter(id__in=id)
        cat.delete()
        status=1
        msg=MSG['CDS']
        mtype='s'
    except:
        status=0
        msg=MSG['OOPS']
        mtype='e'
    data={'status':status,'msg':str(msg),'mtype':get_msg_class_name(mtype)}
    return data

