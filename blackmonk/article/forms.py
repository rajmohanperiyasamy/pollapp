from django import forms
from article.models import ArticleCategory,Article,ArticlePrice
from django.utils.translation import ugettext as _
from django.template.defaultfilters import slugify

attrs_dict = { 'class': 'required' }
attrs_tags = { 'class': 'tagclass' }
Article_Pay_Options=(
                    ('True','Paid'),
                    ('False','Free'),
                    )
TEMPLATE_CHOICES = (('temp1', 'Template 1'), ('temp2', 'Template 2'))
valid_date_formats = ['%m/%d/%Y']


class ArticleCategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        try:self._name = kwargs['instance'].name
        except:self._name= False
        super(ArticleCategoryForm, self).__init__(*args, **kwargs)

    name = forms.CharField(required=True,max_length=150, widget=forms.TextInput({'class':'fm','title':_('Category  Name'),'onkeyUp':'string_to_slug(this.value)','maxlength':'150','autocomplete':'off'}), error_messages={'required': _('Please enter the category name')})
    slug = forms.CharField(required=False, widget=forms.TextInput({'class':'default-url','style':'width:152px;','title':_('Category Slug'),'maxlength':'200','onkeyUp':'string_to_slug(this.value)','autocomplete':'off'}), error_messages={'required': _('Please enter the slug')})
    seo_title = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'fm','title':_('Meta Title'),'maxlength':'200','autocomplete':'off'}), error_messages={'required': _('Please enter the Meta title')})
    seo_description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'fm','title':_('Meta Description'),'onkeyUp':'txtarealimit(this,400);','style':'overflow: hidden; height: 70px;max-width:363px;'}), error_messages={'required': _('Please enter the Meta description')})
    class Meta:
        model = ArticleCategory

    def clean_name(self):
        name = self.cleaned_data.get("name").strip()
        if self._name:
            if str(self._name).lower() != str(name).lower():
                try:
                    flag=ArticleCategory.objects.filter(name__iexact=name)
                    if flag:raise forms.ValidationError(_("This category name is already added."))
                except ArticleCategory.DoesNotExist:pass
        else:
            try:
                flag=ArticleCategory.objects.filter(name__iexact=name)
                if flag:raise forms.ValidationError(_("This category name is already added."))
            except ArticleCategory.DoesNotExist:pass
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


class ArticleCategorySeoForm(forms.ModelForm):
    slug = forms.CharField(required=True, widget=forms.TextInput({'class':'default-url','style':'width:152px;','title':_('Category Slug'),'maxlength':'200','onkeyUp':'string_to_slug(this.value)','autocomplete':'off'}), error_messages={'required': _('Please enter the slug')})
    seo_title = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'fm','title':_('Meta Title'),'maxlength':'200'}), error_messages={'required': _('Please enter the Meta title')})
    seo_description = forms.CharField(required=True, widget=forms.Textarea(attrs={'class':'fm','title':_('Meta Description'),'onkeyUp':'txtarealimit(this,400);','style':'overflow: hidden; height: 70px;'}), error_messages={'required': _('Please enter the Meta description')})
    class Meta:
        model = ArticleCategory
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

class ArticleSeoForm(forms.ModelForm):
    #slug = forms.CharField(required=True, widget=forms.TextInput({'class':'default-url slug_input','style':'width:157px;','title':_('Article Slug'),'maxlength':'200','onkeyUp':'string_to_slug(this.value)','autocomplete':'off'}), error_messages={'required': _('Please enter the slug')})
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

    class Article:
        model = Article
        fields=('seo_title','seo_description')

class UserArticleSeoForm(forms.ModelForm):
    seo_title = forms.CharField(required=True,max_length=70, error_messages={'required': _('Please enter the Title')},widget=forms.TextInput(attrs={'class':'iSp8','maxlength':70,'title':_('Meta Title'),'autocomplete':'off'}))
    seo_description = forms.CharField(required=True,max_length=160, error_messages={'required': _('Please enter Description')},widget=forms.Textarea(attrs={'class':'iSp8','maxlength':160,'cols':30,'rows':4,'style':'height:70px;','title':_('Meta Description'),'onkeyUp':'txtarealimit(this,400);'}))

    def clean_seo_title(self):
        seo_title = self.cleaned_data.get("seo_title").strip()
        if len(seo_title) > 70:
            raise forms.ValidationError(_("Maximum length of seo title field is 70 characters."))
        else:
            if seo_title: return seo_title
            else:return self.cleaned_data.get("name")
    def clean_seo_description(self):
        seo_description = self.cleaned_data.get("seo_description").strip()
        if len(seo_description) > 160:
            raise forms.ValidationError(_("Maximum length of seo description field is 160 characters."))
        else:
            if seo_description: return seo_description
            else:return self.cleaned_data.get("name")

    class Article:
        model = Article
        fields=('seo_title','seo_description')


