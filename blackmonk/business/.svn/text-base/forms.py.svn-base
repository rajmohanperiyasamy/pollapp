from django import forms
from django.utils.translation import ugettext as _

from business.models import display_position,BusinessCategory,Attributes,attributeType,AttributeGroup,Tag,Business,ContactDetails,BusinessClaimSettings
from business.models import BusinessPrice,BusinessProducts,BusinessCoupons,WorkingHours,PaymentOptions,COUPON_OFFER_TYPE
from locality.models import Locality
from common.models import ModuleNames,Address
from common.form_utils import HorizCheckboxSelectMultiple,HorizRadioRenderer,HorizDivCheckboxSelectMultiple
#from captcha.fields import ReCaptchaField

class AttributesForm(forms.ModelForm):#ATTRIBUTE GROUP FORM
    def __init__(self, *args, **kwargs):
        try:self._name = kwargs['instance'].name
        except:self._name= False
        super(AttributesForm, self).__init__(*args, **kwargs)
        self.fields['order_by'].initial = 1
    name = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'tttxt','title':_('Attribute Group Name'),'autocomplete':'off','style':'width:180px;'}),error_messages={'required': _('Please enter the name')})
    display_position = forms.CharField(required=False,max_length=1,widget=forms.Select(attrs={'class':'select-menu','title':_('Attribute Display Position in Detail Page'),'style':'width:183px;'},choices=display_position),error_messages={'required': _('Please select Attribute style')})
    order_by = forms.IntegerField(required=True,widget=forms.TextInput(attrs={'class':'tttxt','title':_('Attribute Ordering Position in Detail Page'),'style':'width:20px;'}),error_messages={'required': _('Please select Attribute Order Position')})

    def clean_name(self):
        name = self.cleaned_data.get("name").strip()
        if self._name:
            if str(self._name).lower() != str(name).lower():
                try:
                    flag=AttributeGroup.objects.filter(name__iexact=name)
                    if flag:raise forms.ValidationError(_("This Attribute Group Name is already added."))
                except AttributeGroup.DoesNotExist:pass
        else:
            try:
                flag=AttributeGroup.objects.filter(name__iexact=name)
                if flag:raise forms.ValidationError(_("This Attribute Group Name is already added."))
            except AttributeGroup.DoesNotExist:pass
        return name.strip()

    class Meta:
        model = AttributeGroup

class AttributeKeyForm(forms.ModelForm):#ATTRIBUTE FORM
    name = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'tttxt','title':_('Attribute Name'),'autocomplete':'off','style':'width:150px;'}),error_messages={'required': _('Please enter the name')})
    type = forms.CharField(required=True,widget=forms.Select(attrs={'class':'select-menu','style':'width:153px;','title':_('Attribute Type')},choices=attributeType), error_messages={'required': _('Please select the type')})


    class Meta:
        model = Attributes
        exclude = ('attribute_group','staff_created','category')


class CategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        try:id = kwargs.pop('id')
        except:id=None
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['parent_cat'].widget = forms.Select(attrs={'class':'select-menu parent-category','style':'width:180px;','onchange':'validate_custom();'})
        self.fields['parent_cat'].queryset = BusinessCategory.objects.filter(parent_cat=None).exclude(id=id).exclude(name='Uncategorized')
        self.fields['parent_cat'].required = False
        self.fields['parent_cat'].empty_label = _("-- Select Parent Category --")
        self.fields['parent_cat'].error_messages = _("Please select category.")

    name = forms.CharField(required=True,max_length=120, error_messages={'required': _('Please enter the name')},widget=forms.TextInput({'class':'fm','maxlength':'120','onkeyUp':'string_to_slug(this.value)','title':_('Category Name'),'autocomplete':'off'}))
    slug = forms.CharField(required=False,max_length=150, widget=forms.TextInput({'class':'default-url','style':'width:139px;','title':_('Category Slug'),'maxlength':'200','onkeyUp':'string_to_slug(this.value)','autocomplete':'off'}), error_messages={'required': _('Please enter the slug')})
    seo_title = forms.CharField(required=False,max_length=70, error_messages={'required': _('Please enter the Title')},widget=forms.TextInput(attrs={'class':'fm','maxlength':'200','title':_('Meta Title'),'autocomplete':'off'}))
    seo_description = forms.CharField(required=False,max_length=160, error_messages={'required': _('Please enter Description')},widget=forms.Textarea(attrs={'class':'fm','cols':30,'rows':5,'style':'height:70px;','title':_('Meta Description'),'onkeyUp':'txtarealimit(this,400);'}))
    price_month = forms.FloatField(required=True,widget=forms.TextInput(attrs={'class':'textField','style':'width:40px; height:21px;'}), error_messages={'required': 'Price Month field Shouldn\'t be empty.','invalid': 'Price field should be a number'})
    price_year = forms.FloatField(required=True,widget=forms.TextInput(attrs={'class':'textField','style':'width:40px; height:21px;'}), error_messages={'required': 'Price Year field Shouldn\'t be empty.','invalid': 'Price field should be a number'})

    def clean_name(self):
        name = self.cleaned_data.get("name").strip()
        qset = BusinessCategory.objects.filter(name=name)
        if not self.data['parent_cat']:
            qset = qset.filter(parent_cat=None)
        else:
            qset = qset.filter(parent_cat__id=self.data['parent_cat'])
        if self.instance:
            qset = qset.exclude(id=self.instance.id)
        if qset.exists():
            raise forms.ValidationError(_("A Category with same name already exist."))
        return name

    def clean_slug(self):
        slug = self.cleaned_data.get("slug")
        if slug:return slug
        else:
            name = self.cleaned_data.get("name")
            return name.strip()

    def clean_seo_title(self):
        print self.cleaned_data
        seo_title = self.cleaned_data.get("seo_title").strip()
        if seo_title: return seo_title
        else:return self.data.get("name").strip()[:70]

    def clean_seo_description(self):
        seo_description = self.cleaned_data.get("seo_description").strip()
        if seo_description: return seo_description
        else:return self.data.get("name").strip()[:160]

