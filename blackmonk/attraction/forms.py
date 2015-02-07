from django import forms
from django.utils.translation import ugettext as _
from django.template.defaultfilters import slugify

from attraction.models import Attraction,AttractionCategory

valid_time_formats = ['%I:%M %p']

class AttractionForm(forms.ModelForm):
    name = forms.CharField(required=True,max_length=200, error_messages={'required': 'Please enter the attraction name'},widget=forms.TextInput(attrs={'class':'tttxt-w','title':_('Enter the main title for attraction'),'placeholder':'Untitled','autocomplete':'off'}))
    alias = forms.CharField(required=False,max_length=350, error_messages={'required': 'Please enter the alias name'},widget=forms.TextInput(attrs={'class':'tttxt-w','title':_('Enter the second title corresponding to the main title.'),'placeholder':'alias','autocomplete':'off'}))
    category = forms.ModelMultipleChoiceField(required=True, error_messages={'required': 'Please select category'},widget=forms.SelectMultiple(attrs={'class':'select-menu fl','title':_('Click and select multiple categories related to the attraction.'),'data-placeholder':_('Select a Category')}),queryset=AttractionCategory.objects.all())
    
    start_time= forms.TimeField(required=False,input_formats=valid_time_formats, error_messages={'required': 'Please enter the attraction opening time','invalid': 'Please enter the vaild attraction opening time'},widget=forms.TimeInput(format='%I:%M %p',attrs={'size':'6','style':'width:161px;','title':'Attraction Opening Time','placeholder':'07:00 AM','autocomplete':'off'}))
    end_time= forms.TimeField(required=False,input_formats=valid_time_formats, error_messages={'required': 'Please enter the attraction closing time','invalid': 'Please enter the vaild attraction closing time'},widget=forms.TimeInput(format='%I:%M %p',attrs={'size':'6','style':'width:160px;','title':'Attraction Closing Time','placeholder':'07:00 PM','autocomplete':'off'}))
    notes = forms.CharField(required=False,max_length=250, error_messages={'required': 'Please enter the Closed on /Notes'},widget=forms.TextInput(attrs={'title':'Closed on /Notes','placeholder':_('Eg:Closed on Wednesday'),'autocomplete':'off','class':'fl'}))
    
    activities = forms.CharField(required=False,max_length=2000, error_messages={'required': 'Please enter the activities'},widget=forms.TextInput(attrs={'title':'Activities','placeholder':_('Eg:Swimming, Snorkelling etc..'),'autocomplete':'off','class':'fl'}))
    time_of_activity = forms.CharField(required=False,max_length=1000, error_messages={'required': 'Please enter the time of activity'},widget=forms.TextInput(attrs={'title':'Time of Activity','placeholder':_('Eg:Half Day'),'autocomplete':'off','class':'fl'}))
    admission_notes = forms.CharField(required=False,max_length=1000, error_messages={'required': 'Please enter the admission notes'},widget=forms.TextInput(attrs={'title':'Admission Notes','placeholder':_('Eg:1 Day Single Park Ticket - Adults: US$82'),'autocomplete':'off','class':'fl'}))
    
    ticket_cost_adult=forms.DecimalField(max_digits=10,decimal_places=2,required=False,error_messages={'required':'Please enter ticket cost for adults'},widget=forms.TextInput(attrs={'maxlength':'10','size':'6','class':'tttxt-w fs prices','title':'Ticket Cost for Adults','placeholder':'Price','autocomplete':'off','style':'margin-top:2px;'}))
    ticket_cost_child=forms.DecimalField(max_digits=10,decimal_places=2,required=False,error_messages={'required':'Please enter ticket cost for adults'},widget=forms.TextInput(attrs={'maxlength':'10','size':'6','class':'tttxt-w fs prices','title':'Ticket Cost for Childrens','placeholder':'Price','autocomplete':'off','style':'margin-top:2px;'}))
    ticket_cost_free=forms.BooleanField(required=False,error_messages={'required':'Please Choose if its free'},widget=forms.CheckboxInput(attrs={'style':'vertical-align:middle;'}))
    
    allow_user_photo=forms.BooleanField(required=False,error_messages={'required':'Please choose if user can add photo'},widget=forms.CheckboxInput(attrs={'style':'vertical-align:middle;'}))
    ticket_url = forms.CharField(required=False,max_length=150, error_messages={'required': 'Please enter the Ticket URL'},widget=forms.TextInput(attrs={'class':'fl','onfocus':'showhttp("t")','onblur':'hidehttp("t")','title':'Ticket URL','placeholder':'https://example.com/ticket','autocomplete':'off'}))
    website_url= forms.CharField(required=False,max_length=150, error_messages={'required': 'Please enter the Ticket URL'},widget=forms.TextInput(attrs={'class':'fl','onfocus':'showhttp("w")','onblur':'hidehttp("w")','title':'Website URL','placeholder':'http://example.com','autocomplete':'off'}))
    
    fb_url = forms.CharField(required=False,max_length=150, error_messages={'required': 'Please enter the Facebook URL'},widget=forms.TextInput(attrs={'onfocus':'showhttp("f")','style':'width:329px;','onblur':'hidehttp("f")','title':'Facebook URL','placeholder':'http://facebook.com/page','autocomplete':'off'}))
    twitter_url = forms.CharField(required=False,max_length=150, error_messages={'required': 'Please enter the Twitter URL'},widget=forms.TextInput(attrs={'onfocus':'showhttp("tw")','style':'width:329px;','onblur':'hidehttp("tw")','title':'Twitter URL','placeholder':'http://twitter.com/page','autocomplete':'off'}))
    gooleplus_url = forms.CharField(required=False,max_length=150, error_messages={'required': 'Please enter the Google+ URL'},widget=forms.TextInput(attrs={'onfocus':'showhttp("g")','style':'width:329px;','onblur':'hidehttp("g")','title':'Google Plus URL','placeholder':'http://plus.google.com/page','autocomplete':'off'}))
    description = forms.CharField(required=True, widget=forms.Textarea({'class':'textField long'}),error_messages={'required': 'Please enter the description'})
    
    class Meta:
        model = Attraction
        fields = ('name','alias','category','description','ticket_url','website_url','fb_url','twitter_url',
                  'gooleplus_url','ticket_cost_adult','ticket_cost_child','ticket_cost_free','start_time',
                  'end_time','notes','allow_user_photo','activities','time_of_activity','admission_notes')

