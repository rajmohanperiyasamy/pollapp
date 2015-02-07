from django import forms
from restaurants.models import RestaurantCategories, MealTypes, Cuisines, RestaurantFeatures, PaymentOptions, RestaurantPrice
from django.utils.translation import ugettext as _ 
from django.template.defaultfilters import slugify

class RestaurantCategoriesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        try:
            self._name = kwargs['instance'].name
        except:
            self._name= False
        super(RestaurantCategoriesForm, self).__init__(*args, **kwargs)
    
    name = forms.CharField(required=True,max_length=200, widget=forms.TextInput({'class':'fm','title':_('Category  Name'),'onkeyUp':'string_to_slug(this.value)','maxlength':'150','autocomplete':'off'}), error_messages={'required': _('Please enter the category name')})
    slug = forms.CharField(required=False, widget=forms.TextInput({'class':'default-url','style':'width:152px;','title':_('Category Slug'),'maxlength':'200','onkeyUp':'string_to_slug(this.value)','autocomplete':'off'}), error_messages={'required': _('Please enter the slug')})
    seo_title = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'fm','title':_('Meta Title'),'maxlength':'200','autocomplete':'off'}), error_messages={'required': _('Please enter the Meta title')})
    seo_description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'fm','title':_('Meta Description'),'onkeyUp':'txtarealimit(this,400);','style':'overflow: hidden; height: 70px;'}), error_messages={'required': _('Please enter the Meta description')})
    introduction = forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'fm','title':_('Introduction'),'onkeyUp':'txtarealimit(this,400);','style':'overflow: hidden; height: 70px;'}), error_messages={'required': _('Please enter the Introduction')})
    
    class Meta:
        model = RestaurantCategories
    
    def clean_name(self):
            print "name..."
            name = self.cleaned_data.get("name").strip()
            if self._name:  #.....update
                print "if: update"
                if str(self._name).lower() != str(name).lower(): 
                    try:
                        print "if try check"
                        flag=RestaurantCategories.objects.filter(name__iexact=name)
                        print flag
                        if flag:raise forms.ValidationError(_("This category name is already added."))
                    except RestaurantCategories.DoesNotExist:pass
                else:
                    print "noononono"
            else: #.....new entry
                print "else: new entry"
                try:
                    flag=RestaurantCategories.objects.filter(name__iexact=name)
                    if flag:raise forms.ValidationError(_("This category name is already added."))
                except RestaurantCategories.DoesNotExist:pass
            return name

    def clean_slug(self):
        slug = self.cleaned_data.get("slug")
        if slug:
            return slugify(slug)
        else:
            name = self.cleaned_data.get("name")
            return slugify(name)
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
            
            

#==================================================== meal types
class MealTypesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        try:
            self._name = kwargs['instance'].name
        except:
            self._name= False
        super(MealTypesForm, self).__init__(*args, **kwargs)
        
    name = forms.CharField(required=True, max_length=200, widget=forms.TextInput({'class':'fm','title':_('Meal  Name'),'onkeyUp':'string_to_slug(this.value)','maxlength':'150','autocomplete':'off'}), error_messages={'required': _('Please enter the meal type')})
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'fm','title':_('Meal Description'),'onkeyUp':'txtarealimit(this,400);','style':'overflow: hidden; height: 70px;'}), error_messages={'required': _('Please enter the meal description')})
  
        
        
    class Meta:
        model = MealTypes
        exclude = ('status', 'modified_by', 'created_by')

    def clean_name(self):
            name = self.cleaned_data.get("name").strip()
            if self._name:  #.....update
                if str(self._name).lower() != str(name).lower(): 
                    try:
                        flag=MealTypes.objects.filter(name__iexact=name)
                        print flag
                        if flag:raise forms.ValidationError(_("This meal type is already added."))
                    except MealTypes.DoesNotExist:pass
            else: #.....new entry
                try:
                    flag=MealTypes.objects.filter(name__iexact=name)
                    if flag:raise forms.ValidationError(_("This meal type is already added."))
                except MealTypes.DoesNotExist:pass
            return name
    