#     def clean_price_month(self):
#         price_month = self.cleaned_data.get("price_month")
#         if price_month == 0.0:
#             raise forms.ValidationError(_("Please enter monthly price greater then zero(0)"))
#         else:
#             return self.cleaned_data.get("price_month")

#     def clean_price_year(self):
#         price_year = self.cleaned_data.get("price_year")
#         if price_year == 0.0:
#             raise forms.ValidationError(_("Please enter yearly price greater then zero(0)"))
#         else:
#             return self.cleaned_data.get("price_year")

    class Meta:
        model=BusinessCategory

class Tag_Form(forms.ModelForm):
    tag = forms.CharField(required=True,max_length=150, error_messages={'required': 'Please enter the tag'},widget=forms.TextInput({'class':'textField normal','style':'padding:4px 3px; font-size:14px;','onkeyup':'txtarealimit(this,150)'}))
    def clean_tag(self):
        tag = self.cleaned_data.get("tag")
        if len(tag)>150:
            raise forms.ValidationError("Maximum length of tags field is 150 charector.")
        return tag
    class Meta:
        model=Tag

MEDIA_CHOICES= (
          ('K', 'CheckBox'),
          ('R', 'Radio Button'),
          ('S', 'Select Box'),
          ('C', 'Text Field'),
          #('I', 'File/Image'),
)
class BusinessForm(forms.ModelForm):
    name = forms.CharField(required=True,max_length=70, error_messages={'required': 'Please enter the business title'},widget=forms.TextInput({'placeholder':_('Untitled Business'),'autocomplete':'off','onkeyup':'string_to_slug(this.value)'}))
    slug = forms.CharField(required=True,max_length=70, error_messages={'required': 'Please enter the business slug'},widget=forms.TextInput({'class':'default-url tttxt-w','style':'width:152px;','title':_('Business Slug'),'autocomplete':'off','style':'padding: 0pt; width: 237px;','onkeyup':'string_to_slug(this.value)'}))
    description = forms.CharField(required=False,widget=forms.Textarea({'class':'textField long'}),error_messages={'required': 'Please enter the description'})
    paymentoptions = forms.ModelMultipleChoiceField(required=False,widget=HorizCheckboxSelectMultiple('add-options'), queryset=PaymentOptions.objects.all())
    lstart_date=forms.DateField(required=False,error_messages={'required':_('Please enter vaild Listing Start Date.')},widget=forms.DateInput(attrs={'placeholder':_('2011-02-02'),'class':'tttxt-n','title':_('Listing Start Date'),'style':'width:75px !important;'}))
    lend_date=forms.DateField(required=False,error_messages={'required':_('Please enter vaild Listing End Date.')},widget=forms.DateInput(attrs={'placeholder':_('2011-04-02'),'class':'tttxt-n','title':_('Listing End Date'),'style':'width:75px !important;'}))
    fb_url = forms.CharField(required=False,max_length=150, error_messages={'required': 'Please enter the Facebook URL'},widget=forms.TextInput(attrs={'onfocus':'showhttp("f")','onblur':'hidehttp("f")','title':'Facebook URL','placeholder':'http://facebook.com/page','autocomplete':'off','style':'width:329px'}))
    twitter_url = forms.CharField(required=False,max_length=150, error_messages={'required': 'Please enter the Twitter URL'},widget=forms.TextInput(attrs={'onfocus':'showhttp("tw")','onblur':'hidehttp("tw")','title':'Twitter URL','placeholder':'http://twitter.com/page','autocomplete':'off','style':'width:329px'}))
    gooleplus_url = forms.CharField(required=False,max_length=150, error_messages={'required': 'Please enter the Google+ URL'},widget=forms.TextInput(attrs={'onfocus':'showhttp("g")','onblur':'hidehttp("g")','title':'Google Plus URL','placeholder':'http://plus.google.com/page','autocomplete':'off','style':'width:329px'}))


    class Meta:
        model = Business
        exclude = ('logo','categories','address','operating_hours','workinghours','tags','summary','votes','ratings','most_viewed','seo_title','seo_description','featured_sponsored','sp_cost','payment','payment_type','is_paid','created_by','modified_by','status')
        

