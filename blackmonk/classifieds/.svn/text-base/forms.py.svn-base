from django import forms
from classifieds.models import ClassifiedCategory,ATTRIBUTE_TYPE,ClassifiedAttribute,Classifieds,ClassifiedComment,ClassifiedPrice,OodleSettings
from common import captcha
from django.utils.translation import ugettext as _
from common.models import Address

attrs_dict = { 'class': 'required' }
attrs_text = {'class': 'TextField'}
ch_choices = [['S','I am offering'],['B','I want']]
Classified_Exposure=(('0','Standard'),('1','1X'),('2','5X'),('3','10X'),('4','15X'),('5','20X'),('6','25X'))
Classified_Pay_Opt=(('True','Paid'),('False','Free'),)
Classified_Contract_Period=(('month','Month'),('year','Year'),)
Classified_Features_Options=(('Y','Yes'),('N','No'),)
Classified_Socialmedia_Options=(('F','Facebook'),('T','Twitter'),('B','FB + Twitter'),('N','No'),)


def validate_blank_space(data,field):
    data = data.strip()
    if data == '':
        error='Blank space is not allowed for ' +field+ ' field'
        raise forms.ValidationError(error)
    else:
        return data


class ClassifiedCategoryForm(forms.ModelForm):
    name = forms.CharField(required=True,max_length=60, error_messages={'required': _('Please enter the name')},widget=forms.TextInput({'class':'fm','maxlength':'120','onkeyUp':'string_to_slug(this.value)','title':_('Category Name'),'autocomplete':'off'}))
    parent = forms.ModelChoiceField(required=False, widget=forms.Select(attrs={'class':'select-menu parent-category','style':'width:200px;','onchange':'validate_custom();'}),queryset=ClassifiedCategory.objects.filter(parent=None).order_by('name'), empty_label="Select Type", error_messages={'required': _('Please select the Parent Category.')})
    is_rent = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'fm','style':'margin-top:7px !important;'}))
    slug = forms.CharField(required=False, widget=forms.TextInput({'class':'default-url','style':'width:132px;','title':_('Category Slug'),'maxlength':'200','onkeyUp':'string_to_slug(this.value)','autocomplete':'off'}), error_messages={'required': _('Please enter the slug')})
    seo_title = forms.CharField(required=False,max_length=70, error_messages={'required': _('Please enter the Title')},widget=forms.TextInput(attrs={'class':'fm','maxlength':'200','title':_('Meta Title'),'autocomplete':'off'}))
    seo_description = forms.CharField(required=False,max_length=160, error_messages={'required': _('Please enter Description')},widget=forms.Textarea(attrs={'class':'fm','cols':30,'rows':5,'style':'height:70px;','title':_('Meta Description'),'onkeyUp':'txtarealimit(this,400);'}))
    sp_price = forms.FloatField(required=True, widget=forms.TextInput(attrs={'class':'textField', 'style':'width:40px; height:21px;'}), error_messages={'required': 'Price field Shouldn\'t be empty.', 'invalid': 'Price field should be a number'})

    
    def clean_name(self):
        name = self.cleaned_data.get("name").strip()
        queryset = ClassifiedCategory.objects.filter(name=name)
        if self.data.get('parent'):
            queryset = queryset.filter(parent__id=self.data.get('parent'))
        if self.instance:
            queryset = queryset.exclude(id=self.instance.id)
        if queryset.exists():
            if not self.data.get('parent'): raise forms.ValidationError(_("Parent Category with same name already exists."))
            else: raise forms.ValidationError(_("Sub Category with same name already exists."))
        else:
            return name
    
    def clean_slug(self):
        slug = self.cleaned_data.get("slug")
        if slug:return slug
        else:
            name = self.cleaned_data.get("name")
            return name
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
    
    def clean_sp_price(self):
        sp_price = self.cleaned_data.get("sp_price")
        if sp_price == 0.0:
            raise forms.ValidationError(_("Please enter sp price grater than zero(0)"))
        else:
            return self.cleaned_data.get("sp_price")

    class Meta:
        model = ClassifiedCategory

