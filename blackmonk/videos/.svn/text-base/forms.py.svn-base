from django import forms
from django.forms import ModelForm

from common.models import ModuleNames
from videos.models import VideoCategory,Videos,VideoComments
from common import captcha
from django.utils.translation import ugettext as _

class VideoCategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        try:self._name = kwargs['instance'].name
        except:self._name= False
        super(VideoCategoryForm, self).__init__(*args, **kwargs)
    name = forms.CharField(required=True,min_length=1,max_length=100,widget=forms.TextInput(attrs={'class':'fm','maxlength':'100', 'title':_('Category Name'),'onkeyUp':'string_to_slug(this.value)'}), label=("Catgeory"),error_messages={'required': _('Category name required.')})
    slug = forms.CharField(required=False,max_length=150, widget=forms.TextInput({'class':'default-url','style':'width:152px;','title':_('Category Slug'),'maxlength':'150','onkeyUp':'string_to_slug(this.value)','autocomplete':'off'}), error_messages={'required': _('Please enter the slug')})
    seo_title = forms.CharField(required=False,max_length=200, error_messages={'required': _('Please enter the Title')},widget=forms.TextInput(attrs={'class':'fm','maxlength':'200','title':_('Meta Title'),'autocomplete':'off'}))
    seo_description = forms.CharField(required=False,max_length=400, error_messages={'required': _('Please enter Description')},widget=forms.Textarea(attrs={'class':'fm','cols':30,'rows':5,'style':'height:70px;','title':_('Meta Description'),'onkeyUp':'txtarealimit(this,400);'}))
    
    def clean_name(self):
        name = self.cleaned_data.get("name").strip()
        if self._name:
            if str(self._name).lower() != str(name).lower():
                try:
                    flag=VideoCategory.objects.filter(name__iexact=name)
                    if flag:raise forms.ValidationError(_("This category name is already added."))
                except VideoCategory.DoesNotExist:pass
        else:
            try:
                flag=VideoCategory.objects.filter(name__iexact=name)
                if flag:raise forms.ValidationError(_("This category name is already added."))
            except VideoCategory.DoesNotExist:pass
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
            
    class Meta:
        model = VideoCategory
        fields = ('name','slug','seo_title','seo_description')

class VideoCategorySeoForm(forms.ModelForm):
    slug = forms.CharField(required=True, widget=forms.TextInput({'class':'default-url','style':'width:150px;','title':_('Category Slug'),'maxlength':'200','onkeyUp':'string_to_slug(this.value)','autocomplete':'off'}), error_messages={'required': _('Please enter the slug')})
    seo_title = forms.CharField(required=True,max_length=200,widget=forms.TextInput(attrs={'class':'fm','maxlength':'200','title':_('Meta Title'),'autocomplete':'off'}), error_messages={'required': _('Please enter the Meta Title')})
    seo_description = forms.CharField(required=True,max_length=400,widget=forms.Textarea(attrs={'class':'fm','cols':30,'rows':5,'style':'height:70px;','title':_('Meta Description'),'onkeyUp':'txtarealimit(this,400);'}), error_messages={'required': _('Please enter the Meta Keyword')})
    
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
            
    class Meta:
        model = VideoCategory
        fields = ('slug','seo_title','seo_description')
        
class AddVideoViaLinkForm(forms.ModelForm):
    title = forms.CharField(required=True,min_length=1,max_length=150,widget=forms.TextInput(attrs={'class':'fm tttxt', 'style':'height:22px;','title':_('Title')}), label=("Title"),error_messages={'required': u'Video Title required.'})
    category = forms.ModelChoiceField( label=("Category"),queryset=VideoCategory.objects.all(),widget=forms.Select(attrs={'class':'fm  lb_select-menu','style':'width:302px','title':_('Category')}),empty_label="Category",error_messages={'required': u'Video Category required.'})
    description = forms.CharField(required=True,min_length=1, max_length=800, widget=forms.Textarea(attrs={'class':'fm tttxt', 'cols':30, 'rows':5, 'style':'height:120px;','title':_('Description')}), label=("description"),error_messages={'required': u'Video Description required.'})
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title.strip()=='':
          raise  forms.ValidationError('Enter a Valid Title')
        else:
            return title    
    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description.strip()=='':
          raise  forms.ValidationError(_("Enter a Valid Description"))
        else:
            return description    
    
    class Meta:
        model = Videos
        fields = ('title','category','description')

