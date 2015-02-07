from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()

from deal.models import DealCategory,Deal,GiftedAddress,Subscribe,Faqs,How,DealPayment
from business.models import Business

from common import captcha
from common.utils import get_global_settings
from locality.models import Locality
from django.utils.translation import ugettext as _
from django.conf import settings as mysettings
from django.contrib.admin.widgets import AdminDateWidget, AdminSplitDateTime
from django.utils.safestring import mark_safe


import datetime
from time import strptime


gift_choices = ( (True, 'Yes'),(False, 'No'))
valid_date_formats = ['%d/%m/%Y']  
class HorizRadioRenderer(forms.RadioSelect.renderer):
    """ this overrides widget method to put radio buttons horizontally
        instead of vertically.
    """
    def render(self):
            """Outputs radios"""
            radio_elements = u'\n'.join([u'%s\n' % w for w in self])
            radio_elements = radio_elements.replace('<input','<span class="cform-radio-container"><input').replace(' /> ','/><span class="cform-radio-element"></span></span>').replace('<label','<label class="pdr6"')
            return mark_safe(radio_elements) 

class DealForm(forms.ModelForm):
    
    title = forms.CharField(required=True,error_messages={'required': 'Please enter the title'},widget=forms.TextInput(attrs={'placeholder':_('Untitled Deal')}),max_length="110")
    category = forms.ModelChoiceField(required=True,error_messages={'required': _('Please select the category')},widget=forms.Select(attrs={'class':'select-menu fl','data-placeholder':_('Select a category')}),queryset=DealCategory.objects.order_by('name'), empty_label="")
    start_date = forms.DateField(required=True,input_formats=valid_date_formats, error_messages={'required': _('Please select the start date')},widget=forms.DateInput(format='%d/%m/%Y',attrs={'autocomplete':'off','placeholder':_('DD/MM/YY'),'style':'width:160px;'}))
    end_date = forms.DateField(required=True,input_formats=valid_date_formats, error_messages={'required': _('Please select the end date')},widget=forms.DateInput(format='%d/%m/%Y',attrs={'autocomplete':'off','placeholder':_('DD/MM/YY'),'style':'width:160px;'}))
    original_price = forms.CharField(required=True,error_messages={'required': _('Please enter the market price')},widget=forms.TextInput(attrs={'placeholder':_('Market Price'),'style':' margin-top:2px;','class':'fs'}),max_length="70")
    discount_price = forms.CharField(required=True,error_messages={'required': _('Please enter the deal/sale price')},widget=forms.TextInput(attrs={'placeholder':_('Deal/Sale Price'),'style':'margin-top:2px;','class':'fs'}),max_length="70")
    max_count = forms.IntegerField(required=True,error_messages={'invalid': _('Max coupon count is not valid'),'required': _('Please enter the maximum coupon count')},widget=forms.TextInput(attrs={'placeholder':_('Max no:'),'maxlength':'4','style':'margin-top:2px;','class':'fs'}))
    voucher_valid = forms.DateField(required=True,input_formats=valid_date_formats, error_messages={'required': 'Please select the voucher date'},widget=forms.DateInput(format='%d/%m/%Y',attrs={'autocomplete':'off','placeholder':_('DD/MM/YY'),'style':'margin-top:2px;','class':'fs'}))
    about = forms.CharField(required=True,error_messages={'required': _('Please enter the about')},widget=forms.Textarea(attrs={'rows':'8'}))
    fineprint = forms.CharField(required=False,error_messages={'required': _('Please enter the fine print details')},widget=forms.Textarea(attrs={'rows':'8'}))
    hihlights = forms.CharField(required=False,error_messages={'required': _('Please enter the hilights')},widget=forms.Textarea(attrs={'rows':'8'}))
    limit_per_customer = forms.IntegerField(required=True,error_messages={'invalid': _('Limit per customer is not valid'),'required': _('Please enter the limit per customer')},widget=forms.TextInput(attrs={'style':'margin-top:2px;','class':'fs','maxlength':'3'}))
    can_gifted = forms.ChoiceField(required=False,error_messages={'required': _('Please select can gifted')},widget=forms.RadioSelect(renderer=HorizRadioRenderer),initial='False',choices = gift_choices)
    address = forms.IntegerField(required=False,error_messages={'required': _('Deal address Required')})
    
    class Meta:
        model = Deal
        exclude = ('dealkey','featured','business','deal_by','address','most_viewed','created_on','modified_on','created_by','modified_by','is_active','status','slug','seo_title','seo_description')
    
    def clean_end_date(self):
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        if start_date > end_date:
            self._errors["end_date"] = self.error_class(["Deal start date shouldn't be greater than end date"])
            return end_date
        else:return end_date
        
    def clean_voucher_valid(self):
        voucher_valid = self.cleaned_data.get('voucher_valid')
        end_date = self.cleaned_data.get('end_date')
        if end_date:
            if end_date > voucher_valid:
                raise forms.ValidationError(_("Voucher valid date should be greater than end date"))
            else:
                return voucher_valid    