class ClassifiedCategorySeoForm(forms.ModelForm):
    slug = forms.CharField(required=True, widget=forms.TextInput({'class':'default-url','style':'width:132px;','title':_('Category Slug'),'maxlength':'200','onkeyUp':'string_to_slug(this.value)','autocomplete':'off'}), error_messages={'required': _('Please enter the slug')})
    seo_title = forms.CharField(required=True,max_length=200, error_messages={'required': _('Please enter the Title')},widget=forms.TextInput(attrs={'class':'fm','maxlength':'200','title':_('Meta Title'),'autocomplete':'off'}))
    seo_description = forms.CharField(required=True,max_length=400, error_messages={'required': _('Please enter Description')},widget=forms.Textarea(attrs={'class':'fm','cols':30,'rows':5,'style':'height:70px;','title':_('Meta Description'),'onkeyUp':'txtarealimit(this,400);'}))

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
        model = ClassifiedCategory
        fields=('slug','seo_title','seo_description')

class ClassifiedAttributeForm(forms.ModelForm):
    name = forms.CharField(required=True,max_length=70 , widget=forms.TextInput(attrs={'class':'tttxt','style':'width:150px;','title':_('Attribute Name')}),error_messages={'required': _('Attribute name required')})
    type = forms.ChoiceField(required=True, widget=forms.Select(attrs={'class':'select-menu parent-category','style':'width:153px;'}), choices=ATTRIBUTE_TYPE, error_messages={'required': _('Please select the type')})

    class Meta:
        model = ClassifiedAttribute
        fields=('name','type')

class ClassifiedUserForm(forms.ModelForm):
    title        =  forms.CharField(required=True,max_length=100,error_messages={'required':_('Please enter the  title')},widget = forms.TextInput(attrs={'class': 'iSp8','placeholder':_('What are you listing?'),'title':_('Classified Title')}))
    classified_price   =  forms.FloatField(required=False,error_messages={'required':_('Please enter the classified price.')}, widget = forms.TextInput(attrs={'class': 'iSp8','class':'fl'}))
    description  =  forms.CharField(required=True,widget=forms.Textarea(attrs = {'class': 'iSp8','rows':'6','placeholder':_('Classified Description'),'title':_('Classified Description')}),error_messages={'required':_('Please enter the  description')})
    action       =  forms.TypedChoiceField(widget=forms.RadioSelect,required=False,choices = ch_choices, error_messages = {'required':_('Please Select Tab Option weather you need to sell or buy.')})
    listing_start_date=forms.DateField(required=False,error_messages={'required':_('Please enter vaild Listing Start Date.')},widget=forms.DateInput(attrs={'class':'tttxt-n','title':_('Listing Start Date'),'style':'width:100px !important;margin-top:10px;'}))
    listing_end_date=forms.DateField(required=False,error_messages={'required':_('Please enter vaild Listing End Date.')},widget=forms.DateInput(attrs={'class':'tttxt-n','title':_('Listing End Date'),'style':'width:100px !important;margin-top:10px;'}))

    class Meta:
        model = Classifieds
        fields = ('title','description','action','classified_price','listing_start_date','listing_end_date')


