import datetime, time
from time import strptime
from datetime import timedelta
from common.models import VenueType,Address
from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()
from django.utils.translation import ugettext as _
from common.form_utils import HorizRadioRenderer
from events.models import Event, EventCategory, EventPrice

attrs_dict = { 'class': 'required' }
attrs_tags = { 'class': 'tagclass' }

Event_Pay_Options = (
                    ('True', 'Paid'),
                    ('False', 'Free'),
                    )

Events_Price_Settings = (
                         ('day', '(per)Day'),
                         #('week','Weekly')
                         )

Events_Features_Option = (
                    ('Y', 'Yes'),
                    ('N', 'No'),
                    )

Events_Socialmedia_Options = (
                              ('F', 'Facebook'),
                              ('T', 'Twitter'),
                              ('B', 'FB + Twitter'),
                              ('N', 'No')
                             )

Events_Exposure = (
                     ('0', 'Standard'),
                     ('1', '1X'),
                     ('2', '5X'),
                     ('3', '10X'),
                     ('4', '15X'),
                     ('5', '20X'),
                     ('6', '25X')
                  )

valid_time_formats = ['%I:%M %p']
valid_date_formats = ['%m/%d/%Y']

# FORM For Tag
class TagForm(forms.Form):
    tag = forms.CharField(required=True, max_length=50, error_messages={'required': _('Please enter the Tag Name')})

# FORM For Category
class EventCategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        try:self._name = kwargs['instance'].name
        except:self._name= False
        super(EventCategoryForm, self).__init__(*args, **kwargs)

    name = forms.CharField(required=True, max_length=50, widget=forms.TextInput({'class':'fm', 'title':_('Category  Name'), 'onkeyUp':'string_to_slug(this.value)', 'maxlength':'50', 'autocomplete':'off'}), error_messages={'required': _('Please enter the category name')})
    slug = forms.CharField(required=False, max_length=200, widget=forms.TextInput({'class':'default-url','style':'width:150px;', 'title':_('Category Slug'), 'maxlength':'200', 'onkeyUp':'string_to_slug(this.value)', 'autocomplete':'off'}), error_messages={'required': _('Please enter the slug')})
    seo_title = forms.CharField(required=False, max_length=200, widget=forms.TextInput(attrs={'class':'fm', 'title':_('Meta Title'), 'maxlength':'200', 'autocomplete':'off'}), error_messages={'required': _('Please enter the Meta title')})
    seo_description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'fm', 'title':_('Meta Description'), 'onkeyUp':'txtarealimit(this,400);', 'style':'overflow: hidden; height: 70px;'}), error_messages={'required': _('Please enter the Meta description')})
    class Meta:
        model = EventCategory

    def clean_name(self):
        name = self.cleaned_data.get("name").strip()
        if self._name:
            if str(self._name).lower() != str(name).lower():
                try:
                    flag=EventCategory.objects.filter(name__iexact=name)
                    if flag:raise forms.ValidationError(_("This category name is already added."))
                except EventCategory.DoesNotExist:pass
        else:
            try:
                flag=EventCategory.objects.filter(name__iexact=name)
                if flag:raise forms.ValidationError(_("This category name is already added."))
            except EventCategory.DoesNotExist:pass
        return name

    def clean_slug(self):
        slug = self.cleaned_data.get("slug")
        if slug:
            return slug
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

# FORM For Event SEO
class CategorySEOForm(forms.ModelForm):
    slug = forms.CharField(required=True, widget=forms.TextInput({'class':'default-url','style':'width:160px;', 'title':_('Category Slug'), 'maxlength':'200', 'onkeyUp':'string_to_slug(this.value)', 'autocomplete':'off'}), error_messages={'required': _('Please enter the slug')})
    seo_title = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'fm', 'title':_('Meta Title'), 'maxlength':'200'}), error_messages={'required': _('Please enter the Meta title')})
    seo_description = forms.CharField(required=True, widget=forms.Textarea(attrs={'class':'fm', 'title':_('Meta Description'), 'onkeyUp':'txtarealimit(this,400);', 'style':'overflow: hidden; height: 70px;'}), error_messages={'required': _('Please enter the Meta description')})
    class Meta:
        model = EventCategory
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


