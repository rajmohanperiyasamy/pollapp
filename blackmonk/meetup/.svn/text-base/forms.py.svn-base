from django import forms
from django.utils.translation import ugettext as _

from meetup.models import MeetupSettings

class MeetupSettingsForm(forms.ModelForm):
    api_key = forms.CharField(required=True,max_length=100,widget=forms.TextInput(attrs={'class':'tttxt-fw fm','maxlength':'100','placeholder':_('API Key'),'title':_('API Key')}),error_messages={'required': _('Please enter the API Key')})
    city = forms.CharField(required=True,max_length=100,widget=forms.TextInput(attrs={'class':'tttxt-fw fm','maxlength':'100','placeholder':_('City name'),'title':_('City name')}),error_messages={'required': _('Please enter the City name')})
    zip = forms.CharField(required=False,max_length=10,widget=forms.TextInput(attrs={'class':'tttxt-fw fm','maxlength':'10','placeholder':_('Zip/PostalCode'),'title':_('Zip/PostalCode')}),error_messages={'required': _('Please enter the Zip/PostalCode')})
    state = forms.CharField(required=True,max_length=50,widget=forms.TextInput(attrs={'class':'tttxt-fw fm','maxlength':'50','placeholder':_('State/Provience'),'title':_('State/Provience name')}),error_messages={'required': _('Please enter the State/Provience')})
    country = forms.CharField(required=True,max_length=50,widget=forms.TextInput(attrs={'class':'tttxt-fw fm','maxlength':'50','placeholder':_('Country'),'title':_('Country name')}),error_messages={'required': _('Please enter the Country name')})
    lat=forms.FloatField(required=False,widget=forms.TextInput(attrs={'class':'tttxt-fw fm','maxlength':'20','placeholder':_('Latitude'),'title':_('Latitude')}),error_messages={'required': _('Please enter the Latitude')})
    lon=forms.FloatField(required=False,widget=forms.TextInput(attrs={'class':'tttxt-fw fm','maxlength':'20','placeholder':_('Longitude'),'title':_('Longitude')}),error_messages={'required': _('Please enter the Longitude')})
    radius = forms.CharField(required=False,max_length=50,widget=forms.TextInput(attrs={'class':'tttxt-fw fm','maxlength':'50','placeholder':_('Radius(in miles)'),'title':_('Radius(in miles)')}),error_messages={'required': _('Please enter the Radius(in miles)')})
    
    class Meta:
        model = MeetupSettings
        exclude=('status')
