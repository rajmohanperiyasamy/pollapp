from django import forms
from django.conf import settings 
from django.utils.translation import ugettext as _

from common.models import CommonConfigure,PaymentConfigure,ApprovalSettings,SocialSettings,SignupSettings
from common.models import GallerySettings,BannerAdds,Contacts,MiscAttribute, SmtpConfigurations, SMTP_AUTH_TYPES
from common.form_utils import HorizRadioRenderer
from videos.utils import validate_vimeo
from common.flickr.flickr import validate_flickr

class UploadImageForm(forms.Form):
    photo = forms.ImageField(required=False)
    
    def clean(self):
        print self.data
        if not self.cleaned_data.get('photo'):
            raise forms.ValidationError(_('Please choose image'))
        else:
            file=self.cleaned_data.get('photo')
            file_type = file.content_type
            if file_type not in settings.IMG_UPLOAD_FILE_TYPES:
                raise forms.ValidationError(_('File type not supported'))
            elif file.size > settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError("File shouldn't exceed 5MB")
            else:
                return self.cleaned_data 
            
class UploadFileForm(forms.Form):
    file = forms.FileField(required=False)
    
    def clean(self):
        if not self.cleaned_data.get('file'):
            raise forms.ValidationError('Please choose file')
        else:
            file=self.cleaned_data.get('file')
            file_type = file.content_type
            if file_type not in settings.UPLOAD_FILE_TYPES:
                raise forms.ValidationError(_('File type not supported for the file %s')%(file.name))
            elif file.size > settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError(_("File shouldn't exceed 5MB"))
            else:
                return self.cleaned_data 
             
class UploadEditorImageForm(forms.Form):
    upload = forms.ImageField(required=False)
    
    def clean(self):
        if not self.cleaned_data.get('upload'):
            raise forms.ValidationError('Please choose image')
        else:
            file=self.cleaned_data.get('upload')
            file_type = file.content_type
            if file_type not in settings.IMG_UPLOAD_FILE_TYPES:
                raise forms.ValidationError('File type not supported')
            elif file.size > settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError("File shouldn't exceed 5MB")
            else:
                return self.cleaned_data

class GeneralSettings(forms.ModelForm):
    site_title = forms.CharField(required=True,max_length="100",widget=forms.TextInput(attrs={'class':'fl','placeholder':_('Site Name')}),error_messages={'required': _('Please enter website title')})
    google_map_key = forms.CharField(required=False,max_length="150",widget=forms.TextInput(attrs={'maxlength':'150','placeholder':'XXXXXXXXXXXXXXXXXXXXXXXXXXXX','class':'fl'}),error_messages={'required':_('Please enter google map key')})
    google_analytics_script = forms.CharField(required=False,max_length="600",widget=forms.TextInput(attrs={'maxlength':'600','placeholder':'UA-XXXXX-YY','class':'fl'}),error_messages={'required':_('Please enter google analytics tracking Id')})
    info_email = forms.EmailField(required=True,widget=forms.TextInput(attrs={'maxlength':'60','class':'fl'}),error_messages={'required':_('Please enter the emailid')})
    facebook_page_url = forms.CharField(required=False,max_length=150, error_messages={'required':_('Please enter the Facebook URL')},widget=forms.TextInput(attrs={'class':'fm social_ad_fld','title':'Facebook URL','placeholder':_('Example: https://www.facebook.com/page'),'autocomplete':'off'}))
    twitter_url = forms.CharField(required=False,max_length=150, error_messages={'required':_('Please enter the Twitter URL')},widget=forms.TextInput(attrs={'class':'fm social_ad_fld','title':'Twitter URL','placeholder':_('Example: https://www.twitter.com/page'),'autocomplete':'off'}))
    googleplus_url = forms.CharField(required=False,max_length=150, error_messages={'required': _('Please enter the Google+ URL')},widget=forms.TextInput(attrs={'class':'fm social_ad_fld','title':'Google Plus URL','placeholder':_('Example: https://plus.google.com/page'),'autocomplete':'off'}))
    pinterest = forms.CharField(required=False,max_length=150, error_messages={'required': _('Please enter the Google+ URL')},widget=forms.TextInput(attrs={'class':'fm social_ad_fld','title':'Pinterest URL','placeholder':_('Example: http://pinterest.com/page'),'autocomplete':'off'}))
    site_dateformat = forms.CharField(required=True,max_length="20",widget=forms.TextInput())
    site_timeformat = forms.CharField(required=True,max_length="20",widget=forms.TextInput()) 
    twitter_widget_id = forms.CharField(required=False,max_length=150, error_messages={'required':_('Please enter the Twitter Widget id')},widget=forms.TextInput(attrs={'class':'fl','title':'Twitter Widget-id','autocomplete':'off'}))
    
    class Meta:
        model=CommonConfigure
        fields=('site_title','site_dateformat','site_timeformat','google_map_key','google_analytics_script','info_email','facebook_page_url','twitter_url','googleplus_url','pinterest','twitter_widget_id')  
        
