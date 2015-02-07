from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()
from gallery.models import PhotoCategory,PhotoAlbum,AlbumComment
from common import captcha
from django.utils.translation import ugettext as _


class PhotoCategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        try:self._name = kwargs['instance'].name
        except:self._name= False
        super(PhotoCategoryForm, self).__init__(*args, **kwargs)
        
    name = forms.CharField(required=True,max_length=150, error_messages={'required': _('Please enter the name')},widget=forms.TextInput({'class':'fm','maxlength':'150','onkeyUp':'string_to_slug(this.value)','title':_('Category Name'),'autocomplete':'off'}))
    slug = forms.CharField(required=False, widget=forms.TextInput({'class':'default-url','style':'width:150px;','title':_('Category Slug'),'maxlength':'200','onkeyUp':'string_to_slug(this.value)','autocomplete':'off'}), error_messages={'required': _('Please enter the slug')})
    seo_title = forms.CharField(required=False,max_length=200, error_messages={'required': _('Please enter the Title')},widget=forms.TextInput(attrs={'class':'fm','maxlength':'200','title':_('Meta Title'),'autocomplete':'off'}))
    seo_description = forms.CharField(required=False,max_length=400, error_messages={'required': _('Please enter Description')},widget=forms.Textarea(attrs={'class':'fm','cols':30,'rows':5,'style':'height:70px;','title':_('Meta Description'),'onkeyUp':'txtarealimit(this,400);'}))
    
    def clean_name(self):
        name = self.cleaned_data.get("name").strip()
        if self._name:
            if str(self._name).lower() != str(name).lower():
                try:
                    flag=PhotoCategory.objects.filter(name__iexact=name)
                    if flag:raise forms.ValidationError(_("This category name is already added."))
                except PhotoCategory.DoesNotExist:pass
        else:
            try:
                flag=PhotoCategory.objects.filter(name__iexact=name)
                if flag:raise forms.ValidationError(_("This category name is already added."))
            except PhotoCategory.DoesNotExist:pass
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
            
    class Meta:
        model = PhotoCategory
        exclude = ('created_by','modified_by','is_active','status','is_editable')
    
        
    

class PhotoCategorySeoForm(forms.ModelForm):
    slug = forms.CharField(required=True, widget=forms.TextInput({'class':'default-url','style':'width:150px;','title':_('Category Slug'),'maxlength':'200','onkeyUp':'string_to_slug(this.value)','autocomplete':'off'}), error_messages={'required': _('Please enter the slug')})
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
        model = PhotoCategory
        exclude = ('name','created_by','modified_by','is_active','status')

class TagForm(forms.Form):
    tags = forms.CharField(required=True,widget=forms.Textarea(),error_messages={'required': 'Please enter the tags'})
    def clean_tags(self):
        tags = self.cleaned_data.get("tags")
        tags=tags.strip()
        if tags=='':
            raise forms.ValidationError("Blank space is not allowed for tags field")
        else:
            tagarray = tags.split(',')
            for tag in tagarray:
                if len(tag)>150:
                    raise forms.ValidationError("Maximum length of tags field is 150 charector.")
            return tags

class UserGalleryForm(forms.ModelForm):
    title = forms.CharField(required=True,max_length=200,widget=forms.TextInput(attrs={'class':'iSp8','maxlength':'200','placeholder':_('Untitled Gallery'),'title':_('Gallery Title')}),error_messages={'required': _('Please enter the title')})
    summary = forms.CharField(required=False,max_length=2000, error_messages={'required':_('Please enter the summary')}, widget=forms.Textarea(attrs={'maxlength':'2000', 'class':'iSp8','placeholder':_('Gallery Description'),'title':_('Gallery Description'),'rows':'4'}))
    category = forms.ModelChoiceField(required=False, widget=forms.Select(attrs={'data-placeholder':_('Please select the category'),'class':'iSp8 bM-sLt'}),queryset=PhotoCategory.objects.filter(is_editable=True).order_by('name'),empty_label="",error_messages={'required': 'Please select the category'})
   
    #related_articles = forms.URLField(required=False,error_messages={'required': 'Please enter the article url'},max_length="250", widget=forms.TextInput(attrs={'class':'textField long','style':'padding:4px 3px; font-size:14px;'}))
    #related_events = forms.URLField(required=False,error_messages={'required': 'Please enter the event url'},max_length="250", widget=forms.TextInput(attrs={'class':'textField long','style':'padding:4px 3px; font-size:14px;'}))
    class Meta:
        model = PhotoAlbum
        fields=('title','summary','category')