class EventSeoForm(forms.ModelForm):
    #slug = forms.CharField(required=True, widget=forms.TextInput({'class':'default-url slug_input','style':'width:265px;','title':_('Event Slug'),'maxlength':'200','onkeyUp':'string_to_slug(this.value)','autocomplete':'off'}), error_messages={'required': _('Please enter the slug')})
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

    class Meta:
        model = Event
        fields=('seo_title','seo_description')
        
class UserEventSeoForm(forms.ModelForm):
    #slug = forms.CharField(required=True, widget=forms.TextInput({'class':'default-url slug_input','style':'width:265px;','title':_('Event Slug'),'maxlength':'200','onkeyUp':'string_to_slug(this.value)','autocomplete':'off'}), error_messages={'required': _('Please enter the slug')})
    seo_title = forms.CharField(required=True,max_length=70, error_messages={'required': _('Please enter the Title')},widget=forms.TextInput(attrs={'class':'iSp8','maxlength':70,'title':_('Meta Title'),'autocomplete':'off'}))
    seo_description = forms.CharField(required=True,max_length=160, error_messages={'required': _('Please enter Description')},widget=forms.Textarea(attrs={'class':'iSp8','maxlength':160,'cols':30,'rows':4,'style':'height:70px;','maxlength':'160','title':_('Meta Description'),'onkeyUp':'txtarealimit(this,160);'}))

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
        model = Event
        fields=('seo_title','seo_description')



class EventFormUser(forms.ModelForm):
    title = forms.CharField(required=True, max_length=150, widget=forms.TextInput(attrs={"autocomplete": "off", "class": "iSp8", 'placeholder':_('Event Name')}), error_messages={'required': _('Title Required')})
    start_date = forms.DateField(required=True, input_formats=valid_date_formats, widget=forms.DateInput(format='%m/%d/%Y',attrs={'placeholder':_('Start Date'),'autocomplete':'off'}), error_messages={'required': _('Start Date Required')})
    end_date = forms.DateField(required=True, input_formats=valid_date_formats, widget=forms.DateInput(format='%m/%d/%Y',attrs={'placeholder':_('End Date'),'autocomplete':'off'}), error_messages={'required': _('End Date Required')})
    start_time = forms.TimeField(required=False,input_formats=valid_time_formats,  widget=forms.TimeInput(format='%I:%M %p',attrs={'placeholder':_('Start Time'),'autocomplete':'off'}), error_messages={'required': _('Start Time Required')})
    end_time = forms.TimeField(required=False, input_formats=valid_time_formats,  widget=forms.TimeInput(format='%I:%M %p',attrs={'placeholder':_('End Time'),'autocomplete':'off'}), error_messages={'required': _('End Time Required')})

    contact_email = forms.EmailField(required=False, max_length=50, widget=forms.TextInput(attrs={'placeholder':_('Enter email'), 'class':'fs'}), error_messages={'required': _('Contact E-mail Required')})
    phone = forms.CharField(required=False, max_length=40, widget=forms.TextInput(attrs={'placeholder':_('Phone No:'),'class':'fs'}), error_messages={'required': _('Contact Number Required')})

    event_website = forms.URLField(required=False, max_length=200, widget=forms.TextInput(attrs={'placeholder':_('Example: http://www.example.com'), 'class':'iSp8'}), error_messages={'invalid':_('Invalid website url.')})
    facebook = forms.CharField(required=False,max_length=150, error_messages={'required':_('Please enter the Facebook URL')},widget=forms.TextInput(attrs={'class':'iSp8','style':'width:329px;','onfocus':'showhttp("f")','onblur':'hidehttp("f")','title':'Facebook URL','placeholder':_('Example: https://www.facebook.com/page'),'autocomplete':'off'}))
    googleplus = forms.CharField(required=False,max_length=150, error_messages={'required': _('Please enter the Google+ URL')},widget=forms.TextInput(attrs={'class':'iSp8','style':'width:329px;','onfocus':'showhttp("g")','onblur':'hidehttp("g")','title':'Google Plus URL','placeholder':_('Example: https://plus.google.com/page'),'autocomplete':'off'}))

    tkt_prize = forms.CharField(required=False,max_length=20, widget=forms.TextInput(attrs={'class':'fs'}), error_messages={'invalid':_('Invalid Ticket price.')})
    ticket_site = forms.URLField(required=False, max_length=200, widget=forms.TextInput(attrs={'placeholder':_('URL'),'onfocus':'showhttp(4)','onblur':'hidehttp(4)', 'class':'fs'}), error_messages={'invalid':_('Invalid Ticket url.')})
    tkt_phone = forms.CharField(required=False, max_length=40, widget=forms.TextInput(attrs={'placeholder':_('Box office phone No:'),'class':'fs'}), error_messages={'required': _('Enter Box office phone No')})

    category = forms.ModelMultipleChoiceField(required=True, queryset=EventCategory.objects.order_by('name'), widget=forms.SelectMultiple(attrs={'data-size':"10", 'class':'iSp8 bM-sLt','title':_('Select multiple categories'),'data-placeholder':_('Select multiple categories')}), error_messages={'required': _('Event categories Required')})
    event_description = forms.CharField(required=True, widget=forms.Textarea(attrs={"class": "iSp8",'rows':'4'}), error_messages={'required': _('Event Description Required')})
    venue = forms.IntegerField(required=True,error_messages={'required': _('Event venue Required')})

    class Meta:
        model = Event
        fields = ('title', 'start_date', 'end_date', 'start_time','tkt_prize','end_time', 'contact_email', 'phone',
                  'ticket_site', 'tkt_phone', 'category', 'event_description','event_website','facebook','googleplus')
    def clean_title(self):
        return validate_blank_space(self.cleaned_data.get("title"), 'title')