class GeneralMapMarker(forms.ModelForm):
    google_map_lat = forms.FloatField(required=True,widget=forms.TextInput(),error_messages={'required':_('Please enter map latitude')})
    google_map_lon = forms.FloatField(required=True,widget=forms.TextInput(),error_messages={'required':_('Please enter map longitude')})
    google_map_zoom = forms.IntegerField(required=True,widget=forms.TextInput(),error_messages={'required':_('Please enter map zoom')})
    
    class Meta:
        model=CommonConfigure
        fields=('google_map_lat','google_map_lon','google_map_zoom')   

   
class GeneralPayment(forms.ModelForm):
    currency_symbol = forms.CharField(required=True,max_length="4",widget=forms.TextInput(attrs={'maxlength':'4','class':'fm tttxt-fw-focus','placeholder':_('Enter currency symbol'),'title':_('Currency symbol Example:$')}),error_messages={'required':_('Please enter currency symbol')})
    currency_code = forms.CharField(required=True,max_length="3",widget=forms.TextInput(attrs={'maxlength':'3','class':'fm tttxt-fw-focus','placeholder':_('Enter currency code'),'title':_('Currency Code Example:USD')}),error_messages={'required':_('Please enter currency code')})
    paypal_receiver_email = forms.EmailField(required=False,widget=forms.TextInput(attrs={'class':'fl tttxt-fw-focus','placeholder':'Enter paypal receiver email','title':_('Paypal Receiver Email')}),error_messages={'required':_('Please enter the Paypal Receiver Email ID')})
    invoice_payment = forms.BooleanField(required=False,widget=forms.CheckboxInput())
    paypal_payment = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'onclick':'fun_fb_disable()'}))
    google_checkout  = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'onclick':'fun_tw_disable()'}))
    merchant_id = forms.CharField(required=False,max_length="150",widget=forms.TextInput(attrs={'maxlength':'150','class':'fl tttxt-fw-focus','placeholder':'xxxxxxxxxxxxx','title':_('Google Checkout Merchant ID')}),error_messages={'required':_('Please enter merchant Id')})
    merchant_key  = forms.CharField(required=False,max_length="150",widget=forms.TextInput(attrs={'maxlength':'150','placeholder':'xxxxxxxxxxxxxxxxxxxxxxxxxxxxx','class':'fl tttxt-fw-focus','title':_('Google Checkout Merchant Key')}),error_messages={'required':_('Please enter merchant key')})
    authorize  = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'onclick':'fun_au_disable()'}))
    login_id = forms.CharField(required=False,max_length="150",widget=forms.TextInput(attrs={'maxlength':'150','class':'fl tttxt-fw-focus','placeholder':'xxxxxxxxxxxxx','title':_('Authorize login ID')}),error_messages={'required':_('Please enter authorize login ID')})
    transaction_key  = forms.CharField(required=False,max_length="150",widget=forms.TextInput(attrs={'maxlength':'150','placeholder':'xxxxxxxxxxxxxxxxxxxxxxxxxxxxx','class':'fl tttxt-fw-focus','title':_('Authorize transaction Key')}),error_messages={'required':_('Please enter authorize transaction Key')})
    online_payment = forms.BooleanField(required=False,widget=forms.CheckboxInput())
    stripe  = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'onclick':'fun_sp_disable()'}))
    stripe_public_key = forms.CharField(required=False,max_length="150",widget=forms.TextInput(attrs={'maxlength':'150','class':'fl tttxt-fw-focus','placeholder':'xxxxxxxxxxxxx','title':_('Stripe Public Key')}),error_messages={'required':_('Please enter Stripe Public Key')})
    stripe_private_key  = forms.CharField(required=False,max_length="150",widget=forms.TextInput(attrs={'maxlength':'150','placeholder':'xxxxxxxxxxxxxxxxxxxxxxxxxxxxx','class':'fl tttxt-fw-focus','title':_('Stripe Private Key')}),error_messages={'required':_('Please enter Stripe Private Key')})
    allow_subscription = forms.BooleanField(required=False,widget=forms.CheckboxInput())

    class Meta: 
        model=PaymentConfigure
        
    def clean(self):
        if self.cleaned_data.get("paypal_payment") or self.cleaned_data.get("google_checkout") or self.cleaned_data.get("authorize") or self.cleaned_data.get("stripe"):
            self.cleaned_data['online_payment']= True
            return self.cleaned_data
        else:
            self.cleaned_data['online_payment']= False
            self.cleaned_data['invoice_payment']= True
            return self.cleaned_data
            