class AddressForm(forms.ModelForm):#globalsettings.city
    address1 = forms.CharField(required=True,max_length=70,widget=forms.TextInput(attrs={'class':'iSp8 fl','title':_('Enter Address'),'placeholder':_('Address')}),error_messages={'required': 'Please enter the address'})
    address2 = forms.CharField(required=False,max_length=70,widget=forms.TextInput(attrs={ 'class': 'iSp8 fl','title':_('Enter Street'),'placeholder':_('Address1/Street') }),error_messages={'required': 'Please enter the street name'})
    zip = forms.CharField(required=True,max_length=16,widget=forms.TextInput(attrs={ 'class': 'iSp8 fl','title':_('Enter Zip/PostalCode'),'placeholder':_('Zip/PostalCode')}),error_messages={'required': 'Please enter the Zipcode'})
    city = forms.CharField(required=False,max_length=70,widget=forms.TextInput(attrs={ 'class': 'iSp8 fl','title':_('Enter name of City/Town'),'placeholder':_('City/Town') }),error_messages={'required': 'Please enter City'})
    telephone1 = forms.CharField(required=False,max_length=15,widget=forms.TextInput(attrs={ 'title':_('Enter telephone number. e.g., 555-555-5555'),'placeholder':_('Example: 555-555-5555'),'style':'margin-top:2px;' }),error_messages={'required': 'Please enter the phone number'})
    fax = forms.CharField(required=False,max_length=15,widget=forms.TextInput(attrs={'class': 'iSp8 fl','title':_('Enter fax number. e.g., 555-5555'),'placeholder':_('Example: 555-5555'),'style':'margin-top:2px;' }),error_messages={'required': 'Please enter the phone number'})
    mobile = forms.CharField(required=False,max_length=15,widget=forms.TextInput(attrs={ 'title':_('Enter mobile number. e.g., 555-555-5555'),'placeholder':_('Example: 555-555-5555'),'style':'margin-top:2px;' }),error_messages={'required': 'Please enter the mobile number'})
    email = forms.EmailField(required=False,max_length=60,widget=forms.TextInput(attrs={ 'class': 'iSp8 fl','title':_('Enter email address. e.g., myname@example.com'),'placeholder':_('Example: myname@example.com') }),error_messages={'required': 'Please enter the valid email address'})
    website = forms.CharField(required=False,max_length=150,widget=forms.TextInput(attrs={ 'class': 'iSp8 fl','title':_('Enter website url. e.g., http://www.example.com'),'placeholder':_('Example: http://www.example.com') }),error_messages={'required': 'Please enter the url'})

    class Meta:
        model = Address
        exclude = ('description','address_type','venue','lat','lon','zoom','status','telephone2','is_active','created_on','created_by','modified_on','modified_by','seo_title','seo_description')

    def clean_city(self):
        city = self.cleaned_data.get("city").strip()
        if len(city) > 70:
            raise forms.ValidationError(_("Maximum length of city field is 70 characters."))
        else:
            return self.cleaned_data.get("city")

class ClassifiedForm(forms.ModelForm):
    title        =  forms.CharField(required=True,max_length=100,error_messages={'required':_('Please enter the  title')},widget = forms.TextInput(attrs={'placeholder':_('What are you listing?'),'title':_('Classified Title')}))
    classified_price   =  forms.FloatField(required=False,error_messages={'required':_('Please enter the classified price.')}, widget = forms.TextInput(attrs={'class':'fl'}))
    description  =  forms.CharField(required=True,widget=forms.Textarea(attrs = {'rows':'6','placeholder':_('Classified Description'),'title':_('Classified Description')}),error_messages={'required':_('Please enter the  description')})
    action       =  forms.TypedChoiceField(widget=forms.RadioSelect,required=False,choices = ch_choices, error_messages = {'required':_('Please Select Tab Option weather you need to sell or buy.')})
    listing_start_date=forms.DateField(required=False,error_messages={'required':_('Please enter vaild Listing Start Date.')},widget=forms.DateInput(attrs={'placeholder':_('2011-02-02'),'class':'tttxt-n','title':_('Listing Start Date'),'style':'width:100px !important;margin-top:10px;'}))
    listing_end_date=forms.DateField(required=False,error_messages={'required':_('Please enter vaild Listing End Date.')},widget=forms.DateInput(attrs={'placeholder':_('2011-04-02'),'class':'tttxt-n','title':_('Listing End Date'),'style':'width:100px !important;margin-top:10px;'}))

    class Meta:
        model = Classifieds
        fields = ('title','description','action','classified_price','listing_start_date','listing_end_date')

class EditClassifiedForm(forms.ModelForm):
    title        =  forms.CharField(required=True,max_length=100,error_messages={'required':_('Please enter the  title')},widget = forms.TextInput(attrs={'placeholder':_('What are you listing?'),'title':_('Classified Title')}))
    classified_price   =  forms.FloatField(required=False,error_messages={'required':_('Please enter the classified price.')}, widget = forms.TextInput(attrs={'class':'fl'}))
    description  =  forms.CharField(required=True,widget=forms.Textarea(attrs = {'rows':'6','placeholder':_('Classified Description'),'title':_('Classified Description')}),error_messages={'required':_('Please enter the  description')})
    action       =  forms.TypedChoiceField(widget=forms.RadioSelect,required=False,choices = ch_choices, error_messages = {'required':_('Please Select Tab Option weather you need to sell or buy.')})

    class Meta:
        model = Classifieds
        fields = ('title','description','action','classified_price')