class DealSeoForm(forms.ModelForm):    
    #slug = forms.CharField(required=True, widget=forms.TextInput({'class':'default-url','title':_('Deal Slug'),'maxlength':'200','style':'width:160px;','onkeyUp':'string_to_slug(this.value)','autocomplete':'off'}), error_messages={'required': _('Please enter the slug')})
    seo_title = forms.CharField(required=True,max_length=200, error_messages={'required': _('Please enter the Title')},widget=forms.TextInput(attrs={'class':'fm','maxlength':'200','title':_('Meta Title'),'autocomplete':'off'}))
    seo_description = forms.CharField(required=True,max_length=400, error_messages={'required': _('Please enter Description')},widget=forms.Textarea(attrs={'class':'fxl','cols':30,'rows':4,'style':'max-height:75px;','title':_('Meta Description'),'onkeyUp':'txtarealimit(this,400);'}))
    
    def clean_seo_title(self):
        seo_title = self.cleaned_data.get("seo_title").strip()
        if len(seo_title) > 200:
            raise forms.ValidationError(_("Maximum length of meta-title field is 200 characters."))
        else:
            if seo_title: return seo_title
            else:return self.cleaned_data.get("name")

    def clean_seo_description(self):
        seo_description = self.cleaned_data.get("seo_description").strip()
        if len(seo_description) > 400:
            raise forms.ValidationError(_("Maximum length of meta-description field is 400 characters."))
        else:
            if seo_description: return seo_description
            else:return self.cleaned_data.get("name")
            
    class Deal:
        model = Deal
        fields=('seo_title','seo_description')

class DealFaqForm(forms.ModelForm):
    question = forms.CharField(required=True,error_messages={'required': _('Please enter the question')},widget=forms.TextInput(attrs={'class':'fm','placeholder':_('Frequently Asked Question')}),max_length="99")
    answer = forms.CharField(required=True,error_messages={'required': _('Please enter the answer')},widget=forms.Textarea(attrs={'rows':'8','class':'fm','style':'max-height:100px;'}))
    
    class Meta:
        model = Faqs
        fields=('question','answer')

class DealHowForm(forms.ModelForm):
    heading = forms.CharField(required=True,error_messages={'required': _('Please enter the title')},widget=forms.TextInput(attrs={'placeholder':_('Title'),'class':'fm'}),max_length="99")
    content = forms.CharField(required=True,error_messages={'required': _('Please enter the details')},widget=forms.Textarea(attrs={'rows':'8','class':'fm','style':'max-height:100px;'}))
    
    class Meta:
        model = How
        fields=('heading','content')        
    
    
class DealCategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        try:self._name = kwargs['instance'].name
        except:self._name= False
        super(DealCategoryForm, self).__init__(*args, **kwargs)
    name = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'fm','title':_('Category Name')}),error_messages={'required': _('Please enter the name')},max_length="150")
    
    def clean_name(self):
        name = self.cleaned_data.get("name").strip()
        if self._name:
            if str(self._name).lower() != str(name).lower():
                try:
                    flag=DealCategory.objects.filter(name__iexact=name)
                    if flag:raise forms.ValidationError(_("This category name is already added"))
                except DealCategory.DoesNotExist:pass
        else:
            try:
                flag=DealCategory.objects.filter(name__iexact=name)
                if flag:raise forms.ValidationError(_("This category name is already added."))
            except DealCategory.DoesNotExist:pass
        return name
    
         
    class Meta:
        model = DealCategory 
        exclude = ('slug','created_on','modified_on','created_by','modified_by')