class ApprovalSettingForm(forms.ModelForm):
    free=forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'class':'cform-checkbox'}))
    paid=forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'class':'cform-checkbox'}))
    free_update=forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'class':'cform-checkbox'}))
    paid_update=forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'class':'cform-checkbox'}))
    
    class Meta:
        model=ApprovalSettings    
        fields=('free','paid','free_update','paid_update')
      
class GallerySettingsForm(forms.ModelForm):
    flickr_api_key = forms.CharField(required=False,max_length=150,widget=forms.TextInput(attrs={'maxlength':'100','class':'fm'}),error_messages={'required': _('Please enter the Flicker API Key')})
    flickr_api_secret = forms.CharField(required=False,max_length=150,widget=forms.TextInput(attrs={'maxlength':'100','class':'fm'}),error_messages={'required': _('Please enter the Flicker API Secret')})
    #flickr_email = forms.CharField(required=False,max_length=150,widget=forms.TextInput(attrs={'maxlength':'100','class':'fm'}),error_messages={'required': _('Please enter the Flicker Email')})
    #flickr_password = forms.CharField(required=False,max_length=64,widget=forms.TextInput(attrs={'maxlength':'100','class':'fm'}),error_messages={'required': _('Please enter the Flicker Password')})
    
    def clean_flickr_api_secret(self):
        flickr_api_key = self.cleaned_data.get("flickr_api_key")
        flickr_api_secret = self.cleaned_data.get("flickr_api_secret")
        if flickr_api_key.strip() == '' and flickr_api_secret.strip() == '':return flickr_api_secret
        else:
            try:
                flag=validate_flickr(flickr_api_key,flickr_api_secret)
                return flickr_api_secret
            except:
                raise forms.ValidationError(_("Please enter the Valid API key/Secret"))
    
    class Meta: 
        model=GallerySettings
        fields=('flickr_api_key','flickr_api_secret')    