class GalleryForm(forms.ModelForm):
    title = forms.CharField(required=True,max_length=200,widget=forms.TextInput(attrs={'class':'fl','maxlength':'200','placeholder':_('Untitled Gallery'),'title':_('Gallery Title')}),error_messages={'required': _('Please enter the title')})
    summary = forms.CharField(required=False,max_length=2000,widget=forms.Textarea(attrs={'class':'fl','maxlength':'2000','placeholder':_('Gallery Description'),'title':_('Gallery Description'),'rows':'4'}),error_messages={'required':_('Please enter the summary')})
    category = forms.ModelChoiceField(required=False, widget=forms.Select(attrs={'data-placeholder':_('Please select the category'),'class':'select-menu fl'}),queryset=PhotoCategory.objects.filter(is_editable=True).order_by('name'),empty_label="",error_messages={'required': 'Please select the category'})

    #related_articles = forms.URLField(required=False,error_messages={'required': 'Please enter the article url'},max_length="250", widget=forms.TextInput(attrs={'class':'textField long','style':'padding:4px 3px; font-size:14px;'}))
    #related_events = forms.URLField(required=False,error_messages={'required': 'Please enter the event url'},max_length="250", widget=forms.TextInput(attrs={'class':'textField long','style':'padding:4px 3px; font-size:14px;'}))
    class Meta:
        model = PhotoAlbum
        fields=('title','summary','category')

        
class GallerySEOForm(forms.ModelForm):
    #slug = forms.CharField(required=True, widget=forms.TextInput({'class':'default-url slug_input','style':'width:265px;','title':_('Category Slug'),'maxlength':'200','onkeyUp':'string_to_slug(this.value)','autocomplete':'off'}), error_messages={'required': _('Please enter the slug')})
    seo_title = forms.CharField(required=True,max_length=70,widget=forms.TextInput(attrs={'class':'fm','maxlength':70,'title':_('Meta Title'),'autocomplete':'off'}), error_messages={'required': _('Please enter the Meta Title')})
    seo_description = forms.CharField(required=True,max_length=160,widget=forms.Textarea(attrs={'class':'fxl','maxlength':160,'cols':30,'rows':4,'style':'height:70px;','title':_('Meta Description'),'onkeyUp':'txtarealimit(this,400);'}), error_messages={'required': _('Please enter the Meta Keyword')})
    
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
        model = PhotoAlbum
        fields = ('seo_title','seo_description')

class UserGallerySEOForm(forms.ModelForm):
    seo_title = forms.CharField(required=True,max_length=70,widget=forms.TextInput(attrs={'class':'iSp8','maxlength':'70','title':_('Meta Title'),'autocomplete':'off'}), error_messages={'required': _('Please enter the Meta Title')})
    seo_description = forms.CharField(required=True,max_length=160,widget=forms.Textarea(attrs={'class':'iSp8','cols':30,'rows':4,'style':'height:70px;','title':_('Meta Description'),'onkeyUp':'txtarealimit(this,160);'}), error_messages={'required': _('Please enter the Meta Keyword')})
    
    def clean_seo_title(self):
        seo_title = self.cleaned_data.get("seo_title").strip()
        if len(seo_title) > 70:
            raise forms.ValidationError(_("Maximum length of seo-title field is 70 characters."))
        else:
            if seo_title: return seo_title
            else:return self.cleaned_data.get("name")
    def clean_seo_description(self):
        seo_description = self.cleaned_data.get("seo_description").strip()
        if len(seo_description) > 160:
            raise forms.ValidationError(_("Maximum length of seo-description field is 160 characters."))
        else:
            if seo_description: return seo_description
            else:return self.cleaned_data.get("name")
            
    class Meta:
        model = PhotoAlbum
        fields = ('seo_title','seo_description')
 
        
