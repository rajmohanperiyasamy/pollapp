from django.conf import settings
from random import choice,randint
try:
    from hashlib import sha1
except ImportError:
    import sha

def getCaptcha():
    if True:
        return {}
    TOTAL_CHAR = 3
    WIDTH = 30*TOTAL_CHAR
    HEIGHT = 35
    randcolor=[(36,24,130),(210,105,30),(47,79,47)]
    rotatechoice = [-30,-25,-20,-10,10,20,25,30]
    FONTS = ['absci___.ttf','luxirri.ttf']
    FONTS_SIZE = [25,22]
    from PIL import Image, ImageDraw, ImageFont
    SALT = settings.SECRET_KEY[:20]
    imgtext = ''.join([choice('QWERTYUPASDFGHKLXVBNMabdeh') for i in range(TOTAL_CHAR)])
    try:
        imghash = sha1(SALT+imgtext).hexdigest()
    except:
        imghash = sha.new(SALT+imgtext).hexdigest()
    im = Image.new("RGB",(WIDTH,HEIGHT),(999,999,999))
    fon = randint(0,1)
    font=ImageFont.truetype('%s/fonts/%s'%(settings.MEDIA_ROOT,FONTS[fon]), FONTS_SIZE[fon])
    
    xd=0
    for simgtext in imgtext:
        single = Image.new("RGBA",(100,100),(999,999,999))
        draw = ImageDraw.Draw(single)        
        rc = randint(0,2)
        draw.text((38,38), simgtext, font=font, fill=randcolor[rc])
        r = randint(0,6)
        single = single.rotate(rotatechoice[r])
        single = single.crop((35, 37, 65, 72))
        im.paste(single, (xd, 0, xd+30, 35))
        xd = xd +30
       
    tempname = ''.join([choice('abcdefghijklmnopqrstuvwxyz') for i in range(3)])
    temp = settings.MEDIA_ROOT +'/images/captcha/'+ tempname + '.jpg'
    tempname = tempname + '.jpg'
    im.save(temp,'JPEG')
    captcha={'hash': imghash,'image' : tempname,'width':WIDTH,'height':HEIGHT,'charlength':TOTAL_CHAR}
    return captcha

def checkCaptcha(hash,code):
    try:
        s_hash = sha1(settings.SECRET_KEY[:20]+code).hexdigest()
    except:
        s_hash = sha.new(settings.SECRET_KEY[:20]+code).hexdigest()
    if hash == s_hash:return True
    else:return False

def getNew(request):
    from django.http import HttpResponse
    import os
    try:
        os.remove('%simages/captcha/%s' % (settings.MEDIA_ROOT, request.GET['img']))
    except:pass
    scaptcha = getCaptcha()
    imghash = scaptcha['hash']
    tempname = scaptcha['image']
    data = imghash+','+tempname
    return HttpResponse(data)