class UserBusinessForm(forms.ModelForm):
    name = forms.CharField(required=True,max_length=70, error_messages={'required': 'Please enter the business title'},widget=forms.TextInput({"class":"iSp8",'placeholder':_('Business Name'),'autocomplete':'off','onkeyUp':'fillslug(this.value)'}))
    slug = forms.CharField(required=True,max_length=70, error_messages={'required': 'Please enter the business slug'},widget=forms.TextInput({'class':'default-url tttxt-w','style':'width:152px;','title':_('Business Slug'),'autocomplete':'off','style':'padding: 0pt; width: 237px;','onkeyup':'string_to_slug(this.value)'}))
    description = forms.CharField(required=False,max_length=5000,widget=forms.Textarea({'class':'iSp8'}),error_messages={'required': 'Please enter the description'})
    paymentoptions = forms.ModelMultipleChoiceField(required=False,widget=HorizDivCheckboxSelectMultiple('span6 pLlTmP pD0 sP6mP'), queryset=PaymentOptions.objects.all())
    lstart_date=forms.DateField(required=False,error_messages={'required':_('Please enter vaild Listing Start Date.')},widget=forms.DateInput(attrs={'placeholder':_('2011-02-02'),'class':'tttxt-n','title':_('Listing Start Date'),'style':'width:75px !important;'}))
    lend_date=forms.DateField(required=False,error_messages={'required':_('Please enter vaild Listing End Date.')},widget=forms.DateInput(attrs={'placeholder':_('2011-04-02'),'class':'tttxt-n','title':_('Listing End Date'),'style':'width:75px !important;'}))
    fb_url = forms.CharField(required=False,max_length=150, error_messages={'required': 'Please enter the Facebook URL'},widget=forms.TextInput(attrs={'onfocus':'showhttp("f")','onblur':'hidehttp("f")','title':'Facebook URL','placeholder':'http://facebook.com/page','autocomplete':'off','style':'width:329px','class':'iSp8'}))
    twitter_url = forms.CharField(required=False,max_length=150, error_messages={'required': 'Please enter the Twitter URL'},widget=forms.TextInput(attrs={'onfocus':'showhttp("tw")','onblur':'hidehttp("tw")','title':'Twitter URL','placeholder':'http://twitter.com/page','autocomplete':'off','style':'width:329px','class':'iSp8'}))
    gooleplus_url = forms.CharField(required=False,max_length=150, error_messages={'required': 'Please enter the Google+ URL'},widget=forms.TextInput(attrs={'onfocus':'showhttp("g")','onblur':'hidehttp("g")','title':'Google Plus URL','placeholder':'http://plus.google.com/page','autocomplete':'off','style':'width:329px','class':'iSp8'}))


    class Meta:
        model = Business
        exclude = ('logo','categories','address','operating_hours','workinghours','tags','summary','votes','ratings','most_viewed','seo_title','seo_description','featured_sponsored','sp_cost','payment','payment_type','is_paid','created_by','modified_by','status')
    
class EditBusinessForm(forms.ModelForm):
    name = forms.CharField(required=True,max_length=70, error_messages={'required': 'Please enter the business title'},widget=forms.TextInput({'class':'tttxt-w','title':_('Business Name'),'placeholder':_('Untitled Business'),'autocomplete':'off','onkeyup':'string_to_slug(this.value)'}))
    slug = forms.CharField(required=True,max_length=70, error_messages={'required': 'Please enter the business slug'},widget=forms.TextInput({'class':'default-url tttxt-w','style':'width:152px;','title':_('Business Slug'),'autocomplete':'off','style':'padding: 0pt; width: 237px;','onkeyup':'string_to_slug(this.value)'}))
    description = forms.CharField(required=False,max_length=5000,widget=forms.Textarea({'class':'textField long'}),error_messages={'required': 'Please enter the description'})
    paymentoptions = forms.ModelMultipleChoiceField(required=False,widget=HorizCheckboxSelectMultiple('add-options'), queryset=PaymentOptions.objects.all())
    fb_url = forms.CharField(required=False,max_length=150, error_messages={'required': 'Please enter the Facebook URL'},widget=forms.TextInput(attrs={'onfocus':'showhttp("f")','onblur':'hidehttp("f")','title':'Facebook URL','placeholder':'http://facebook.com/page','autocomplete':'off','style':'width:329px;'}))
    twitter_url = forms.CharField(required=False,max_length=150, error_messages={'required': 'Please enter the Twitter URL'},widget=forms.TextInput(attrs={'onfocus':'showhttp("tw")','onblur':'hidehttp("tw")','title':'Twitter URL','placeholder':'http://twitter.com/page','autocomplete':'off','style':'width:329px;'}))
    gooleplus_url = forms.CharField(required=False,max_length=150, error_messages={'required': 'Please enter the Google+ URL'},widget=forms.TextInput(attrs={'onfocus':'showhttp("g")','onblur':'hidehttp("g")','title':'Google Plus URL','placeholder':'http://plus.google.com/page','autocomplete':'off','style':'width:329px;'}))


    class Meta:
        model = Business
        exclude = ('lstart_date','address','lend_date','logo','categories','operating_hours','workinghours','tags','summary','votes','ratings','most_viewed','seo_title','seo_description','featured_sponsored','sp_cost','payment','payment_type','is_paid','created_by','modified_by','status')

