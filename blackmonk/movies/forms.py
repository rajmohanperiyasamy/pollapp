from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()
from django.forms import ModelForm
from django.forms.util import ErrorList
from django.utils.translation import ugettext as _

from common import captcha
from common.models import ModuleNames,Address


from movies.models import Movies,MovieLanguage,MovieType,CriticSource,Theatres,CriticReview
from locality.models import Locality



class AddMovieForm(ModelForm):
    title = forms.CharField(required=True,max_length=300,widget=forms.TextInput(attrs={'maxlength':'300','placeholder':_('Movie Name '),'title':_('Movie Name')}), error_messages={'required': 'Movie title required'})
    release_date = forms.DateField(required=False,widget=forms.DateInput(attrs={'placeholder':_('DD/MM/YY'),'class':'textField long fs', 'style':'margin-top:2px;','autocomplete':'off','title':_('Movie release date')}), error_messages={'required': 'Movie release date required'})
    movie_url = forms.CharField(required=False,max_length=200,widget=forms.TextInput(attrs={'maxlength':'200','class':'fl', 'placeholder':_('http://www.youtube.com/watch?v=oX9ZT3RbYE4&feature=fvsr'),'title':_('Movie Trailor Youtube Link ')}), error_messages={'required': 'Movie release date required'})
    image=forms.ImageField(required=False, error_messages={'required': 'Please upload the image'})
    web = forms.CharField(required=False,max_length=300,widget=forms.TextInput(attrs={'maxlength':'300','onfocus':'showhttp(4)','onblur':'hidehttp(4)','class':'fl', 'placeholder':_('http://www.mymovie.com'),'title':_('official web Link')}), error_messages={'required': 'Link Is Required'})
    duration_hours = forms.CharField(required=False,max_length=100,widget=forms.TextInput(attrs={'maxlength':'100','style':'margin-top:2px;','class':'fs','placeholder':_('2.02'),'title':_('Movie Runtime')}), error_messages={'required': 'Movie Runtime required'})
    certification = forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs={'style':'margin-top:2px;','class':'fs','placeholder':_('example:PG-13'),'title':_('Movie Rating/Certification')}), error_messages={'required': 'Movie rating required'})
    movie_type = forms.ModelMultipleChoiceField(required=True,queryset=MovieType.objects.all(), widget=forms.SelectMultiple(attrs={'class':'select-menu fl','title':_('Movie Type'),'data-placeholder':_('Select the movie type')}),error_messages={'required': 'Movie Type required'})

   # web=forms.CharField(required=False,widget=forms.TextInput(attrs={'placeholder':_('Example: http://www.example.com'),'class':'textField long', 'style':'height:22px;'}), error_messages={'required': 'Movie genre required'})
    language = forms.ModelChoiceField(required=True,queryset=MovieLanguage.objects.all(),empty_label="Select Language",widget=forms.Select(attrs={'class':'select-menu fl','title':_('Movie Language')}), error_messages={'required': 'Please select a language type'})
    director = forms.CharField(required=False,widget=forms.Textarea(attrs={'class':'fl', 'cols':8, 'rows':2,'title':_('Movie Director')}), error_messages={'required': 'Movie director required'})
    cast = forms.CharField(required=False,widget=forms.Textarea(attrs={'class':'fl','title':_('Movie Cast'), 'cols':8, 'rows':2,}), error_messages={'required': 'Movie cast required'})
    writer = forms.CharField(required=False,max_length=100,widget=forms.Textarea(attrs={'maxlength':'100','class':'fl', 'cols':8, 'rows':2,'title':_('Script Writer') }), error_messages={'required': _('Movie Writer required')})
    synopsis = forms.CharField(required=False,min_length=1, widget=forms.Textarea(attrs={'rows':'4','class':'fxl','title':_('About Movie ')}), label=("synopsis"),error_messages={'required': u'Movie synopsis required.'})
    facebook_url = forms.CharField(required=False,max_length=150, error_messages={'required':_('Please enter the Facebook URL')},widget=forms.TextInput(attrs={'style':'width:329px;','class':'tttxt-fw-focus','onfocus':'showhttp(2)','onblur':'hidehttp(2)','title':'Facebook: Enter Facebook fanpage of the movie listing.','placeholder':_('Example: https://www.facebook.com/page'),'autocomplete':'off'}))
    googleplus = forms.CharField(required=False,max_length=150, error_messages={'required': _('Please enter the Google+ URL')},widget=forms.TextInput(attrs={'style':'width:329px;','class':'tttxt-fw-focus','onfocus':'showhttp(3)','onblur':'hidehttp(3)','title':'Google+: Enter Google+ page name of the movie listing','placeholder':_('Example: https://plus.google.com/page'),'autocomplete':'off'}))
    
    class Meta:
        model = Movies
        fields = ('title','release_date','movie_url','image','duration_hours','movie_type','web','language','director','cast','writer','synopsis','facebook_url','googleplus','certification')

    
