from django import forms
from hotels.models import ApiSettings
from django.utils.translation import ugettext as _

class ApiSettingsForm(forms.ModelForm):
    city = forms.CharField(required=True, max_length=200, widget=forms.TextInput({'placeholder':'New York', 'title':_('City'),'class':'fm',  'maxlength':'255', 'autocomplete':'off'}), error_messages={'required': _('Please enter the city')})
    api_key = forms.CharField(required=True, max_length=400, widget=forms.TextInput({'placeholder':'xxxxxxxxxxxxxxxxxx', 'title':_('API Key'),'class':'fm',  'maxlength':'400', 'autocomplete':'off'}), error_messages={'required': _('Please enter the api key')})
    customer_id = forms.CharField(required=True, max_length=400, widget=forms.TextInput({'placeholder':'1234', 'title':_('Customer ID'),'class':'fm',  'maxlength':'400', 'autocomplete':'off'}), error_messages={'required': _('Please enter the CID')})
    tripadvisor_key = forms.CharField(required=False, max_length=400, widget=forms.TextInput({'placeholder':'xxxxxxxx', 'title':_('Trip Advisor Affiliate ID'),'class':'fm',  'maxlength':'400', 'autocomplete':'off'}), error_messages={'required': _('Please enter the trip advisor affiliate ID')})
    
    class Meta:
        model=ApiSettings
        exclude=('option')  