#     def clean_end_date(self):
#         start_date = self.cleaned_data.get('start_date')
#         end_date = self.cleaned_data.get('end_date')
#         if start_date > end_date:
#             raise forms.ValidationError(_("Event start date shouldn't be greater than end date"))
#         else:
#             return end_date

class EventFormStaff(forms.ModelForm):
    title = forms.CharField(required=True, max_length=150, widget=forms.TextInput(attrs={'placeholder':_('Enter Event Title')}), error_messages={'required': _('Title Required')})
    start_date = forms.DateField(required=True, input_formats=valid_date_formats, widget=forms.DateInput(format='%m/%d/%Y',attrs={'placeholder':_('Start Date'),'class':'fxs','style':'margin-right:7px;','autocomplete':'off'}), error_messages={'required': _('Start Date Required')})
    end_date = forms.DateField(required=True, input_formats=valid_date_formats, widget=forms.DateInput(format='%m/%d/%Y',attrs={'placeholder':_('End Date'),'class':'fxs','autocomplete':'off'}), error_messages={'required': _('End Date Required')})
    start_time = forms.TimeField(required=False,input_formats=valid_time_formats,  widget=forms.TimeInput(format='%I:%M %p',attrs={'placeholder':_('Start Time'),'class':'fxxs','style':'margin-right:3px;'}), error_messages={'required': _('Start Time Required')})
    end_time = forms.TimeField(required=False, input_formats=valid_time_formats,  widget=forms.TimeInput(format='%I:%M %p',attrs={'placeholder':_('End Time'),'class':'fxxs','style':'margin-left:3px;margin-right:6px;'}), error_messages={'required': _('End Time Required')})

    contact_email = forms.EmailField(required=False, max_length=50, widget=forms.TextInput(attrs={'placeholder':_('Enter email'), 'class':'fs'}), error_messages={'required': _('Contact E-mail Required')})
    phone = forms.CharField(required=False, max_length=40, widget=forms.TextInput(attrs={'placeholder':_('Phone No:'),'class':'fs'}), error_messages={'required': _('Contact Number Required')})

    event_website = forms.URLField(required=False, max_length=200, widget=forms.TextInput(attrs={'placeholder':_('Example: http://www.example.com'),'onfocus':'showhttp(1)','onblur':'hidehttp(1)', 'class':'fl'}), error_messages={'invalid':_('Invalid website url.')})
    facebook = forms.CharField(required=False,max_length=150, error_messages={'required':_('Please enter the Facebook URL')},widget=forms.TextInput(attrs={'style':'width:329px;','onfocus':'showhttp(2)','onblur':'hidehttp(2)','title':'Facebook URL','placeholder':_('Example: https://www.facebook.com/page'),'autocomplete':'off'}))
    googleplus = forms.CharField(required=False,max_length=150, error_messages={'required': _('Please enter the Google+ URL')},widget=forms.TextInput(attrs={'style':'width:329px;','onfocus':'showhttp(3)','onblur':'hidehttp(3)','title':'Google Plus URL','placeholder':_('Example: https://plus.google.com/page'),'autocomplete':'off'}))

    tkt_prize = forms.CharField(required=False, max_length=20,widget=forms.TextInput(attrs={'class':'fs'}), error_messages={'invalid':_('Invalid Ticket price.')})
    ticket_site = forms.URLField(required=False, max_length=200, widget=forms.TextInput(attrs={'placeholder':_('http://www.ticketmaster.com'),'onfocus':'showhttp(4)','onblur':'hidehttp(4)', 'class':'fs'}), error_messages={'invalid':_('Invalid Ticket url.')})
    tkt_phone = forms.CharField(required=False, max_length=40, widget=forms.TextInput(attrs={'placeholder':_('Box office phone No:'),'class':'fs'}), error_messages={'required': _('Enter Box office phone No')})

    category = forms.ModelMultipleChoiceField(required=True, queryset=EventCategory.objects.order_by('name'), widget=forms.SelectMultiple(attrs={'class':'select-menu fl','data-placeholder':_('Select multiple categories')}), error_messages={'required': _('Event categories Required')})
    event_description = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows':'4','class':'fxl'}), error_messages={'required': _('Event Description Required')})

    listing_price = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'size':'9'}),initial='0', error_messages={'required': _('Enter the listing price'),'invalid':_('Invalid listing price')})
    listing_start = forms.DateField(required=False, input_formats=valid_date_formats, widget=forms.DateInput(format='%d/%m/%Y',attrs={'placeholder':_('DD/MM/YY'),'size':'9','autocomplete':'off', 'onchange': 'load_rate()'}), error_messages={'required': _('Select the listing start date')})
    listing_end = forms.DateField(required=False, input_formats=valid_date_formats, widget=forms.DateInput(format='%d/%m/%Y',attrs={'placeholder':_('DD/MM/YY'),'size':'9','autocomplete':'off', 'onchange': 'load_rate()'}), error_messages={'required': _('Select the listing end date')})
    venue = forms.IntegerField(required=True,error_messages={'required': _('Event venue Required')})

    class Meta:
        model = Event
        fields = ('title', 'start_date', 'end_date', 'start_time','tkt_prize','end_time', 'contact_email', 'phone',
                  'ticket_site', 'tkt_phone', 'category', 'event_description','listing_start','listing_price','listing_end','event_website','facebook','googleplus')
    def clean_title(self):
        return validate_blank_space(self.cleaned_data.get("title"), 'title')
    def clean_end_date(self):
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        if start_date > end_date:
            raise forms.ValidationError(_("Event start date shouldn't be greater than end date"))
        else:
            return end_date

