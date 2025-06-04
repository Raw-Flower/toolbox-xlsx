from django import forms
from django.core.validators import RegexValidator
from django.apps import apps
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Product, Category, Supplier, Status, Configuration, Template
from .utils import getCurrentApps, getCurrentModels, getColumnsChoices

class ConfigurationForm(forms.ModelForm):
    app = forms.ChoiceField(
        label='App',
        help_text='Apps located physically in your project',
        choices=getCurrentApps
    )
    
    model = forms.ChoiceField(
        label='Model',
        help_text='Models related to the app selected',
        choices=getCurrentModels
    )
    
    class Meta:
        model = Configuration
        fields = ['app','model']
    
    def clean_app(self):
        app = self.cleaned_data.get('app')
        allow_apps = [v[1] for i,v in enumerate(getCurrentApps()) if v[1] !='-- Select app --']
        if app not in allow_apps:
            raise ValidationError(
                message=_("The app selected is not located physically in your project or doesn't exist"),
                code='app_not_found'
            )
        return app
    
    def clean_model(self):
        model = self.cleaned_data.get('model')
        app = self.cleaned_data.get('app')
        if not app:
            raise ValidationError(
                message=_("You must to select an app first"),
                code='app_required'
            )
        else:
            app_obj = apps.get_app_config(app)
            models_related = [model.__name__ for model in app_obj.get_models()]
            if model not in models_related:
                raise ValidationError(
                    message=_("The model is not related to the app selected"),
                    code='model_not_related'
                )
            if Configuration.objects.filter(app=app,model=model).exists():
                raise ValidationError(
                    message=_("This model already have a XLSX configuration"),
                    code='config_exist'
                )
        return model
    
    
class TemplateForm(forms.ModelForm):
    column = forms.ChoiceField(
        label='Column',
        help_text='Column on XLSX file',
        choices=getColumnsChoices
    )
    
    value = forms.ChoiceField(
        label='Value',
        help_text='Fields from model'
    )
    
    class Meta:
        model = Template 
        fields = ['label','column','value']
        help_texts = {
            'label':'Column label located in XLSX file'
        }
      
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Check if instance exist
        if self.instance:
            app2get = self.instance.configuration.app # Get the app
            model2get = self.instance.configuration.model # Get the model
            model = apps.get_model(app2get,model2get) # Get the model instance
            field_choices = [(field.name,field.name) for field in model._meta.fields] #Create choices list
            self.fields['value'].choices = field_choices #Assing choices to the field
            
    def clean_column(self):
        column2check = self.cleaned_data.get('column')
        if Template.objects.filter(column=column2check,type=self.instance.type).exclude(pk=self.instance.id).exists():
            raise ValidationError(
                message=_('Column already configure'),
                code='column_occupied'
            )
        return column2check

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['code','name','category','supplier','income_price','outcome_price','extra_info']
        widgets = {
            'extra_info':forms.Textarea(
                attrs={
                    'rows':'3',
                    'style':'max-width:500px;'
                }
            )
        }
        
class ProductFilterForm(forms.Form):
    code = forms.CharField(
        help_text='filter_option',
        required=False,
        max_length=6, 
        strip=True,
        widget=forms.TextInput(attrs={
            'placeholder':'Code'
        }),
        validators=[
            RegexValidator(regex='^[a-zA-Z0-9 -]+$',message='This field contains invalid characters.')
        ]
    )
    
    name = forms.CharField(
        help_text='filter_option',
        required=False,
        max_length=100, 
        strip=True,
        widget=forms.TextInput(attrs={
            'placeholder':'Name'
        }),
        validators=[
            RegexValidator(regex='^[a-zA-Z0-9 ]+$',message='This field contains invalid characters.')
        ]
    )
    
    category = forms.ModelChoiceField(
        help_text='filter_option',
        required=False,
        queryset=Category.objects.filter(status=1),
        empty_label='-- Category --',
        validators=[
            RegexValidator(regex='^[a-zA-Z0-9 ]+$',message='This field contains invalid characters.')
        ]
    )
        
    supplier = forms.ModelChoiceField(
        help_text='filter_option',
        required=False,
        queryset=Supplier.objects.filter(status=1),
        empty_label='-- Supplier --',
        validators=[
            RegexValidator(regex='^[a-zA-Z0-9 ]+$',message='This field contains invalid characters.')
        ]
    )
    
    status = forms.ChoiceField(
        help_text='filter_option',
        required=False,
        choices=Status.choices,
        widget = forms.Select(
            attrs={
                'class':'form-control'
            }
        ),
         validators=[
            RegexValidator(regex='^[0-9]+$',message='This field contains unvalid characters.')
        ]
    )

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name','description']
        widgets = {
            'description':forms.Textarea(
                attrs={
                    'rows':'3',
                    'style':'max-width:500px;'
                }
            )
        }
        
class CategoryFilterForm(forms.Form):
    name = forms.CharField(
        help_text='filter_option',
        required=False,
        max_length=100, 
        strip=True,
        widget=forms.TextInput(attrs={
            'placeholder':'Name'
        }),
        validators=[
            RegexValidator(regex='^[a-zA-Z0-9 ]+$',message='This field contains invalid characters.')
        ]
    )

    status = forms.ChoiceField(
        help_text='filter_option',
        required=False,
        choices=Status.choices,
        widget = forms.Select(
            attrs={
                'class':'form-control'
            }
        ),
         validators=[
            RegexValidator(regex='^[0-9]+$',message='This field contains unvalid characters.')
        ]
    )

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name','extra_info']
        widgets = {
            'extra_info':forms.Textarea(
                attrs={
                    'rows':'3',
                    'style':'max-width:500px;'
                }
            )
        }

class SupplierFilterForm(forms.Form):
    name = forms.CharField(
        help_text='filter_option',
        required=False,
        max_length=100, 
        strip=True,
        widget=forms.TextInput(attrs={
            'placeholder':'Name'
        }),
        validators=[
            RegexValidator(regex='^[a-zA-Z0-9 ]+$',message='This field contains invalid characters.')
        ]
    )

    status = forms.ChoiceField(
        help_text='filter_option',
        required=False,
        choices=Status.choices,
        widget = forms.Select(
            attrs={
                'class':'form-control'
            }
        ),
         validators=[
            RegexValidator(regex='^[0-9]+$',message='This field contains unvalid characters.')
        ]
    )
    
class ConfigurationFilterForm(forms.Form):
    app = forms.CharField(
        help_text='filter_option',
        required=False,
        max_length=255, 
        strip=True,
        widget=forms.TextInput(attrs={
            'placeholder':'App'
        }),
        validators=[
            RegexValidator(regex='^[a-zA-Z]+$',message='This field contains invalid characters.')
        ]
    )
    
    model = forms.CharField(
        help_text='filter_option',
        required=False,
        max_length=255, 
        strip=True,
        widget=forms.TextInput(attrs={
            'placeholder':'Model'
        }),
        validators=[
            RegexValidator(regex='^[a-zA-Z]+$',message='This field contains invalid characters.')
        ]
    )
    
    status = forms.ChoiceField(
        help_text='filter_option',
        required=False,
        choices=Status.choices,
        widget = forms.Select(
            attrs={
                'class':'form-control'
            }
        ),
         validators=[
            RegexValidator(regex='^[0-9]+$',message='This field contains unvalid characters.')
        ]
    )