class EditUserBusinessForm(forms.ModelForm):
    name = forms.CharField(required=True,max_length=70, error_messages={'required': 'Please enter the business title'},widget=forms.TextInput({'class':'tttxt-w','title':_('Business Name'),'placeholder':_('Untitled Business'),'autocomplete':'off','onkeyup':'string_to_slug(this.value)'}))
    slug = forms.CharField(required=True,max_length=70, error_messages={'required': 'Please enter the business slug'},widget=forms.TextInput({'class':'default-url tttxt-w','style':'width:152px;','title':_('Business Slug'),'autocomplete':'off','style':'padding: 0pt; width: 237px;','onkeyup':'string_to_slug(this.value)'}))
    description = forms.CharField(required=False,max_length=5000,widget=forms.Textarea({'class':'iSp8'}),error_messages={'required': 'Please enter the description'})
    paymentoptions = forms.ModelMultipleChoiceField(required=False,widget=HorizCheckboxSelectMultiple('add-options'), queryset=PaymentOptions.objects.all())
    fb_url = forms.CharField(required=False,max_length=150, error_messages={'required': 'Please enter the Facebook URL'},widget=forms.TextInput(attrs={'onfocus':'showhttp("f")','onblur':'hidehttp("f")','title':'Facebook URL','placeholder':'http://facebook.com/page','autocomplete':'off','style':'width:329px;'}))
    twitter_url = forms.CharField(required=False,max_length=150, error_messages={'required': 'Please enter the Twitter URL'},widget=forms.TextInput(attrs={'onfocus':'showhttp("tw")','onblur':'hidehttp("tw")','title':'Twitter URL','placeholder':'http://twitter.com/page','autocomplete':'off','style':'width:329px;'}))
    gooleplus_url = forms.CharField(required=False,max_length=150, error_messages={'required': 'Please enter the Google+ URL'},widget=forms.TextInput(attrs={'onfocus':'showhttp("g")','onblur':'hidehttp("g")','title':'Google Plus URL','placeholder':'http://plus.google.com/page','autocomplete':'off','style':'width:329px;'}))


    class Meta:
        model = Business
        exclude = ('lstart_date','address','lend_date','logo','categories','operating_hours','workinghours','tags','summary','votes','ratings','most_viewed','seo_title','seo_description','featured_sponsored','sp_cost','payment','payment_type','is_paid','created_by','modified_by','status')

class UserAddressForm(forms.ModelForm):#globalsettings.city
    address1 = forms.CharField(required=True,max_length=200,widget=forms.TextInput(attrs={'autocomplete':'off','class':'iSp8','title':_('Enter Address'),'placeholder':_('Address')}),error_messages={'required': 'Please enter the address'})
    address2 = forms.CharField(required=False,max_length=200,widget=forms.TextInput(attrs={'autocomplete':'off', 'class': 'iSp8','title':_('Enter Street'),'placeholder':_('Address1/Street') }),error_messages={'required': 'Please enter the street name'})
    zip = forms.CharField(required=True,max_length=16,widget=forms.TextInput(attrs={ 'autocomplete':'off','class': 'iSp8','title':_('Enter Zip/PostalCode'),'placeholder':_('Zip/PostalCode')}),error_messages={'required': 'Please enter the Zipcode'})
    state = forms.CharField(required=False,max_length=100,widget=forms.TextInput(attrs={ 'autocomplete':'off','class': 'iSp8','title':_('Enter name of State'),'placeholder':_('State') }),error_messages={'required': 'Please enter State'})
    city = forms.CharField(required=False,max_length=100,widget=forms.TextInput(attrs={ 'autocomplete':'off','class': 'iSp8','title':_('Enter name of City/Town'),'placeholder':_('City/Town') }),error_messages={'required': 'Please enter City'})
    telephone1 = forms.CharField(required=False,max_length=20,widget=forms.TextInput(attrs={ 'title':_('Enter telephone number. e.g., 555-555-5555'),'placeholder':_('Example: 555-555-5555'),'style':'margin-top:2px;' }),error_messages={'required': 'Please enter the phone number'})
    fax = forms.CharField(required=False,max_length=20,widget=forms.TextInput(attrs={ 'autocomplete':'off','class': 'iSp8','title':_('Enter fax number. e.g., (555)-555-5555'),'placeholder':_('Example: (555)-555-5555'),'style':'margin-top:2px;' }),error_messages={'required': 'Please enter the phone number'})
    mobile = forms.CharField(required=False,max_length=20,widget=forms.TextInput(attrs={ 'autocomplete':'off','title':_('Enter mobile number. e.g., 555-555-5555'),'placeholder':_('Example: 555-555-5555'),'style':'margin-top:2px;' }),error_messages={'required': 'Please enter the mobile number'})
    email = forms.EmailField(required=False,max_length=75,widget=forms.TextInput(attrs={ 'autocomplete':'off','class': 'iSp8','title':_('Enter email address. e.g., myname@example.com'),'placeholder':_('Example: myname@example.com') }),error_messages={'required': 'Please enter the valid email address'})
    website = forms.CharField(required=False,max_length=250,widget=forms.TextInput(attrs={ 'autocomplete':'off','class': 'iSp8','title':_('Enter website url. e.g., http://www.example.com'),'placeholder':_('Example: http://www.example.com') }),error_messages={'required': 'Please enter the url'})

    class Meta:
        model = Address
        exclude = ('description','address_type','venue','lat','lon','zoom','status','telephone2','is_active','created_on','created_by','modified_on','modified_by','seo_title','seo_description')

