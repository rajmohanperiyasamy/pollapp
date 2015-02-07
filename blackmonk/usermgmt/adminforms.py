import mimetypes, urllib

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils.translation import ugettext as _
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
User = get_user_model()
from django.forms import ModelForm

from common.admin_utils import get_unique_username
from common.models import ModuleNames

class CreateUserForm(ModelForm):
    display_name = forms.CharField(required=False, max_length=255, widget=forms.TextInput({'class':'tttxt', 'title':_('First Name'),  'maxlength':'255', 'autocomplete':'off'}), error_messages={'required': _('Please enter the first name')})
    useremail = forms.EmailField(required=True, widget=forms.TextInput({'class':'tttxt', 'title':_('Email'),  'maxlength':'255', 'autocomplete':'off'}), error_messages={'required': _('Please enter the email')})
    password = forms.CharField(required=True, max_length=255, widget=forms.PasswordInput({'class':'tttxt', 'title':_('Password'),  'maxlength':'255', 'autocomplete':'off'}), error_messages={'required': _('Please enter the password')})
    
    class Meta:
        model = User
        fields=('display_name','useremail','password')
  
    def clean(self):
        cleaned_data = super(CreateUserForm, self).clean()
        display_name = cleaned_data.get("display_name")
        useremail = cleaned_data.get("useremail").lower()
        cleaned_data["useremail"] = useremail
        password = cleaned_data.get("password")
        
        try:
            User.objects.get(useremail=useremail)
            self._errors["useremail"] = self.error_class(['That e-mail is already used.'])
        except User.DoesNotExist:
            useremail = useremail
            
        if len(password)<5:
            self._errors["password"] = self.error_class(['Password field should contain atleast 5 characters'])
        else:
            password = password
        return cleaned_data 
        
class EditUserForm(ModelForm):
    display_name = forms.CharField(required=False, max_length=255, widget=forms.TextInput({'class':'tttxt', 'title':_('First Name'),  'maxlength':'255', 'autocomplete':'off'}), error_messages={'required': _('Please enter the first name')})
    useremail = forms.EmailField(required=True, widget=forms.TextInput({'class':'tttxt', 'title':_('Email'),  'maxlength':'255', 'autocomplete':'off'}), error_messages={'required': _('Please enter the email')})
    class Meta:
        model = User
        fields=('display_name','useremail')   
    
    def clean_useremail(self):
        """
        Verify that the email exists
        """
        userobj = User.objects.get(id=self.instance.id)
        useremail = self.cleaned_data.get("useremail").lower()
        
        if User.objects.filter(useremail=useremail).exclude(id=userobj.id).count() != 0:
            raise forms.ValidationError(_("That e-mail is already used."))
        else:
            return useremail

class PromoteUserForm(ModelForm):
    display_name = forms.CharField(required=False, max_length=255, widget=forms.TextInput({'class':'tttxt','readonly':'readonly', 'title':_('First Name'),  'maxlength':'255', 'autocomplete':'off'}))
    useremail = forms.EmailField(required=False, widget=forms.TextInput({'class':'tttxt','readonly':'readonly', 'title':_('Email'),  'maxlength':'255', 'autocomplete':'off'}))
    groups = forms.ModelChoiceField(required=False, queryset= Group.objects.all().order_by('name'), widget=forms.Select(attrs={'class':'lb_select-menu', 'style':'width:116px', 'title':_('Role'), 'data-placeholder':_('Select a role'), 'autocomplete':'off'}),empty_label="Select a role" )
    
    
    class Meta:
        model = User
        fields=('display_name','profile_slug','useremail','groups')
  
    def clean(self):
        cleaned_data = super(CreateStaffForm, self).clean()
        displayname = cleaned_data.get("display_name")
        useremail = cleaned_data.get("useremail").lower()
                
        profile_slug = useremail.split('@')[0]
        try:profile_slug = profile_slug.replace('.','')
        except:profile_slug = profile_slug 
        profile_slug = get_unique_username(profile_slug)  
        cleaned_data['profile_slug']=profile_slug
        try:
            User.objects.get(useremail=useremail)
            self._errors["useremail"] = self.error_class(['That e-mail is already used.'])
        except User.DoesNotExist:
            useremail = useremail
        
        return cleaned_data 

