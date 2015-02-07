from django import forms
from django.conf import settings
from django.forms import ModelForm
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _

from buzz.models import Category,BuzzTwitterLists,TwitterAPISettings
from common.getunique import getUniqueValue


User = settings.AUTH_USER_MODEL
attrs_dict = { 'class': 'required' }
attrs_text = {'class': 'TextField'}

class BuzzCategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        try:self._name = kwargs['instance'].name
        except:self._name= False
        super(BuzzCategoryForm, self).__init__(*args, **kwargs)
        
    name = forms.CharField(required=True, error_messages={'required': 'Please enter the Category name'},widget=forms.TextInput(attrs={'class':'fm','maxlength':'150','title':'Category Name','onkeyup':'string_to_slug(this.value)','autocomplete':'off'}))
    slug = forms.CharField(required=False, error_messages={'required': 'Please enter the slug'},widget=forms.TextInput(attrs={'class':'default-url tttxt','maxlength':'200','title':'Category Slug','onkeyup':'string_to_slug(this.value)','autocomplete':'off','style':'width:152px;'}))
    description = forms.CharField(required=False, error_messages={'required': 'Please enter Description'},widget=forms.Textarea(attrs={'class':'fm','onkeyUp':'txtarealimit(this,400);','cols':30,'rows':5,'style':'height:70px;','title':'Category Description'}))
    seo_title = forms.CharField(required=False,max_length=200, error_messages={'required': 'Please enter the Title'},widget=forms.TextInput(attrs={'class':'fm','maxlength':'200','title':'Meta Title','autocomplete':'off'}))
    seo_description = forms.CharField(required=False, error_messages={'required': 'Please enter Description'},widget=forms.Textarea(attrs={'class':'fm','onkeyUp':'txtarealimit(this,400);','cols':30,'rows':5,'style':'height:70px;','title':'Meta Description'}))
    
    class Meta:
        model = Category
        fields = ('name','slug','description','seo_title','seo_description')
    def clean_name(self):
        name = self.cleaned_data.get("name").strip()
        if self._name:
            if str(self._name).lower() != str(name).lower():
                try:
                    flag=Category.objects.filter(name__iexact=name)
                    if flag:raise forms.ValidationError(_("This category name is already added."))
                except Category.DoesNotExist:pass
        else:
            try:
                flag=Category.objects.filter(name__iexact=name)
                if flag:raise forms.ValidationError(_("This category name is already added."))
            except Category.DoesNotExist:pass
        return name
    
    def clean_slug(self):
        slug = self.cleaned_data.get("slug")
        if slug:return slug
        else:
            name = self.cleaned_data.get("name")
            return name
    def clean_seo_title(self):
        seo_title = self.cleaned_data.get("seo_title").strip()
        if len(seo_title) > 200:
            raise forms.ValidationError(_("Maximum length of meta-title field is 200 characters."))
        else:
            if seo_title: return seo_title
            else:return self.cleaned_data.get("name")
    def clean_seo_description(self):
        seo_description = self.cleaned_data.get("seo_description").strip()
        if len(seo_description) > 400:
            raise forms.ValidationError(_("Maximum length of meta-description field is 400 characters."))
        else:
            if seo_description: return seo_description
            else:return self.cleaned_data.get("name")

class TwitterlistsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        try:self._lists_name = kwargs['instance'].lists_name
        except:self._lists_name= False
        super(TwitterlistsForm, self).__init__(*args, **kwargs)
        
    lists_name = forms.CharField(required=True, error_messages={'required': 'Please enter the List name'},widget=forms.TextInput(attrs={'class':'tttxt','maxlength':'150','title':'List Name','style':'width:263px;','autocomplete':'off'}))
    list_description = forms.CharField(required=True, error_messages={'required': 'Please enter Description'},widget=forms.Textarea(attrs={'class':'tttxt','cols':30,'rows':5,'style':'height:70px;','title':'Category Description'}))
    category = forms.ModelChoiceField(required=True,queryset=Category.objects.filter(occupied=False).order_by('name'), empty_label="",error_messages={'required': _('Please select the category')})
    
    class Meta:
        model = BuzzTwitterLists
        fields = ('lists_name','list_description')
    def clean_lists_name(self):
        lists_name = self.cleaned_data.get("lists_name").strip()
        if self._lists_name:
            if str(self._lists_name).lower() != str(lists_name).lower():
                try:
                    flag=BuzzTwitterLists.objects.filter(lists_name__iexact=lists_name)
                    if flag:raise forms.ValidationError(_("This list name is already added."))
                except Category.DoesNotExist:pass
        else:
            try:
                flag=BuzzTwitterLists.objects.filter(lists_name__iexact=lists_name)
                if flag:raise forms.ValidationError(_("This list name is already added."))
            except Category.DoesNotExist:pass
        return lists_name

class TwitterSettingsForm(forms.ModelForm):
    twitter_user = forms.CharField(required=True, max_length=250, widget=forms.TextInput({'title':_('Username'),  'maxlength':'255','class':'fm', 'autocomplete':'off'}), error_messages={'required': _('Please enter the Username')})
    twitter_auth_key = forms.CharField(required=True, max_length=250, widget=forms.TextInput({'title':_('Authentication Key'), 'class':'fm', 'maxlength':'255', 'autocomplete':'off'}), error_messages={'required': _('Please enter the Auth Key')})
    twitter_auth_secret = forms.CharField(required=True, max_length=250, widget=forms.TextInput({'title':_('Secret key'),  'maxlength':'255', 'class':'fm','autocomplete':'off'}), error_messages={'required': _('Please enter the Auth Secret')})
    twitter_consumer_key = forms.CharField(required=True, max_length=250, widget=forms.TextInput({'title':_('Consumer Key'),  'maxlength':'255','class':'fm', 'autocomplete':'off'}), error_messages={'required': _('Please enter the Consumer Key')})
    twitter_consumer_secret = forms.CharField(required=True, max_length=250, widget=forms.TextInput({'title':_('Consumer Secret key'), 'class':'fm', 'maxlength':'255', 'autocomplete':'off'}), error_messages={'required': _('Please enter the Consumer Secret')})
    
    class Meta:
        model=TwitterAPISettings
        fields=('twitter_auth_key','twitter_auth_secret','twitter_consumer_key','twitter_consumer_secret','twitter_user')
        
        