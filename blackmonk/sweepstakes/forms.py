import datetime

from django import forms
from django.utils.translation import ugettext as _

from common.models import Pages
from sweepstakes.models import Sweepstakes,SweepstakesOffers,SweepstakesImages,SweepstakesQandA,SweepstakesParticipant

class SweepstakesParticipantForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        try:user = kwargs.pop('user')
        except:user=None
        super(SweepstakesParticipantForm, self).__init__(*args, **kwargs)
        try:
            self.fields['first_name'].initial = user.first_name()
            self.fields['last_name'].initial = user.last_name()
        except:pass
    first_name= forms.CharField(required=True,max_length=30, error_messages={'required': 'Please enter the first name'},widget=forms.TextInput(attrs={'placeholder':_('First Name'),'autocomplete':'off'}))
    last_name= forms.CharField(required=True,max_length=30, error_messages={'required': 'Please enter the last name'},widget=forms.TextInput(attrs={'placeholder':_('Last Name'),'autocomplete':'off'}))
    address = forms.CharField(required=False,max_length=250, error_messages={'required': _('Please enter Address')},widget=forms.Textarea(attrs={'class':'fm','cols':30,'rows':5,'style':'height:70px;','title':_('Address'),'onkeyUp':'txtarealimit(this,250);'}))
    zip= forms.CharField(required=True,max_length=15, error_messages={'required': 'Please enter the Pin/Zip Code'},widget=forms.TextInput(attrs={'placeholder':_('Zip/Pin Code'),'autocomplete':'off'}))
    phone= forms.CharField(required=True,max_length=15, error_messages={'required': 'Please enter the phone number'},widget=forms.TextInput(attrs={'placeholder':_('Phone Number'),'autocomplete':'off'}))
    city= forms.CharField(required=True,max_length=30, error_messages={'required': 'Please enter the city name'},widget=forms.TextInput(attrs={'placeholder':_('City'),'autocomplete':'off'}))
     
    class Meta:
        model = SweepstakesParticipant
        exclude = ('sweepstakes','participant','status','reg_point','fb_point','friend_point','total','comments')
  

    
class SweepstakesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        try:self._name = kwargs['instance'].name
        except:self._name= False
        super(SweepstakesForm, self).__init__(*args, **kwargs)
        self.fields['total_winners'].initial = 1
        self.fields['start_date'].initial = datetime.date.today()
        self.fields['static_page'].widget = forms.Select(attrs={'class':'select-menu','style':'width:180px;'})
        self.fields['static_page'].queryset = Pages.objects.filter(is_active=True)
        self.fields['static_page'].required = False
        self.fields['static_page'].empty_label = _("-- Select Terms Page --")
        self.fields['static_page'].error_messages = _("Please select Static Page.")
       
        
    title = forms.CharField(required=True,max_length=70, error_messages={'required': 'Please enter the sweepstakes title'},widget=forms.TextInput(attrs={'placeholder':_('Untitled Business'),'autocomplete':'off','onkeyup':'string_to_slug(this.value)'}))
    slug = forms.CharField(required=False,max_length=70, error_messages={'required': 'Please enter the sweepstakes slug'},widget=forms.TextInput(attrs={'class':'default-url tttxt-w','style':'width:152px;','title':_('Business Slug'),'autocomplete':'off','style':'padding: 0pt; width: 237px;','onkeyup':'string_to_slug(this.value)'}))
    description = forms.CharField(required=True,max_length=5000,widget=forms.Textarea(attrs={'class':'textField long'}),error_messages={'required': 'Please enter the description'})
    start_date=forms.DateField(required=False,error_messages={'required':_('Please enter vaild Listing Start Date.')},widget=forms.DateInput(attrs={'placeholder':_('2011-02-02'),'readonly':'true','class':'tttxt-n','title':_('Listing Start Date'),'style':'width:75px !important;'}))
    end_date=forms.DateField(required=True,error_messages={'required':_('Please enter vaild Listing End Date.')},widget=forms.DateInput(attrs={'placeholder':_('2011-04-02'),'readonly':'true','class':'tttxt-n','title':_('Listing End Date'),'style':'width:75px !important;'}))
    total_winners = forms.CharField(required=True,max_length=3, error_messages={'required': 'Please enter the number of winners'},widget=forms.TextInput({'autocomplete':'off','style':'width:35px;heigth:25px;','class':'tttxt-w','title':_('Specify total number of winners')}))
    seo_title = forms.CharField(required=False,max_length=200, error_messages={'required': _('Please enter the Title')},widget=forms.TextInput(attrs={'class':'fm','maxlength':'200','title':_('Meta Title'),'autocomplete':'off'}))
    seo_description = forms.CharField(required=False,max_length=400, error_messages={'required': _('Please enter Description')},widget=forms.Textarea(attrs={'class':'fm','cols':30,'rows':5,'style':'height:70px;','title':_('Meta Description'),'onkeyUp':'txtarealimit(this,400);'}))
    duration = forms.CharField(required=True,error_messages={'required': 'Please select duration'},widget=forms.Select())
    image = forms.CharField(required=True,error_messages={'required': 'Please upload a image'},widget=forms.HiddenInput())
    
    def clean_seo_title(self):
        seo_title = self.cleaned_data.get("seo_title").strip()
        if len(seo_title) > 200:
            raise forms.ValidationError(_("Maximum length of meta-title field is 200 characters."))
        else:
            if seo_title: return seo_title
            else:return self.cleaned_data.get("title")
    def clean_seo_description(self):
        seo_description = self.cleaned_data.get("seo_description").strip()
        if len(seo_description) > 400:
            raise forms.ValidationError(_("Maximum length of meta-description field is 400 characters."))
        else:
            if seo_description: return seo_description
            else:return self.cleaned_data.get("title")
    def clean_image(self):
        image_id = self.cleaned_data.get("image").strip()
        try:
            image=SweepstakesImages.objects.get(id=image_id)
            return image
        except:raise forms.ValidationError(_("Please Upload a image."))
            
    class Meta:
        model = Sweepstakes
        exclude=('winner','sweepstakes_id','created_by','modified_by','status','contest_id','select_winners_on','current_end_date','settings','reg_point','fb_point', 'friend_point','comments','advice_e','discussions_e')
        