class ArticleStaffForm(forms.ModelForm):
    title = forms.CharField(required=True,max_length=150,widget=forms.TextInput(attrs={'placeholder':_('Enter Article Title'),'autocomplete':'off','onkeyUp':'string_to_slug(this.value)'}),error_messages={'required': _('Please enter the  title')})
    category = forms.ModelChoiceField(required=True, widget=forms.Select(attrs={'class':'select-menu fl','data-placeholder':_('Choose a category')}),queryset=ArticleCategory.objects.all().order_by('name'), empty_label="",error_messages={'required': _('Please select the category')})
    summary = forms.CharField(required=True, max_length=250,widget=forms.Textarea(attrs={'maxlength':250,'style':'max-width:566px;', 'rows': '4','class': 'fl', 'placeholder': "Enter a short summary concerning about this article in this text box"}),error_messages={'required': _('Please enter the summary')})
    content = forms.CharField(required=True,widget=forms.Textarea(attrs={'rows':'8'}),error_messages={'required': _('Please enter the content')})
    gallery_url = forms.URLField(required=False, max_length=250, widget=forms.TextInput(attrs={'placeholder':_('Example : http://www.example.com/gallery_name'),'class':'fl'}), error_messages={'invalid':_('Invalid gallery url.')})
    published_on = forms.DateField(required=True, input_formats=valid_date_formats, widget=forms.DateInput(format='%m/%d/%Y',attrs={'class':'fxs','style':'margin-right:7px;','autocomplete':'off'}), error_messages={'required': _('Published date Required')})

    class Meta:
        model = Article
        fields = ('title','summary','content','category','gallery_url', 'published_on')

    def clean_title(self):
        title = self.cleaned_data.get("title").strip()
        if len(title)>150:
            raise forms.ValidationError(_("Maximum length of title field is 150 characters."))
        else:
            return title
    def clean_summary(self):
        summary = self.cleaned_data.get("summary").strip()
        if len(summary)>250:
            raise forms.ValidationError(_("Maximum length of summary field is 250 characters."))
        else:
            return summary
    def clean_content(self):
        content = self.cleaned_data.get("content").strip()
        if len(content)==0:
            raise forms.ValidationError(_("Please enter the description."))
        else:
            return content
        
class ArticleUserForm(forms.ModelForm):
    title = forms.CharField(required=True,max_length=150,widget=forms.TextInput(attrs={'class': 'iSp8','placeholder':_('Enter Article Title'),'autocomplete':'off','onkeyUp':'fillslug(this.value)'}),error_messages={'required': _('Please enter the  title')})
    category = forms.ModelChoiceField(required=True, widget=forms.Select(attrs={'class':'iSp8 bM-sLt select-menu','data-placeholder':_('Choose a category'),'data-size':'8','title':_('Choose a category')}),queryset=ArticleCategory.objects.all().order_by('name'), empty_label="",error_messages={'required': _('Please select the category')})
    summary = forms.CharField(required=True,widget=forms.Textarea(attrs={'maxlength':250, 'rows': '4','class': 'iSp8', 'placeholder': "Enter a short summary concerning about this article in this text box"}),error_messages={'required': _('Please enter the summary')})
    content = forms.CharField(required=True,widget=forms.Textarea(attrs={'class': 'iSp8', 'rows':'8'}),error_messages={'required': _('Please enter the content')})
    gallery_url = forms.URLField(required=False, max_length=250, widget=forms.TextInput(attrs={'class': 'iSp8', 'placeholder':_('Example : http://www.example.com/gallery_name'),'class':'fl'}), error_messages={'invalid':_('Invalid gallery url.')})

    class Meta:
        model = Article
        fields = ('title','summary','content','category','gallery_url')

    def clean_title(self):
        title = self.cleaned_data.get("title").strip()
        if len(title)>150:
            raise forms.ValidationError(_("Maximum length of title field is 150 characters."))
        else:
            return title
    def clean_summary(self):
        summary = self.cleaned_data.get("summary").strip()
        if len(summary)>250:
            raise forms.ValidationError(_("Maximum length of summary field is 250 characters."))
        else:
            return summary
    def clean_content(self):
        content = self.cleaned_data.get("content").strip()
        if len(content)==0:
            raise forms.ValidationError(_("Please enter the description."))
        else:
            return content




# FORM For Tag
class TagForm(forms.Form):
    tags = forms.CharField(required=True,widget=forms.Textarea(),error_messages={'required': 'Please enter the tags'})

    def clean_tags(self):
        tags = self.cleaned_data.get("tags")
        tagarray = tags.split(',')
        for tag in tagarray:
            if len(tag)>150:
                raise forms.ValidationError("Maximum length of tags field is 150 charector.")
        return tags


