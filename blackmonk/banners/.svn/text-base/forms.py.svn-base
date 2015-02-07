from django import forms
from django.utils.translation import ugettext as _
from django.template.defaultfilters import slugify

from banners.models import BannerAdvertisements, BannerSections, BannerZones, HeroBanners
from common.form_utils import HorizCheckboxSelectMultiple,HorizRadioRenderer

valid_date_formats = ['%m/%d/%Y']
target_types = ((False, 'No'), (True, 'Yes'))
banner_script_options = ((True, 'Paste Banner Script'), (False, 'Upload Banner Creative'))

class AddBannerForm(forms.ModelForm):
    caption = forms.CharField(required=True,max_length=300, error_messages={'required': 'Please enter the banner caption'},widget=forms.TextInput({'placeholder':_('Untitled Banner'),'autocomplete':'off','class':'iSp8'}))
    zones = forms.ModelChoiceField(required=True, widget=forms.Select(attrs={'class':'iSp8 bM-sLt', 'onchange':'update_banner_pricing($(this).val());', 'title':_('Select a zone/type')}),queryset=BannerZones.objects.all().order_by('name'), empty_label="",error_messages={'required': _('Please select the zone/type')})
    image = forms.ImageField(required=False, error_messages={'required': 'Please upload Image'},widget=forms.FileInput)
    expiry_date = forms.DateField(required=False, input_formats=valid_date_formats, widget=forms.DateInput(format='%m/%d/%Y',attrs={'class':'fx','style':'margin-right:7px;','autocomplete':'off'}), error_messages={'required': _('Expiry date Required')})
    section = forms.ModelChoiceField(required=True, widget=forms.Select(attrs={'class':'iSp8 bM-sLt','title':_('Select a module'),'data-size':'8','onchange':'load_categories(),load_banner_zones();'}),queryset=BannerSections.objects.all().order_by('name'), empty_label="",error_messages={'required': _('Please select the banner module')})
    is_new_tab = forms.TypedChoiceField(required=True, widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices = target_types, initial=True, error_messages = {'required':'Please Select option open in a new window.'})
    destination_url = forms.URLField(required=False, max_length=250, widget=forms.TextInput(attrs={'placeholder':_('Destination URL'),'onfocus':'showhttp(4)','onblur':'hidehttp(4)', 'class':'iSp8'}), error_messages={'invalid':_('Invalid Destination URL.')})
    is_script = forms.TypedChoiceField(required=True, widget=forms.RadioSelect(attrs={'onclick':'select_banner_upload_choice($(this).val());'},renderer=HorizRadioRenderer),choices = banner_script_options, initial=False, error_messages = {'required':'Please Select option open in a new window.'})
    banner_script = forms.CharField(required=False,widget=forms.Textarea(attrs={'rows': '6','class': 'fl', 'placeholder': "Copy and Paste the banner script from any third party banner management. Eg: OpenX, Google DFP and more... "}),error_messages={'required': _('Please enter the banner script code')})
    
    class Meta:
        model = BannerAdvertisements
        exclude = ('created_by','modified_by','status','temp_amount','temp_impressions','impressions','total_amount')
        
    def __init__(self, *args, **kwargs):
        sectionobj = kwargs.pop('sectionobj', None)
        super(AddBannerForm, self).__init__(*args, **kwargs)
        if sectionobj:self.fields['zones'].queryset = BannerZones.objects.filter(sections=sectionobj)    
    
    def clean(self):
        from PIL import Image
        cleaned_data = super(AddBannerForm, self).clean()
        try:
            image = cleaned_data.get("image")
            zones = cleaned_data.get("zones")
            image_attr=Image.open(image)
            width,height = image_attr.size
            if width > zones.width or height > zones.height:
                self._errors["image"] = self.error_class(['Banner Image size is bigger than the selected zone size'])
        except:pass        
        return cleaned_data 