class EditEventFormStaff(forms.ModelForm):
    title = forms.CharField(required=True, max_length=150, widget=forms.TextInput(attrs={'placeholder':_('Enter Event Title')}), error_messages={'required': _('Title Required')})
    start_date = forms.DateField(required=True, input_formats=valid_date_formats, widget=forms.DateInput(format='%m/%d/%Y',attrs={'placeholder':_('Start Date'),'class':'fxs','style':'margin-right:7px;','autocomplete':'off'}), error_messages={'required': _('Start Date Required')})
    end_date = forms.DateField(required=True, input_formats=valid_date_formats, widget=forms.DateInput(format='%m/%d/%Y',attrs={'placeholder':_('End Date'),'class':'fxs','autocomplete':'off'}), error_messages={'required': _('End Date Required')})
    start_time = forms.TimeField(required=False,input_formats=valid_time_formats,  widget=forms.TimeInput(format='%I:%M %p',attrs={'placeholder':_('Start Time'),'class':'fxxs','style':'margin-right:3px;'}), error_messages={'required': _('Start Time Required')})
    end_time = forms.TimeField(required=False, input_formats=valid_time_formats,  widget=forms.TimeInput(format='%I:%M %p',attrs={'placeholder':_('End Time'),'class':'fxxs','style':'margin-left:3px;margin-right:6px;'}), error_messages={'required': _('End Time Required')})

    contact_email = forms.EmailField(required=False, max_length=50, widget=forms.TextInput(attrs={'placeholder':_('Enter email'), 'style':'width:180px;'}), error_messages={'required': _('Contact E-mail Required')})
    phone = forms.CharField(required=False, max_length=40, widget=forms.TextInput(attrs={'placeholder':_('Phone No:'),'style':'width:150px;'}), error_messages={'required': _('Contact Number Required')})

    event_website = forms.URLField(required=False, max_length=200, widget=forms.TextInput(attrs={'placeholder':_('Example: http://www.example.com'),'onfocus':'showhttp(1)','onblur':'hidehttp(1)', 'style':'width:348px;'}), error_messages={'invalid':_('Invalid website url.')})
    facebook = forms.CharField(required=False,max_length=150, error_messages={'required':_('Please enter the Facebook URL')},widget=forms.TextInput(attrs={'style':'width:330px;','onfocus':'showhttp(2)','onblur':'hidehttp(2)','title':'Facebook URL','placeholder':_('Example: https://www.facebook.com/page'),'autocomplete':'off'}))
    googleplus = forms.CharField(required=False,max_length=150, error_messages={'required': _('Please enter the Google+ URL')},widget=forms.TextInput(attrs={'style':'width:330px;','onfocus':'showhttp(3)','onblur':'hidehttp(3)','title':'Google Plus URL','placeholder':_('Example: https://plus.google.com/page'),'autocomplete':'off'}))

    tkt_prize = forms.CharField(required=False,max_length=20, widget=forms.TextInput(attrs={'style':'width:180px;'}), error_messages={'invalid':_('Invalid Ticket price.')})
    ticket_site = forms.URLField(required=False, max_length=200, widget=forms.TextInput(attrs={'placeholder':_('URL'),'onfocus':'showhttp(4)','onblur':'hidehttp(4)', 'style':'width:180px;'}), error_messages={'invalid':_('Invalid Ticket url.')})
    tkt_phone = forms.CharField(required=False, max_length=40, widget=forms.TextInput(attrs={'placeholder':_('Box office phone No:'),'style':'width:150px;'}), error_messages={'required': _('Enter Box office phone No')})

    category = forms.ModelMultipleChoiceField(required=True, queryset=EventCategory.objects.order_by('name'), widget=forms.SelectMultiple(attrs={'style':'width:356px;','class':'select-menu','data-placeholder':_('Select multiple categories')}), error_messages={'required': _('Event categories Required')})
    event_description = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows':'4'}), error_messages={'required': _('Event Description Required')})
    venue = forms.IntegerField(required=True,error_messages={'required': _('Event venue Required')})

    class Meta:
        model = Event
        fields = ('title', 'start_date', 'end_date', 'start_time','tkt_prize','end_time', 'contact_email', 'phone',
                  'ticket_site', 'tkt_phone', 'category', 'event_description','event_website','facebook','googleplus')
    def clean_title(self):
        return validate_blank_space(self.cleaned_data.get("title"), 'title')
    def clean_end_date(self):
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        if start_date > end_date:
            raise forms.ValidationError(_("Event start date shouldn't be greater than end date"))
        else:
            return end_date