class RedeemForm(forms.Form):
    voucher_key = forms.CharField(required=True, max_length="50", widget=forms.TextInput(attrs={'style':'width: 95%;','autocomplete':'off'}), error_messages={'required': _('Please enter the Voucher Key')})
    
    def clean_voucher_key(self):
        voucher_key = self.cleaned_data.get("voucher_key")
        today=datetime.datetime.now()
        try:
            dr = DealPayment.objects.get(dealkey = voucher_key)
        except:
            raise forms.ValidationError(_("Wrong voucher code! Please enter a valid code"))    
        if dr.status == 'D':
            raise forms.ValidationError(_("This voucher already redeemed !"))
        elif dr.status == 'B':
            raise forms.ValidationError(_("This voucher is blocked !"))
        elif dr.status == 'P':
            raise forms.ValidationError(_("Wrong voucher code! Please enter a valid code !"))
        elif dr.deal.voucher_valid <= today.date():
            raise forms.ValidationError(_("Sorry,This voucher is out of date !"))
        elif dr.status == 'S':
            return voucher_key 
        else:
            raise forms.ValidationError(_("Wrong voucher code! Please enter a valid code !"))
                
                        
class GiftedAddressForm(forms.ModelForm):
    g_name = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'textField normal'}),error_messages={'required': _('Please enter the name')})
    g_mobile = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'textField small'}),error_messages={'required': _('Please enter the mobile number')})
    g_email = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'textField normal'}),error_messages={'invalid': _('Please enter the valid email address'),'required': _('Please enter the email address')})
    g_message = forms.CharField(required=False,error_messages={'required': 'Please enter the message'},widget=forms.Textarea(attrs={'class':'textField long','style':'padding: 3px 1px;height:40px'}),max_length="70")
    class Meta:
        model = GiftedAddress 
        exclude = ('deal')

class DealAddressForm(forms.ModelForm):
    name = forms.CharField(required=True,max_length=100,widget=forms.TextInput(attrs={'class':'textField normal'}),error_messages={'required': _('Please enter the name')})
    mobile = forms.CharField(required=False,max_length=20,widget=forms.TextInput(attrs={'class':'textField small'}),error_messages={'required': _('Please enter the mobile number')})
    email = forms.EmailField(required=True,widget=forms.TextInput(attrs={'class':'textField normal'}),error_messages={'invalid': _('Please enter the valid email address'),'required': _('Please enter the email address')})
    address = forms.CharField(required=True,max_length=200,widget=forms.Textarea(attrs={'class':'textField normal'}),error_messages={'required': _('Please enter the Address')})
    
    class Meta:
        model = DealPayment 
        fields = ('name','mobile','email','address')

class UserDealAddressForm(forms.ModelForm):
    name = forms.CharField(required=True,max_length=100,widget=forms.TextInput(attrs={'class':'form-control input-xlarge'}),error_messages={'required': _('Please enter the name')})
    mobile = forms.CharField(required=False,max_length=20,widget=forms.TextInput(attrs={'class':'form-control input-xlarge'}),error_messages={'required': _('Please enter the mobile number')})
    email = forms.EmailField(required=True,widget=forms.TextInput(attrs={'class':'form-control input-xlarge'}),error_messages={'invalid': _('Please enter the valid email address'),'required': _('Please enter the email address')})
    address = forms.CharField(required=True,max_length=200,widget=forms.Textarea(attrs={'class':'form-control input-xlarge','rows':0, 'cols':0}),error_messages={'required': _('Please enter the Address')})
    
    class Meta:
        model = DealPayment 
        fields = ('name','mobile','email','address')
        
class ContactForm(forms.Form):
    name = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'input-xlarge'}),error_messages={'required': _('Please enter the name')},max_length="100")
    mobile = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'input-xlarge'}),error_messages={'required': _('Please enter the mobile number')})
    email = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'input-xlarge'}),error_messages={'invalid': _('Please enter the valid email address'),'required': _('Please enter the email address')},max_length="100")
    details = forms.CharField(required=True,widget=forms.Textarea(attrs={'class':'input-xlarge', 'rows':0, 'cols':0}), error_messages={'required': _('Please enter the details')})
