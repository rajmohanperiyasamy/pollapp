import mimetypes, urllib

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils.translation import ugettext as _
from django.conf import settings
from django.contrib.auth import get_user_model 
User = get_user_model()
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.forms import UserCreationForm
from common.getunique import getUniqueValue
from django.template.defaultfilters import slugify
from usermgmt.models import BmUser,Gender,ProfilePrivacy
from common.form_utils import HorizRadioRenderer
from django_countries.countries import COUNTRIES

GENDER_CHOICES = ( ('F', _('Female')), ('M', _('Male')),)

class RegistrationForm(forms.Form):
    display_name = forms.CharField(required=True,max_length=255, min_length = 3, label=_("Username"),error_messages={'required': u'Please enter the Username.'})
    password1 = forms.CharField(required=True,min_length=5, widget=forms.PasswordInput(render_value=False), label=_("Password"),error_messages={'required': u'Please enter the Password.'})
    useremail = forms.EmailField(required=True, label=_("E-mail address"),error_messages={'required': u'Please enter the Email.'})
    terms = forms.CharField(required=True, label=_("Terms"),error_messages={'required': u'Please check the Terms of Use.'})
    newsletter = forms.CharField(required=False, label=_("Newsletter"))
    
    def clean_username(self):
        """
        Verify that the username isn't already registered
        """
        username = self.cleaned_data.get("username")
        if not set(username).issubset("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"):
            raise forms.ValidationError(_("That username has invalid characters. The valid values are letters, numbers and underscore."))
        elif username in ['admin','webmaster','info']:
            raise forms.ValidationError(_("Please enter valid username"))
        elif User.objects.filter(username__iexact=username).count() == 0:
            return username
        else:
            raise forms.ValidationError(_("Sorry! Username is already registered."))

    def clean_useremail(self):
        """
        Verify that the email exists
        """
        email = self.cleaned_data.get("useremail").lower()
        if not email: return  email
        
        try:
            User.objects.get(email=email)
            raise forms.ValidationError(_("Sorry! E-mail is already used."))
        except User.DoesNotExist:
            return email


class SignUpForm(forms.ModelForm):
    """ Require email address when a user signs up """
  
    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
    }
    useremail = forms.EmailField(label='Email address', max_length=75)
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput, error_messages={'required': u'Please enter password'}
    )

    class Meta:
        model = BmUser
        fields = ('display_name', 'useremail',) 

    def clean_useremail(self):
        useremail = self.cleaned_data["useremail"].lower()
        try:
            user = User.objects.get(useremail=useremail)
            raise forms.ValidationError("This email address already exists.")
        except User.DoesNotExist:
            return useremail
    
    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        display_name = self.cleaned_data["display_name"]
        try:
            User.objects.get(display_name=display_name)
        except User.DoesNotExist:
            return display_name
        raise forms.ValidationError(self.error_messages['duplicate_username'])
    
    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.useremail = user.email = self.cleaned_data["useremail"].lower()
        user.profile_slug = getUniqueValue(User,slugify(user.useremail.split("@")[0]),field_name="profile_slug") 
        user.status = 'A' # change to false if using email activation
        if commit:
            user.save()
        
        return user        

        
class PasswordReset(forms.Form):
    oldpassword = forms.CharField(required=True,widget=forms.PasswordInput({'class':'iSp8'}),error_messages={'required': _('Please enter the current password')})
    password1 = forms.CharField(required=True,widget=forms.PasswordInput({'class':'iSp8'}),error_messages={'required': _('Please enter the new password ')})
    password2 = forms.CharField(required=True,widget=forms.PasswordInput({'class':'iSp8'}),error_messages={'required': _('Please re-enter the new password')})

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(PasswordReset, self).__init__(*args, **kwargs)

    def clean_oldpassword(self):
        if self.cleaned_data.get('oldpassword') and not self.user.check_password(self.cleaned_data['oldpassword']):
            raise forms.ValidationError(_("Your current password is wrong"))
        else:
            return self.cleaned_data['oldpassword']
    def clean_password1(self):
        if len(self.cleaned_data['password1']) < 6:
            raise forms.ValidationError(_("Your password has to be at least 6 characters long"))
        elif self.cleaned_data.get('oldpassword'):
            if self.cleaned_data['password1'] == self.cleaned_data['oldpassword']:
                raise forms.ValidationError(_("The password entered already exists."))
        return self.cleaned_data['password1']
    def clean_password2(self):
        if self.cleaned_data.get('password1') and self.cleaned_data.get('password2') and self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise forms.ValidationError(_("The new passwords are not the same"))
        return self.cleaned_data['password2']
    
class RetrivePassword(forms.Form):
    password1 = forms.CharField(required=True,widget=forms.PasswordInput({'style':'width: 80%;','placeholder':_('Type your new password')}),error_messages={'required': _('Please enter the new password ')})
    password2 = forms.CharField(required=True,widget=forms.PasswordInput({'style':'width: 80%;','placeholder':_('Re-type your new password')}),error_messages={'required': _('Please re-enter the new password')})
    #captcha = ReCaptchaField(attrs={'theme' : 'clean'},use_ssl=False, error_messages={'required': u'Please enter the text given in image','captcha_invalid': u'Please enter the text exactly as given in image'})
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(RetrivePassword, self).__init__(*args, **kwargs)

    def clean_password1(self):
        if len(self.cleaned_data['password1']) < 6:
            raise forms.ValidationError(_("Your password has to be at least 6 characters long"))
        return self.cleaned_data['password1']
    def clean_password2(self):
        if self.cleaned_data.get('password1') and self.cleaned_data.get('password2') and self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise forms.ValidationError(_("The new passwords are not the same"))
        return self.cleaned_data['password2']
    