class EventPriceForm(forms.ModelForm):
    level = forms.CharField(required=False, max_length="10", widget=forms.TextInput(attrs={'size':'30', 'class':'input_text'}), error_messages={'required': 'Title field Shouldn\'t be empty.'})
    level_visibility = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'onclick':'change_visiblity($(this))'}), error_messages={'required': 'Label content field Shouldn\'t be empty.'})
    level_label = forms.CharField(required=True, max_length=50, widget=forms.TextInput({'title':_('First Name'),'readonly':'true',  'maxlength':'50', 'style':'height:21px;', 'autocomplete':'off'}), error_messages={'required': _('Label field Shouldn\'t be empty.')})
    exposure = forms.ChoiceField(required=True, choices=Events_Exposure, widget=forms.Select(attrs={'class':'select-menu', 'style':'width:88px;'}), error_messages={'required': 'Exposure field Shouldn\'t be empty.'})
    images = forms.ChoiceField(required=True, choices=Events_Features_Option, widget=forms.Select(attrs={'class':'select-menu', 'style':'width:70px;'}), error_messages={'required': 'Images field Shouldn\'t be empty.'})
    comments = forms.ChoiceField(required=True, choices=Events_Features_Option, widget=forms.Select(attrs={'class':'select-menu', 'style':'width:70px;'}), error_messages={'required': 'Comments field Shouldn\'t be empty.'})
    ticket_info = forms.ChoiceField(required=True, choices=Events_Features_Option, widget=forms.Select(attrs={'class':'select-menu', 'style':'width:70px;'}), error_messages={'required': 'Ticket info field Shouldn\'t be empty.'})
    share_buttons = forms.ChoiceField(required=True, choices=Events_Features_Option, widget=forms.Select(attrs={'class':'select-menu', 'style':'width:70px;'}), error_messages={'required': 'Share Buttons field Shouldn\'t be empty.'})
    newsletter = forms.ChoiceField(required=True, choices=Events_Features_Option, widget=forms.Select(attrs={'class':'select-menu', 'style':'width:70px;'}), error_messages={'required': 'Newsletter field Shouldn\'t be empty.'})
    social_media = forms.ChoiceField(required=True, choices=Events_Features_Option, widget=forms.Select(attrs={'class':'select-menu', 'style':'width:70px;'}), error_messages={'required': 'Social Media field Shouldn\'t be empty.'})
    price = forms.FloatField(required=True, widget=forms.TextInput(attrs={'class':'textField', 'maxlength':'10','style':'width:32px; height:21px;'}), error_messages={'required': 'Price field Shouldn\'t be empty.', 'invalid': 'Price field should be a number'})

    class Meta:
        model = EventPrice
        exclude = ('level','sms')

