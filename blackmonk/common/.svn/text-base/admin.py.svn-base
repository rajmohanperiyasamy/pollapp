from django.contrib import admin
from django import forms
from common.models import ModuleNames,CommonConfigure, ModuleSetting, COMMENT_STATUS, MODULE_STATUS, M_CLASSIFIED_STATUS, PAYMENT_EVENT,PAYMENT_BUSINESS,PAYMENT_ARTICLE,PAYMENT_CLASSIFIED



class CommonConfigureForm( forms.ModelForm ):
    logo = forms.CharField( widget=forms.TextInput(attrs={'style':'width:600px;'}), label='Logo' )
    signin_logo = forms.CharField( widget=forms.TextInput(attrs={'style':'width:600px;'}), label='Signin Logo' )
    staff_logo = forms.CharField( widget=forms.TextInput(attrs={'style':'width:600px;'}), label='Staff Logo' )
    bookmark_logo = forms.CharField( widget=forms.TextInput(attrs={'style':'width:600px;'}), label='Bookmark Logo' )
    google_map_key = forms.CharField( widget=forms.TextInput(attrs={'style':'width:600px;'}), label='Map Key' )
    google_analytics_script = forms.CharField( widget=forms.Textarea(attrs={'style':'width:600px;height:90px;'}), label='Analytics Script' )
    google_meta = forms.CharField( widget=forms.Textarea(attrs={'style':'width:600px;height:50px;'}), label='Meta Data' )
    paypal_identity_token = forms.CharField( required = False, widget=forms.TextInput(attrs={'style':'width:600px;'}), label='Paypal Identity Token' )
    facebook_page_url = forms.CharField(required = False, widget=forms.TextInput(attrs={'style':'width:600px;'}), label='Page Url' )
    facebook_api_key = forms.CharField(required = False, widget=forms.TextInput(attrs={'style':'width:600px;'}), label='API Key' )
    facebook_secret_key = forms.CharField(required = False, widget=forms.TextInput(attrs={'style':'width:600px;'}), label='Secret Key' )
    twitter_api = forms.CharField(required = False, widget=forms.TextInput(attrs={'style':'width:600px;'}), label='Api Key' )
    twitter_auth_key = forms.CharField(required = False, widget=forms.TextInput(attrs={'style':'width:600px;'}), label='Auth Key' )
    twitter_auth_secret = forms.CharField(required = False, widget=forms.TextInput(attrs={'style':'width:600px;'}), label='Auth Secret' )
    twitter_consumer_key = forms.CharField(required = False, widget=forms.TextInput(attrs={'style':'width:600px;'}), label='Consumer Key' )
    twitter_consumer_secret = forms.CharField(required = False, widget=forms.TextInput(attrs={'style':'width:600px;'}), label='Consumer Secret' )
    flickr_api_key = forms.CharField( required = False,widget=forms.TextInput(attrs={'style':'width:600px;'}), label='Api Key' )
    flickr_api_secret = forms.CharField(required = False, widget=forms.TextInput(attrs={'style':'width:600px;'}), label='Api Secret' )
    smugmug_api_key = forms.CharField( widget=forms.TextInput(attrs={'style':'width:600px;'}), label='Api Key' )
    linkedin_api = forms.CharField(required = False, widget=forms.TextInput(attrs={'style':'width:600px;'}), label='Api Key' )
    linkedin_secret = forms.CharField(required = False, widget=forms.TextInput(attrs={'style':'width:600px;'}), label='Secret Key' )
    airport_name = forms.CharField(required = False, widget=forms.TextInput(attrs={'style':'width:600px;'}), label='Airport Name' )
    airport_code = forms.CharField(required = False, widget=forms.TextInput(attrs={'style':'width:200px;'}), label='Airport Code' )
    airport_address = forms.CharField(required = False, widget=forms.TextInput(attrs={'style':'width:600px;'}), label='Airport address' )
    flightstats_arrival_guid = forms.CharField(required = False, widget=forms.TextInput(attrs={'style':'width:600px;'}), label='Flight Arrival GUID' )
    flightstats_departure_guid = forms.CharField(required = False, widget=forms.TextInput(attrs={'style':'width:600px;'}), label='Flight Departure GUID' )
    weather_xml = forms.CharField(required = False, widget=forms.TextInput(attrs={'style':'width:600px;'}), label='Weather Xml path' )
    weather_unit = forms.TypedChoiceField(widget=forms.RadioSelect, choices=(('&deg;C','Celsius'),('F','Fahrenheit')))
    class Meta:
        model = CommonConfigure