class AddCriticsSource(forms.ModelForm):
    source_title= forms.CharField(required=True,max_length=100,widget=forms.TextInput(attrs={'maxlength':'100','placeholder':_('Critic Source Title '),'style':'width:250px;','title':_('Critic Source Title')}), error_messages={'required': 'Critic Source title required'})
    url= forms.URLField(required=True,max_length=2000,widget=forms.TextInput(attrs={'placeholder':_('Critic Source url '),'style':'width:250px;','title':_('Critic Source url')}), error_messages={'required': 'Critic Source url required'})
    #logo = forms.ImageField(required=False, error_messages={'required': 'Please upload the image'})
    copyright= forms.CharField(required=True,max_length=100,widget=forms.TextInput(attrs={'placeholder':_('Critic Source copyright '),'style':'width:250px;','title':_('Critic Source copyright')}), error_messages={'required': 'Critic Source copyright required'})
    
    def clean_source_title(self):
       source_title = self.cleaned_data.get('source_title')
       if source_title.strip()=='':
          raise  forms.ValidationError(_("Source Title should not start with  blank spaces"))
       else:
        return source_title
    class Meta:
        model =  CriticSource 
        fields = ('source_title','url','copyright')


class AddressForm(forms.ModelForm):#globalsettings.city
    address1 = forms.CharField(required=True,max_length=200,widget=forms.TextInput(attrs={ 'maxlength':'200','class':'fm'}), error_messages={'required': 'Please enter theatre address'})
    address2 =  forms.CharField(required=False,max_length=200,widget=forms.TextInput(attrs={ 'maxlength':'200','class':'fm'}), error_messages={'required': 'Please enter theatre address'}) 
    website= forms.URLField(required=False,max_length=250,widget=forms.TextInput(attrs={ 'maxlength':'250','class':'fm'}), error_messages={'required': 'Please enter a Valid Url'})
    email= forms.EmailField(required=False,max_length=75,widget=forms.TextInput(attrs={'maxlength':'75', 'class':'fm'}), error_messages={'required': 'Please enter a valid Email Id'})
    telephone1 = forms.CharField(required=False,max_length=20,widget=forms.TextInput(attrs={'maxlength':'20','class':'fm'}), error_messages={'required': 'Please enter integers only'})
    zip = forms.CharField(required=True,max_length=16,widget=forms.TextInput(attrs={'maxlength':'16','class':'fm'}), error_messages={'required': 'ZipCode is required'})


    class Meta:
        model = Address
        exclude = ('type','description','mobilemobile_no','fax','city','address_type','venue','lat','lon','zoom','status','telephone2','is_active','created_on','created_by','modified_on','modified_by','seo_title','seo_description')



class AddTheatreForm(forms.ModelForm):
    name = forms.CharField(required=True,max_length=200,widget=forms.TextInput(attrs={ 'maxlength':'200','class':'fm'}),error_messages={'required': 'Please enter theatre name'})
    image = forms.ImageField(required=False, error_messages={'required': 'Please upload the image'})
    tkt_url = forms.URLField(required=False,max_length=300,widget=forms.TextInput(attrs={ 'maxlength':'300','class':'fm'}),)
    boxoffice_no = forms.CharField(required=False,max_length=300,widget=forms.TextInput(attrs={ 'maxlength':'300','class':'fm'}),)
    '''def clean_name(self):
       name = self.cleaned_data.get('name')
       if name.strip()=='':
          raise  forms.ValidationError('Name should not start with  blank spaces ')
       else:
          return name
    def clean_pincode(self):
        import re
        pincode = self.cleaned_data.get('pincode')
        pattern = r'[^\.A-Z0-9-]'
        if re.search(pattern, pincode):
            raise  forms.ValidationError('should contain only  alphanumeric character in capital letters')
        else:
            return pincode
    '''
       
    class Meta:
        model = Theatres
        fields = ('name','boxoffice_no','image','tkt_url')


class AddMovieCriticsReviewForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        try:cr_reviews = kwargs.pop('cr_reviews')
        except:cr_reviews= []
        super(AddMovieCriticsReviewForm, self).__init__(*args, **kwargs)
        self.fields['source'].widget = forms.Select(attrs={'class':'lb_select-menu fl','data-placeHolder':'Select Critic Source'})
        self.fields['source'].queryset = CriticSource.objects.all().exclude(id__in=cr_reviews)
        self.fields['source'].required = True
        self.fields['source'].empty_label = ''
        self.fields['source'].error_messages = {'required': 'Please a select a language type'}
        
    #source = forms.ModelChoiceField(required=True,queryset=CriticSource.objects.all(),widget=forms.Select(attrs={'class':'lb_select-menu','style':'width:354px','data-placeHolder':'Select Critic Source'}),empty_label="", error_messages={'required': 'Please a select a language type'})
    title = forms.CharField(required=True,max_length=200,widget=forms.TextInput(attrs={'maxlength':'200','class':'fl','autocomplete':'off'}), error_messages={'required': 'Please Enter the Title'})
    reviewed_by = forms.CharField(required=True,max_length=30,widget=forms.TextInput(attrs={'maxlength':'30','class':'fl','autocomplete':'off'}), error_messages={'required': 'Please Enter the reviewed by name'})
    published_on =  forms.DateTimeField(required=False,input_formats='%Y-%m-%d',widget=forms.DateInput(attrs={'class':'textField long', 'style':'height:18px;width:130px;'}), error_messages={'required': 'Please select the date'})
    review = forms.CharField(required=True,min_length=1, max_length=5000, widget=forms.Textarea(attrs={ 'maxlength':'5000','cols':50, 'rows':10, 'style':'height:120px;'}), label=("review"),error_messages={'required': u'This is not a valid Review please enter some value.'})
    rating = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'tttxt', 'style':'height:18px;width:230px;'}), error_messages={'required': 'Please Enter the Rating'})

    def clean_name(self):
       source = self.cleaned_data.get('source')
       if source.strip()=='':
          raise  forms.ValidationError(_("source should not start with  blank spaces "))
       else:
          return source
 
    
    class Meta:
         model = CriticReview
         fields = ('title','source','reviewed_by','review','rating')
         
         