class EditGalleryForm(forms.ModelForm):
    title = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'textField long','style':'padding:4px 3px; font-size:14px;'}),error_messages={'required': 'Please enter the title'})
    caption = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'textField long','style':'padding:4px 3px; font-size:14px;'}),error_messages={'required': 'Please enter the name'})
    summary = forms.CharField(required=True,error_messages={'required': 'Please enter the summary'},max_length="350", widget=forms.Textarea(attrs={'class':'textField long','style':'padding:4px 3px; font-size:14px;height:80px'}))
    category = forms.ModelChoiceField(required=True, widget=forms.Select(attrs={'class':'textField normal','id':'id_categories0','onchange':'loadsubcategory(0)'}),queryset=PhotoCategory.objects.filter().order_by('name'), empty_label="--Please select the category--",error_messages={'required': 'Please select the category'})
    sub_category = forms.CharField(required=False)
    related_articles = forms.URLField(required=False,error_messages={'required': 'Please enter the article url'},max_length="250", widget=forms.TextInput(attrs={'class':'textField long','style':'padding:4px 3px; font-size:14px;'}))
    related_events = forms.URLField(required=False,error_messages={'required': 'Please enter the event url'},max_length="250", widget=forms.TextInput(attrs={'class':'textField long','style':'padding:4px 3px; font-size:14px;'}))
    class Meta:
        model = PhotoAlbum
        exclude = ('created_by','modified_by','flickr_date','is_active','status','tags','related_articles','related_events','sub_category','slug','most_viewed','like_count','seo_title','seo_description','albumurl')

    def clean_title(self):    
         return validate_blank_space(self.cleaned_data.get("title"),'title')
   
    def clean_summary(self):    
         return validate_blank_space(self.cleaned_data.get("summary"),'summary')    

class GalleryFormUserSide(forms.ModelForm):
    title = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'textField long','style':'padding:4px 3px; font-size:14px;'}),error_messages={'required': 'Please enter the title'})
    caption = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'textField long','style':'padding:4px 3px; font-size:14px;'}),error_messages={'required': 'Please enter the name'})
    summary = forms.CharField(required=True,error_messages={'required': 'Please enter the summary'},max_length="350", widget=forms.Textarea(attrs={'class':'textField long','style':'padding:4px 3px; font-size:14px;height:80px'}))
    category = forms.ModelChoiceField(required=True, widget=forms.Select(attrs={'class':'textField normal','id':'id_category'}),queryset=PhotoCategory.objects.all().order_by('name'), empty_label="--Please select the category--",error_messages={'required': 'Please select the category'})
    albumurl = forms.URLField(required=False,error_messages={'required': 'Please enter the albumurl'},max_length="200", widget=forms.TextInput(attrs={'class':'textField long','style':'padding:4px 3px; font-size:14px;'}))
    tags = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'textField long','style':'padding:4px 3px; font-size:14px;'}),error_messages={'required': 'Please enter the keyword'})
    class Meta:
        model = PhotoAlbum
        exclude = ('created_by','modified_by','flickr_date','is_active','status','tags','related_articles','related_events','slug','most_viewed','like_count','seo_title','seo_description')
   
    def clean_title(self):    
         return validate_blank_space(self.cleaned_data.get("title"),'title')     
    
    def clean_summary(self):    
         return validate_blank_space(self.cleaned_data.get("summary"),'summary')    


SORT_TYPE = (('relevance', 'Relevance'),
              ('date-posted-asc','Last Posted'),
              ('date-posted-desc', 'First Posted'),
              ('interestingness-asc', 'Interesting'))
class SearchForm(forms.Form):
    tag = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'textField long','style':'padding:4px 3px; font-size:14px;'}),error_messages={'required': 'Please enter the tag'})
    title = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'textField small','style':'padding:4px 3px; font-size:14px;'}),error_messages={'required': 'Please enter the title'})
    per_page = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'textField small','style':'padding:4px 3px; font-size:14px;','value':'20'}),error_messages={'required': 'Please enter how many photos per page'})
    page = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'textField small','style':'padding:4px 3px; font-size:14px;','value':'1'}),error_messages={'required': 'Please enter the page number'})
    sort = forms.CharField(required=True,widget=forms.Select(attrs={'class':'textField normal'},choices=SORT_TYPE), error_messages={'required': 'Please select the sort'})


class PhotoForm(forms.Form):
    title = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'textField long','style':'padding:4px 3px; font-size:14px;'}),error_messages={'required': 'Please enter the title'})
    caption = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'textField long','style':'padding:4px 3px; font-size:14px;'}),error_messages={'required': 'Please enter the caption'})
    summary = forms.CharField(required=False,error_messages={'required': 'Please enter the summary'},max_length="350", widget=forms.Textarea(attrs={'class':'textField long','style':'padding:4px 3px; font-size:14px;height:80px'}))


