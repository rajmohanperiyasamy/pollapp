from django import forms
from django.utils.translation import ugettext as _
from locality.models import Locality

from common.models import ModuleNames
from common.form_utils import HorizCheckboxSelectMultiple, HorizRadioRenderer

from django.forms.widgets import SelectMultiple
from restaurants.models import Restaurants, PaymentOptions, RestaurantWorkingHours, RestaurantAddress, RestaurantCategories, MealTypes, Cuisines, RestaurantFeatures, RestaurantMenus
from restaurants.models import Rating_Options, Price_Range, RestaurantImages, RestaurantVideos

#......................................................
class RestaurantsForm(forms.ModelForm):
    name = forms.CharField(required=True,max_length=200, error_messages={'required': 'Please enter the restaurant title'},widget=forms.TextInput({'placeholder':_('Enter Restaurant Name'),'autocomplete':'off','onkeyup':'string_to_slug(this.value)'}))
    slug = forms.CharField(required=True,max_length=200, error_messages={'required': 'Please enter the restaurant slug'},widget=forms.TextInput({'class':'default-url tttxt-w','style':'width:152px;','title':_('Restaurant Slug'),'autocomplete':'off','style':'padding: 0pt; width: 237px;','onkeyup':'string_to_slug(this.value)'}))
    description = forms.CharField(required=False,max_length=5000,widget=forms.Textarea({'class':'textField long'}),error_messages={'required': 'Please enter the description'})
    fb_url = forms.CharField(required=False,max_length=150, error_messages={'required': 'Please enter the Facebook URL'},widget=forms.TextInput(attrs={'onfocus':'showhttp("f")','onblur':'hidehttp("f")','title':'Facebook URL','placeholder':'http://facebook.com/page','autocomplete':'off','style':'width:329px'}))
    twitter_url = forms.CharField(required=False,max_length=150, error_messages={'required': 'Please enter the Twitter URL'},widget=forms.TextInput(attrs={'onfocus':'showhttp("tw")','onblur':'hidehttp("tw")','title':'Twitter URL','placeholder':'http://twitter.com/page','autocomplete':'off','style':'width:329px'}))
    gooleplus_url = forms.CharField(required=False,max_length=150, error_messages={'required': 'Please enter the Google+ URL'},widget=forms.TextInput(attrs={'onfocus':'showhttp("g")','onblur':'hidehttp("g")','title':'Google Plus URL','placeholder':'http://plus.google.com/page','autocomplete':'off','style':'width:329px'}))
    categories = forms.ModelMultipleChoiceField(required=True, queryset=RestaurantCategories.objects.order_by('name'), widget=forms.SelectMultiple(attrs={'class':'select-menu fl','data-placeholder':_('Select multiple categories')}), error_messages={'required': _('categories Required')})
    meal_types = forms.ModelMultipleChoiceField(required=False, queryset=MealTypes.objects.order_by('name'), widget=forms.SelectMultiple(attrs={'class':'select-menu fl','data-placeholder':_('Select multiple meal types')}),  error_messages={'required': _('meal types Required')})
    cuisines = forms.ModelMultipleChoiceField(required=True, queryset=Cuisines.objects.order_by('name'), widget=forms.SelectMultiple(attrs={'class':'select-menu fl','data-placeholder':_('Select multiple cuisines')}), error_messages={'required': _('cuisines Required')})
    start_date=forms.DateField(required=False,error_messages={'required':_('Please enter vaild Listing Start Date.')},widget=forms.DateInput(attrs={'placeholder':_('2011-02-02'),'class':'tttxt-n','title':_('Listing Start Date'),'style':'width:75px !important;'}))
    end_date=forms.DateField(required=False,error_messages={'required':_('Please enter vaild Listing End Date.')},widget=forms.DateInput(attrs={'placeholder':_('2011-04-02'),'class':'tttxt-n','title':_('Listing End Date'),'style':'width:75px !important;'}))
    paymentoptions = forms.ModelMultipleChoiceField(required=True, queryset=PaymentOptions.objects.order_by('name'), widget=forms.SelectMultiple(attrs={'class':'select-menu fl','data-placeholder':_('Select multiple payment options')}))
    features = forms.ModelMultipleChoiceField(required=False, queryset=RestaurantFeatures.objects.order_by('name'), widget=forms.SelectMultiple(attrs={'class':'select-menu fl','data-placeholder':_('Select multiple features')}), error_messages={'required': _('features Required')})
    ratings = forms.ChoiceField(required=False,choices=Rating_Options,widget=forms.Select(attrs={'class':'select-menu fs'}), error_messages={'required': _(' rating Required')})
    price_range = forms.ChoiceField(required=False,choices=Price_Range,widget=forms.Select(attrs={'class':'select-menu fs'}), error_messages={'required': _(' price Required')})
    class Meta:
        model = Restaurants
        fields = ('categories', 'name','slug', 'description', 'fb_url', 'twitter_url', 'gooleplus_url', 'meal_types','cuisines', 'features', 'ratings', 'price_range', 'paymentoptions', 'start_date', 'end_date')

