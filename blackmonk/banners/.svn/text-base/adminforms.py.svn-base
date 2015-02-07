from django import forms
from banners.models import BannerZones, BannerSections, BannerPayment
from django.utils.translation import ugettext as _
from django.template.defaultfilters import slugify

SLOT_TYPES = (('','Select a Type'),('T', 'Top'),('R', 'Right'),('B', 'Bottom'))

class AddBannerZoneForm(forms.ModelForm):
    name = forms.CharField(required=True,max_length=200, widget=forms.TextInput({'class':'fm','title':_('Name'), 'maxlength':'200','autocomplete':'off'}), error_messages={'required': _('Please enter the zone name')})
    sections = forms.ModelMultipleChoiceField(required=True, queryset=BannerSections.objects.order_by('name'), widget=forms.SelectMultiple(attrs={'class':'select-menu fm', 'onchange':'resize_cb();', 'data-placeholder':_('Select multiple modules')}), error_messages={'required': _('Please select a module')})
    slot = forms.ChoiceField(required=True, choices=SLOT_TYPES, widget=forms.Select(attrs={'class':'select-menu', 'style':'width:168px;'}), error_messages={'required': 'Please select a slot'})
    height = forms.CharField(required=True,max_length=10, widget=forms.TextInput({'class':'fs','title':_('Height'), 'maxlength':'10','autocomplete':'off'}), error_messages={'required': _('Please enter the zone height')})
    width = forms.CharField(required=True,max_length=10, widget=forms.TextInput({'class':'fs','title':_('Width'),'maxlength':'10','autocomplete':'off'}), error_messages={'required': _('Please enter the zone width')})
    
    class Meta:
        model = BannerZones
    
    def clean_name(self):
        name = self.cleaned_data.get("name")
        if self.instance.id:
            if BannerZones.objects.filter(name__iexact=name).exclude(id=self.instance.id).count()!=0:
                raise forms.ValidationError(_("Zone with this name already exists."))
            else:return name   
        else:
            if BannerZones.objects.filter(name__iexact=name).count()!=0:
                raise forms.ValidationError(_("Zone with this name already exists."))
            else:return name 
    
    def clean_height(self):
        height = self.cleaned_data.get("height")
        if height > 9999999999:
            raise forms.ValidationError(_("Please enter a correct height value"))
    def clean_width(self):
        width = self.cleaned_data.get("width")
        if width > 9999999999:
            raise forms.ValidationError(_("Please enter a correct width value"))
    

class BannerPaymentForm(forms.ModelForm):
    #price_year = forms.FloatField(required=False, widget=forms.TextInput(attrs={'class':'textField', 'style':'width:72px; height:25px;'}), error_messages={'required': 'Banner Price per Year field Shouldn\'t be empty.', 'invalid': 'Banner Price per Year field should be a number'})
    impressions = forms.IntegerField(required=True, widget=forms.TextInput(attrs={'class':'textField val','maxlength':'12', 'style':'width:72px; height:25px;'}), error_messages={'required': 'Impressions Block field Shouldn\'t be empty.', 'invalid': 'Impressions Block field should be a number'})
    price_impressions = forms.FloatField(required=True, widget=forms.TextInput(attrs={'class':'textField val', 'maxlength':'12','style':'width:72px; height:25px;'}), error_messages={'required': 'Banner Price per Impressions field Shouldn\'t be empty.', 'invalid': 'Banner Price per Impressions field should be a number'})
    
    class Meta:
        model = BannerPayment 
        exclude=('level','created_on','created_by')