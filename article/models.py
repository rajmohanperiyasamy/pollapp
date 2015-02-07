from django.db import models
from django.forms import ModelForm
from django import forms
from django.utils.translation import ugettext as _
from django.conf import settings
#User = settings.AUTH_USER_MODEL


class ClientsData(models.Model):
    name = models.ForeignKey("Clients",null=True,blank=True)
    account = models.ForeignKey("Accounts",null=True,blank=True)
#    account = models.ManyToManyField("Accounts",null=True,blank=True)
    total = models.IntegerField()
    completed = models.IntegerField()
    pending = models.IntegerField()
    added_date = models.DateField(blank=True, null=True)
    status = models.BooleanField(default=True)
    def __unicode__(self):
       return _("%s") % self.name

    def __str__(self):              # __unicode__ on Python 2
        return self.name

class Accounts(models.Model):
    acc_name = models.CharField(max_length=100)
    

    def __str__(self):              # __unicode__ on Python 2
        return self.acc_name


class Clients(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    mobile=models.CharField(max_length=20,blank=True)
    email=models.EmailField(max_length=75,null=True)
    country = models.CharField(max_length=100, blank=True)
    joined_date = models.DateField(blank=True, null=True)

    def __str__(self):              # __unicode__ on Python 2
        return self.first_name



class Document(models.Model):
    docfile = models.FileField(upload_to='media')








#class Article(models.Model):
#    title = models.CharField(max_length=200)
#    body = models.TextField()
#    pub_date = models.DateTimeField('Date published')
#    likes = models.IntegerField() 
#    
#    def __unicode__(self):
#        return self.title
#    
#    
#TITLE_CHOICES = (
#    ('MR', 'Mr.'),
#    ('MRS', 'Mrs.'),
#    ('MS', 'Ms.'),
#)
#
#class Author(models.Model):
#    name = models.CharField(max_length=100)
#    title = models.CharField(max_length=3, choices=TITLE_CHOICES)
#    birth_date = models.DateField(blank=True, null=True)
#    
#    
#
#    def __str__(self):              # __unicode__ on Python 2
#        return self.name


#ACCOUNT_CHOICES = (
#    ('GMAIL', 'gmail.'),
#    ('HOTMAIL', 'hotmail.'),
#    ('YAHOO', 'yahoo.'),
#    ('ROCKET', 'rocket.'),
#    ('JABONG', 'jabong.'),
#    ('FLIPKART', 'flipkart.'),
#)
#
#class ClientData(models.Model):
##    models.OneToOneField(User, primary_key=True)
##    name = models.CharField(max_length=100)
##    name = models.OneToOneField(User, primary_key=True)
#    name = models.ForeignKey(User,null=True,blank=True)
#    account = models.CharField(max_length=100, choices=ACCOUNT_CHOICES)
#    total_accounts = models.IntegerField()
#    completed = models.IntegerField()
#    pending = models.IntegerField()
#    status = models.BooleanField(default=True)
#    added_date = models.DateField(blank=True, null=True)
##    def __unicode__(self):
##        return _("%s") % self.name
#
#    def __str__(self):              # __unicode__ on Python 2
#        return self.name
#    def __str__(self):              # __unicode__ on Python 2
#        return self.account
#
#class Accounts(models.Model):
#    acc_name = models.CharField(max_length=100)
#    completed = models.IntegerField()
#    pending = models.IntegerField()
#    added_date = models.DateField(blank=True, null=True)
    
#class Book(models.Model):
#    name = models.CharField(max_length=100)
#    authors = models.ManyToManyField(Author)
#
#
##class CommonAddress(models.model):
##    name = models.ForeignKey(Aut)
##    members = models.ManyToManyField(Person, through='Membership', through_fields=('group', 'person'))
#
#
#class Person(models.Model):
#    name = models.CharField(max_length=50)
#
#class Group(models.Model):
#    name = models.CharField(max_length=128)
#    members = models.ManyToManyField(Person)
#
#class Membership(models.Model):
#    group = models.ForeignKey(Group)
#    person = models.ForeignKey(Person)
#    inviter = models.ForeignKey(Person, related_name="membership_invites")
#    invite_reason = models.CharField(max_length=64)
#
#
#class AuthorForm(ModelForm):
#    class Meta:
#        model = Author
#        fields = ['name', 'title', 'birth_date']
#    name = forms.CharField(required=True,error_messages={'required': _('Please enter the name')}, max_length=100, widget=forms.TextInput({'style':'padding-right: 100px;'}))
#    title = forms.CharField(required=True,error_messages={'required': _('Please enter the title')},max_length=3,widget=forms.Select(choices=TITLE_CHOICES))
#    birth_date = forms.DateField(required=False)
#    status = models.BooleanField(default=True)

#class ArticleForm(ModelForm):
#    class Meta:
#        model = Article
#        fields = ['title', 'body', 'pub_date']
#        
#    title = models.CharField(max_length=200)
#    body = forms.Textarea()
#    pub_date = forms.DateTimeField('Date published')
        
    
    
# Create your models here.
