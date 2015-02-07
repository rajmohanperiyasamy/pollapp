from django import forms
from django.forms import ModelForm
from article.models import Document

#class ContactForm(forms.Form):
#    subject = forms.CharField(max_length=100)
#    message = forms.CharField()
#    sender = forms.EmailField()
#    cc_myself = forms.BooleanField(required=False)
#    
#    
#class ArticleForm(ModelForm):
#    class Meta:
#        model = Article
#        fields = ['title', 'body', 'pub_date']
#        
#    title = forms.CharField(required=True,max_length=70, error_messages={'required': 'Please enter the business title'})
#    body = forms.Textarea()
#    pub_date = forms.DateTimeField('Date published')

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )
#class ArticleForm(ModelForm):
#    class Meta:
#        model = Article
#        fields = ['title', 'pub_date', 'likes']
#    title = forms.CharField()
#    pub_date = forms.DateField()
#    likes = forms.CharField(required=False)
#    