class CommonConfigureAdmin(admin.ModelAdmin):
    fieldsets = [
        ('City', {'fields': ['city','native','display_city','country','domain','website_url','info_email','phone','company_name','company_address']}),
        ('Logo', {'fields': ['logo','signin_logo','staff_logo','bookmark_logo']}),
        ('Google', {'fields': ['google_map_key','google_map_lat','google_map_lon','google_map_zoom','google_analytics_script','google_meta'], 'classes': ['collapse']}),
        ('Payment', {'fields': ['currency','paypal_identity_token','paypal_receiver_email','paypal_test'], 'classes': ['collapse']}),
        ('FaceBook', {'fields': ['facebook_page_url','facebook_app_id','facebook_api_key','facebook_secret_key'], 'classes': ['collapse']}),
        ('Twitter - Buzz', {'fields': ['twitter_url','twitter_user','twitter_password','twitter_city_km','twitter_api','twitter_auth_key','twitter_auth_secret','twitter_consumer_key','twitter_consumer_secret'], 'classes': ['collapse']}),
        ('Flickr', {'fields': ['flickr_api_key','flickr_api_secret','flickr_email','flickr_password'], 'classes': ['collapse']}),
        ('SmugMug', {'fields': ['smugmug_url','smugmug_api_key','smugmug_username','smugmug_password','smugmug_default_category_id','smugmug_default_album_id'], 'classes': ['collapse']}),
        ('Linked in', {'fields': ['linkedin_api','linkedin_secret'], 'classes': ['collapse']}),
        ('Flight Stats', {'fields': ['airport_name','airport_code','airport_address','flightstats_arrival_guid','flightstats_departure_guid'], 'classes': ['collapse']}),
        ('Weather', {'fields': ['weather_xml','weather_unit'], 'classes': ['collapse']}),
        ('Others', {'fields': ['souvenir'], 'classes': ['collapse']}),
    ]
    form = CommonConfigureForm
admin.site.register(CommonConfigure, CommonConfigureAdmin)

class ModuleSettingForm( forms.ModelForm ):
    def __init__(self, *args, **kwargs):
        super(ModuleSettingForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f] = forms.TypedChoiceField()
            self.fields[f].widget = forms.RadioSelect()
            if f in ['article_comment','event_comment','business_review','classified_comment',
                     'movie_comment','theatre_comment','gallery_comment','video_comment',
                     'venue_comment','advice_comment']:
                self.fields[f].label = 'When %s is posted?'%f
                self.fields[f].choices = COMMENT_STATUS
            elif f == 'classified_active':
                self.fields[f].choices = M_CLASSIFIED_STATUS
            elif f == 'event_payment':
                self.fields[f].choices = PAYMENT_EVENT
            elif f == 'business_payment':
                self.fields[f].choices = PAYMENT_BUSINESS
            elif f == 'article_payment':
                self.fields[f].choices = PAYMENT_ARTICLE 
            elif f == 'classified_payment':
                self.fields[f].choices = PAYMENT_CLASSIFIED                       
            else:
                self.fields[f].choices = MODULE_STATUS
    class Meta:
        model = ModuleSetting
class ModuleSettingAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Article', {'fields': ['article_add', 'article_comment']}),
        ('Events', {'fields': ['event_add', 'event_comment', 'venue_comment']}),
        ('Business', {'fields': ['business_adding', 'business_review']}),
        ('Classified', {'fields': ['classified_active', 'classified_comment']}),
        ('Movies', {'fields': ['movie_comment', 'theatre_comment']}),
        ('Q and A', {'fields': ['advice_active', 'advice_comment']}),
        ('Photo Gallery', {'fields': ['gallery_photo_active', 'gallery_comment']}),
        ('Video Gallery', {'fields': ['video_active', 'video_comment']}),
        ('Forum', {'fields': ['topics_active']}),
        ('Payment', {'fields': ['event_payment','article_payment','business_payment','classified_payment']}),
        
    ]
    form = ModuleSettingForm

admin.site.register(ModuleSetting, ModuleSettingAdmin)
admin.site.register(ModuleNames)