class CreateStaffForm(ModelForm):
    display_name = forms.CharField(required=False, max_length=255, widget=forms.TextInput({'class':'tttxt', 'title':_('First Name'),  'maxlength':'255', 'autocomplete':'off'}), error_messages={'required': _('Please enter the first name')})
    useremail = forms.EmailField(required=True, widget=forms.TextInput({'class':'tttxt', 'title':_('Email'),  'maxlength':'255', 'autocomplete':'off'}), error_messages={'required': _('Please enter the email')})
    password = forms.CharField(required=True, max_length=255, widget=forms.PasswordInput({'class':'tttxt', 'title':_('Password'),  'maxlength':'255', 'autocomplete':'off'}), error_messages={'required': _('Please enter the password')})
    groups = forms.ModelChoiceField(required=False, queryset= Group.objects.all().order_by('name'), widget=forms.Select(attrs={'class':'lb_select-menu', 'style':'width:116px', 'title':_('Role'), 'data-placeholder':_('Select a role'), 'autocomplete':'off'}),empty_label="Select a role" ,error_messages={'required': _('Please select a role')})
    
    
    class Meta:
        model = User
        fields=('display_name','useremail','password','groups')
  
    def clean(self):
        cleaned_data = super(CreateStaffForm, self).clean()
        displayname = cleaned_data.get("display_name")
        useremail = cleaned_data.get("useremail").lower()
        cleaned_data['useremail'] = useremail
        password = cleaned_data.get("password")
        
        try:
            User.objects.get(useremail=useremail)
            self._errors["useremail"] = self.error_class(['That e-mail is already used.'])
        except User.DoesNotExist:
            useremail = useremail
            
        if len(password)<5:
            self._errors["password"] = self.error_class(['Password field should contain atleast 5 characters'])
        else:
            password = password
        return cleaned_data 

class UpdateStaffForm(ModelForm):
    display_name = forms.CharField(required=False, max_length=255, widget=forms.TextInput({'class':'tttxt', 'title':_('First Name'),  'maxlength':'255', 'autocomplete':'off'}), error_messages={'required': _('Please enter the first name')})
    useremail = forms.EmailField(required=True, widget=forms.TextInput({'class':'tttxt', 'title':_('Email'),  'maxlength':'255', 'autocomplete':'off'}), error_messages={'required': _('Please enter the email')})
    groups = forms.ModelChoiceField(required=False, queryset= Group.objects.all().order_by('name'), widget=forms.Select(attrs={'class':'lb_select-menu', 'style':'width:116px', 'title':_('Role'), 'data-placeholder':_('Select a role'), 'autocomplete':'off'}),empty_label="Select a role" ,error_messages={'required': _('Please select a role')})
    
    class Meta:
        model = User
        fields=('display_name','useremail','groups')
    
    def clean_useremail(self):
        """
        Verify that the email exists
        """
        userobj = User.objects.get(id=self.instance.id)
        useremail = self.cleaned_data.get("useremail").lower()
        
        if User.objects.filter(useremail=useremail).exclude(id=userobj.id).count() != 0:
            raise forms.ValidationError(_("That e-mail is already used."))
        else:
            return useremail    

class AddRoleForm(ModelForm):
    name = forms.CharField(required=True, max_length=255, widget=forms.TextInput({'title':_('Name'),  'maxlength':'255', 'style':'width:300px;', 'autocomplete':'off'}), error_messages={'required': _('Please enter the role name')})
    
    class Meta:
        model = Group
        fields=('name',)
   
    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name.strip()=='':raise forms.ValidationError(_("Please enter the role name"))
        else:return name         
        try:
            Group.objects.get(name=name)
            raise forms.ValidationError(_("Group with this Name already exists."))
        except:return name
           
class addSEOForm(ModelForm):
    seo_title = forms.CharField(required=True,max_length=200,widget=forms.TextInput(attrs={'class':'textField long'}),error_messages={'required': 'Please enter the Title'})
    seo_description = forms.CharField(required=True,max_length=400,widget=forms.Textarea(attrs={'class':'textField normal','cols':30 ,'rows':5,'style':'overflow: hidden; height: 100px;','onkeyUp':'txtarealimit(this,400);'}) ,error_messages={'required': 'Please enter Description'})
    
    class Meta:
        model = ModuleNames
        fields = ('seo_title','seo_description')
    
