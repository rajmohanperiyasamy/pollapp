from django.conf import settings
from PIL import Image
import os
import ImageEnhance
import ImageFilter

def cropImage(PATH,filename,SIZE):
    #####################################
    #    it store same SIZE or more
    ####################################
    try:
        im = Image.open('%simages/%s/%s' % (settings.MEDIA_ROOT,PATH,filename)).convert("RGB")
    except:
        im = Image.open('%simages/%s/%s' % (settings.MEDIA_ROOT,PATH,filename))
    x,y = im.size
    X,Y,SIZEX,SIZEY = get_width_height(x,y,SIZE)
    im.thumbnail((X, Y), Image.ANTIALIAS)
    try:
        enhancer = ImageEnhance.Sharpness(im)
        image=enhancer.enhance(1)
        image = image.filter(ImageFilter.DETAIL)
        image.save('%simages/%s/%s' % (settings.MEDIA_ROOT,PATH,filename), "JPEG",quality=90,optimize=True)
    except:
        image.save('%simages/%s/%s' % (settings.MEDIA_ROOT,PATH,filename))
    return filename


def get_width_height(x,y,SIZE):
    try:
        SIZEX = SIZE[0]
        SIZEY = SIZE[1]
        r1 = x*1.0/y
        r2 = SIZEX*1.0/SIZEY
        if r1==r2:
            X=SIZEX
            Y=SIZEY
        elif x==y:
            if SIZEX>SIZEY:
                X=SIZEX
                Y=SIZEX
            else:
                X=SIZEY
                Y=SIZEY
        elif (x-SIZEX)>(y-SIZEY):
            Y = SIZEY
            X = Y*x/y
        else:
            X = SIZEX
            Y = X*y/x
    except:
        SIZEX = SIZE
        SIZEY = SIZE
        r1 = x*1.0/y
        r2 = SIZEX*1.0/SIZEY
        if r1==r2:
            X=SIZEX
            Y=SIZEY
        elif x==y:
            X=SIZE
            Y=SIZE
        elif x > y:
            Y = SIZE
            X = Y*x/y
        else:
            X = SIZE
            Y = X*y/x
    return [X,Y,SIZEX,SIZEY]

def get_image_xy(image, SIZE):
    x,y = image.size
    X,Y,SIZEX,SIZEY = get_width_height(x,y,SIZE)
    left= int((X-SIZEX)/2)
    upper= int((Y-SIZEY)/2)
    right = left+SIZEX
    lower = upper+SIZEY
    image.thumbnail((X, Y), Image.ANTIALIAS)
    if SIZEX<=x and SIZEY<=y:
        try:
            image = image.crop((left, upper, right, lower))
        except:pass
    try:
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(1)
        image = image.filter(ImageFilter.DETAIL)
    except:pass
    return image


def imageThumbnail(PATH,filename,SIZE):
    #####################################
    #    it store same SIZE only
    ####################################
    try:
        image = Image.open('%simages/%s/%s' % (settings.MEDIA_ROOT,PATH,filename)).convert("RGB")
    except:
        image = Image.open('%simages/%s/%s' % (settings.MEDIA_ROOT,PATH,filename))
    
    image = get_image_xy(image,SIZE)

    try:
        image.save('%simages/%s/%s' % (settings.MEDIA_ROOT,PATH,filename), "JPEG",quality=90,optimize=True)
    except:
        image.save('%simages/%s/%s' % (settings.MEDIA_ROOT,PATH,filename))
    return filename

def db_thumbnail(image,width,height):
    image = get_image_xy(image,[width,height])
    return image

## PATH="gallery/fdsf" APPEND=id  FEIELD="image" SIZE="100"  DELETEIMG="_NoImg_"
def Uploadimage(request,PATH,APPEND,FEIELD,SIZE,DELETEIMG):
    if '%s' % FEIELD in request.FILES:
        file = request.FILES['%s' % FEIELD]
        filename = file
        filename = str(APPEND) + str(filename)
        if DELETEIMG != "_NoImg_" and DELETEIMG != None:
            try:
                os.remove('%simages/%s/%s' % (settings.MEDIA_ROOT,PATH, DELETEIMG))
            except:
                pass
        fd = open('%simages/%s/%s' % (settings.MEDIA_ROOT,PATH,filename), 'wb+')
        di = file.read()
        fd.write(di)
        fd.close()
        return imageThumbnail(PATH,filename,SIZE)
    else:
        return False