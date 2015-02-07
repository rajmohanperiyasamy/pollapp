from django import forms
from community.models import Topic,Entry
from django.utils.translation import ugettext as _


class CommunityTopicForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        try:self._name = kwargs['instance'].name
        except:self._name= False
        super(CommunityTopicForm, self).__init__(*args, **kwargs)
        
    name = forms.CharField(required=True,max_length=200, error_messages={'required': _('Please enter the name')},widget=forms.TextInput({'class':'tttxt','maxlength':'120','onkeyUp':'string_to_slug(this.value)','title':_('Topic Name'),'autocomplete':'off'}))
    slug = forms.CharField(required=False, widget=forms.TextInput({'class':'default-url','style':'width:152px;','title':_('Topic Slug'),'maxlength':'200','onkeyUp':'string_to_slug(this.value)','autocomplete':'off'}), error_messages={'required': _('Please enter the slug')})
    seo_title = forms.CharField(required=False,max_length=70, error_messages={'required': _('Please enter the Title')},widget=forms.TextInput(attrs={'class':'tttxt','maxlength':'70','title':_('Meta Title'),'autocomplete':'off'}))
    seo_description = forms.CharField(required=False,max_length=160, error_messages={'required': _('Please enter Description')},widget=forms.Textarea(attrs={'class':'tttxt','cols':30,'rows':5,'style':'height:70px;','title':_('Meta Description'),'onkeyUp':'txtarealimit(this,160);'}))
    
    def clean_name(self):
        name = self.cleaned_data.get("name").strip()
        if self._name:
            if str(self._name).lower() != str(name).lower():
                try:
                    flag=Topic.objects.filter(name__iexact=name)
                    if flag:raise forms.ValidationError(_("This category name is already added."))
                except Topic.DoesNotExist:pass
        else:
            try:
                flag=Topic.objects.filter(name__iexact=name)
                if flag:raise forms.ValidationError(_("This category name is already added."))
            except Topic.DoesNotExist:pass
        return name
    
    def clean_slug(self):
        slug = self.cleaned_data.get("slug")
        if slug:return slug
        else:
            name = self.cleaned_data.get("name")
            return name
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
        model = Topic

class CommunityTopicSeoForm(forms.ModelForm):
    slug = forms.CharField(required=True, widget=forms.TextInput({'class':'default-url','style':'width:152px;','title':_('Category Slug'),'maxlength':'200','onkeyUp':'string_to_slug(this.value)','autocomplete':'off'}), error_messages={'required': _('Please enter the slug')})
    seo_title = forms.CharField(required=True,max_length=200,widget=forms.TextInput(attrs={'class':'tttxt','maxlength':'200','title':_('Meta Title'),'autocomplete':'off'}), error_messages={'required': _('Please enter the Meta Title')})
    seo_description = forms.CharField(required=True,max_length=400,widget=forms.Textarea(attrs={'class':'tttxt','cols':30,'rows':5,'style':'height:70px;','title':_('Meta Description'),'onkeyUp':'txtarealimit(this,400);'}), error_messages={'required': _('Please enter the Meta Keyword')})
    
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
        model = Topic
        exclude = ('name')

class AddEntryForm(forms.ModelForm):
    title = forms.CharField(required=True,widget=forms.Textarea(attrs={'class':'cMnT-tXtArA fS16 cLr-bLk', 'placeholder':_("Share What's new..."), 'data-focus':'true', 'data-expand':'true','onkeyUp':'limit_charecters(this,150)'}),error_messages={'required': _('Please enter the Question')})
    content = forms.CharField(required=False,error_messages={'required':_('Please enter the description'), 'invalid': _('Description: Ensure this value has at most 5000 characters')}, widget=forms.Textarea(attrs={'class':'cMnT-tXtArA h60', 'placeholder':_('Enter the description'),'title':_('Question Description')}))
    topic = forms.ModelChoiceField(required=True, widget=forms.Select(attrs={'data-placeholder':_('Please select the topic'), 'class':'bUiSlCt'}),queryset = Topic.objects.filter().order_by('name'), empty_label="Select Topic",error_messages={'required': 'Please select the topic'})
    
    def clean_title(self):
        title = self.cleaned_data.get("title").strip()
        if len(title) > 150:
            raise forms.ValidationError(_("Maximum length of question field is 200 characters."))
        else:
            return title
        
    def clean_content(self):
        content = self.cleaned_data.get("content").strip()
        if len(content) > 10000:
            raise forms.ValidationError(_("Maximum length of description field is 5000 characters."))
        else:
            return content

    class Meta:
        model = Entry
        fields=('title','content','topic') 