class AddressForm(forms.ModelForm):#globalsettings.city
    address1 = forms.CharField(required=True,max_length=200,widget=forms.TextInput(attrs={'autocomplete':'off','class':'fl','title':_('Enter Address'),'placeholder':_('Address')}),error_messages={'required': 'Please enter the address'})
    address2 = forms.CharField(required=False,max_length=200,widget=forms.TextInput(attrs={ 'autocomplete':'off','class': 'fl','title':_('Enter Street'),'placeholder':_('Address1/Street') }),error_messages={'required': 'Please enter the street name'})
    zip = forms.CharField(required=True,max_length=16,widget=forms.TextInput(attrs={'autocomplete':'off', 'class': 'fl','title':_('Enter Zip/PostalCode'),'placeholder':_('Zip/PostalCode')}),error_messages={'required': 'Please enter the Zipcode'})
    state = forms.CharField(required=False,max_length=100,widget=forms.TextInput(attrs={'autocomplete':'off', 'class': 'fl','title':_('Enter name of State'),'placeholder':_('State') }),error_messages={'required': 'Please enter State'})
    city = forms.CharField(required=False,max_length=100,widget=forms.TextInput(attrs={'autocomplete':'off', 'class': 'fl','title':_('Enter name of City/Town'),'placeholder':_('City/Town') }),error_messages={'required': 'Please enter City'})
    telephone1 = forms.CharField(required=False,max_length=20,widget=forms.TextInput(attrs={ 'class': 'fs','title':_('Enter telephone number. e.g., 555-555-5555'),'placeholder':_('Example: 555-555-5555'),'style':'margin-top:2px;' }),error_messages={'required': 'Please enter the phone number'})
    fax = forms.CharField(required=False,max_length=20,widget=forms.TextInput(attrs={ 'class': 'fl','title':_('Enter fax number. e.g., (555)-555-5555'),'placeholder':_('Example: (555)-555-5555'),'style':'margin-top:2px;' }),error_messages={'required': 'Please enter the phone number'})
    mobile = forms.CharField(required=False,max_length=20,widget=forms.TextInput(attrs={ 'class': 'fs','title':_('Enter mobile number. e.g., 555-555-5555'),'placeholder':_('Example: 555-555-5555'),'style':'margin-top:2px;' }),error_messages={'required': 'Please enter the mobile number'})
    email = forms.EmailField(required=False,max_length=75,widget=forms.TextInput(attrs={ 'class': 'fl','title':_('Enter email address. e.g., myname@example.com'),'placeholder':_('Example: myname@example.com') }),error_messages={'required': 'Please enter the valid email address'})
    website = forms.CharField(required=False,max_length=250,widget=forms.TextInput(attrs={'autocomplete':'off','class': 'fl','title':_('Enter website url. e.g., http://www.example.com'),'placeholder':_('Example: http://www.example.com') }),error_messages={'required': 'Please enter the url'})

    class Meta:
        model = Address
        exclude = ('description','address_type','venue','lat','lon','zoom','status','telephone2','is_active','created_on','created_by','modified_on','modified_by','seo_title','seo_description')



class DealBusinessForm(forms.ModelForm):
    name = forms.CharField(required=True,max_length=70, error_messages={'required': 'Please enter the business title'},widget=forms.TextInput({'class':'fm','placeholder':_('Untitled Business'),'autocomplete':'off'}))

    class Meta:
        model = Business
        fields = ('name',)

class DealAddressForm(forms.ModelForm):#globalsettings.city
    venue = forms.CharField(required=True,max_length=70,widget=forms.TextInput(attrs={'class':'fm','title':_('Enter Title'),'placeholder':_('Title')}),error_messages={'required': 'Please enter the Title'})
    address1 = forms.CharField(required=True,max_length=70,widget=forms.TextInput(attrs={'class':'fm','placeholder':_('Address')}),error_messages={'required': 'Please enter the address'})
    address2 = forms.CharField(required=False,max_length=70,widget=forms.TextInput(attrs={ 'class': 'fm','placeholder':_('Address1/Street') }),error_messages={'required': 'Please enter the street name'})
    zip = forms.CharField(required=True,max_length=70,widget=forms.TextInput(attrs={ 'class': 'fm','placeholder':_('Zip/PostalCode')}),error_messages={'required': 'Please enter the Zipcode'})
    city = forms.CharField(required=False,widget=forms.TextInput(attrs={ 'class': 'fm','title':_('City/Town'),'placeholder':_('City/Town') }),error_messages={'required': 'Please enter City'})
    telephone1 = forms.CharField(required=False,max_length=15,widget=forms.TextInput(attrs={ 'class': 'fm','placeholder':_(' 555-555-5555')}),error_messages={'required': 'Please enter the phone number'})
    email = forms.EmailField(required=True,max_length=60,widget=forms.TextInput(attrs={ 'class': 'fm','placeholder':_('myname@example.com') }),error_messages={'required': 'Please enter the email address'})
    fax = forms.CharField(required=False,max_length=15,widget=forms.TextInput(attrs={ 'class': 'fm','title':_('Enter fax number. e.g., 555-5555'),'placeholder':_('Example: 555-5555'),'style':'margin-top:2px;' }),error_messages={'required': 'Please enter the phone number'})
    mobile = forms.CharField(required=False,max_length=15,widget=forms.TextInput(attrs={ 'class': 'fm','title':_('Enter mobile number. e.g., 555-555-5555'),'placeholder':_('Example: 555-555-5555'),'style':'margin-top:2px;' }),error_messages={'required': 'Please enter the mobile number'})
    website = forms.CharField(required=False,max_length=150,widget=forms.TextInput(attrs={ 'class': 'fm','title':_('Enter website url. e.g., http://www.example.com'),'placeholder':_('Example: http://www.example.com') }),error_messages={'required': 'Please enter the url'})
    
    class Meta:
        model = Address
        fields = ('venue','address1','address2','zip','city','telephone1','email','website','fax','mobile')

#SEO Home
class SEO_Home_Form(forms.ModelForm):
    seo_title= forms.CharField(required=True, max_length="200", widget=forms.TextInput(attrs={'style':'padding:3px;','class':'textField long'}), error_messages={'required': 'SEO title required'})
    seo_description= forms.CharField(required=True, max_length="350", widget=forms.Textarea(attrs={'style':'overflow: hidden; height: 70px;','class':'textField small'}), error_messages={'required': 'SEO description required'})

    class Meta:
        model = ModuleNames
        exclude=('name','modified_by')