class ClassifiedSeoForm(forms.ModelForm):
    #slug = forms.CharField(required=True, widget=forms.TextInput({'class':'default-url','style':'width:180px;','title':_('Category Slug'),'maxlength':'200','onkeyUp':'string_to_slug(this.value)','autocomplete':'off'}), error_messages={'required': _('Please enter the slug')})
    seo_title = forms.CharField(required=True,max_length=70, error_messages={'required': _('Please enter the Title')},widget=forms.TextInput(attrs={'class':'fm','maxlength':70,'title':_('Meta Title'),'autocomplete':'off'}))
    seo_description = forms.CharField(required=True,max_length=160, error_messages={'required': _('Please enter Description')},widget=forms.Textarea(attrs={'class':'fxl','maxlength':160,'cols':30,'rows':4,'style':'height:70px;','title':_('Meta Description'),'onkeyUp':'txtarealimit(this,400);'}))

    def clean_seo_title(self):
        seo_title = self.cleaned_data.get("seo_title").strip()
        if len(seo_title) > 70:
            raise forms.ValidationError(_("Maximum length of meta-title field is 70 characters."))
        else:
            if seo_title: return seo_title
            else:return self.cleaned_data.get("name")
    def clean_seo_description(self):
        seo_description = self.cleaned_data.get("seo_description").strip()
        if len(seo_description) > 160:
            raise forms.ValidationError(_("Maximum length of meta-description field is 160 characters."))
        else:
            if seo_description: return seo_description
            else:return self.cleaned_data.get("name")

    class Meta:
        model = Classifieds
        fields=('seo_title','seo_description')

class UserClassifiedSeoForm(forms.ModelForm):
    #slug = forms.CharField(required=True, widget=forms.TextInput({'class':'default-url','style':'width:180px;','title':_('Category Slug'),'maxlength':'200','onkeyUp':'string_to_slug(this.value)','autocomplete':'off'}), error_messages={'required': _('Please enter the slug')})
    seo_title = forms.CharField(required=True,max_length=70, error_messages={'required': _('Please enter the Title')},widget=forms.TextInput(attrs={'class':'iSp8','maxlength':70,'title':_('Meta Title'),'autocomplete':'off'}))
    seo_description = forms.CharField(required=True,max_length=160, error_messages={'required': _('Please enter Description')},widget=forms.Textarea(attrs={'class':'iSp8','maxlength':160,'cols':30,'rows':4,'style':'height:70px;','title':_('Meta Description'),'onkeyUp':'txtarealimit(this,400);'}))

    def clean_seo_title(self):
        seo_title = self.cleaned_data.get("seo_title").strip()
        if len(seo_title) > 70:
            raise forms.ValidationError(_("Maximum length of meta-title field is 70 characters."))
        else:
            if seo_title: return seo_title
            else:return self.cleaned_data.get("name")
    def clean_seo_description(self):
        seo_description = self.cleaned_data.get("seo_description").strip()
        if len(seo_description) > 160:
            raise forms.ValidationError(_("Maximum length of meta-description field is 160 characters."))
        else:
            if seo_description: return seo_description
            else:return self.cleaned_data.get("name")

    class Meta:
        model = Classifieds
        fields=('seo_title','seo_description')

