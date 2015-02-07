from django.http import HttpResponse
from django.utils import simplejson
from django.conf import settings
from django.core.urlresolvers import reverse

from common.forms import UploadImageForm, UploadFileForm
from photo_library  import signals

def response_mimetype(request):
    if "application/json" in request.META['HTTP_ACCEPT']:
        return "application/json"
    else:
        return "text/plain"

"""
#######################################################################################################################
##############################################   GET DEFAULT IMAGES     ###############################################
#######################################################################################################################
"""
def get_default_images(request, ids, model):
    try:
        try:ids = ids.split(',')
        except:ids = ids
        photos = model.objects.filter(id__in=ids)
        data = []
        for clsphoto in photos:
            if clsphoto.photo:
                photo_dict = {'id':clsphoto.id, 'url': clsphoto.photo.url, 'thumbnail_url': clsphoto.photo.url, 'delete_url': clsphoto.get_delete_url(), 'delete_type': "DELETE"}
            else:
                photo_dict = {'id':clsphoto.id, 'url': clsphoto.photo_url, 'thumbnail_url': clsphoto.photo_url, 'delete_url': clsphoto.get_delete_url(), 'delete_type': "DELETE"}
            data.append(photo_dict)
        response = JSONResponse(data, {}, response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response
    except:return []
"""
#######################################################################################################################
##############################################   UPLOAD/DELETE FILES    ###############################################
#######################################################################################################################
"""
def upload_files(request, model, fk_object, fk_field):
    try:
        if request.FILES:
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                file = form.cleaned_data.get('file')
            else:
                data = [{'error': form.non_field_errors()}]
                response = JSONResponse(data, {}, response_mimetype(request))
                response['Content-Disposition'] = 'inline; filename=files.json'
                return response#HttpResponse(form.non_field_errors())

            if fk_object:files = model(**{fk_field: fk_object})
            else:files = model()

            files.file = file
            files.title = file.name
            files.uploaded_by = request.user
            files.save()
            data = [{'id':files.id, 'title': files.title, 'delete_url': files.get_delete_url(), 'delete_type': "DELETE"}]
            response = JSONResponse(data, {}, response_mimetype(request))
            response['Content-Disposition'] = 'inline; filename=files.json'
            return response

        else:
            if fk_object:
                files = model.objects.filter(**{fk_field: fk_object})
                data = []
                for clsphoto in files:
                    photo_dict = {'id':clsphoto.id, 'title': clsphoto.title, 'delete_url': clsphoto.get_delete_url(), 'delete_type': "DELETE"}
                    data.append(photo_dict)
                response = JSONResponse(data, {}, response_mimetype(request))
                response['Content-Disposition'] = 'inline; filename=files.json'
                return response
            else:return []
    except:
        data = [{'error': "Error in upload, Please try after sometime"}]
        response = JSONResponse(data, {}, response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response#HttpResponse(form.non_field_errors())

def delete_files(request, model, pk):
    try:
        file_obj = model.objects.get(id=pk)
        file_obj.delete()
        response = JSONResponse(True, {}, response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response
    except: return HttpResponse("Error in delete file")

"""
#######################################################################################################################
#####################################     UPLOAD PRODUCT/COUPON PHOTO      ############################################
#######################################################################################################################
"""
def upload_pro_cup_photo(request, model, fk_object, id):
    try:
        if request.FILES:
            form = UploadImageForm(request.POST, request.FILES)
            if form.is_valid():
                photo = form.cleaned_data.get('photo')
            else:
                data = [{'error': form.non_field_errors()}]
                response = JSONResponse(data, {}, response_mimetype(request))
                response['Content-Disposition'] = 'inline; filename=files.json'
                return response#HttpResponse(form.non_field_errors())

            photos = model.objects.get(id=id)
            photos.photo = photo
            photos.save()

            data = [{'id':photos.id, 'url': photos.photo.url, 'thumbnail_url': photos.photo.url, 'delete_url': photos.get_delete_url(), 'delete_type': "DELETE"}]
            response = JSONResponse(data, {}, response_mimetype(request))
            response['Content-Disposition'] = 'inline; filename=files.json'
            return response

        else:
            if id:
                photos = model.objects.filter(id=id)
                data = []
                for clsphoto in photos:
                    if clsphoto.photo:
                        photo_dict = {'id':clsphoto.id, 'url': clsphoto.photo.url, 'thumbnail_url': clsphoto.photo.url, 'delete_url': clsphoto.get_delete_url(), 'delete_type': "DELETE"}
                        data.append(photo_dict)
                response = JSONResponse(data, {}, response_mimetype(request))
                response['Content-Disposition'] = 'inline; filename=files.json'
                return response
            else:return []
    except:
        data = [{'error': "Error in upload photo url, Please try after sometime"}]
        response = JSONResponse(data, {}, response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response#HttpResponse(form.non_field_errors())

def delete_pro_cup_photos(request, model, pk):
    try:
        photo_obj = model.objects.get(id=pk)
        if photo_obj.business:
            photo_obj.photo = None
            photo_obj.save()
        else:
            photo_obj.delete()
        response = JSONResponse(True, {}, response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response
    except: return HttpResponse("Error in delete photo")
"""
#######################################################################################################################
#################################################     UPLOAD LOGO       ###############################################
#######################################################################################################################
"""
def upload_logo(request, model, fk_object=False,sweepstackes=False):
    try:
        if request.FILES:
            form = UploadImageForm(request.POST, request.FILES)
            if form.is_valid():
                photo = form.cleaned_data.get('photo')
            else:
                data = [{'error': form.non_field_errors()}]
                response = JSONResponse(data, {}, response_mimetype(request))
                response['Content-Disposition'] = 'inline; filename=files.json'
                return response#HttpResponse(form.non_field_errors())
            
            try:
                if sweepstackes and fk_object:
                    dphotos=model.objects.get(id=fk_object.image.id)
                    dphotos.delete()
            except:pass
            
            photos = model()
            if sweepstackes:photos.image = photo
            else:photos.logo = photo
            photos.uploaded_by = request.user
            photos.save()
            if fk_object:
                if sweepstackes:fk_object.image = photos
                else:fk_object.logo = photos
                fk_object.save()
            if sweepstackes:data = [{'id':photos.id, 'url': photos.image.url, 'thumbnail_url': photos.image.url, 'delete_url': photos.get_delete_url(), 'delete_type': "DELETE"}]
            else:data = [{'id':photos.id, 'url': photos.logo.url, 'thumbnail_url': photos.logo.url, 'delete_url': photos.get_delete_url(), 'delete_type': "DELETE"}]
            response = JSONResponse(data, {}, response_mimetype(request))
            response['Content-Disposition'] = 'inline; filename=files.json'
            return response

        else:
            if fk_object:
                if sweepstackes and fk_object.image:
                    photos = model.objects.filter(id=fk_object.image.id)
                    data = []
                    for clsphoto in photos:
                        photo_dict = {'id':clsphoto.id, 'url': clsphoto.image.url, 'thumbnail_url': clsphoto.image.url, 'delete_url': clsphoto.get_delete_url(), 'delete_type': "DELETE"}
                        data.append(photo_dict)
                        response = JSONResponse(data, {}, response_mimetype(request))
                        response['Content-Disposition'] = 'inline; filename=files.json'
                        return response  
                elif fk_object.logo:
                    photos = model.objects.filter(id=fk_object.logo.id)
                    data = []
                    for clsphoto in photos:
                        photo_dict = {'id':clsphoto.id, 'url': clsphoto.logo.url, 'thumbnail_url': clsphoto.logo.url, 'delete_url': clsphoto.get_delete_url(), 'delete_type': "DELETE"}
                        data.append(photo_dict)
                    response = JSONResponse(data, {}, response_mimetype(request))
                    response['Content-Disposition'] = 'inline; filename=files.json'
                    return response
                else:return []
            else:return []
    except:
        data = [{'error': "Error in upload photo url, Please try after sometime"}]
        response = JSONResponse(data, {}, response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response#HttpResponse(form.non_field_errors())
"""
#######################################################################################################################
##########################################      UPLOAD Profile PIc       ##############################################
#######################################################################################################################
"""
def upload_profile_pic(request, fk_object):
    try:
        if request.FILES:
            form = UploadImageForm(request.POST, request.FILES)
            if form.is_valid():
                photo = form.cleaned_data.get('photo')
            else:
                data = [{'error': form.non_field_errors()}]
                response = JSONResponse(data, {}, response_mimetype(request))
                response['Content-Disposition'] = 'inline; filename=files.json'
                return response#HttpResponse(form.non_field_errors())

            fk_object.image = photo
            fk_object.save()

            data = [{'id':fk_object.id, 'url': fk_object.image.url, 'thumbnail_url': fk_object.image.url, 'delete_url': fk_object.get_delete_url(), 'delete_type': "DELETE"}]
            response = JSONResponse(data, {}, response_mimetype(request))
            response['Content-Disposition'] = 'inline; filename=files.json'
            return response
        else:
            if fk_object:
                if fk_object.image:
                    data = [{'id':fk_object.id, 'url': fk_object.image.url, 'thumbnail_url': fk_object.image.url, 'delete_url': fk_object.get_delete_url(), 'delete_type': "DELETE"}]
                    response = JSONResponse(data, {}, response_mimetype(request))
                    response['Content-Disposition'] = 'inline; filename=files.json'
                    return response
                else:return []
            else:return []
    except:
        data = [{'error': "Error in upload photo url, Please try after sometime"}]
        response = JSONResponse(data, {}, response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response#HttpResponse(form.non_field_errors())
"""
#######################################################################################################################
###############################################     UPLOAD PHOTO        ###############################################
#######################################################################################################################
"""
def upload_photos(request, model, fk_object, fk_field, attraction=False, staff=False, approved=False):
    try:
        if request.FILES:
            form = UploadImageForm(request.POST, request.FILES)
            if form.is_valid():
                photo = form.cleaned_data.get('photo')
            else:
                data = [{'error': form.non_field_errors()}]
                response = JSONResponse(data, {}, response_mimetype(request))
                response['Content-Disposition'] = 'inline; filename=files.json'
                return response#HttpResponse(form.non_field_errors())
            if fk_object:
                photos = model(**{fk_field: fk_object})
                photos.title = fk_object
            else:
                photos = model()

            if attraction:
                if staff:photos.is_approved = True
                else:photos.is_approved = False
            photos.photo = photo
            photos.uploaded_by = request.user
            photos.save()
            data = []
            photo_dict = {'id':photos.id, 'url': photos.photo.url, 'thumbnail_url': photos.photo.url, 'delete_url': photos.get_delete_url(), 'delete_type': "DELETE"}
            if attraction:
                if photos.is_approved:photo_dict['is_approved'] = False
                else:photo_dict['is_approved'] = True
                photo_dict['uploaded_by'] = str(photos.uploaded_by)
                photo_dict['uploaded_on'] = str(photos.uploaded_on.strftime("%B %d %Y"))
            data.append(photo_dict)
            response = JSONResponse(data, {}, response_mimetype(request))
            response['Content-Disposition'] = 'inline; filename=files.json'
            return response

        else:
            if fk_object:
                if approved:photos = model.objects.filter(**{fk_field: fk_object}).exclude(is_approved=False)
                else:photos = model.objects.filter(**{fk_field: fk_object})
                data = []
                for clsphoto in photos:
                    if clsphoto.photo:
                        photo_dict = {'id':clsphoto.id, 'url': clsphoto.photo.url, 'thumbnail_url': clsphoto.photo.url, 'delete_url': clsphoto.get_delete_url(), 'delete_type': "DELETE"}
                        if attraction:
                            if clsphoto.is_approved:photo_dict['is_approved'] = False
                            else:photo_dict['is_approved'] = True
                            photo_dict['uploaded_by'] = str(clsphoto.uploaded_by)
                            photo_dict['uploaded_on'] = str(clsphoto.uploaded_on.strftime("%B %d %Y"))
                    else:
                        photo_dict = {'id':clsphoto.id, 'url': clsphoto.photo_url, 'thumbnail_url': clsphoto.photo_url, 'delete_url': clsphoto.get_delete_url(), 'delete_type': "DELETE"}
                    data.append(photo_dict)
                response = JSONResponse(data, {}, response_mimetype(request))
                response['Content-Disposition'] = 'inline; filename=files.json'
                return response
            else:
                return HttpResponse('No Photo Album')
    except:
        data = [{'error': "Error in upload photo url, Please try after sometime"}]
        response = JSONResponse(data, {}, response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response#HttpResponse(form.non_field_errors())
"""
#######################################################################################################################
###############################################   UPLOAD PHOTO GALLERY  ###############################################
#######################################################################################################################
"""
def upload_photos_forgallery(request, model, fk_object, fk_field, caption=False,featured=False):
    try:
        if request.FILES:
            form = UploadImageForm(request.POST, request.FILES)
            if form.is_valid():
                photo = form.cleaned_data.get('photo')
            else:
                data = [{'error': form.non_field_errors()}]
                response = JSONResponse(data, {}, response_mimetype(request))
                response['Content-Disposition'] = 'inline; filename=files.json'
                return response#HttpResponse(form.non_field_errors())
            if fk_object:
                photos = model(**{fk_field: fk_object})
                if caption:
                    photos.caption = caption
                else:
                    photos.caption = fk_object
                photos.photo = photo
                photos.created_by = request.user
                photos.modified_by = request.user
                photos.is_active = True
                photos.status = 'N'
                if featured:
                    photos.featured=True
                fk_object.save()
                photos.save()
                update_caption_url = reverse("gallery_ajax_update_photo_caption", args=[photos.id])
                data = [{"gal_id":fk_object.id,
                         "photo_id": photos.id,
                         'url': photos.photo.url,
                         'thumbnail_url': photos.photo.url,
                         'delete_url': photos.get_delete_url(),
                         'delete_type': "DELETE",
                         'caption':str(photos.caption),
                         "update_caption_url": update_caption_url,
                         'uploaded_by': str(photos.created_by),
                         'uploaded_on': str(photos.created_on.strftime("%B %d %Y")) 
                 }]
                response = JSONResponse(data, {}, response_mimetype(request))
                response['Content-Disposition'] = 'inline; filename=files.json'
                return response
            else:
                photoobj = model()
                if caption: 
                    photoobj.caption = caption
                photoobj.photo = photo
                photoobj.created_by = request.user
                photoobj.modified_by = request.user
                photoobj.is_active = True
                photoobj.status = 'N'
                photoobj.save()
                update_caption_url = reverse("gallery_ajax_update_photo_caption", args=[photoobj.id])
                data = [{"photo_id":photoobj.id,
                         'url': photoobj.photo.url,
                         'thumbnail_url': photoobj.photo.url,
                         'delete_url': photoobj.get_delete_url(),
                         'delete_type': "DELETE",
                         'caption':str(photoobj.caption),
                         "update_caption_url": update_caption_url,
                         'uploaded_by': str(photoobj.created_by),
                         'uploaded_on': str(photoobj.created_on.strftime("%B %d %Y")) 
                }]
                response = JSONResponse(data, {}, response_mimetype(request))
                response['Content-Disposition'] = 'inline; filename=files.json'
                return response
        else:
            if fk_object:
                photos = fk_object.get_gallery_uploaded_images()
                data = []
                for clsphoto in photos:
                    update_caption_url = reverse("gallery_ajax_update_photo_caption", args=[clsphoto.id])
                    if clsphoto.photo:
                        photo_dict = {"photo_id": clsphoto.id, "gal_id":fk_object.id, 'id':clsphoto.id, 'url': clsphoto.photo.url, 'thumbnail_url': clsphoto.photo.url, 'delete_url': clsphoto.get_delete_url(), 'delete_type': "DELETE", 'caption':clsphoto.caption, "update_caption_url": update_caption_url}
                    else:
                        photo_dict = {"photo_id": clsphoto.id, "gal_id":fk_object.id, 'id':clsphoto.id, 'url': clsphoto.photo_url, 'thumbnail_url': clsphoto.photo_url, 'delete_url': clsphoto.get_delete_url(), 'delete_type': "DELETE", 'caption':clsphoto.caption, "update_caption_url": update_caption_url}
                    photo_dict['uploaded_by'] = str(clsphoto.created_by)
                    photo_dict['uploaded_on'] = str(clsphoto.created_on.strftime("%B %d %Y"))
                    data.append(photo_dict)
                response = JSONResponse(data, {}, response_mimetype(request))
                response['Content-Disposition'] = 'inline; filename=files.json'
                return response
            else:
                return HttpResponse('No Photo Album')
    except:
        from sys import exc_info
        data = [{'error': str(exc_info())}]  # "Error in upload photo url, Please try after sometime"}] 
        response = JSONResponse(data, {}, response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response #HttpResponse(form.non_field_errors())


def update_photo_caption(request,photo_obj):
    from common.templatetags.ds_utils import get_msg_class_name
    from common.static_msg import COMMON_MESSAGES
    return_data={}
    try:
        photo_obj.caption = request.REQUEST['caption']
        photo_obj.save()
        status = True
        msg = str(COMMON_MESSAGES['PCUS'])
        mtype = get_msg_class_name('s')
    except:
        status = True
        msg = str(COMMON_MESSAGES['ERROR'])
        mtype = get_msg_class_name('e') 
    return_data['status'] = status
    return_data['msg'] = msg   
    return_data['mtype'] = mtype   
    return HttpResponse(simplejson.dumps(return_data))
"""
#######################################################################################################################
#################################################     DELETE PHOTOS    ###############################################
#######################################################################################################################
"""

def delete_photos(request, model, pk):
    try:
        photo_obj = model.objects.get(id=pk)
        photo_obj.delete()
        response = JSONResponse(True, {}, response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response
    except: return HttpResponse("Error in delete photo")

def delete_photos_fake(request):
    try:
        response = JSONResponse(True, {}, response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response
    except: return HttpResponse("Error in delete photo")
    
def delete_profile_photo(request, obj):
    try:
        obj.image = None
        obj.save()
        response = JSONResponse(True, {}, response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response
    except: return HttpResponse("Error in delete photo")

class JSONResponse(HttpResponse):
    """JSON response class."""
    def __init__(self, obj='', json_opts={}, mimetype="application/json", *args, **kwargs):
        content = simplejson.dumps(obj, **json_opts)
        super(JSONResponse, self).__init__(content, mimetype, *args, **kwargs)


"""
#######################################################################################################################
#################################################   UPLOAD LOGO CONFIG  ###############################################
#######################################################################################################################
"""
def config_upload_logo(request, model, fk_object, type=False):
    try:
        if request.FILES:
            form = UploadImageForm(request.POST, request.FILES)
            if form.is_valid():
                photo = form.cleaned_data.get('photo')
            else:
                data = [{'error': form.non_field_errors()}]
                response = JSONResponse(data, {}, response_mimetype(request))
                response['Content-Disposition'] = 'inline; filename=files.json'
                return response#HttpResponse(form.non_field_errors())

            photos = fk_object
            if type == 'fav':photos.fav_ico = photo
            elif type == 'logo':photos.logo = photo
            else:photos.iphone_logo = photo
            photos.save()
            if type == 'fav':data = [{'id':photos.id, 'url': photos.fav_ico.url, 'thumbnail_url': photos.fav_ico.url, 'delete_url': photos.get_delete_fav_url(), 'delete_type': "DELETE"}]
            elif type == 'logo':data = [{'id':photos.id, 'url': photos.logo.url, 'thumbnail_url': photos.logo.url, 'delete_url': photos.get_delete_logo_url(), 'delete_type': "DELETE"}]
            else:data = [{'id':photos.id, 'url': photos.iphone_logo.url, 'thumbnail_url': photos.iphone_logo.url, 'delete_url': photos.get_delete_iphonelogo_url(), 'delete_type': "DELETE"}]
            response = JSONResponse(data, {}, response_mimetype(request))
            response['Content-Disposition'] = 'inline; filename=files.json'
            return response

        else:
            if fk_object:
                if type == 'fav':
                    if fk_object.fav_ico:
                        photos = model.objects.filter(id=fk_object.id)
                        data = []
                        for clsphoto in photos:
                            photo_dict = {'id':clsphoto.id, 'url': clsphoto.fav_ico.url, 'thumbnail_url': clsphoto.fav_ico.url, 'delete_url': clsphoto.get_delete_fav_url(), 'delete_type': "DELETE"}
                            data.append(photo_dict)
                        response = JSONResponse(data, {}, response_mimetype(request))
                        response['Content-Disposition'] = 'inline; filename=files.json'
                        return response
                    else:return []
                elif type == 'logo':
                    if fk_object.logo:
                        photos = model.objects.filter(id=fk_object.id)
                        data = []
                        for clsphoto in photos:
                            photo_dict = {'id':clsphoto.id, 'url': clsphoto.logo.url, 'thumbnail_url': clsphoto.logo.url, 'delete_url': clsphoto.get_delete_logo_url(), 'delete_type': "DELETE"}
                            data.append(photo_dict)
                        response = JSONResponse(data, {}, response_mimetype(request))
                        response['Content-Disposition'] = 'inline; filename=files.json'
                        return response
                    else:return []
                else:
                    if fk_object.iphone_logo:
                        photos = model.objects.filter(id=fk_object.id)
                        data = []
                        for clsphoto in photos:
                            photo_dict = {'id':clsphoto.id, 'url': clsphoto.iphone_logo.url, 'thumbnail_url': clsphoto.iphone_logo.url, 'delete_url': clsphoto.get_delete_iphonelogo_url(), 'delete_type': "DELETE"}
                            data.append(photo_dict)
                        response = JSONResponse(data, {}, response_mimetype(request))
                        response['Content-Disposition'] = 'inline; filename=files.json'
                        return response
                    else:return []
            else:return []
    except:
        data = [{'error': "Error in upload photo url, Please try after sometime"}]
        response = JSONResponse(data, {}, response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response#HttpResponse(form.non_field_errors())     

def config_delete_logo(request, obj):
    try:
        obj.logo = None
        obj.save()
        response = JSONResponse(True, {}, response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response
    except: return HttpResponse("Error in delete photo")

def config_delete_fav(request, obj):
    try:
        obj.fav_ico = None
        obj.save()
        response = JSONResponse(True, {}, response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response
    except: return HttpResponse("Error in delete photo")

def config_delete_iphone(request, obj):
    try:
        obj.iphone_logo = None
        obj.save()
        response = JSONResponse(True, {}, response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response
    except: return HttpResponse("Error in delete photo")
 
from common.models import CoverPhoto
from PIL import ImageFile
ImageFile.MAXBLOCK = 1048576

def upload_cover_photo(request, ctype=None, cobj=None):
    try:
        if request.FILES:
            form = UploadImageForm(request.POST, request.FILES)
            if form.is_valid():
                photo = form.cleaned_data.get('photo')
            else:
                data = [{'error': form.non_field_errors()}]
                response = JSONResponse(data, {}, response_mimetype(request))
                response['Content-Disposition'] = 'inline; filename=files.json'
                return response
            
            try:
                CoverObject = CoverPhoto.objects.get(content_type=ctype, object_id=cobj.id)
            except:
                CoverObject = CoverPhoto()
                if cobj is not None:
                    CoverObject.content_object = cobj
            CoverObject.photo = photo
            CoverObject.save()
        else:
            try:
                CoverObject = CoverPhoto.objects.get(content_type=ctype, object_id=cobj.id)
            except:
                return HttpResponse("No Cover Photo")
        data = [{
            'cover_id': CoverObject.id, 
            'cover_url': CoverObject.photo.url, 
            'delete_url': CoverObject.get_delete_url(),
            'update_url': CoverObject.get_update_url(),
        },]
        response = JSONResponse(data, {}, response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response
    except:
        import sys
        return HttpResponse(str(sys.exc_info()))
        data = [{'error': "Error in upload photo url, Please try after sometime"}]
        response = JSONResponse(data, {}, response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response#HttpResponse(form.non_field_errors())