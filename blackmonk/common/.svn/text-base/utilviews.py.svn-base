import Image
import ImageEnhance
import ImageFilter
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse

from common.fileupload import upload_cover_photo, delete_photos
from common.models import CoverPhoto


@login_required
def cover_photo(request):
    try:
        ctype_id = int(request.REQUEST['ctype'])
        cobj_id = int(request.REQUEST['cobj'])
        ctype = ContentType.objects.get_for_id(ctype_id)
        cobj = ctype.get_object_for_this_type(pk=cobj_id)
        response = upload_cover_photo(request, ctype, cobj)
        return response
    except:
        if request.POST:
            response = upload_cover_photo(request)
            return response
        else:
            return HttpResponse('No Object')

@login_required
def delete_cover_photo(request, pk):
    return delete_photos(request, CoverPhoto, pk)

def image_cropper(request, CoverObject):
    try:
        top = int(request.POST['cover_y1'])
        left = int(request.POST['cover_x1'])
        right = int(request.POST['cover_x2'])
        bottom = int(request.POST['cover_y2'])
        path = CoverObject.photo.path
        image = Image.open(path)
        box = [left, top, right, bottom]
        image = image.crop(box)
        if image.mode not in ('L', 'RGB'):
            image = image.convert('RGB')
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(0.8)
        image = image.filter(ImageFilter.DETAIL)
        image.save(path,quality=90,optimised=True)
    except:
        pass
    

@login_required
def crop_and_save_coverphoto(request, cobj):
    ctype = ContentType.objects.get_for_model(cobj)
    cover_id = int(request.POST['cover_id'])
    CoverObject = CoverPhoto.objects.get(id=cover_id)
    CoverObject.content_object = cobj
    image_cropper(request, CoverObject)
    CoverObject.save()
    return True

@login_required
def ajax_crop_and_save(request, pk):
    CoverObject = CoverPhoto.objects.get(id=pk)
    image_cropper(request, CoverObject)
    CoverObject.save()
    return HttpResponse('Success')