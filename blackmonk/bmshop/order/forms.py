from django import forms
from django.utils.translation import ugettext_lazy as _

from bmshop.customer.models import Address


class AddressForm(forms.ModelForm):
    firstname = forms.CharField(required=True,max_length=100,widget=forms.TextInput(attrs={'class':'textField normal'}),error_messages={'required': _('Please enter the name')})
    address = forms.CharField(required=True,max_length=200,widget=forms.Textarea(attrs={'class':'textField small'}),error_messages={'required': _('Please enter the Address')})
    zip_code = forms.CharField(required=True,max_length=100,widget=forms.TextInput(attrs={'class':'textField small'}),error_messages={'required': _('Please enter the zip code')})
    city = forms.CharField(required=True,max_length=100,widget=forms.TextInput(attrs={'class':'textField normal'}),error_messages={'required': _('Please enter the city')})
    state = forms.CharField(required=True,max_length=100,widget=forms.TextInput(attrs={'class':'textField normal'}),error_messages={'required': _('Please enter the state')})
    phone = forms.CharField(required=False,max_length=20,widget=forms.TextInput(attrs={'class':'textField small'}),error_messages={'required': _('Please enter the phone number')})
    
    class Meta:
        model = Address 
        exclude = ('user','country',)