class StaffAddHeroBannerForm(forms.ModelForm):
    title = forms.CharField(required=True,max_length=200, error_messages={'required': 'Please enter the banner caption'},widget=forms.TextInput({'placeholder':_('Untitled Banner'),'autocomplete':'off'}))
    image = forms.ImageField(required=False, error_messages={'required': 'Please upload Image'},widget=forms.FileInput)
    is_new_tab = forms.TypedChoiceField(required=True, widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices = target_types, initial=True, error_messages = {'required':'Please Select option open in a new window.'})
    destination_url = forms.URLField(required=False, max_length=250, widget=forms.TextInput(attrs={'placeholder':_('Destination URL'), 'class':'fl'}), error_messages={'invalid':_('Invalid Destination URL.')})
    display_order = forms.IntegerField(required=True, widget=forms.TextInput(attrs={'class':'textField','placeholder':_('eg: 1 or 2 or 3 ...'),'autocomplete':'off'}), error_messages={'required': 'Please Enter the order.'})
    class Meta:
        model = HeroBanners
        fields=('title','image','is_new_tab','destination_url','display_order')
    

class StaffAddBannerForm(forms.ModelForm):
    caption = forms.CharField(required=True,max_length=200, error_messages={'required': 'Please enter the banner caption'},widget=forms.TextInput({'placeholder':_('Untitled Banner'),'autocomplete':'off'}))
    zones = forms.ModelChoiceField(required=True, widget=forms.Select(attrs={'class':'select-menu fl', 'onchange':'update_banner_pricing($(this).val());', 'data-placeholder':_('Select a zone/type')}),queryset=BannerZones.objects.all().order_by('name'), empty_label="",error_messages={'required': _('Please select the zone/type')})
    image = forms.ImageField(required=False, error_messages={'required': 'Please upload Image'},widget=forms.FileInput)
    expiry_date = forms.DateField(required=False, input_formats=valid_date_formats, widget=forms.DateInput(format='%m/%d/%Y',attrs={'class':'fx','readonly':'readonly','style':'margin-right:7px;','autocomplete':'off'}), error_messages={'required': _('Expiry date Required')})
    section = forms.ModelChoiceField(required=True, widget=forms.Select(attrs={'class':'select-menu fl','data-placeholder':_('Select a module'),'onchange':'load_categories(),load_banner_zones();'}),queryset=BannerSections.objects.all().order_by('name'), empty_label="",error_messages={'required': _('Please select the banner module')})
    is_new_tab = forms.TypedChoiceField(required=True, widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices = target_types, initial=True, error_messages = {'required':'Please Select option open in a new window.'})
    destination_url = forms.URLField(required=False, max_length=250, widget=forms.TextInput(attrs={'placeholder':_('Destination URL'),'onfocus':'showhttp(4)','onblur':'hidehttp(4)', 'class':'fl'}), error_messages={'invalid':_('Invalid Destination URL.')})
    is_script = forms.TypedChoiceField(required=True, widget=forms.RadioSelect(attrs={'onclick':'select_banner_upload_choice($(this).val());'},renderer=HorizRadioRenderer),choices = banner_script_options, initial=False, error_messages = {'required':'Please Select option open in a new window.'})
    banner_script = forms.CharField(required=False,widget=forms.Textarea(attrs={'rows': '6','class': 'fl', 'placeholder': "Enter the third party banner script code in this text box"}),error_messages={'required': _('Please enter the banner script code')})
    
    class Meta:
        model = BannerAdvertisements
        exclude = ('created_by','modified_by','status','temp_amount','temp_impressions','impressions','total_amount')
        
    def __init__(self, *args, **kwargs):
        sectionobj = kwargs.pop('sectionobj', None)
        super(StaffAddBannerForm, self).__init__(*args, **kwargs)
        if sectionobj:self.fields['zones'].queryset = BannerZones.objects.filter(sections=sectionobj)    
    
    def clean(self):
        from PIL import Image
        cleaned_data = super(StaffAddBannerForm, self).clean()
        try:
            image = cleaned_data.get("image")
            zones = cleaned_data.get("zones")
            image_attr=Image.open(image)
            width,height = image_attr.size 
            if width > zones.width or height > zones.height:
                self._errors["image"] = self.error_class(['Banner Image size is bigger than the selected zone size'])
        except:pass        
        return cleaned_data 
    
   