class VideoSettingsForm(forms.ModelForm):
    vimeo_api_key = forms.CharField(required=False,max_length=150,widget=forms.TextInput(attrs={'maxlength':'100','class':'fm'}),error_messages={'required': _('Please enter the Flicker API Key')})
    vimeo_api_secret = forms.CharField(required=False,max_length=150,widget=forms.TextInput(attrs={'maxlength':'100','class':'fm'}),error_messages={'required': _('Please enter the Flicker API Secret')})
    
    def clean_vimeo_api_secret(self):
        vimeo_api_key = self.cleaned_data.get("vimeo_api_key")
        vimeo_api_secret = self.cleaned_data.get("vimeo_api_secret")
        if vimeo_api_key.strip() == '' and vimeo_api_secret.strip() == '':return vimeo_api_secret
        else:
            flag=validate_vimeo(vimeo_api_key,vimeo_api_secret)
            if flag:return vimeo_api_secret
            else:raise forms.ValidationError(_("Please enter the Valid API key/Secret"))
        
        
    class Meta: 
        model=GallerySettings
        fields=('vimeo_api_key','vimeo_api_secret')    
                
class SignupSettingsForm(forms.ModelForm):
    openid=forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={}))
    facebook=forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'onclick':'fun_fb_disable()'}))
    twitter=forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'onclick':'fun_tw_disable()'}))
    linkedin=forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'onclick':'fun_ln_disable()'}))
    facebook_app_id = forms.CharField(required=False,max_length=100,widget=forms.TextInput(attrs={'class':'fl','placeholder':'XXXXXXXXXXXXXXX'}),error_messages={'required': _('Please enter the Facebook App ID')})
    facebook_secret_key = forms.CharField(required=False,max_length=150,widget=forms.TextInput(attrs={'class':'fl','placeholder':'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'}),error_messages={'required': _('Please enter the Facebook Secret Key')})
    twitter_consumer_key = forms.CharField(required=False,max_length=150,widget=forms.TextInput(attrs={'class':'fl','placeholder':'XXXXXXXXXXXXXXX'}),error_messages={'required': _('Please enter the Twitter Consumer Key')})
    twitter_consumer_secret = forms.CharField(required=False,max_length=150,widget=forms.TextInput(attrs={'class':'fl','placeholder':'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'}),error_messages={'required': _('Please enter the Twitter Consumer Secret Key')})
    linkedin_app_id = forms.CharField(required=False,max_length=150,widget=forms.TextInput(attrs={'class':'fl','placeholder':'XXXXXXXXXXXXXXX'}),error_messages={'required': _('Please enter the LinkedIn API Key')})
    linkedin_secret_key = forms.CharField(required=False,max_length=150,widget=forms.TextInput(attrs={'class':'fl','placeholder':'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'}),error_messages={'required': _('Please enter the LinkedIn Secret Key')})
    
    class Meta:
        model=SignupSettings    
        
class UpdateBannerContents(forms.ModelForm):
    top = forms.CharField(required=False,widget=forms.Textarea(attrs={'style':'width:300px', 'rows':'8'}),error_messages={'required':  _('Please enter the meta description')})
    right = forms.CharField(required=False,widget=forms.Textarea(attrs={'style':'width:300px', 'rows':'8'}),error_messages={'required':  _('Please enter the meta description')})
    
    class Meta:
        model=BannerAdds  
        exclude=('name','bottom')
       
#SEO Category
class SEOForm(forms.Form):
    slug = forms.CharField(required=False,max_length=200,error_messages={'required': _('Please enter the slug')})
    meta_title = forms.CharField(required=False,error_messages={'required':  _('Please enter the meta title')})
    meta_description = forms.CharField(required=False,widget=forms.Textarea(),error_messages={'required':  _('Please enter the meta description')})
    meta_keywords = forms.CharField(required=False,widget=forms.Textarea(),error_messages={'required':  _('Please enter the meta keywords')})
    
    def clean_meta_title(self):
        meta_title = self.cleaned_data.get("meta_title")
        if len(meta_title)>200:
            raise forms.ValidationError(_("Maximum length of Page Tile(SEO) field is 200 characters."))
        elif meta_title.strip() == '':
            raise forms.ValidationError(_("Please enter the meta title"))
        else:
            return meta_title
    def clean_meta_description(self):
        meta_description = self.cleaned_data.get("meta_description")
        if len(meta_description)>400:
            raise forms.ValidationError(_("Maximum length of Page Description(SEO) field is 400 characters."))
        elif meta_description.strip() == '':
            raise forms.ValidationError(_("Please enter the meta description"))
        else:
            return meta_description
   