class RestaurantSEOForm(forms.ModelForm):
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
        model = Restaurants
        fields = ('seo_title', 'seo_description')

    
    
#......................................................
class EditRestaurantsForm(forms.ModelForm):
    name = forms.CharField(required=True,max_length=200, error_messages={'required': 'Please enter the restaurant title'},widget=forms.TextInput({'placeholder':_('Untitled Restaurant'),'autocomplete':'off','onkeyup':'string_to_slug(this.value)'}))
    slug = forms.CharField(required=True,max_length=200, error_messages={'required': 'Please enter the restaurant slug'},widget=forms.TextInput({'class':'default-url tttxt-w','style':'width:152px;','title':_('Restaurant Slug'),'autocomplete':'off','style':'padding: 0pt; width: 237px;','onkeyup':'string_to_slug(this.value)'}))
    description = forms.CharField(required=False,max_length=5000,widget=forms.Textarea({'class':'textField long'}),error_messages={'required': 'Please enter the description'})
    fb_url = forms.CharField(required=False,max_length=150, error_messages={'required': 'Please enter the Facebook URL'},widget=forms.TextInput(attrs={'onfocus':'showhttp("f")','onblur':'hidehttp("f")','title':'Facebook URL','placeholder':'http://facebook.com/page','autocomplete':'off','style':'width:329px'}))
    twitter_url = forms.CharField(required=False,max_length=150, error_messages={'required': 'Please enter the Twitter URL'},widget=forms.TextInput(attrs={'onfocus':'showhttp("tw")','onblur':'hidehttp("tw")','title':'Twitter URL','placeholder':'http://twitter.com/page','autocomplete':'off','style':'width:329px'}))
    gooleplus_url = forms.CharField(required=False,max_length=150, error_messages={'required': 'Please enter the Google+ URL'},widget=forms.TextInput(attrs={'onfocus':'showhttp("g")','onblur':'hidehttp("g")','title':'Google Plus URL','placeholder':'http://plus.google.com/page','autocomplete':'off','style':'width:329px'}))
    categories = forms.ModelMultipleChoiceField(required=True, queryset=RestaurantCategories.objects.order_by('name'), widget=forms.SelectMultiple(attrs={'class':'select-menu fl','data-placeholder':_('Select multiple categories')}), error_messages={'required': _('categories Required')})
    meal_types = forms.ModelMultipleChoiceField(required=False, queryset=MealTypes.objects.order_by('name'), widget=forms.SelectMultiple(attrs={'class':'select-menu fl','data-placeholder':_('Select multiple meal types')}),  error_messages={'required': _('meal types Required')})
    cuisines = forms.ModelMultipleChoiceField(required=True, queryset=Cuisines.objects.order_by('name'), widget=forms.SelectMultiple(attrs={'class':'select-menu fl','data-placeholder':_('Select multiple cuisines')}), error_messages={'required': _('cuisines Required')})
    paymentoptions = forms.ModelMultipleChoiceField(required=True, queryset=PaymentOptions.objects.order_by('name'), widget=forms.SelectMultiple(attrs={'class':'select-menu fl','data-placeholder':_('Select multiple payment options')}))
    features = forms.ModelMultipleChoiceField(required=False, queryset=RestaurantFeatures.objects.order_by('name'), widget=forms.SelectMultiple(attrs={'class':'select-menu fl','data-placeholder':_('Select multiple features')}), error_messages={'required': _('features Required')})
    ratings = forms.ChoiceField(required=False,choices=Rating_Options,widget=forms.Select(attrs={'class':'select-menu fs'}), error_messages={'required': _(' rating Required')})
    price_range = forms.ChoiceField(required=False,choices=Price_Range,widget=forms.Select(attrs={'class':'select-menu fs'}), error_messages={'required': _(' price Required')})
    class Meta:
        model = Restaurants
        fields = ('categories', 'name','slug', 'description', 'fb_url', 'twitter_url', 'gooleplus_url', 'meal_types','cuisines', 'features', 'ratings', 'price_range', 'paymentoptions')


