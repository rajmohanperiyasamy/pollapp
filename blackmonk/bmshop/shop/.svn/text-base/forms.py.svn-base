from django import forms
from django.utils.translation import ugettext_lazy as _
from django_countries.countries import COUNTRIES

from bmshop.shop.models import Shop,PymentSettings,Shipping



class ShopSettingsForm(forms.ModelForm):
    notification_emails = forms.CharField(required=True,widget=forms.HiddenInput(),error_messages={'required': _('Notification Email Required.')})
    default_country = forms.CharField(required=True, widget=forms.Select(attrs={'class':'select-menu fxl','data-placeholder':_('Choose Country')},choices=COUNTRIES),error_messages={'required': _('Please select the default country')})
    is_taxes  = forms.BooleanField(required=False,widget=forms.CheckboxInput())
    tax_value  = forms.FloatField(required=False, error_messages={'required': _('Please enter the tax rate')},widget=forms.TextInput({'class':'fm','placeholder':_('10'),'maxlength':'5','placeholder':'Ex. 7.0','autocomplete':'off','title':_('Tax rate')}),initial=0)
    meta_title = forms.CharField(required=True,max_length=200, error_messages={'required': _('Please enter the Meta Title')},widget=forms.TextInput(attrs={'class':'fxl','maxlength':'200','title':_('Meta Title'),'data-placeholder':_('Enter a short title'),'autocomplete':'off'}))
    meta_description = forms.CharField(required=True,max_length=400, error_messages={'required': _('Please enter Meta Description')},widget=forms.Textarea(attrs={'class':'fxl','cols':30,'rows':8,'style':'height:70px;','title':_('Meta Description'),'data-placeholder':_('Enter a short description'),'onkeyUp':'txtarealimit(this,400);'}))
    
    class Meta:
        model = Shop
        fields = ('notification_emails','default_country','is_taxes','tax_value','meta_title','meta_description')


class PaymentSettingsForm(forms.ModelForm):
    paypal  = forms.BooleanField(required=False,widget=forms.CheckboxInput())
    googlecheckout  = forms.BooleanField(required=False,widget=forms.CheckboxInput())
    
    class Meta:
        model = PymentSettings
        exclude = ()
        
class ShippingForm(forms.ModelForm):
    name = forms.CharField(required=True,max_length=200, error_messages={'required': _('Please enter the Name')},widget=forms.TextInput(attrs={'class':'fxl','maxlength':'200','title':_('Name'),'data-placeholder':_('Name'),'autocomplete':'off'}))
    description = forms.CharField(required=False,max_length=400, error_messages={'required': _('Please enter the Description')},widget=forms.Textarea(attrs={'class':'fxl','cols':30,'rows':8,'style':'height:70px;','title':_('Description'),'data-placeholder':_('Enter a short description'),'onkeyUp':'txtarealimit(this,400);'}))
    price  = forms.FloatField(required=False,initial=0,error_messages={'required': _('Please enter the tax rate')},widget=forms.TextInput({'class':'fm','placeholder':_('10'),'maxlength':'5','placeholder':'Ex. 7.0','autocomplete':'off','title':_('Shipping Charges')}))
    
    class Meta:
        model = Shipping
        exclude = ('active',)