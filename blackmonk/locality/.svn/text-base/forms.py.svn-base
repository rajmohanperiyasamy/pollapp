from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()

from common.models import VenueType,Address
from locality.models import Zipcode,Locality
from django.utils.translation import ugettext as _

attrs_choice = { 'class': 'choicestyle' }
attrs_multi = { 'class' : 'multisele' }
attrs_text = { 'class' : 'textstyle' }
attrs_choicelocation = {'class': 'choicestyle', 'onchange':'newlocation(this)'}


class CityForm(forms.Form):
    name = forms.CharField(required=True,error_messages={'required': 'Please enter the city name'})
    logo = forms.ImageField(required=False,error_messages={'required': 'Please enter a valid path for the image'})

class LocationForm(forms.ModelForm):
    name = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'tttxt'}),error_messages={'required': 'Please enter the name'})
    zipcodes = forms.ModelMultipleChoiceField(required=True, label=("zip"),queryset=Zipcode.objects.order_by('zip'),widget=forms.SelectMultiple(attrs={'class':'textField normal'}),error_messages={'required': u'Please pick zip codes.'})
    
    class Meta:
        model = Locality
        exclude = ('latitude','longitude','zoom')
    def clean_name(self):
        name = self.cleaned_data.get("name")
        name = name.strip()
        if name:
            try:
                Locality.objects.get(name=name)
                raise forms.ValidationError("The locality '"+name+"' already added")
            except Locality.DoesNotExist:pass
            except:pass
        return name

class ZipForm(forms.ModelForm):
    zip = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'tttxt postal','title':_('ZipCodes')}),error_messages={'required': _('Please enter the zip code')})
    class Meta:
        model = Zipcode
        exclude = ('latitude','longitude','zoom')
    def clean_zip(self):
        zip = self.cleaned_data.get("zip")
        zip = zip.strip()
        return zip
    
class LocationImageForm(forms.Form):
    image = forms.ImageField(required=True,error_messages={'required': 'Please select a valid path for the image'})

class GalleryImageForm(forms.Form):
    gallery = forms.ImageField(required=False,error_messages={'required': 'Please select a valid path for the image'})


class LocalityDetailForm(forms.Form):
    locality = forms.CharField(required=True,error_messages={'required': 'Please select the locality'})
    slug = forms.CharField(required=True,error_messages={'required': 'Please enter the slug value'})
    description = forms.CharField(required=True,error_messages={'required': 'Please enter the description'})


class VenueForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(VenueForm, self).__init__(*args, **kwargs)
        self.fields['type'].widget = forms.Select(attrs={'class':'select-menu fm'})
        self.fields['type'].queryset = VenueType.objects.all().order_by('title')
        self.fields['type'].required = False
        self.fields['type'].empty_label = _("-- Venue Type --")
        self.fields['type'].error_messages = _("Please select venue type.")
    venue = forms.CharField(required=True,max_length=100, error_messages={'required': _('Please enter the Venue')},widget=forms.TextInput(attrs={'id':'id_venues','class':'fm','title':_('Venue Name')}))
    address1 = forms.CharField(required=True,max_length=150, error_messages={'required': _('Please enter the Address')},widget=forms.TextInput(attrs={'class':'fm','title':_('Address')}))
    address2 = forms.CharField(required=False,max_length=150,widget=forms.TextInput(attrs={'class':'fm','title':_('Address 2')}))
    telephone1=forms.CharField(required=False,max_length=20,widget=forms.TextInput(attrs={'class':'fm','title':_('Telephone No 1')}))
    telephone2=forms.CharField(required=False,max_length=20,widget=forms.TextInput(attrs={'class':'fm','title':_('Telephone No 2')}))
    mobile=forms.CharField(required=False,max_length=20,widget=forms.TextInput(attrs={'class':'fm','title':_('Mobile No')}))
    email=forms.EmailField(required=False,max_length=75,widget=forms.TextInput(attrs={'class':'fm','title':_('Email ID')}))
    website=forms.URLField(required=False,max_length=240,widget=forms.TextInput(attrs={'class':'fm','title':_('Website')}))
    description=forms.CharField(required=False,widget=forms.Textarea(attrs={'id':'id_descriptions','class':'fm','title':_('Description'),'cols':25,'rows':3}))
    city = forms.CharField(required=False,max_length=100, error_messages={'required': _('Please enter the City')},widget=forms.TextInput(attrs={'id':'id_city','class':'fm','title':_('City Name')}))
    #locality = forms.ModelChoiceField(required=True, queryset = Locality.objects.order_by('name'), error_messages={'required': 'Please select the Location'}, empty_label='Select The Locality', widget=forms.Select(attrs={'class':'textField locality','onchange':'newlocation();'}))
    zip = forms.CharField(required=True,max_length=26, error_messages={'required': _('Please enter the zip code')},widget=forms.TextInput(attrs={'class':'fm postal','title':_('ZipCodes')}))
    
    class Meta:
        model = Address
        exclude = ('address_type','lat','lon','zoom','status','is_active','created_on','created_by','modified_on','modified_by','seo_title','seo_description')
    