#SEO Category
class SEOCategoryForm(forms.ModelForm):
    slug = forms.CharField(required=True, widget=forms.TextInput({'class':'default-url','style':'width:139px;','title':_('Category Slug'),'maxlength':'200','onkeyUp':'string_to_slug(this.value)','autocomplete':'off'}), error_messages={'required': _('Please enter the slug')})
    seo_title = forms.CharField(required=True,max_length=200,widget=forms.TextInput(attrs={'class':'fm','maxlength':'200','title':_('Meta Title'),'autocomplete':'off'}), error_messages={'required': _('Please enter the Meta Title')})
    seo_description = forms.CharField(required=True,max_length=400,widget=forms.Textarea(attrs={'class':'fm','cols':30,'rows':5,'style':'height:70px;','title':_('Meta Description'),'onkeyUp':'txtarealimit(this,400);'}), error_messages={'required': _('Please enter the Meta Keyword')})

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
        model = BusinessCategory
        fields=('slug','seo_title','seo_description')

#SEO Business
class BusinessSEOForm(forms.ModelForm):
    #slug = forms.CharField(required=True, widget=forms.TextInput({'class':'default-url','style':'width:186px;','title':_('Category Slug'),'maxlength':'200','onkeyUp':'string_to_slug(this.value)','autocomplete':'off'}), error_messages={'required': _('Please enter the slug')})
    seo_title = forms.CharField(required=True,max_length=70,widget=forms.TextInput(attrs={'class':'fm','maxlength':70,'title':_('Meta Title'),'autocomplete':'off'}), error_messages={'required': _('Please enter the Meta Title')})
    seo_description = forms.CharField(required=True,max_length=160,widget=forms.Textarea(attrs={'maxlength':160,'class':'fxl','cols':30,'rows':4,'style':'height:70px;','title':_('Meta Description'),'onkeyUp':'txtarealimit(this,400);'}), error_messages={'required': _('Please enter the Meta Keyword')})

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
        model = Business
        fields=('seo_title','seo_description')

class UserBusinessSEOForm(forms.ModelForm):
    seo_title = forms.CharField(required=True,max_length=70,widget=forms.TextInput(attrs={'class':'iSp8','maxlength':70,'title':_('Meta Title'),'autocomplete':'off'}), error_messages={'required': _('Please enter the Meta Title')})
    seo_description = forms.CharField(required=True,max_length=160,widget=forms.Textarea(attrs={'class':'iSp8','maxlength':160,'cols':30,'rows':4,'style':'height:70px;','title':_('Meta Description'),'onkeyUp':'txtarealimit(this,400);'}), error_messages={'required': _('Please enter the Meta Keyword')})

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
        model = Business
        fields=('seo_title','seo_description')


Business_Pay_Opt=(('True','Paid'),('False','Free'),)
Business_Contract_Period=(('month','Month'),('year','Year'),)
Business_Exposure=(('0','Standard'),('1',' 5X'),('2','10X'),('3','15X'),('4','20X'),('5','25X'),)
Business_Features_Opt=(('Y','Yes'),('N','No'),)
Business_Socialmedia_Options=(('N','No'),('T','Twitter'),('F','Facebook'),('B','FB + Twitter'),)

class BusinessPriceForm(forms.ModelForm):
    level = forms.CharField(required=False, max_length="10", widget=forms.TextInput(attrs={'size':'30','class':'input_text'}), error_messages={'required': 'Title field Shouldn\'t be empty.'})
    level_visibility = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'onclick':'change_visiblity($(this))'}),error_messages={'required': 'Label content field Shouldn\'t be empty.'})
    level_label = forms.CharField(required=True, max_length=50, widget=forms.TextInput({'title':_('Label'),'maxlength':'50', 'style':'height:21px;', 'autocomplete':'off'}), error_messages={'required': _('Label field Shouldn\'t be empty.')})
    exposure = forms.ChoiceField(required=True, choices=Business_Exposure, widget=forms.Select(attrs={'class':'select-menu','style':'width:88px;'}), error_messages={'required': 'Exposure field Shouldn\'t be empty.'})
    images = forms.ChoiceField(required=True, choices=Business_Features_Opt, widget=forms.Select(attrs={'class':'select-menu','style':'width:70px;'}), error_messages={'required': 'Image field Shouldn\'t be empty.'})
    offer_coupon = forms.ChoiceField(required=True, choices=Business_Features_Opt, widget=forms.Select(attrs={'class':'select-menu','style':'width:70px;'}), error_messages={'required': 'Offers/Coupons field Shouldn\'t be empty.'})
    product = forms.ChoiceField(required=True, choices=Business_Features_Opt, widget=forms.Select(attrs={'class':'select-menu','style':'width:70px;'}), error_messages={'required': 'Products field Shouldn\'t be empty.'})
    share_buttons = forms.ChoiceField(required=True, choices=Business_Features_Opt, widget=forms.Select(attrs={'class':'select-menu','style':'width:70px;'}), error_messages={'required': 'Share Buttons field Shouldn\'t be empty.'})
    comments = forms.ChoiceField(required=True, choices=Business_Features_Opt, widget=forms.Select(attrs={'class':'select-menu','style':'width:70px;'}), error_messages={'required': 'Comments field Shouldn\'t be empty.'})
    newsletter = forms.ChoiceField(required=True, choices=Business_Features_Opt, widget=forms.Select(attrs={'class':'select-menu','style':'width:70px;'}), error_messages={'required': 'Newsletter field Shouldn\'t be empty.'})
    socialmedia = forms.ChoiceField(required = True, choices = Business_Features_Opt, widget=forms.Select(attrs={'class':'select-menu','style':'width:70px;'}), error_messages={'required': 'Social Media Promotion field Shouldn\'t be empty.'})
    price_month = forms.FloatField(required=True,widget=forms.TextInput(attrs={'class':'textField','style':'width:40px; height:21px;'}), error_messages={'required': 'Price Month field Shouldn\'t be empty.','invalid': 'Price field should be a number'})
    price_year = forms.FloatField(required=True,widget=forms.TextInput(attrs={'class':'textField','style':'width:40px; height:21px;'}), error_messages={'required': 'Price Year field Shouldn\'t be empty.','invalid': 'Price field should be a number'})
    
    

    class Meta:
        model = BusinessPrice
        exclude = ('level')