class ProfileEditForm(forms.ModelForm):
    """
    Profile Form. 
    """
    
    display_name=forms.CharField(required=True, error_messages={'required': u'Please enter your diplay name'})
    gender = forms.TypedChoiceField(required=False,widget=forms.RadioSelect(renderer=HorizRadioRenderer,),choices = Gender)
    about=forms.CharField(widget=forms.Textarea(attrs={'class':'iSp10','rows':'5'}),required=False)
    location=forms.CharField(required=False,max_length=150,widget=forms.TextInput(attrs={'maxlength':'150','class':'iSp8','placeholder':'e.g. New York, NY'}))
    twitter_url=forms.URLField(max_length=150,widget=forms.TextInput(),required=False, label=_("Twitter profile"),error_messages={'invalid': u'Please enter a valid twitter URL'})
    fb_url=forms.URLField(max_length=150,widget=forms.TextInput(attrs={'maxlength':'150'}),required=False, label=_("Facebook profile"),error_messages={'invalid': u'Please enter a valid facebook URL'})
    gooleplus_url=forms.URLField(max_length=150,widget=forms.TextInput(attrs={'maxlength':'150'}),required=False, label=_("Google profile"),error_messages={'invalid': u'Please enter a valid google URL'})
    website=forms.URLField(widget=forms.TextInput(),required=False, label=_("Website"),error_messages={'invalid': u'Please enter a valid URL'})
    useremail = forms.EmailField(required=False,max_length=75,widget=forms.TextInput(attrs={ 'class': 'iSp8 fl','title':_('Enter email address. e.g., myname@example.com'),'placeholder':_('Example: myname@example.com') }),error_messages={'required': 'Please enter the valid email address'})
    
    def clean_useremail(self):
        useremail = self.cleaned_data.get("useremail").strip().lower()
        if len(useremail) > 75:
            raise forms.ValidationError(_("Maximum length of Email field is 75 characters."))
        try:
            user = User.objects.filter(useremail=useremail).exclude(useremail=self.instance.useremail)
            print len(user)
            if len(user)>0:
                raise forms.ValidationError("This email address already exists.")
            else:
                return useremail
        except User.DoesNotExist:
            return useremail
        
    def clean_location(self):
        location = self.cleaned_data.get("location").strip()
        if len(location) > 150:
            raise forms.ValidationError(_("Maximum length of location field is 150 characters."))
        else:
            return location
    
    class Meta:
        model = BmUser
        fields = ['display_name','location','gender','about','useremail','fb_url','twitter_url','gooleplus_url','website']
        


class ContactEditForm(forms.ModelForm):
    """
    Contact Form. 
    """
    address1=forms.CharField(widget=forms.TextInput(attrs={'maxlength':'255','class':'iSp8','placeholder':'Address Line 1'}),required=False)
    address2=forms.CharField(required=False,widget=forms.TextInput(attrs={'maxlength':'255','class':'iSp8','placeholder':'Address Line 2'}))
    country = forms.CharField(required=False, widget=forms.Select(attrs={'class':'iSp8 bM-sLt','data-size':'5',},choices=COUNTRIES),error_messages={'required': _('Please select the default country')})
    state=forms.CharField(widget=forms.TextInput(attrs={'maxlength':'100','class':'iSp8'}),required=False)
    city=forms.CharField(widget=forms.TextInput(attrs={'maxlength':'100'}),required=False)
    phone=forms.CharField(widget=forms.TextInput(attrs={'maxlength':'25','class':'iSp8'}),required=False)
    pin=forms.CharField(widget=forms.TextInput(attrs={'maxlength':'20'}),required=False)
    company=forms.CharField(widget=forms.TextInput(attrs={'maxlength':'150','class':'iSp8'}),required=False)
    
    class Meta:
        model = BmUser
        fields = ['address1','address2','country','state','city','pin','phone','company']
        
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            try:
                ph = int(phone)
            except:
                raise forms.ValidationError("Invalid phone number")
        return phone
    
    def clean_pin(self):
        pin = self.cleaned_data.get('pin')
        if pin:
            try:
                pin_no = int(pin)
            except:
                raise forms.ValidationError("Invalid pin number")
        return pin
        

class ProfilePrivacyForm(forms.ModelForm):
    """
    Profile Privacy Form. 
    """
    is_public = forms.TypedChoiceField(choices=((True, 'Everyone'), (False, 'Only you')),widget=forms.RadioSelect)
    
    class Meta:
        model = ProfilePrivacy
        fields = ['show_contact','show_community_post','show_reviews','show_articles','show_events',
                  'show_photos','show_videos','show_business','show_classifieds','show_bookmarks','is_public','show_email_form']
        
    