from django import forms
from flowers.models import FlowerApiSettings
from django.utils.translation import ugettext as _

class FlowerApiSettingsForm(forms.ModelForm):
    api_key = forms.CharField(required=True, max_length=400, widget=forms.TextInput({'placeholder':'', 'title':_('API Key'),  'maxlength':'300','class':'fm', 'autocomplete':'off'}), error_messages={'required': _('Please enter the api key')})
    api_password = forms.CharField(required=True, max_length=400, widget=forms.TextInput({'placeholder':'', 'title':_('API Password'),  'maxlength':'300','class':'fm', 'autocomplete':'off'}), error_messages={'required': _('Please enter the api password')})
    
    class Meta:
        model=FlowerApiSettings