class Listing_Form(forms.ModelForm):
    lstart_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'style':'height:18px;width:95px;','class':'textField'}),  error_messages={'required': 'Please enter start date'})
    lend_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'style':'height:18px;width:95px;','class':'textField'}), error_messages={'required': 'Please enter end date'})
    sp_cost = forms.DecimalField(required=True, widget=forms.DateInput(attrs={'style':'height:18px;width:95px;','class':'textField'}), error_messages={'required': 'Please listing price.'})

    class Meta:
        model = Business
        fields = ('lstart_date','lend_date','sp_cost')

class ProductForm(forms.ModelForm):
    title = forms.CharField(required=True,max_length="150",widget=forms.TextInput({'class':'tttxt-w','title':_('Product Title'),'style':'width:310px;','placeholder':_('Product Title'),'maxlength':'150','autocomplete':'off'}), error_messages={'required': _('Please enter the Product Title')})
    price = forms.CharField(required=False,max_length="150",widget=forms.TextInput({'class':'tttxt-w','title':_('Price'),'placeholder':_('Price'),'maxlength':'150','style':'width:300px; margin-left:5px;','autocomplete':'off'}), error_messages={'required': _('Please enter the price')})
    description = forms.CharField(required=False,max_length="1000",widget=forms.Textarea({'class':'tttxt-w','title':_('Description'),'placeholder':_('Description'),'maxlength':'1000','autocomplete':'off'}), error_messages={'required': _('Please enter the Description')})

    def clean_description(self):
        description = self.cleaned_data.get("description").strip()
        if len(description) > 1000:
            raise forms.ValidationError(_("Please enter the description with in 1000 characters."))
        else:return description
    class Meta:
        model=BusinessProducts
        exclude=('created_by','is_active','business','photo')

class CouponForm(forms.ModelForm):
    title = forms.CharField(required=True,max_length="150",widget=forms.TextInput({'title':_('Coupon Title'),'style':'width:310px;','placeholder':_('Coupon Title'),'maxlength':'150','autocomplete':'off'}), error_messages={'required': _('Please enter the Coupon Title')})
    start_date= forms.DateField(required=False, widget=forms.DateInput(attrs={'title':_('Coupon Start Date'),'style':'width:141px;','placeholder':_('2011-12-01'),'maxlength':'15'}), error_messages={'required':_('Coupon Start Date is required.')})
    end_date= forms.DateField(required=True, widget=forms.DateInput(attrs={'title':_('Coupon End Date'),'style':'width:141px;','placeholder':_('2012-01-01'),'maxlength':'15'}), error_messages={'required':_('Coupon End Date is required.')})
    description = forms.CharField(required=False,max_length="1000",widget=forms.Textarea({'title':_('Description'),'placeholder':_('Description'),'maxlength':'1000','autocomplete':'off'}), error_messages={'required': _('Please enter the Description')})
    type=forms.ChoiceField(required=False,error_messages={'required': _('Please select the type')},widget=forms.RadioSelect(renderer=HorizRadioRenderer),initial='C',choices = COUPON_OFFER_TYPE)

    def clean_description(self):
        description = self.cleaned_data.get("description").strip()
        if len(description) > 2000:
            raise forms.ValidationError(_("Please enter the description with in 2000 characters."))
        else:return description
    def clean_end_date(self):
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        if start_date > end_date:
            raise forms.ValidationError(_("Coupon start date shouldn't be greater than end date"))
        else:
            return end_date
    class Meta:
        model=BusinessCoupons
        exclude=('created_by','is_active','business','photo')

