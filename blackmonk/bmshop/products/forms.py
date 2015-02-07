from django import forms
from django.utils.translation import ugettext_lazy as _

from bmshop.products.models import BMPropertyGroup,Product,DeliveryTime,TAX_OPTION,Manufacturer
from bmshop.products.models import Product,Category,DeliveryTime,BMProperty
from bmshop.products.settings import DELIVERY_TIME_UNIT_CHOICES
from bmshop.products.settings import PROPERTY_FIELD_CHOICES

from mptt.forms import TreeNodeChoiceField

class CategoryForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        node= kwargs.pop('instance', None)
        if node:
            opts = node._mptt_meta
            valid_targets = node._tree_manager.exclude(**{
               opts.tree_id_attr: getattr(node, opts.tree_id_attr),
                '%s__gte' % opts.left_attr: getattr(node, opts.left_attr),
                '%s__lte' % opts.right_attr: getattr(node, opts.right_attr),
                 })
        else:
            valid_targets = Category.objects.all()
        self.fields['parent']= TreeNodeChoiceField(
                required = False,
                queryset = valid_targets,
                widget = forms.Select(attrs={'class':'select-menu parent-category fm'} ),
                level_indicator = u'--',
                empty_label = _("Select Parent Category ")
            )
        
    name = forms.CharField(required=True,max_length=200, error_messages={'required': _('Please enter the name')},
                    widget=forms.TextInput({'class':'fm','maxlength':'120','onkeyUp':'string_to_slug(this.value)','title':_('Category Name'),'autocomplete':'off'}))
    slug = forms.CharField(required=True,error_messages={'required': _('Please enter the slug')},
                    widget=forms.TextInput({'class':'default-url','style':'width:139px;','title':_('Category Slug'),'maxlength':'200','onkeyUp':'string_to_slug(this.value)','autocomplete':'off'}))
    description = forms.CharField(required=False,max_length=400, error_messages={'required': _('Please enter Description')},
                    widget=forms.Textarea(attrs={'class':'fm','cols':30,'rows':5,'style':'height:40px;','title':_('Description')}))
    position = forms.IntegerField(required=False,initial=0,
                    widget=forms.TextInput(attrs={'class':'textField','style':'width:40px; height:21px;'}))
    featured = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={}))
    meta_title = forms.CharField(required=False,max_length=200, error_messages={'required': _('Please enter the Title')},
                    widget=forms.TextInput(attrs={'class':'fm','maxlength':'200','title':_('Meta Title'),'autocomplete':'off'}))
    meta_description = forms.CharField(required=False,max_length=400, error_messages={'required': _('Please enter Meta Description')},
                    widget=forms.Textarea(attrs={'class':'fm','cols':30,'rows':5,'style':'height:70px;','title':_('Meta Description'),'onkeyUp':'txtarealimit(this,400);'}))
    
    class Meta:
        model=Category
        fields = ('name','slug','parent','description','position','featured','meta_title','meta_description')


class AddProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        node = Category.tree.all()
        all_node = []
        for n in node:
            if n.is_leaf_node():
                all_node.append(n.id)
        super(AddProductForm, self).__init__(*args, **kwargs)
        self.fields['categories'].widget = forms.SelectMultiple(attrs={'class':'select-menu fl','data-placeholder':_('Select Categories')})
        self.fields['categories'].queryset = Category.objects.filter(id__in=all_node).order_by('name')
        self.fields['categories'].required = False
        self.fields['categories'].error_messages = _("Please select categories")
    
    name = forms.CharField(required=True,max_length=200, error_messages={'required': _('Property name is required')},
                    widget=forms.TextInput({'class':'fm','maxlength':'120','onkeyUp':'string_to_slug(this.value)','title':_('Property Name'),'autocomplete':'off'}))   
    manufacturer = forms.ModelChoiceField(required=True,error_messages={'required': _('Manufacturer is required')},empty_label="",
                    widget=forms.Select(attrs={'class':'select-menu fl','data-placeholder':_('Choose Manufacturer')}),queryset=Manufacturer.objects.order_by('name'))
    
    price = forms.FloatField(required=True,error_messages={'required': _('Price is required')},
                    widget=forms.TextInput({'class':'fl','placeholder':_('Price'),'autocomplete':'off','title':_('Product Price')}))
    tax_calculator = forms.ChoiceField(choices=TAX_OPTION,error_messages={'required': _('Tax details is required')},
                    widget=forms.Select(attrs={'class':'select-menu fl'}))

    for_sale  = forms.BooleanField(required=False,widget=forms.CheckboxInput(),initial=True)
    for_sale_price = forms.FloatField(required=True,error_messages={'required': _('Sale Price is required')},
                    widget=forms.TextInput({'class':'fl','placeholder':_('Sale Price'),'autocomplete':'off','title':_('Sale Price')}))
    
    short_description = forms.CharField(required=True, error_messages={'required': _('Please enter highlights')},
                    widget=forms.Textarea(attrs={'class':'fl','cols':30,'rows':5,'title':_('Highlights')}))
    description = forms.CharField(required=False, error_messages={'required': _('Please enter Description')},
                    widget=forms.Textarea(attrs={'class':'fl','cols':30,'rows':8,'title':_('Description')}))
    
    manual_delivery_time  = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'onclick':'show_delivery_time()'}))
    delivery_time = forms.ModelChoiceField(required=False,error_messages={'required': _('Delivery time is required')},queryset=DeliveryTime.objects.order_by('min_unit'), 
                    widget=forms.Select(attrs={'class':'select-menu fl','data-placeholder':_('Choose Delivery Time')}),empty_label="")
    manage_stock_amount  = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'onclick':'show_manage_stock()'}))
    stock_amount = forms.CharField(required=False,error_messages={'required': _('No. of Stock Items is required')},
                    widget=forms.TextInput({'class':'fl','placeholder':_('Total Stock Items'),'autocomplete':'off','title':_('Stock Amount')}))
    
    featured  = forms.BooleanField(required=False,widget=forms.CheckboxInput())
    related_products = forms.ModelMultipleChoiceField(required=False, queryset=Product.objects.order_by('name'), error_messages={'required': _('Related products are required')},
                    widget=forms.SelectMultiple(attrs={'class':'select-menu fl','data-placeholder':_('Choose Realated Products')}))
    
    class Meta:
        model=Product
        fields = ('name','categories','manufacturer','short_description','description','price',
                  'tax_calculator','for_sale','for_sale_price','manual_delivery_time','delivery_time',
                  'featured','manage_stock_amount','stock_amount','related_products')
    
    def clean(self):
        cleaned_data = super(AddProductForm, self).clean()
        
        if self.cleaned_data.get("manual_delivery_time"):
            if not self.cleaned_data.get("delivery_time"):
                self._errors["delivery_time"] = self.error_class([_("Please choose a delivery time.")]) 
                
        if self.cleaned_data.get("manage_stock_amount"):
            if not self.cleaned_data.get("stock_amount"):
                self._errors["stock_amount"] = self.error_class([_("Please enter stock amount")])         
            
        return cleaned_data

class ProductSeoForm(forms.ModelForm):
    meta_title = forms.CharField(required=True,max_length=200, error_messages={'required': _('Please enter the Title')},widget=forms.TextInput(attrs={'class':'fm','maxlength':'200','title':_('Meta Title'),'autocomplete':'off'}))
    meta_description = forms.CharField(required=True,max_length=400, error_messages={'required': _('Please enter Description')},widget=forms.Textarea(attrs={'class':'fxl','cols':30,'rows':4,'style':'height:70px;','title':_('Meta Description'),'onkeyUp':'txtarealimit(this,400);'}))

    def clean_seo_title(self):
        seo_title = self.cleaned_data.get("meta_title").strip()
        if len(seo_title) > 200:
            raise forms.ValidationError(_("Maximum length of meta-title field is 200 characters."))
        else:
            if seo_title: return seo_title
            else:return self.cleaned_data.get("name")
    def clean_seo_description(self):
        seo_description = self.cleaned_data.get("meta_description").strip()
        if len(seo_description) > 400:
            raise forms.ValidationError(_("Maximum length of meta-description field is 400 characters."))
        else:
            if seo_description: return seo_description
            else:return self.cleaned_data.get("name")

    class Meta:
        model = Product
        fields=('meta_title','meta_description')
        
        
class DeliveryTimeForm(forms.ModelForm):
    min_unit = forms.CharField(required=True,error_messages={'required': _('Please enter the minimum value')},widget=forms.TextInput({'class':'fm','placeholder':_('1'),'title':_('Minimum Value')}))
    max_unit = forms.CharField(required=True, error_messages={'required': _('Please enter the maximum value')},widget=forms.TextInput({'class':'fm','placeholder':_('2'),'maxlength':'120','title':_('Maximum Value')}))
    unit = forms.ChoiceField(choices=DELIVERY_TIME_UNIT_CHOICES, widget=forms.Select(attrs={'class':'select-menu fm'}),error_messages={'required': _('Please select the unit')})
    description = forms.CharField(required=False,max_length=300, error_messages={'required': _('Please enter Description')},widget=forms.Textarea(attrs={'class':'fm','cols':30,'rows':5,'style':'height:70px;','title':_('Description')}))
    
    class Meta:
        model=DeliveryTime  
        fields=('min_unit','max_unit','unit','description')     
        
        