class RestaurantWorkingHoursForm(forms.ModelForm):
    notes = forms.CharField(required=False, widget=forms.TextInput({'class':'fl','title':_('Notes'),'placeholder':_('Notes'),'maxlength':'150','autocomplete':'off'}), error_messages={'required': _('Please enter the Notes')})
    mon_start= forms.CharField(required=False,error_messages={'required':  _('Please enter the Valid Time')},widget=forms.TextInput(attrs={'size':'6','class':'horkinghour starttime fxs on','placeholder':'09:00 AM','autocomplete':'off'}))
    mon_end= forms.CharField(required=False,error_messages={'required':  _('Please enter the Valid Time')},widget=forms.TextInput(attrs={'size':'6','class':'horkinghour endtime fxs on','placeholder':'06:00 AM','autocomplete':'off'}))
    tue_start= forms.CharField(required=False,error_messages={'required':  _('Please enter the Valid Time')},widget=forms.TextInput(attrs={'size':'6','class':'horkinghour starttime fxs on','placeholder':'09:00 AM','autocomplete':'off'}))
    tue_end= forms.CharField(required=False,error_messages={'required':  _('Please enter the Valid Time')},widget=forms.TextInput(attrs={'size':'6','class':'horkinghour endtime fxs on','placeholder':'06:00 AM','autocomplete':'off'}))
    wed_start= forms.CharField(required=False,error_messages={'required':  _('Please enter the Valid Time')},widget=forms.TextInput(attrs={'size':'6','class':'horkinghour starttime fxs on','placeholder':'09:00 AM','autocomplete':'off'}))
    wed_end= forms.CharField(required=False,error_messages={'required':  _('Please enter the Valid Time')},widget=forms.TextInput(attrs={'size':'6','class':'horkinghour endtime fxs on','placeholder':'06:00 AM','autocomplete':'off'}))
    thu_start= forms.CharField(required=False,error_messages={'required':  _('Please enter the Valid Time')},widget=forms.TextInput(attrs={'size':'6','class':'horkinghour starttime fxs on','placeholder':'09:00 AM','autocomplete':'off'}))
    thu_end= forms.CharField(required=False,error_messages={'required':  _('Please enter the Valid Time')},widget=forms.TextInput(attrs={'size':'6','class':'horkinghour endtime fxs on','placeholder':'06:00 AM','autocomplete':'off'}))
    fri_start= forms.CharField(required=False,error_messages={'required':  _('Please enter the Valid Time')},widget=forms.TextInput(attrs={'size':'6','class':'horkinghour starttime fxs on','placeholder':'09:00 AM','autocomplete':'off'}))
    fri_end= forms.CharField(required=False,error_messages={'required':  _('Please enter the Valid Time')},widget=forms.TextInput(attrs={'size':'6','class':'horkinghour endtime fxs on','placeholder':'06:00 AM','autocomplete':'off'}))
    sat_start= forms.CharField(required=False,error_messages={'required':  _('Please enter the Valid Time')},widget=forms.TextInput(attrs={'size':'6','class':'horkinghour starttime fxs on','placeholder':'09:00 AM','autocomplete':'off'}))
    sat_end= forms.CharField(required=False,error_messages={'required':  _('Please enter the Valid Time')},widget=forms.TextInput(attrs={'size':'6','class':'horkinghour endtime fxs on','placeholder':'06:00 AM','autocomplete':'off'}))
    sun_start= forms.CharField(required=False,error_messages={'required':  _('Please enter the Valid Time')},widget=forms.TextInput(attrs={'size':'6','class':'horkinghour starttime fxs on','placeholder':'09:00 AM','autocomplete':'off'}))
    sun_end= forms.CharField(required=False,error_messages={'required':  _('Please enter the Valid Time')},widget=forms.TextInput(attrs={'size':'6','class':'horkinghour endtime fxs on','placeholder':'06:00 AM','autocomplete':'off'}))

    class Meta:
        model=RestaurantWorkingHours
        exclude=('status')
        
        