class VenueTypeForm(forms.ModelForm):
    title = forms.CharField(required=True,max_length=200, error_messages={'required': _('Please enter the name')},widget=forms.TextInput({'class':'fm','maxlength':'120','onkeyUp':'string_to_slug(this.value)','title':_('Category Name'),'autocomplete':'off'}))
    slug = forms.CharField(required=False, widget=forms.TextInput({'class':'default-url','style':'width:152px;','title':_('Category Slug'),'maxlength':'200','onkeyUp':'string_to_slug(this.value)','autocomplete':'off'}), error_messages={'required': _('Please enter the slug')})
    seo_title = forms.CharField(required=False,max_length=200, error_messages={'required': _('Please enter the Title')},widget=forms.TextInput(attrs={'class':'fm','maxlength':'200','title':_('Meta Title'),'autocomplete':'off'}))
    seo_description = forms.CharField(required=False,max_length=400, error_messages={'required': _('Please enter Description')},widget=forms.Textarea(attrs={'class':'fm','cols':30,'rows':5,'style':'height:70px;','title':_('Meta Description'),'onkeyUp':'txtarealimit(this,400);'}))
    
    def clean_slug(self):
        slug = self.cleaned_data.get("slug")
        if slug:return slug
        else:
            title = self.cleaned_data.get("title")
            return title
    def clean_seo_title(self):
        seo_title = self.cleaned_data.get("seo_title").strip()
        if len(seo_title) > 200:
            raise forms.ValidationError(_("Maximum length of meta-title field is 200 characters."))
        else:
            if seo_title: return seo_title
            else:return self.cleaned_data.get("title")
    def clean_seo_description(self):
        seo_description = self.cleaned_data.get("seo_description").strip()
        if len(seo_description) > 400:
            raise forms.ValidationError(_("Maximum length of meta-description field is 400 characters."))
        else:
            if seo_description: return seo_description
            else:return self.cleaned_data.get("title")
    class Meta:
        model = VenueType
           
class VenueSeoForm(forms.ModelForm):
    seo_title = forms.CharField(required=True,max_length=200, error_messages={'required': _('Please enter the Title')},widget=forms.TextInput(attrs={'class':'tttxt','maxlength':'200','title':_('Meta Title'),'autocomplete':'off'}))
    seo_description = forms.CharField(required=True,max_length=400, error_messages={'required': _('Please enter Description')},widget=forms.Textarea(attrs={'class':'tttxt','cols':30,'rows':5,'style':'height:70px;','title':_('Meta Description'),'onkeyUp':'txtarealimit(this,400);'}))
    
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
        model = Address
        fields = ('seo_title','seo_description')
        
