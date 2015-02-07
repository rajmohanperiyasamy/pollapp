import uuid
import os
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser,
    PermissionsMixin)
from django.db import models
from django.contrib.auth.models import Group
import datetime
import cPickle as pickle
import base64
import Image, ImageFilter
import os.path
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.shortcuts import get_object_or_404, get_list_or_404
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from common.getunique import getUniqueValue
from django.template.defaultfilters import slugify
from django.conf import settings
from django.utils import timezone
from django_countries.countries import COUNTRIES


User = settings.AUTH_USER_MODEL


from easy_thumbnails.fields  import ThumbnailerImageField
Gender = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('R', 'Unspecified'),
)
RealtionshipStatus = (
        ('S', 'Single'),
        ('T', 'Taken'),
)


def get_profile_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('profile', filename)

class AbstractAddress(models.Model):
    address1 = models.CharField(max_length=255, null=True)
    address2 = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=50, blank=True, choices=COUNTRIES)
    state = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    pin = models.CharField(max_length=20, null=True)
    mobile = models.CharField(max_length=25, null=True)
    phone = models.CharField(max_length=25, null=True)

    email = models.EmailField(null=True)

    pointer_lat = models.FloatField(null=True)
    pointer_lng = models.FloatField(null=True)
    map_zoom = models.SmallIntegerField(default=11, null=True)

    class Meta:
        abstract = True



class BmUserManager(BaseUserManager):

    def create_user(self, useremail, display_name, password=None):
        if not useremail:
            raise ValueError('Users must have an email address')
        
        now = timezone.now()
        
        user = self.model(useremail=BmUserManager.normalize_email(useremail.lower()))
        user.display_name = display_name
        user.email = useremail.lower()
        user.profile_slug = getUniqueValue(BmUser,slugify(useremail.split("@")[0]),field_name="profile_slug")
        user.set_password(password)
        user.status='A'
        user.last_login = user.date_joined = now
        user.save(using=self._db)
        return user

    def create_superuser(self, useremail, display_name, password):
        user = self.create_user(useremail=useremail.lower(),
            display_name=display_name, password=password)
        user.email = useremail.lower()
        user.display_name = display_name
        user.is_superuser = True
        user.is_staff = True
        user.status='A'
        user.save(using=self._db)
        return user


class BmUser(AbstractBaseUser, PermissionsMixin, AbstractAddress):
    display_name = models.CharField(max_length=25)
    profile_slug = models.CharField(max_length=25,null=True)
    image = ThumbnailerImageField(
        upload_to=get_profile_path,
        resize_source=dict(size=(300, 0), crop='smart'),
        null=True
    )
    gender = models.CharField(max_length=1, blank=True, choices=Gender)
    dateofbirth = models.DateField(null=True, blank=True)
    about = models.TextField(blank=True)
    
    location = models.CharField(max_length=150, null=True)
    company = models.CharField(max_length=150, null=True)
    website = models.CharField(max_length=150, null=True)
    
    fb_url = models.CharField(max_length=150, null=True)
    twitter_url = models.CharField(max_length=150, null=True)
    gooleplus_url = models.CharField(max_length=150, null=True)

    useremail = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    email_isvalid = models.CharField(max_length=1,default='N')# 'N'=ValidationPending, 'I'=invalid, 'V'=valid 
    # status {A:Active, B:Blocked, P:private}
    status = models.CharField(max_length=1, default='A')

    USERNAME_FIELD = 'useremail'
    REQUIRED_FIELDS = ['display_name']
    objects = BmUserManager()

    def __unicode__(self):
        return self.display_name
    
    def get_full_name(self):
        return self.display_name
    
    def user(self):
        return self
    
    def username(self):
        return self.profile_slug
    
    def first_name(self):
        return self.display_name
    
    def last_name(self):
        return ""

    @property 
    def is_active(self):
        if self.status == 'A':
            return True
        else:
            return False
    
    def get_delete_url(self):
        return reverse('usermgmt_ajax_delete_photos', args=[self.id])
        
class EmailSetting(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    qa_reply = models.BooleanField(default=False)
    profile_update= models.BooleanField(default=False)
    classified_reply= models.BooleanField(default=False)
    article_comment= models.BooleanField(default=False)
    business_comment=models.BooleanField(default=False)
    def __unicode__(self):
        return _("%s") % self.user
    
INVITE_STATUS = (
    ("1", "Created"),
    ("2", "Sent"),
    ("3", "Failed"),
    ("4", "Accepted")
)

class EmailTemplates(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    code = models.CharField(max_length=3)
    template = models.TextField(blank=True)
    subject = models.CharField(max_length=1000)
    active = models.BooleanField(default=True)
    date_updated = models.DateTimeField(auto_now = True)
    
    def __unicode__(self):
        return _("%s") % self.name


class Favorite(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    user = models.ForeignKey(User)
    date_added = models.DateTimeField(default=datetime.datetime.now)
    def __unicode__(self):
        return "%s-%s" % (self.user, self.content_object)
    @classmethod
    def create_favorite(cls, user, content_object):
        """
        creates a favorite relation between user and content_object and saves it
        to the database.
        
        It returns the created Favorite object
        """
        ct = ContentType.objects.get_for_model(type(content_object))
        try:
            cls.objects.get(user=user,content_type = ct,object_id = content_object.id)
            return False
        except:
            fav = cls(
                user=user, 
                content_type = ct, 
                object_id = content_object.id, 
                content_object = content_object
            )
            fav.save()
            return fav
    
class RetivePwd(models.Model):
    user = models.OneToOneField(User)
    code = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    
    
class ProfilePrivacy(models.Model):
    profile = models.OneToOneField(BmUser, primary_key=True)
    show_sex = models.BooleanField(default=True)
    show_contact = models.BooleanField(default=False)
    show_community_post = models.BooleanField(default=True)
    show_reviews = models.BooleanField(default=True)
    show_articles = models.BooleanField(default=True)
    show_events = models.BooleanField(default=True)
    show_photos = models.BooleanField(default=True)
    show_videos = models.BooleanField(default=True)
    show_business = models.BooleanField(default=True)
    show_classifieds = models.BooleanField(default=True)
    show_bookmarks = models.BooleanField(default=True)
    is_public = models.BooleanField(default=True)
    show_email_form = models.BooleanField(default=True)
     
    def __unicode__(self):
        return _("%s") % self.profile
