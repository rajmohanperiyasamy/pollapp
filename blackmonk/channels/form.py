from django import forms
from django.utils.translation import ugettext as _
from django.template.defaultfilters import slugify
    
from channels.models import Channel

class ChannelForm(forms.ModelForm):
    title = forms.CharField(required=True, max_length=100, error_messages={'required': 'Please enter the channel title'},widget=forms.TextInput(attrs={'class':'tttxt-w','maxlength':'40','title':_('Page Name'),'style':'width:90%;','placeholder':'Untitled','autocomplete':'off','onkeyUp':'string_to_slug(this.value)'}))
    slug = forms.CharField(required=False, max_length=100, widget=forms.TextInput({'class':'default-url','title':_('Channel Slug'),'style':'width:150px; padding:0; color:#666; font-size:12px; font-weight:normal;','maxlength':'40','onkeyUp':'string_to_slug(this.value)','autocomplete':'off'}), error_messages={'required': _('Please enter the slug')})
    description = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows':'8'}),error_messages={'required': _('Please enter the description')})
    
    class Meta:
        model=Channel
        exclude=('status', 'seo_title', 'seo_description', 'created_by', 'modified_by', 'template_name')  
 
    def clean_slug(self):
        slug = self.cleaned_data.get("slug")
        if slug:return slug
        else:return slugify(self.cleaned_data.get("title"))
        

class ChannelSeoForm(forms.ModelForm):
    seo_title = forms.CharField(required=True,max_length=70, error_messages={'required': _('Please enter the Title')},widget=forms.TextInput(attrs={'class':'fm','maxlength':'200','title':_('Meta Title'),'autocomplete':'off'}))
    seo_description = forms.CharField(required=True,max_length=160, error_messages={'required': _('Please enter Description')},widget=forms.Textarea(attrs={'class':'fxl','cols':30,'rows':4,'style':'height:70px;','title':_('Meta Description'),'onkeyUp':'txtarealimit(this,400);'}))

    def clean_seo_title(self):
        seo_title = self.cleaned_data.get("seo_title").strip()
        if len(seo_title) > 70:
            raise forms.ValidationError(_("Maximum length of meta-title field is 70 characters."))
        else:
            if seo_title: return seo_title
            else:return self.cleaned_data.get("name")
    def clean_seo_description(self):
        seo_description = self.cleaned_data.get("seo_description").strip()
        if len(seo_description) > 160:
            raise forms.ValidationError(_("Maximum length of meta-description field is 160 characters."))
        else:
            if seo_description: return seo_description
            else:return self.cleaned_data.get("name")

    class Meta:
        model = Channel
        fields=('seo_title','seo_description')