class MovieTypeForm(forms.ModelForm):
    name = forms.CharField(required=True,max_length=200, error_messages={'required': _('Please enter the Movie Genre')},widget=forms.TextInput({'class':'fm','maxlength':'120','onkeyUp':'string_to_slug(this.value)','title':_('Genre'),'autocomplete':'off'}))
    slug = forms.CharField(required=False, widget=forms.TextInput({'class':'default-url','title':_('Category Slug'),'maxlength':'200','onkeyUp':'string_to_slug(this.value)','autocomplete':'off','style':'width:117px'}), error_messages={'required': _('Please enter the slug')})
    seo_title = forms.CharField(required=False,max_length=200, error_messages={'required': _('Please enter the Title')},widget=forms.TextInput(attrs={'class':'fm','maxlength':'200','title':_('Meta Title'),'autocomplete':'off'}))
    seo_description = forms.CharField(required=False,max_length=400, error_messages={'required': _('Please enter Description')},widget=forms.Textarea(attrs={'class':'fm','cols':30,'rows':5,'style':'height:70px;','title':_('Meta Description'),'onkeyUp':'txtarealimit(this,400);'}))
    
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
            
    class Meta:
        model = MovieType


class MovieTypeSEOForm(forms.ModelForm):
    #slug = forms.CharField(required=False, widget=forms.TextInput({'class':'default-url','title':_('Category Slug'),'maxlength':'200','onkeyUp':'string_to_slug(this.value)','autocomplete':'off','style':'width:117px'}), error_messages={'required': _('Please enter the slug')})
    seo_title = forms.CharField(required=True,max_length=200,widget=forms.TextInput(attrs={'class':'fm','maxlength':'200','title':_('Meta Title'),'autocomplete':'off'}), error_messages={'required': _('Please enter the Meta Title')})
    seo_description = forms.CharField(required=True,max_length=400,widget=forms.Textarea(attrs={'maxlength':'400','class':'fxl','cols':30,'rows':4,'style':'height:70px;','title':_('Meta Description')}), error_messages={'required': _('Please enter the Meta Keyword')})
    
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
        model = Movies
        fields = ('seo_title','seo_description')

class MovieLanguageForm(forms.ModelForm):
    name = forms.CharField(required=True,max_length=40, error_messages={'required': _('Please enter the Language')},widget=forms.TextInput({'class':'fm','style':'width:250px;','maxlength':'120','onkeyUp':'string_to_slug(this.value)','title':_('Language'),'autocomplete':'off'}))

    class Meta:
        model = MovieLanguage
        
        
class TheatresSEOFORM(forms.ModelForm):    
    theatreseo_title = forms.CharField(required=True,max_length=200,widget=forms.TextInput(attrs={'class':'tttxt','maxlength':'200','title':_('Meta Title'),'autocomplete':'off'}), error_messages={'required': _('Please enter the Meta Title')})
    theatreseo_description = forms.CharField(required=True,max_length=400,widget=forms.Textarea(attrs={'maxlength':'400','class':'fxl','cols':30,'rows':4,'style':'height:70px;','title':_('Meta Description')}), error_messages={'required': _('Please enter the Meta Keyword')})
    
    def clean_seo_title(self):
        theatreseo_title = self.cleaned_data.get("theatreseo_title").strip()
        if len(theatreseo_title) > 200:
            raise forms.ValidationError(_("Maximum length of theatreseo_title field is 200 characters."))
        else:
            if theatreseo_title: return theatreseo_title
            else:return self.cleaned_data.get("name")
    def clean_seo_description(self):
        theatreseo_description = self.cleaned_data.get("theatreseo_description").strip()
        if len(theatreseo_description) > 400:
            raise forms.ValidationError(_("Maximum length of theatreseo_description field is 400 characters."))
        else:
            if theatreseo_description: return theatreseo_description
            else:return self.cleaned_data.get("name")
    
    class Meta:
        model = Theatres
        fields = ('theatreseo_title','theatreseo_description')