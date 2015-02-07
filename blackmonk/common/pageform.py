from django import forms
from django.utils.translation import ugettext as _
from django.template.defaultfilters import slugify
    
from common.models import Pages
 
class PagesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        try:self._name = kwargs['instance'].name
        except:self._name= False
        super(PagesForm, self).__init__(*args, **kwargs)
        
    name = forms.CharField(required=True,max_length=30, error_messages={'required': 'Please enter the page name'},widget=forms.TextInput(attrs={'class':'tttxt-w','maxlength':'40','title':_('Page Name'),'style':'width:90%;','placeholder':'Untitled','autocomplete':'off','onkeyUp':'string_to_slug(this.value)'}))
    slug = forms.CharField(required=False,max_length=40, widget=forms.TextInput({'class':'default-url','title':_('Category Slug'),'style':'width:150px; padding:0; color:#666; font-size:12px; font-weight:normal;','maxlength':'40','onkeyUp':'string_to_slug(this.value)','autocomplete':'off'}), error_messages={'required': _('Please enter the slug')})
    seo_title = forms.CharField(required=False,max_length=70, error_messages={'required': _('Please enter the Title')},widget=forms.TextInput(attrs={'class':'tttxt','maxlength':'70','title':_('Meta Title'),'autocomplete':'off','style':'width:90%;'}))
    seo_description = forms.CharField(required=False,max_length=200, error_messages={'required': _('Please enter Description')},widget=forms.Textarea(attrs={'class':'tttxt','cols':30,'rows':5,'style':'width:90%;','title':_('Meta Description'),'onkeyUp':'txtarealimit(this,200);'}))
    content = forms.CharField(required=True, error_messages={'required': _('Please enter page content')},widget=forms.Textarea(attrs={'class':'tttxt','cols':30,'rows':5,'style':'width:100%;','title':_('Page Content')}))
    is_active=forms.BooleanField(required=False,error_messages={'required':'Please Set status'},widget=forms.CheckboxInput(attrs={'style':'vertical-align: middle; margin: 9px 9px 0px 0px; display: inline-block; width: auto;'}))
    
    def clean_name(self):
        name = self.cleaned_data.get("name").strip()
        if self._name:
            if str(self._name).lower() != str(name).lower():
                try:
                    flag=Pages.objects.filter(name__iexact=name)
                    if flag:raise forms.ValidationError(_("This page name is already exist."))
                except Pages.DoesNotExist:pass
        else:
            try:
                flag=Pages.objects.filter(name__iexact=name)
                if flag:raise forms.ValidationError(_("This page name is already exist."))
            except Pages.DoesNotExist:pass
        return name
    
    def clean_slug(self):
        slug = self.cleaned_data.get("slug")
        if slug:return slug
        else:return self.cleaned_data.get("name")
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
        model=Pages
        exclude=('modified_by','modified_on','is_static')  
 