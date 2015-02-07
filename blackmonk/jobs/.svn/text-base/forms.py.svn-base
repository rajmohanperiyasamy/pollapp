from django import forms
from django.utils.translation import ugettext as _

from jobs.models import JobSettings


class JobSettingsForm(forms.ModelForm):
    jurl = forms.CharField(required=True, widget=forms.TextInput({'class':'fm','autocomplete':'off','placeholder':'http://api.simplyhired.com/a/jobs-api/xml-v2/'}), error_messages={'required': _('Please enter the Job-a-matic Url')})
    jbd = forms.CharField(required=True, widget=forms.TextInput({'class':'fm','autocomplete':'off','placeholder':_('Job-a-matic domain')}), error_messages={'required': _('Please enter the Job-a-matic domain')})
    pshid = forms.CharField(required=True, widget=forms.TextInput({'class':'fm','autocomplete':'off','placeholder':_('Publisher ID')}), error_messages={'required': _('Please enter the Publisher ID')})
    ssty = forms.CharField(required=True, widget=forms.TextInput({'class':'fm','autocomplete':'off','placeholder':_('Search Style')}), error_messages={'required': _('Please enter the Search Style')})
    cflg = forms.CharField(required=True, widget=forms.TextInput({'class':'fm','autocomplete':'off','placeholder':_('Configuration Flag')}), error_messages={'required': _('Please enter the Configuration Flag')})
    location = forms.CharField(required=False, widget=forms.TextInput({'class':'fm','autocomplete':'off','placeholder':_('Location')}))
    miles = forms.CharField(required=False, widget=forms.TextInput({'class':'fm','autocomplete':'off','placeholder':_('Miles')}))
    post_buttonurl = forms.CharField(required=False,max_length=500,widget=forms.TextInput(attrs={'class':'fxl','autocomplete':'off','placeholder':_('Post a Job Url')}))
 
    class Meta:
        model = JobSettings