class Attraction_SeoForm(forms.ModelForm):
    #slug = forms.CharField(required=True, widget=forms.TextInput({'class':'default-url','title':_('Category Slug'),'style':'width:180px;','maxlength':'200','onkeyUp':'string_to_slug(this.value)','autocomplete':'off'}), error_messages={'required': _('Please enter the slug')})
    seo_title = forms.CharField(required=True,max_length=200, error_messages={'required': _('Please enter the Title')},widget=forms.TextInput(attrs={'class':'fm','maxlength':'200','title':_('Meta Title'),'autocomplete':'off'}))
    seo_description = forms.CharField(required=True,max_length=400, error_messages={'required': _('Please enter Description')},widget=forms.Textarea(attrs={'class':'fxl','cols':30,'rows':4,'style':'height:70px;','title':_('Meta Description'),'onkeyUp':'txtarealimit(this,400);'}))
    
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
        model = Attraction
        fields = ('seo_title','seo_description')
    
    
class AttractionCategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        try:self._name = kwargs['instance'].name
        except:self._name= False
        super(AttractionCategoryForm, self).__init__(*args, **kwargs)
        
    name = forms.CharField(required=True, error_messages={'required': 'Please enter the Category name'},widget=forms.TextInput(attrs={'class':'fm','maxlength':'150','title':'Category Name','onkeyup':'string_to_slug(this.value)','autocomplete':'off'}))
    slug = forms.CharField(required=False, error_messages={'required': 'Please enter the slug'},widget=forms.TextInput(attrs={'class':'default-url','maxlength':'200','title':'Category Slug','onkeyup':'string_to_slug(this.value)','autocomplete':'off','style':'width:138px;'}))
    seo_title = forms.CharField(required=False,max_length=200, error_messages={'required': 'Please enter the Title'},widget=forms.TextInput(attrs={'class':'fm','maxlength':'200','title':'Meta Title','autocomplete':'off'}))
    seo_description = forms.CharField(required=False, error_messages={'required': 'Please enter Description'},widget=forms.Textarea(attrs={'class':'fm','onkeyUp':'txtarealimit(this,400);','cols':30,'rows':5,'style':'height:70px;','title':'Meta Description'}))
    
    class Meta:
        model = AttractionCategory
        exclude = ('created_by','modified_by')
    def clean_name(self):
        name = self.cleaned_data.get("name").strip()
        if self._name:
            if str(self._name).lower() != str(name).lower():
                try:
                    flag=AttractionCategory.objects.filter(name__iexact=name)
                    if flag:raise forms.ValidationError(_("This category name is already added."))
                except AttractionCategory.DoesNotExist:pass
        else:
            try:
                flag=AttractionCategory.objects.filter(name__iexact=name)
                if flag:raise forms.ValidationError(_("This category name is already added."))
            except AttractionCategory.DoesNotExist:pass
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
    
        
class AttractionCategorySeoForm(forms.ModelForm):
    slug = forms.CharField(required=True, error_messages={'required': 'Please enter the  name'},widget=forms.TextInput(attrs={'class':'default-url','maxlength':'200','style':'width:138px;','onkeyup':'string_to_slug(this.value)','autocomplete':'off'}))
    seo_title = forms.CharField(required=True,max_length=200, error_messages={'required': 'Please enter the Title'},widget=forms.TextInput(attrs={'class':'fm','maxlength':'200','title':'Meta Title','autocomplete':'off'}))
    seo_description = forms.CharField(required=True, error_messages={'required': 'Please enter Description'},widget=forms.Textarea(attrs={'class':'fm','onkeyUp':'txtarealimit(this,400);','title':'Meta Description','cols':30,'rows':5,'style':'height:70px;'}))
    
    class Meta:
        model = AttractionCategory
        fields = ('slug','seo_title','seo_description')
        
    def clean_seo_title(self):
        seo_title = self.cleaned_data.get("seo_title").strip()
        if len(seo_title) > 200:
            raise forms.ValidationError(_("Maximum length of meta-title field is 200 characters."))
        else:return seo_title
    def clean_seo_description(self):
        seo_description = self.cleaned_data.get("seo_description").strip()
        if len(seo_description) > 400:
            raise forms.ValidationError(_("Maximum length of meta-description field is 400 characters."))
        else:return seo_description
            
    