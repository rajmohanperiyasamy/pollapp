from django import forms
from bookmarks.models import *
from django.utils.translation import ugettext as _

class BookmarkCategoryForm(forms.ModelForm):
    name            = forms.CharField(required=True , max_length=200, widget=forms.TextInput({'class':'fm','title':'Category  Name','onkeyUp':'string_to_slug(this.value)','maxlength':'150','autocomplete':'off'}), error_messages={'required': 'Please enter the category name'})
    slug            = forms.CharField(required=False, widget=forms.TextInput({'class':'default-url','style':'width:128px;','title':'Category Slug','maxlength':'200','onkeyUp':'string_to_slug(this.value)','autocomplete':'off'}), error_messages={'required': 'Please enter the slug'})
    seo_title       = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'fm','title':'Meta Title','maxlength':'200','autocomplete':'off'}), error_messages={'required': 'Please enter the Meta title'})
    seo_description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'fm','title':'Meta Description','onkeyUp':'txtarealimit(this,400);','style':'overflow: hidden; height: 70px;'}), error_messages={'required': 'Please enter the Meta description'})
    class Meta:
        model = BookmarkCategory

class BookmarkForm(forms.ModelForm):
    title           = forms.CharField(required=True,  max_length=200, widget=forms.TextInput({}), error_messages={'required': 'Please enter the title'})
    slug            = forms.CharField(required=True,  max_length=250, error_messages={'required': 'Please enter the slug'})
    category        = forms.ModelChoiceField(required=True, widget=forms.Select(attrs={'class':'select-menu fl'}),queryset=BookmarkCategory.objects.all().order_by('name'), empty_label="",error_messages={'required': _('Please select the category')})
    summary         = forms.CharField(required=False,widget=forms.Textarea(attrs={'rows':'8','class':'fxl','rows':'8','cols':'40'}),error_messages={'required': _('Please enter the sumary')})
    class Meta:
        model = Bookmark
        fields = ('title','category','summary','slug')
    def clean_title(self):
        title = self.cleaned_data.get("title").strip()
        if len(title)>200:
            raise forms.ValidationError(_("Maximum length of title field is 200 characters."))
        else:
            return title  
    def clean_slug(self):
        slug = self.cleaned_data.get("slug")
        try:
            slug = Bookmark.objects.get(slug = slug)
        except:
            return slug
        raise forms.ValidationError(_("Maximum length of title field is 200 characters."))

class UserBookmarkForm(forms.ModelForm):
    title           = forms.CharField(required=True,  max_length=200, widget=forms.TextInput({'class': 'iSp8'}), error_messages={'required': 'Please enter the title'})
    category        = forms.ModelChoiceField(required=True, widget=forms.Select(attrs={'class':'iSp8 bM-sLt', 'title': 'Select a Category'}),queryset=BookmarkCategory.objects.all().order_by('name'), empty_label="",error_messages={'required': _('Please select the category')})
    summary         = forms.CharField(required=False,widget=forms.Textarea(attrs={'rows':'8','class':'iSp8','rows':'8','cols':'40'}),error_messages={'required': _('Please enter the sumary')})
    class Meta:
        model = Bookmark
        fields = ('title','category','summary')
        
    def clean_title(self):
        title = self.cleaned_data.get("title").strip()
        if len(title)>200:
            raise forms.ValidationError(_("Maximum length of title field is 200 characters."))
        else:
            return title
         

class BookmarkSeoForm(forms.ModelForm):
    #slug = forms.CharField(required=True, widget=forms.TextInput({'class':'default-url slug_input','style':'width:265px;','title':_('Bookmark Slug'),'maxlength':'200','onkeyUp':'string_to_slug(this.value)','autocomplete':'off'}), error_messages={'required': _('Please enter the slug')})
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
            
    class Bookmark:
        model = Bookmark
        fields=('seo_title','seo_description')

class UserBookmarkSeoForm(forms.ModelForm):
    #slug = forms.CharField(required=True, widget=forms.TextInput({'class':'default-url slug_input','style':'width:265px;','title':_('Bookmark Slug'),'maxlength':'200','onkeyUp':'string_to_slug(this.value)','autocomplete':'off'}), error_messages={'required': _('Please enter the slug')})
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
            
    class Bookmark:
        model = Bookmark
        fields=('seo_title','seo_description')


class BookmarkCategorySeoForm(forms.ModelForm):
    slug = forms.CharField(required=True, widget=forms.TextInput({'class':'default-url','style':'width:128px;','title':_('Category Slug'),'maxlength':'200','onkeyUp':'string_to_slug(this.value)','autocomplete':'off'}), error_messages={'required': _('Please enter the slug')})
    seo_title = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'fm','title':_('Meta Title'),'maxlength':'200'}), error_messages={'required': _('Please enter the Meta title')})
    seo_description = forms.CharField(required=True, widget=forms.Textarea(attrs={'class':'fm','title':_('Meta Description'),'onkeyUp':'txtarealimit(this,400);','style':'overflow: hidden; height: 70px;'}), error_messages={'required': _('Please enter the Meta description')})

    class Meta:
        model = BookmarkCategory
        exclude = ('name')

    def clean_seo_title(self):
        seo_title = self.cleaned_data.get("seo_title").strip()
        if len(seo_title) > 200:
            raise forms.ValidationError(_("Maximum length of meta-title field is 200 characters."))
        else: return seo_title
    def clean_seo_description(self):
        seo_description = self.cleaned_data.get("seo_description").strip()
        if len(seo_description) > 400:
            raise forms.ValidationError(_("Maximum length of meta-description field is 400 characters."))
        else:return seo_description