#=========================================== Cuisine
class CuisinesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        try:
            self._name = kwargs['instance'].name
        except:
            self._name= False
        super(CuisinesForm, self).__init__(*args, **kwargs)
        
        
    name = forms.CharField(required=True,max_length=200, widget=forms.TextInput({'class':'fm','title':_('Cuisines  Name'),'onkeyUp':'string_to_slug(this.value)','maxlength':'150','autocomplete':'off'}), error_messages={'required': _('Please enter the cuisine type')})
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'fm','title':_('Cuisines Description'),'onkeyUp':'txtarealimit(this,400);','style':'overflow: hidden; height: 70px;'}), error_messages={'required': _('Please enter the Cuisine description')})
    
    class Meta:
        model = Cuisines
        exclude = ('status', 'modified_by', 'created_by','slug')
        
    def clean_name(self):
            name = self.cleaned_data.get("name").strip()
            if self._name:  #.....update
                if str(self._name).lower() != str(name).lower(): 
                    try:
                        flag=Cuisines.objects.filter(name__iexact=name)
                        print flag
                        if flag:raise forms.ValidationError(_("This cuisine is already added."))
                    except Cuisines.DoesNotExist:pass
            else: #.....new entry
                try:
                    flag=Cuisines.objects.filter(name__iexact=name)
                    if flag:raise forms.ValidationError(_("This cuisine is already added."))
                except Cuisines.DoesNotExist:pass
            return name 


            
        
    
#=========================================== Features
class RestaurantFeaturesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        try:
            self._name = kwargs['instance'].name
        except:
            self._name= False
        super(RestaurantFeaturesForm, self).__init__(*args, **kwargs)
        
        
    name = forms.CharField(required=True,max_length=200, widget=forms.TextInput({'class':'fm','title':_('Feature Name'),'onkeyUp':'string_to_slug(this.value)','maxlength':'150','autocomplete':'off'}), error_messages={'required': _('Please enter the feature')})
    #description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'fm','title':_('Feature Description'),'onkeyUp':'txtarealimit(this,400);','style':'overflow: hidden; height: 70px;'}), error_messages={'required': _('Please enter the Feature description')})
    
    class Meta:
        model = RestaurantFeatures
        exclude = ('status', 'modified_by', 'created_by')
        
    def clean_name(self):
            name = self.cleaned_data.get("name").strip()
            if self._name:  #.....update
                if str(self._name).lower() != str(name).lower(): 
                    try:
                        flag=RestaurantFeatures.objects.filter(name__iexact=name)
                        print flag
                        if flag:raise forms.ValidationError(_("This Feature is already added."))
                    except RestaurantFeatures.DoesNotExist:pass
            else: #.....new entry
                try:
                    flag=RestaurantFeatures.objects.filter(name__iexact=name)
                    if flag:raise forms.ValidationError(_("This Feature is already added."))
                except RestaurantFeatures.DoesNotExist:pass
            return name 
    


#=========================================== Payment
class PaymentOptionsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        try:
            self._name = kwargs['instance'].name
        except:
            self._name= False
        super(PaymentOptionsForm, self).__init__(*args, **kwargs)
        
        
    name = forms.CharField(required=True,max_length=200, widget=forms.TextInput({'class':'fm','title':_('Payment Name'),'onkeyUp':'string_to_slug(this.value)','maxlength':'150','autocomplete':'off'}), error_messages={'required': _('Please enter the payment option')})
    #description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'fm','title':_('Feature Description'),'onkeyUp':'txtarealimit(this,400);','style':'overflow: hidden; height: 70px;'}), error_messages={'required': _('Please enter the Feature description')})
    
    class Meta:
        model = PaymentOptions
        exclude = ('status', 'modified_by', 'created_by')
        
    def clean_name(self):
            name = self.cleaned_data.get("name").strip()
            if self._name:  #.....update
                if str(self._name).lower() != str(name).lower(): 
                    try:
                        flag=PaymentOptions.objects.filter(name__iexact=name)
                        print flag
                        if flag:raise forms.ValidationError(_("This payment option is already added."))
                    except PaymentOptions.DoesNotExist:pass
            else: #.....new entry
                try:
                    flag=PaymentOptions.objects.filter(name__iexact=name)
                    if flag:raise forms.ValidationError(_("This payment option is already added."))
                except PaymentOptions.DoesNotExist:pass
            return name 
    
    