def validate_blank_space(data, field):
    if data.strip() == '':
        raise forms.ValidationError('Blank space is not allowed for ' + field + ' field')
    else:
        return data

class UserVenueForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserVenueForm, self).__init__(*args, **kwargs)
        self.fields['type'].widget = forms.Select(attrs={'class':'iSp12 bM-sLt'})
        self.fields['type'].queryset = VenueType.objects.all().order_by('title')
        self.fields['type'].required = False
        self.fields['type'].empty_label = _("-- Venue Type --")
        self.fields['type'].error_messages = _("Please select venue type.")
    venue = forms.CharField(required=True,max_length=100, error_messages={'required': _('Please enter the Venue')},widget=forms.TextInput(attrs={'id':'id_venues','class':'iSp12','title':_('Venue Name')}))
    address1 = forms.CharField(required=True,max_length=150, error_messages={'required': _('Please enter the Address')},widget=forms.TextInput(attrs={'class':'iSp12','title':_('Address')}))
    address2 = forms.CharField(required=False,max_length=150,widget=forms.TextInput(attrs={'class':'iSp12','title':_('Address 2')}))
    telephone1=forms.CharField(required=False,max_length=20,widget=forms.TextInput(attrs={'class':'iSp12','title':_('Telephone No 1')}))
    telephone2=forms.CharField(required=False,max_length=20,widget=forms.TextInput(attrs={'class':'iSp12','title':_('Telephone No 2')}))
    mobile=forms.CharField(required=False,max_length=20,widget=forms.TextInput(attrs={'class':'iSp12','title':_('Mobile No')}))
    email=forms.EmailField(required=False,max_length=75,widget=forms.TextInput(attrs={'class':'iSp12','title':_('Email ID')}))
    website=forms.URLField(required=False,max_length=240,widget=forms.TextInput(attrs={'class':'iSp12','title':_('Website')}))
    description=forms.CharField(required=False,widget=forms.Textarea(attrs={'id':'id_descriptions','class':'iSp12','title':_('Description'),'cols':25,'rows':3}))
    city = forms.CharField(required=False,max_length=100, error_messages={'required': _('Please enter the City')},widget=forms.TextInput(attrs={'id':'id_city','class':'iSp12','title':_('City Name')}))
    #locality = forms.ModelChoiceField(required=True, queryset = Locality.objects.order_by('name'), error_messages={'required': 'Please select the Location'}, empty_label='Select The Locality', widget=forms.Select(attrs={'class':'textField locality','onchange':'newlocation();'}))
    zip = forms.CharField(required=False,max_length=16, error_messages={'required': _('Please enter the zip code')},widget=forms.TextInput(attrs={'class':'iSp12 postal','title':_('ZipCodes')}))
    
    class Meta:
        model = Address
        exclude = ('address_type','lat','lon','zoom','status','is_active','created_on','created_by','modified_on','modified_by','seo_title','seo_description')