class SweepstakesSeoForm(forms.ModelForm):
    seo_title = forms.CharField(required=True,max_length=200,widget=forms.TextInput(attrs={'class':'fm','maxlength':'200','title':_('Meta Title'),'autocomplete':'off'}), error_messages={'required': _('Please enter the Meta Title')})
    seo_description = forms.CharField(required=True,max_length=400,widget=forms.Textarea(attrs={'class':'fxl','cols':30,'rows':4,'style':'height:70px;','title':_('Meta Description'),'onkeyUp':'txtarealimit(this,400);'}), error_messages={'required': _('Please enter the Meta Keyword')})
    
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
            
    class Meta:
        model = Sweepstakes
        fields=('seo_title','seo_description')
        
class SweepstakesOffersFrom(forms.ModelForm):
    title = forms.CharField(required=True,max_length="100",widget=forms.TextInput({'class':'tttxt-w','title':_('Offer Title'),'style':'width:310px;','placeholder':_('Offer Title'),'maxlength':'100','autocomplete':'off'}), error_messages={'required': _('Please enter the Offer Title')})
    url = forms.CharField(required=False,max_length=150, error_messages={'required': 'Please enter the Offer URL'},widget=forms.TextInput(attrs={'onfocus':'showhttp()','onblur':'hidehttp()','title':'Offer URL','placeholder':'http://example.com/offers','autocomplete':'off','style':'width:329px;'}))
    description = forms.CharField(required=False,max_length="1000",widget=forms.Textarea({'class':'tttxt-w','title':_('Description'),'placeholder':_('Description'),'maxlength':'1000','autocomplete':'off'}), error_messages={'required': _('Please enter the Description')})
    
    def clean_description(self):
        description = self.cleaned_data.get("description").strip()
        if len(description) > 1000:
            raise forms.ValidationError(_("Please enter the description with in 1000 characters."))
        else:return description
        
    class Meta:
        model=SweepstakesOffers
        exclude=('image','sweepstakes')
     
class SweepstakesQandAForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        try:self._name = kwargs['instance'].name
        except:self._name= False
        super(SweepstakesQandAForm, self).__init__(*args, **kwargs)
        self.fields['position'].initial = 1
        
    title = forms.CharField(required=True,max_length=150, error_messages={'required': 'Please enter the Question'},widget=forms.TextInput(attrs={'placeholder':_('Question'),'class':'fl','autocomplete':'off'}))
    description = forms.CharField(required=False,max_length=5000,widget=forms.Textarea(attrs={'class':'textField long'}),error_messages={'required': 'Please enter the answer'})
    position = forms.IntegerField(required=True,widget=forms.TextInput(attrs={'size':'3',"style":"height: 22px;",'class':'tttxt-n numbersOnly'}),error_messages={'required': _('Please enter postion.')})
    class Meta:
        model = SweepstakesQandA
        fields=('title','description','position')

