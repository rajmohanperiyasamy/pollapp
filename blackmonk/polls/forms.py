from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext as _

from polls.models import Poll 
ch_options = (
    ('True', 'Single-answer question'),
    ('False', 'Multiple-answer question')
)
class PollsForm(ModelForm):
    title = forms.CharField(required=True,max_length=200, widget=forms.TextInput({'class':'tttxt','maxlength':'150','autocomplete':'off'}), error_messages={'required': 'Please enter the polls name'})
    expiry_date = forms.DateField(required=True,input_formats=['%d/%m/%Y'], widget=forms.DateInput(format='%d/%m/%Y',attrs={'placeholder':_('Expires on'),'class':'fxs','style':'margin-right:7px;','autocomplete':'off','readonly':'readonly'}), error_messages={'required': _('Expiry Date Required')})
    is_single = forms.TypedChoiceField(widget=forms.RadioSelect(attrs={'class':'validate[required]'}),required=True,initial='True',choices = ch_options, error_messages = {'required':'Please Select the options.'})
    
    class Meta:
        model = Poll
        fields  = ('title','expiry_date','is_single')