class RestaurantAddressForm(forms.ModelForm):#globalsettings.city
    address1 = forms.CharField(required=True,max_length=70,widget=forms.TextInput(attrs={'class':'fl','title':_('Enter Address'),'placeholder':_('Address')}),error_messages={'required': 'Please enter the address'})
    address2 = forms.CharField(required=False,max_length=70,widget=forms.TextInput(attrs={ 'class': 'fl','title':_('Enter Street'),'placeholder':_('Address1/Street') }))
    pin = forms.CharField(required=True,max_length=70,widget=forms.TextInput(attrs={ 'class': 'fl','title':_('Enter Zip/PostalCode'),'placeholder':_('Zip/PostalCode')}),error_messages={'required': 'Please enter the Zipcode'})
    city = forms.CharField(required=False,widget=forms.TextInput(attrs={ 'class': 'fl','title':_('Enter name of City/Town'),'placeholder':_('City/Town') }),error_messages={'required': 'Please enter City'})
    telephone = forms.CharField(required=False,max_length=15,widget=forms.TextInput(attrs={ 'class': 'fs','title':_('Enter telephone number. e.g., 555-555-5555'),'placeholder':_('Example: 555-555-5555'),'style':'margin-top:2px;' }),error_messages={'required': 'Please enter the phone number'})
    fax = forms.CharField(required=False,max_length=15,widget=forms.TextInput(attrs={ 'class': 'fl','title':_('Enter fax number. e.g., 555-5555'),'placeholder':_('Example: 555-5555'),'style':'margin-top:2px;' }),error_messages={'required': 'Please enter the phone number'})
    mobile_no = forms.CharField(required=False,max_length=15,widget=forms.TextInput(attrs={ 'class': 'fs','title':_('Enter mobile number. e.g., 555-555-5555'),'placeholder':_('Example: 555-555-5555'),'style':'margin-top:2px;' }),error_messages={'required': 'Please enter the mobile number'})
    email = forms.EmailField(required=False,max_length=60,widget=forms.TextInput(attrs={ 'class': 'fl','title':_('Enter email address. e.g., myname@example.com'),'placeholder':_('Example: myname@example.com') }))
    website = forms.CharField(required=False,max_length=150,widget=forms.TextInput(attrs={ 'class': 'fl','title':_('Enter website url. e.g., http://www.example.com'),'placeholder':_('Example: http://www.example.com') }),error_messages={'required': 'Please enter the url'})

    class Meta:
        model = RestaurantAddress
        exclude = ('restaurant', 'pointer_lat', 'pointer_lng', 'map_zoom')        
        

















#.....................................................  Restaurant staff listing      
class RestaurantMenusForm(forms.ModelForm):
    title = forms.CharField(max_length=120, required=True)
    categories = forms.ModelMultipleChoiceField(required=True, queryset=MealTypes.objects.order_by('name'), widget=forms.SelectMultiple(attrs={'class':'select-menu fl','data-placeholder':_('Select multiple categories')}), error_messages={'required': _('categories Required')})
    description = forms.CharField(required=False, widget=forms.Textarea({'class':'tttxt-w','title':_('Description'),'placeholder':_('Description'),'maxlength':'1000','autocomplete':'off'}), error_messages={'required': _('Please enter the Description')})
    files = forms.FileField(required=False)
    price = forms.CharField(required=False,max_length="50",widget=forms.TextInput({'class':'tttxt-w','title':_('Price'),'placeholder':_('Price'),'maxlength':'50','style':'width:300px; margin-left:5px;','autocomplete':'off'}), error_messages={'required': _('Please enter the price')})
    discount_price = forms.CharField(required=False,max_length="50",widget=forms.TextInput({'class':'tttxt-w','title':_('Discount Price'),'placeholder':_('Discount Price'),'maxlength':'50','style':'width:300px; margin-left:5px;','autocomplete':'off'}), error_messages={'required': _('Please enter the price')})
    
    class Meta:
        model= RestaurantMenus
        exclude = ('restaurant', 'uploaded_on', 'uploaded_by','discount_price','files')      




class RestaurantImagesForm(forms.ModelForm):
    title = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'class':'fl','title':_('Enter Title'),'placeholder':_('title')}), error_messages={'required': 'Please enter title'})
    photo = forms.ImageField(required=True) 
    
    class Meta:
        model= RestaurantImages
        exclude = ('restaurant', 'uploaded_on', 'uploaded_by',)


   



    















        