valid_time_formats = ['%I:%M %p']
class WorkingHoursForm(forms.ModelForm):
    notes = forms.CharField(required=False, widget=forms.TextInput({'class':'fl','title':_('Notes'),'placeholder':_('Notes'),'maxlength':'150','autocomplete':'off'}), error_messages={'required': _('Please enter the Notes')})
    mon_start= forms.CharField(required=False,error_messages={'required':  _('Please enter the Valid Time')},widget=forms.TextInput(attrs={'size':'6','class':'W80 workinghour starttime on fxs','placeholder':'09:00 AM','autocomplete':'off'}))
    mon_end= forms.CharField(required=False,error_messages={'required':  _('Please enter the Valid Time')},widget=forms.TextInput(attrs={'size':'6','class':'W80 workinghour endtime on fxs','placeholder':'06:00 PM','autocomplete':'off'}))
    tue_start= forms.CharField(required=False,error_messages={'required':  _('Please enter the Valid Time')},widget=forms.TextInput(attrs={'size':'6','class':'W80 workinghour starttime on fxs','placeholder':'09:00 AM','autocomplete':'off'}))
    tue_end= forms.CharField(required=False,error_messages={'required':  _('Please enter the Valid Time')},widget=forms.TextInput(attrs={'size':'6','class':'W80 workinghour endtime on fxs','placeholder':'06:00 PM','autocomplete':'off'}))
    wed_start= forms.CharField(required=False,error_messages={'required':  _('Please enter the Valid Time')},widget=forms.TextInput(attrs={'size':'6','class':'W80 workinghour starttime on fxs','placeholder':'09:00 AM','autocomplete':'off'}))
    wed_end= forms.CharField(required=False,error_messages={'required':  _('Please enter the Valid Time')},widget=forms.TextInput(attrs={'size':'6','class':'W80 workinghour endtime on fxs','placeholder':'06:00 PM','autocomplete':'off'}))
    thu_start= forms.CharField(required=False,error_messages={'required':  _('Please enter the Valid Time')},widget=forms.TextInput(attrs={'size':'6','class':'W80 workinghour starttime on fxs','placeholder':'09:00 AM','autocomplete':'off'}))
    thu_end= forms.CharField(required=False,error_messages={'required':  _('Please enter the Valid Time')},widget=forms.TextInput(attrs={'size':'6','class':'W80 workinghour endtime on fxs','placeholder':'06:00 PM','autocomplete':'off'}))
    fri_start= forms.CharField(required=False,error_messages={'required':  _('Please enter the Valid Time')},widget=forms.TextInput(attrs={'size':'6','class':'W80 workinghour starttime on fxs','placeholder':'09:00 AM','autocomplete':'off'}))
    fri_end= forms.CharField(required=False,error_messages={'required':  _('Please enter the Valid Time')},widget=forms.TextInput(attrs={'size':'6','class':'W80 workinghour endtime on fxs','placeholder':'06:00 PM','autocomplete':'off'}))
    sat_start= forms.CharField(required=False,error_messages={'required':  _('Please enter the Valid Time')},widget=forms.TextInput(attrs={'size':'6','class':'W80 workinghour starttime on fxs','placeholder':'09:00 AM','autocomplete':'off'}))
    sat_end= forms.CharField(required=False,error_messages={'required':  _('Please enter the Valid Time')},widget=forms.TextInput(attrs={'size':'6','class':'W80 workinghour endtime on fxs','placeholder':'06:00 PM','autocomplete':'off'}))
    sun_start= forms.CharField(required=False,error_messages={'required':  _('Please enter the Valid Time')},widget=forms.TextInput(attrs={'size':'6','class':'W80 workinghour starttime on fxs','placeholder':'09:00 AM','autocomplete':'off'}))
    sun_end= forms.CharField(required=False,error_messages={'required':  _('Please enter the Valid Time')},widget=forms.TextInput(attrs={'size':'6','class':'W80 workinghour endtime on fxs','placeholder':'06:00 PM','autocomplete':'off'}))

    class Meta:
        model=WorkingHours
        exclude=('status')

class PaymentOptionsForm(forms.ModelForm):
    name = forms.CharField(required=True, max_length=100, widget=forms.TextInput({'title':_('Payment Option'),'placeholder':_('Payment Option'),'maxlength':'100','autocomplete':'off'}), error_messages={'required': _('Please enter the Payment Option')})

    class Meta:
        model=PaymentOptions
        exclude=('image_position')

attrs_text={'class':'textstyle'}

class ContactDetailsForm(forms.ModelForm):
    name = forms.CharField(required=True,widget=forms.TextInput(attrs=attrs_text),error_messages={'required': 'Please enter the Name'})
    email = forms.CharField(required=False,widget=forms.TextInput(attrs=attrs_text),error_messages={'required': 'Please enter the Phone'})
    phone = forms.CharField(required=False,widget=forms.TextInput(attrs=attrs_text),error_messages={'required': 'Please enter the Email'})
    subject = forms.CharField(required=False,widget=forms.TextInput(attrs=attrs_text),error_messages={'required': 'Please enter the subject'})
    comment = forms.CharField(required=True,widget=forms.TextInput(attrs=attrs_text),error_messages={'required': 'Please enter the Comment'})
    #captcha = ReCaptchaField(attrs={'theme' : 'custom'})

    class Meta:
        model = ContactDetails
        exclude = ('created_on','business')

#class CaptchaForms(forms.Form):
#   custom_captcha = ReCaptchaField(attrs={'theme' : 'custom'})
FAILED_PAYMENT=(('F','Make it Free Listing'),('B','Block Listing'),)

class BusinessClaimSettingsForm(forms.ModelForm):
    allow_claim                 =forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'class':'cform-checkbox'}))
    allow_free_buz_claim        =forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'class':'cform-checkbox'}))
    auto_aprove_free_buz_claim  =forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'class':'cform-checkbox'}))
    auto_aprove_paid_buz_claim  =forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'class':'cform-checkbox'}))
    after_failed_payment = forms.ChoiceField(required=True, choices=FAILED_PAYMENT, widget=forms.Select(attrs={'class':'select-menu','style':'width:150px;'}), error_messages={'required': 'Please select action after end of payment/canceled.'})
    
    class Meta:
        model=BusinessClaimSettings 