class ClassifiedPricingForm(forms.ModelForm):
    level = forms.CharField(required=False, max_length="10", widget=forms.TextInput(attrs={'size':'30', 'class':'input_text'}), error_messages={'required': 'Title field Shouldn\'t be empty.'})
    level_visibility = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'onclick':'change_visiblity($(this))'}), error_messages={'required': 'Label content field Shouldn\'t be empty.'})
    level_label = forms.CharField(required=True, max_length=50, widget=forms.TextInput({'title':_('Label'),'readonly':'true',  'maxlength':'50', 'style':'height:21px;', 'autocomplete':'off'}), error_messages={'required': _('Label field Shouldn\'t be empty.')})
    exposure = forms.ChoiceField(required=True, choices=Classified_Exposure, widget=forms.Select(attrs={'class':'select-menu', 'style':'width:88px;'}), error_messages={'required': 'Exposure field Shouldn\'t be empty.'})
    images = forms.ChoiceField(required=True, choices=Classified_Features_Options, widget=forms.Select(attrs={'class':'select-menu', 'style':'width:70px;'}), error_messages={'required': 'Images field Shouldn\'t be empty.'})
    comments = forms.ChoiceField(required=True, choices=Classified_Features_Options, widget=forms.Select(attrs={'class':'select-menu', 'style':'width:70px;'}), error_messages={'required': 'Comments field Shouldn\'t be empty.'})
    share_buttons = forms.ChoiceField(required=True, choices=Classified_Features_Options, widget=forms.Select(attrs={'class':'select-menu', 'style':'width:70px;'}), error_messages={'required': 'Share Buttons field Shouldn\'t be empty.'})
    newsletter = forms.ChoiceField(required=True, choices=Classified_Features_Options, widget=forms.Select(attrs={'class':'select-menu', 'style':'width:70px;'}), error_messages={'required': 'Newsletter field Shouldn\'t be empty.'})
    social_media = forms.ChoiceField(required=True, choices=Classified_Features_Options, widget=forms.Select(attrs={'class':'select-menu', 'style':'width:70px;'}), error_messages={'required': 'Social Media field Shouldn\'t be empty.'})
    contract_period = forms.IntegerField(required=True,widget=forms.TextInput(attrs={'class':'textField','style':'width:20px; height:21px;'}), error_messages={'required': 'Listing duration field Shouldn\'t be empty.','invalid': 'Listing duration field should be a number'})
    price = forms.FloatField(required=True, widget=forms.TextInput(attrs={'class':'textField', 'style':'width:40px; height:21px;'}), error_messages={'required': 'Price field Shouldn\'t be empty.', 'invalid': 'Price field should be a number'})

    class Meta:
        model = ClassifiedPrice
        exclude = ('level','sms','contract_period_option')

    def clean_level_label(self):
        return validate_blank_space(self.cleaned_data.get("level_label"),'Label')
    def clean_level_content(self):
        return validate_blank_space(self.cleaned_data.get("level_content"),'Label Content')
    #def clean_price(self):
        #return validate_blank_space(self.cleaned_data.get("price"),'Price')

class CommentsForm(forms.ModelForm):
    title = forms.CharField(required=False, max_length="100", widget=forms.TextInput(attrs={'size':'30','class':'input_text'}), error_messages={'required': 'Title field Shouldn\'t be empty.'})
    name = forms.CharField(required=True, max_length="75", widget=forms.TextInput(attrs={'size':'30','class':'input_text'}), error_messages={'required': 'Name field Shouldn\'t be empty.'})
    email=  forms.EmailField(required=True, max_length="150", widget=forms.TextInput(attrs={'size':'30','class':'input_text'}), error_messages={'required': 'Email field Shouldn\'t be empty.'})
    comment = forms.CharField(required=True, max_length="350", widget=forms.Textarea(attrs={'class':'medium','rows':'7','cols':'30'}), error_messages={'required': 'Comment field Shouldn\'t be empty.'})
    hashkey = forms.CharField(required=True, error_messages={'required': 'Please reload the page.'})
    hashvalue = forms.CharField(required=True, max_length="3", widget=forms.TextInput(attrs={'size':'10', 'class':'input_text captcha_field'}), error_messages={'required': 'Image field Shouldn\'t be empty.'})
    def clean_hashvalue(self):
        hashkey = self.cleaned_data.get("hashkey")
        hashvalue = self.cleaned_data.get("hashvalue")
        if not captcha.checkCaptcha(hashkey,hashvalue):
            raise forms.ValidationError("Wrong Image key! Please re-enter the text in the image.")
        else:
            return hashkey
    class Meta:
        model = ClassifiedComment
        fields = ['name','email','comment']

class OodleSettingsForm(forms.ModelForm):
    api_key     = forms.CharField(required=True,max_length=20,widget=forms.TextInput(attrs={'maxlength':'20'}),error_messages={'required': _('Please enter the Oodel API Key.')})
    radius      = forms.IntegerField(required=True,widget=forms.TextInput(attrs={'maxlength':'3'}),error_messages={'required': _('Please enter the radius.')})
    location    = forms.CharField(required=False,max_length=50,widget=forms.TextInput(attrs={'maxlength':'50'}),error_messages={'required': _('Please enter the Location.')})
    region      = forms.CharField(required=False,max_length=20,widget=forms.TextInput(attrs={'maxlength':'20'}),error_messages={'required': _('Please enter the Regoin.')})
    class Meta:
        model=OodleSettings