Restaurant_Pay_Opt=(('True','Paid'),('False','Free'),)
Restaurant_Contract_Period=(('month','Month'),('year','Year'),)
Restaurant_Exposure=(('0','Standard'),('1',' 5X'),('2','10X'),('3','15X'),('4','20X'),('5','25X'),)
Restaurant_Features_Opt=(('Y','Yes'),('N','No'),)
Restaurant_Socialmedia_Options=(('N','No'),('T','Twitter'),('F','Facebook'),('B','FB + Twitter'),)

class RestaurantPriceForm(forms.ModelForm):
    level = forms.CharField(required=False, max_length="10", widget=forms.TextInput(attrs={'size':'30','class':'input_text'}), error_messages={'required': 'Title field Shouldn\'t be empty.'})
    level_visibility = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'onclick':'change_visiblity($(this))'}),error_messages={'required': 'Label content field Shouldn\'t be empty.'})
    level_label = forms.CharField(required=True, max_length=50, widget=forms.TextInput({'title':_('Label'),'readonly':'true',  'maxlength':'50', 'style':'height:21px;', 'autocomplete':'off'}), error_messages={'required': _('Label field Shouldn\'t be empty.')})
    exposure = forms.ChoiceField(required=True, choices=Restaurant_Exposure, widget=forms.Select(attrs={'class':'select-menu','style':'width:88px;'}), error_messages={'required': 'Exposure field Shouldn\'t be empty.'})
    images = forms.ChoiceField(required=True, choices=Restaurant_Features_Opt, widget=forms.Select(attrs={'class':'select-menu','style':'width:70px;'}), error_messages={'required': 'Image field Shouldn\'t be empty.'})
    videos = forms.ChoiceField(required=True, choices=Restaurant_Features_Opt, widget=forms.Select(attrs={'class':'select-menu','style':'width:70px;'}), error_messages={'required': 'Products field Shouldn\'t be empty.'})
    share_buttons = forms.ChoiceField(required=True, choices=Restaurant_Features_Opt, widget=forms.Select(attrs={'class':'select-menu','style':'width:70px;'}), error_messages={'required': 'Share Buttons field Shouldn\'t be empty.'})
    comments = forms.ChoiceField(required=True, choices=Restaurant_Features_Opt, widget=forms.Select(attrs={'class':'select-menu','style':'width:70px;'}), error_messages={'required': 'Comments field Shouldn\'t be empty.'})
    newsletter = forms.ChoiceField(required=True, choices=Restaurant_Features_Opt, widget=forms.Select(attrs={'class':'select-menu','style':'width:70px;'}), error_messages={'required': 'Newsletter field Shouldn\'t be empty.'})
    socialmedia = forms.ChoiceField(required = True, choices = Restaurant_Features_Opt, widget=forms.Select(attrs={'class':'select-menu','style':'width:70px;'}), error_messages={'required': 'Social Media Promotion field Shouldn\'t be empty.'})
    price_month = forms.FloatField(required=True,widget=forms.TextInput(attrs={'class':'textField','style':'width:40px; height:21px;'}), error_messages={'required': 'Price Month field Shouldn\'t be empty.','invalid': 'Price field should be a number'})
    price_year = forms.FloatField(required=True,widget=forms.TextInput(attrs={'class':'textField','style':'width:40px; height:21px;'}), error_messages={'required': 'Price Year field Shouldn\'t be empty.','invalid': 'Price field should be a number'})

    class Meta:
        model = RestaurantPrice
        exclude = ('level')
    
    
    
    
    
    
    
    
    
             
            