class TellAFriend(forms.Form):
    name = forms.CharField(required=True, max_length="75", widget=forms.TextInput(attrs={'size':'30','class':'textField normal'}), error_messages={'required': 'Please enter the name'})
    f_name = forms.CharField(required=True, max_length="75", widget=forms.TextInput(attrs={'size':'30','class':'textField normal'}), error_messages={'required': 'Please enter the name'})
    f_email=  forms.EmailField(required=True, max_length="150", widget=forms.TextInput(attrs={'size':'30','class':'textField normal'}), error_messages={'required': 'Please enter the email.'})
    comment = forms.CharField(required=True, max_length="350", widget=forms.Textarea(attrs={'style':'width:200px;height:60px'}), error_messages={'required': 'Please enter the comment'})


class ArticleFeaturedForm(forms.Form):
    #smodule = forms.SelectMultiple(required=True, error_messages={'required': 'Please select the module'})
    title = forms.CharField(required=True, error_messages={'required': 'Please enter the title'})
    article_url = forms.URLField(required=True, error_messages={'required': 'Please enter the article url'})
    image_url = forms.URLField(required=True, error_messages={'required': 'Please enter the image url'})
    description = forms.CharField(required=False, error_messages={'required': 'Please enter the description'})
    def clean_title(self):
        title = self.cleaned_data.get("title")
        if len(title)>200:
            raise forms.ValidationError("Maximum length of title is 200 characters.")
        elif title.strip() == '':
            raise forms.ValidationError("Please enter the title")
        else:
            return title
    def clean_image_url(self):
        image_url = self.cleaned_data.get("image_url")
        if len(image_url)>200:
            raise forms.ValidationError("Maximum length of Image URL is 200 characters.")
        elif image_url.strip() == '':
            raise forms.ValidationError("Please enter the title")
        else:
            return image_url

class ArticlePriceForm(forms.ModelForm):
    ownstory_is_paid = forms.ChoiceField(required=True, choices=Article_Pay_Options, widget=forms.Select(attrs={'class':'select-menu','style':'width:70px;','onchange':'change_payment_own($(this))'}), error_messages={'required': 'Label content field shouldn\'t be empty.'})
    pressrelease_is_paid = forms.ChoiceField(required=True, choices=Article_Pay_Options, widget=forms.Select(attrs={'class':'select-menu','style':'width:70px;','onchange':'change_payment_press($(this))'}), error_messages={'required': 'Label content field shouldn\'t be empty.'})
    advertorial_is_paid  = forms.ChoiceField(required=True, choices=Article_Pay_Options, widget=forms.Select(attrs={'class':'select-menu','style':'width:70px;','onchange':'change_payment_advert($(this))'}), error_messages={'required': 'Label content field shouldn\'t be empty.'})
    requestreview_is_paid = forms.ChoiceField(required=True, choices=Article_Pay_Options, widget=forms.Select(attrs={'class':'select-menu','style':'width:70px;','onchange':'change_payment_request($(this))'}), error_messages={'required': 'Label content field shouldn\'t be empty.'})
    ownstory_price = forms.FloatField(required=True,widget=forms.TextInput(attrs={'class':'textField','style':'width:66px;'}), error_messages={'required': 'Own Story Price  shouldn\'t be empty.','invalid': 'Price field should be a number'})
    pressrelease_price = forms.FloatField(required=True,widget=forms.TextInput(attrs={'class':'textField','style':'width:66px;'}), error_messages={'required': 'Press Release Price  shouldn\'t be empty.','invalid': 'Price field should be a number'})
    advertorial_price = forms.FloatField(required=True,widget=forms.TextInput(attrs={'class':'textField','style':'width:66px;'}), error_messages={'required': 'Advertorial Price  shouldn\'t be empty.','invalid': 'Price field should be a number'})
    requestreview_price = forms.FloatField(required=True,widget=forms.TextInput(attrs={'class':'textField','style':'width:66px;'}), error_messages={'required': 'Request review Price shouldn\'t be empty.','invalid': 'Price field should be a number'})

    class Meta:
        model = ArticlePrice
    
    def clean_ownstory_price(self):
        ownstory_price = self.cleaned_data.get("ownstory_price")
        if ownstory_price == 0.0:
            raise forms.ValidationError(_("Please enter ownstory price grater than zero(0)"))
        else:
            return self.cleaned_data.get("ownstory_price")
        
    def clean_pressrelease_price(self):
        pressrelease_price = self.cleaned_data.get("pressrelease_price")
        if pressrelease_price == 0.0:
            raise forms.ValidationError(_("Please enter pressrelease price grater than zero(0)"))
        else:
            return self.cleaned_data.get("pressrelease_price")
        
    def clean_advertorial_price(self):
        advertorial_price = self.cleaned_data.get("advertorial_price")
        if advertorial_price == 0.0:
            raise forms.ValidationError(_("Please enter advertorial price grater than zero(0)"))
        else:
            return self.cleaned_data.get("advertorial_price")
    
    def clean_requestreview_price(self):
        requestreview_price = self.cleaned_data.get("requestreview_price")
        if requestreview_price == 0.0:
            raise forms.ValidationError(_("Please enter requestreview price grater than zero(0)"))
        else:
            return self.cleaned_data.get("requestreview_price")