class AddPropertyForm(forms.ModelForm):
    name = forms.CharField(required=True,max_length=200, error_messages={'required': _('Property name is required')},
                    widget=forms.TextInput({'class':'fl','maxlength':'120','placeholder':_('Internal name of the property'),'title':_('Property Name'),'autocomplete':'off'}))    
    title = forms.CharField(required=True,max_length=200, error_messages={'required': _('property title is required')},
                    widget=forms.TextInput({'class':'fl','maxlength':'120','placeholder':_('Title Displayed to the customer'),'title':_('Property Title Displayed to the customer'),'autocomplete':'off'}))    
    short_description = forms.CharField(required=False,max_length=200, error_messages={'required': _('Please enter the description')},
                    widget=forms.Textarea({'class':'fl','cols':30,'rows':5,'style':'height:90px;','title':_('Description')})) 
    position = forms.IntegerField(required=False,initial=0,
                    widget=forms.TextInput(attrs={'class':'textField','style':'width:40px; height:21px;'}))
    type = forms.ChoiceField(choices=PROPERTY_FIELD_CHOICES,error_messages={'required': _('Field type is required')},
                    widget=forms.Select(attrs={'class':'select-menu fm','onchange':'show_field_type()'}))
    display_on_product  = forms.BooleanField(required=False,widget=forms.CheckboxInput())
    filterable  = forms.BooleanField(required=False,widget=forms.CheckboxInput())
    display_no_results  = forms.BooleanField(required=False,widget=forms.CheckboxInput())
    
    class Meta:
        model=BMProperty  
        fields=('name','title','short_description','position','type','display_on_product','filterable')         
    
    def clean(self):
        cleaned_data = super(AddPropertyForm, self).clean()   
        p_name = self.cleaned_data.get("name")
        if p_name:
            flag=BMProperty.objects.filter(name__iexact=p_name)
            if flag:self._errors["name"] = self.error_class([_("This property is alerady exist!")]) 
        return cleaned_data    

class EditPropertyForm(forms.ModelForm):
    name = forms.CharField(required=True,max_length=200, error_messages={'required': _('Property name is required')},
                    widget=forms.TextInput({'class':'fl','maxlength':'120','title':_('Property Name'),'autocomplete':'off'}))    
    title = forms.CharField(required=True,max_length=200, error_messages={'required': _('property title is required')},
                    widget=forms.TextInput({'class':'fl','maxlength':'120','title':_('property Title'),'autocomplete':'off'}))    
    short_description = forms.CharField(required=False,max_length=200, error_messages={'required': _('Please enter the description')},
                    widget=forms.Textarea({'class':'fl','cols':30,'rows':5,'style':'height:70px;','title':_('Description')})) 
    position = forms.IntegerField(required=False,initial=0,
                    widget=forms.TextInput(attrs={'class':'textField','style':'width:40px; height:21px;'}))
    type = forms.ChoiceField(choices=PROPERTY_FIELD_CHOICES,error_messages={'required': _('Field type is required')},
                    widget=forms.Select(attrs={'class':'select-menu fm','onchange':'show_field_type()'}))
    display_on_product  = forms.BooleanField(required=False,widget=forms.CheckboxInput())
    filterable  = forms.BooleanField(required=False,widget=forms.CheckboxInput())
    display_no_results  = forms.BooleanField(required=False,widget=forms.CheckboxInput())
    
    class Meta:
        model=BMProperty  
        fields=('name','title','short_description','position','type','display_on_product','filterable','display_no_results')      
        
class AddPropertyGroupForm(forms.ModelForm):
    name = forms.CharField(required=True,max_length=200, error_messages={'required': _('Property Group name is required')},
                    widget=forms.TextInput({'class':'fm','maxlength':'120','title':_('Property Group Name'),'autocomplete':'off'}))    
    """
    products = forms.ModelMultipleChoiceField(required=False, queryset=Product.objects.order_by('name'),
                    widget=forms.SelectMultiple(attrs={'class':'select-menu fm','data-placeholder':_('Select products'),'onchange':'$.colorbox.resize();'}), error_messages={'required': _('Please select products')})
    """
    position = forms.IntegerField(required=False,initial=0,
                    widget=forms.TextInput(attrs={'class':'textField','style':'width:40px; height:21px;'}))
    class Meta:
        model=BMPropertyGroup  
        fields=('name','position')   
    
            
class ManufactureForm(forms.ModelForm):
    name = forms.CharField(required=True,max_length=200, error_messages={'required': _('Please enter the name')},widget=forms.TextInput({'class':'fm','maxlength':'120','onkeyUp':'string_to_slug(this.value)','title':_('Category Name'),'autocomplete':'off'}))
    slug = forms.CharField(required=True, widget=forms.TextInput({'class':'default-url','style':'width:139px;','title':_('Category Slug'),'maxlength':'200','onkeyUp':'string_to_slug(this.value)','autocomplete':'off'}), error_messages={'required': _('Please enter the slug')})
    class Meta:
        model = Manufacturer
        exclude = ('categories',)    
                
        
        
        
        
        
        
        
        
        
        
        
        
           
        