class AdvertiseForm(forms.ModelForm):
    name = forms.CharField(required=True,max_length=300,widget=forms.TextInput(attrs={'class':'iSp8'}),error_messages={'required': _('Please enter the name')})
    company = forms.CharField(required=True,max_length=600,widget=forms.TextInput(attrs={'class':'iSp8'}),error_messages={'required': _('Please enter the company')})
    website = forms.CharField(required=False,max_length=800,widget=forms.TextInput(attrs={'class':'iSp8'}),error_messages={'required': _('Please enter the website')})
    phone = forms.CharField(required=True,max_length=30,widget=forms.TextInput(attrs={'class':'iSp8'}),error_messages={'required': _('Please enter the phone')})
    email = forms.EmailField(required=True,max_length=200,widget=forms.TextInput(attrs={'class':'iSp8','maxlength':'200'}),error_messages={'required': _('Please enter the email')})
    notes = forms.CharField(required=False,max_length=2500,widget=forms.Textarea(attrs={'class':'iSp8','rows':'3','maxlength':'2500'}),error_messages={'required': _('Please enter the notes')})
    
    class Meta:
        model=Contacts  
        exclude=('type','website','subject')
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if len(email)>200:
            raise forms.ValidationError(_("Maximum length of Email field is 200 characters."))
        elif email.strip() == '':
            raise forms.ValidationError(_("Please enter your Email"))
        else:
            return email
        
    def clean_notes(self):
        notes = self.cleaned_data.get("notes")
        if len(notes)>2500:
            raise forms.ValidationError(_("Maximum length of Notes field is 2500 characters."))
        else:
            return notes
    
class ContactForm(forms.ModelForm):
    name = forms.CharField(required=True,max_length=300,widget=forms.TextInput(attrs={'class':'textField', 'style':'padding: 3px; width: 250px;'}),error_messages={'required': _('Please enter the name')})
    company = forms.CharField(required=False,max_length=600,widget=forms.TextInput(attrs={'class':'textField', 'style':'padding: 3px; width: 250px;'}),error_messages={'required': _('Please enter the company')})
    website = forms.CharField(required=False,max_length=800,widget=forms.TextInput(attrs={'class':'textField', 'style':'padding: 3px; width: 250px;'}),error_messages={'required': _('Please enter the website')})
    phone = forms.CharField(required=False,max_length=30,widget=forms.TextInput(attrs={'class':'textField', 'style':'padding: 3px; width: 250px;'}),error_messages={'required': _('Please enter the phone')})
    email = forms.EmailField(required=True,max_length=200,widget=forms.TextInput(attrs={'class':'textField','maxlength':'200', 'style':'padding: 3px; width: 250px;'}),error_messages={'required': _('Please enter the email')})
    subject = forms.CharField(required=True,max_length=30,widget=forms.TextInput(attrs={'class':'textField', 'style':'padding: 3px; width: 250px;'}),error_messages={'required': _('Please enter the subject')})
    notes = forms.CharField(required=False,max_length=2500,widget=forms.Textarea(attrs={'class':'textField','maxlength':'2500', 'style':'width: 510px; height: 150px;','rows':'3'}),error_messages={'required': _('Please enter the notes')})
    
    class Meta:
        model=Contacts  
        exclude=('type','company','website')   
        
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if len(email)>200:
            raise forms.ValidationError(_("Maximum length of Email field is 200 characters."))
        elif email.strip() == '':
            raise forms.ValidationError(_("Please enter your Email"))
        else:
            return email
        
    def clean_notes(self):
        notes = self.cleaned_data.get("notes")
        if len(notes)>2500:
            raise forms.ValidationError(_("Maximum length of Notes field is 2500 characters."))
        else:
            return notes
        