class AlbumCommentForm(forms.ModelForm):
    title = forms.CharField(required=False, max_length="100", widget=forms.TextInput(attrs={'size':'30','class':'input_text'}), error_messages={'required': 'Please enter the title'})
    name = forms.CharField(required=True, max_length="75", widget=forms.TextInput(attrs={'size':'30','class':'input_text'}), error_messages={'required': 'Please enter the name'})
    email=  forms.EmailField(required=True, max_length="150", widget=forms.TextInput(attrs={'size':'30','class':'input_text'}), error_messages={'required': 'Please enter the email.'})
    comment = forms.CharField(required=True, max_length="350", widget=forms.Textarea(attrs={'class':'large','rows':'8','cols':'30'}), error_messages={'required': 'Please enter the comment'})
    hashkey = forms.CharField(required=True, error_messages={'required': 'Please reload the page.'})
    hashvalue = forms.CharField(required=True, max_length="3", widget=forms.TextInput(attrs={'size':'10', 'class':'input_text captcha_field'}), error_messages={'required': 'Please enter the Image Key.'})
    def clean_hashvalue(self):
        hashkey = self.cleaned_data.get("hashkey")
        hashvalue = self.cleaned_data.get("hashvalue")
        if not captcha.checkCaptcha(hashkey,hashvalue):
            raise forms.ValidationError("Wrong Image key! Please re-enter the text in the image.")
        else:
            return hashkey
    class Meta:
        model = AlbumComment
        exclude = ('album','created_by','approved_on','status','abuse_count','like_count')


#SEO
class SEOHomeForm(forms.Form):
    meta_title = forms.CharField(required=True,max_length="200",error_messages={'required': 'Please enter the meta title'})
    meta_description = forms.CharField(required=True,widget=forms.Textarea(),error_messages={'required': 'Please enter the meta description'})
    meta_keywords = forms.CharField(required=True,widget=forms.Textarea(),error_messages={'required': 'Please enter the meta keywords'})
    def clean_meta_title(self):
        meta_title = self.cleaned_data.get("meta_title")
        if len(meta_title)>200:
            raise forms.ValidationError("Maximum length of metakeyword field is 200 characters.")
        elif meta_title.strip() == '':
            raise forms.ValidationError("Please enter the meta title")
        else:
            return meta_title
    def clean_meta_description(self):
        meta_description = self.cleaned_data.get("meta_description")
        if len(meta_description)>400:
            raise forms.ValidationError("Maximum length of metadescription field is 400 characters.")
        elif meta_description.strip() == '':
            raise forms.ValidationError("Please enter the meta description")
        else:
            return meta_description
    def clean_meta_keywords(self):
        meta_keywords = self.cleaned_data.get("meta_keywords")
        if len(meta_keywords)>350:
            raise forms.ValidationError("Maximum length of metadescription field is 350 characters.")
        elif meta_keywords.strip() == '':
            raise forms.ValidationError("Please enter the meta keywords")
        else:
            return meta_keywords


#SEO Category
class SEOForm(forms.Form):
    slug = forms.CharField(required=True,max_length="200",error_messages={'required': 'Please enter the slug'})
    meta_title = forms.CharField(required=True,max_length="200",error_messages={'required': 'Please enter the meta title'})
    meta_description = forms.CharField(required=True,widget=forms.Textarea(),error_messages={'required': 'Please enter the meta description'})
    meta_keywords = forms.CharField(required=True,widget=forms.Textarea(),error_messages={'required': 'Please enter the meta keywords'})
    def clean_meta_title(self):
        meta_title = self.cleaned_data.get("meta_title")
        if len(meta_title)>200:
            raise forms.ValidationError("Maximum length of metakeyword field is 200 characters.")
        elif meta_title.strip() == '':
            raise forms.ValidationError("Please enter the meta title")
        else:
            return meta_title
    def clean_meta_description(self):
        meta_description = self.cleaned_data.get("meta_description")
        if len(meta_description)>400:
            raise forms.ValidationError("Maximum length of metadescription field is 400 characters.")
        elif meta_description.strip() == '':
            raise forms.ValidationError("Please enter the meta description")
        else:
            return meta_description
    def clean_meta_keywords(self):
        meta_keywords = self.cleaned_data.get("meta_keywords")
        if len(meta_keywords)>350:
            raise forms.ValidationError("Maximum length of metadescription field is 350 characters.")
        elif meta_keywords.strip() == '':
            raise forms.ValidationError("Please enter the meta keywords")
        else:
            return meta_keywords

def validate_blank_space(data,field):
    data = data.strip()
    if data == '':
        error='Blank space is not allowed for ' +field+ ' field'
        raise forms.ValidationError(error)
    else:
        return data 