class UserAddVideoViaLinkForm(forms.ModelForm):
    title = forms.CharField(required=True,min_length=1,max_length=150,widget=forms.TextInput(attrs={'class':'iSp8', 'title':_('Title')}), label=("Title"), error_messages={'required': u'Video Title required.'})
    category = forms.ModelChoiceField( label=("Category"),queryset=VideoCategory.objects.all(),widget=forms.Select(attrs={'class':'iSp8 bM-sLt','title':_('Category')}), empty_label=None,error_messages={'required': u'Video Category required.'})
    description = forms.CharField(required=True,min_length=1, widget=forms.Textarea(attrs={'class':'iSp8', 'cols':30, 'rows':5, 'title':_('Description')}), label=("description"),error_messages={'required': u'Video Description required.'})
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title.strip()=='':
          raise  forms.ValidationError('Enter a Valid Title')
        else:
            return title    
    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description.strip()=='':
          raise  forms.ValidationError(_("Enter a Valid Description"))
        else:
            return description    
    
    class Meta:
        model = Videos
        fields = ('title','category','description')
        
class VideoSEOForm(forms.ModelForm):
    seo_title = forms.CharField(required=True,min_length=1,max_length=70,widget=forms.TextInput(attrs={'maxlength':70,'class':'fm', 'style':'height:22px;','title':_('Meta Title')}), label=("Title"),error_messages={'required': u'Meta Title required.'})
    seo_description = forms.CharField(required=True,min_length=1, max_length=160, widget=forms.Textarea(attrs={'maxlength':160,'class':'fxl', 'cols':30, 'rows':4, 'style':'height:120px;','title':_('Meta Description')}), label=("meta description"),error_messages={'required': u'Meta Description required.'})   
    
    def clean_seo_title(self):
        seo_title = self.cleaned_data.get("seo_title").strip()
        if len(seo_title) > 70:
            raise forms.ValidationError(_("Maximum length of meta-title field is 70 characters."))
    
    def clean_seo_description(self):
        seo_description = self.cleaned_data.get("seo_description").strip()
        if len(seo_description) > 160:
            raise forms.ValidationError(_("Maximum length of meta-description field is 160 characters."))
        else:
            if seo_description: return seo_description
            else:return self.cleaned_data.get("name")
    
    class Meta:
        model = Videos
        fields = ('seo_title','seo_description')

class UserVideoSEOForm(forms.ModelForm):
    seo_title = forms.CharField(required=True,min_length=1,max_length=70,widget=forms.TextInput(attrs={'class':'iSp8','maxlength':70, 'style':'height:22px;','title':_('Meta Title')}), label=("Title"),error_messages={'required': u'Meta Title required.'})
    seo_description = forms.CharField(required=True,min_length=1, max_length=160, widget=forms.Textarea(attrs={'class':'iSp8','maxlength':160, 'cols':30, 'rows':4, 'style':'height:120px;','title':_('Meta Description')}), label=("meta description"),error_messages={'required': u'Meta Description required.'})   
    
    def clean_seo_title(self):
        seo_title = self.cleaned_data.get("seo_title").strip()
        if len(seo_title) > 70:
            raise forms.ValidationError(_("Maximum length of meta-title field is 70 characters."))
    
    def clean_seo_description(self):
        seo_description = self.cleaned_data.get("seo_description").strip()
        if len(seo_description) > 160:
            raise forms.ValidationError(_("Maximum length of meta-description field is 160 characters."))
        else:
            if seo_description: return seo_description
            else:return self.cleaned_data.get("name")
    
    class Meta:
        model = Videos
        fields = ('seo_title','seo_description')