arr_keys = (
              ('', '-- Select key --'),
              ('VIATOR_URL', 'VIATOR_URL'),
              ('GOOGLE_VERIFICATION_CODE', 'GOOGLE_VERIFICATION_CODE'),
              ('MEETUP_API','MEETUP_API'),
              ('GOLF_LINK','GOLF_LINK'),
              )        
         
    
class MiscAttributeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        try:self.attr_key = kwargs['instance'].attr_key
        except:self.attr_key= False
        super(MiscAttributeForm, self).__init__(*args, **kwargs)
    
    attr_name = forms.CharField(required=True,max_length=100, error_messages={'required': _('Please enter the attribute name')},widget=forms.TextInput(attrs={'class':'tttxt-w','maxlength':'40','title':_('Attribute Name'),'style':'width:90%;','placeholder':_('Attribute Name'),'autocomplete':'off'}))   
    attr_key = forms.ChoiceField(required=True,choices=arr_keys,widget=forms.Select(attrs={'class':'select-menu fm','style':'width:92%;','title':'Attribute Key)'}),error_messages={'required':_('Please select the attribute key')})
    attr_value = forms.CharField(required=True,max_length=300, error_messages={'required':_('Please enter the value')},widget=forms.Textarea(attrs={'class':'fm', 'rows':'2'}))
    
    def clean_attr_key(self):
        key = self.cleaned_data.get('attr_key','').strip()
        flag=MiscAttribute.objects.filter(attr_key__iexact=key).exclude(id=self.instance.id)
        if flag:raise forms.ValidationError(_("This key name is already selected"))
        return key
    
    class Meta:
        model=MiscAttribute
        fields=('attr_name','attr_key','attr_value')  
    
class GeneralReport(forms.ModelForm):
    google_analytics_script = forms.CharField(required=True,max_length="600",widget=forms.TextInput(attrs={'maxlength':'600','style':'width:350px;'}),error_messages={'required':_('Please enter google analytics script')})
 
    class Meta:
        model=CommonConfigure
        fields=('google_analytics_script',)        
        
class SmtpConfigForm(forms.ModelForm):
    email_host = forms.CharField(required=True, max_length=100, error_messages={'required': _('Please enter the smtp server')},widget=forms.TextInput(attrs={'class':'tttxt-w','maxlength':'100','title':_('Server Name'),'style':'width:90%;','placeholder':_('smtp.gmail.com'),'autocomplete':'off'}))
    email_port = forms.CharField(required=True, max_length=100, error_messages={'required': _('Please enter the port number')},widget=forms.TextInput(attrs={'class':'tttxt-w','maxlength':'100','title':_('Port Number'),'style':'width:90%;','placeholder':_('587'),'autocomplete':'off'}))
    secure_type = forms.TypedChoiceField(required=True, widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices = SMTP_AUTH_TYPES, initial='TLS', error_messages = {'required':'Please Select smtp authentication types.'})
    email_host_user = forms.CharField(required=True,max_length=100, error_messages={'required': _('Please enter username')},widget=forms.TextInput(attrs={'class':'tttxt-w','maxlength':'100','title':_('Username'),'style':'width:90%;','placeholder':_('testuser@gmail.com'),'autocomplete':'off'}))
    email_host_password = forms.CharField(required=True,max_length=120, error_messages={'required': _('Please enter password')},widget=forms.PasswordInput(render_value=True, attrs={'class':'tttxt-w','maxlength':'100','title':_('Password'),'style':'width:90%;','autocomplete':'off'}))
    
    class Meta:
        model = SmtpConfigurations
        fields=('email_host', 'email_port', 'secure_type', 'email_host_user', 'email_host_password')  
            
