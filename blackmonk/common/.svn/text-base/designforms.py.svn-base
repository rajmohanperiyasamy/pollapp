import urllib

from django import forms
from django.conf import settings 
from django.utils.translation import ugettext as _

from common.models import AvailableModules
from common.utils import get_global_settings
        
class UpdateMenuForm(forms.ModelForm):
    name = forms.CharField(required=True, max_length=200, widget=forms.TextInput({'placeholder':'Article', 'title':_('Menu Name'),  'maxlength':'400', 'autocomplete':'off'}), error_messages={'required': _('Please enter the menu name')})
    base_url = forms.CharField(required=True, max_length=200, widget=forms.TextInput({'placeholder':'/articles/', 'title':_('Menu URL'),  'maxlength':'400', 'autocomplete':'off'}), error_messages={'required': _('Please enter the menu URL')})
    #parent = forms.ModelChoiceField(required=False, queryset= AvailableModules.objects.filter(parent=None).order_by('name'), widget=forms.Select(attrs={'class':'lb_select-menu', 'style':'width:116px', 'title':_('Main Menu'), 'data-placeholder':_('Select Main Menu'), 'autocomplete':'off'}),empty_label="Select Main Menu" ,error_messages={'required': _('Select Main Menu')})
    
    class Meta:
        model=AvailableModules  
        fields=('name','base_url')
    
       
#     def clean_name(self):
#         name = self.cleaned_data.get("name")
#         if self.instance.id:
#             if AvailableModules.objects.filter(name__iexact=name).exclude(id=self.instance.id).count()!=0:
#                 raise forms.ValidationError(_("Menu with this name already exists."))
#             else:return name   
#         else:
#             if AvailableModules.objects.filter(name__iexact=name).count()!=0:
#                 raise forms.ValidationError(_("Menu with this name already exists."))
#             else:return name  
            
    def clean_base_url(self): 
        base_url = self.cleaned_data.get("base_url")
        globalsettings=get_global_settings()
        url=globalsettings.website_url+base_url
        invalid=cinvalid=error=False
        try:
            flag=urllib.urlopen(url).code
            if flag == 404:invalid=True
            else:invalid=False
        except:error=True
        if error or invalid:
            try:
                flag1=urllib.urlopen(base_url).code
                if flag1 == 404:cinvalid=True
                else:cinvalid=False;error=False
            except:error=True   
        if cinvalid and invalid:raise forms.ValidationError(_("Url specified does not exist."))
        elif error:raise forms.ValidationError(_("Url specified is invalid."))
        else:return base_url
            

