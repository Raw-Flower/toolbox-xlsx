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
      
    # Init method with custom parameter
    def __init__(self,*args, config_id=None, file_type=None, **kwargs): #Send custom parameter to form
        self.file_type = 1 if file_type == 'export' else 2
        self.config_id = config_id
        super().__init__(*args, **kwargs)
        
        if config_id: # Check if the custom parameter has form
            instance = Configuration.objects.get(id=config_id)
            model = apps.get_model(instance.app,instance.model) # Get the model instance
            field_choices = [(field.name,field.name) for field in model._meta.fields] #Create choices list
            field_choices.insert(0,('','--Select field--')) #Default choice
            self.fields['value'].choices = field_choices #Assing choices to the field
            
    def clean_column(self):
        column2check = self.cleaned_data.get('column')
        type2filter = self.file_type if not self.instance.id else self.instance.type
        queryset = Template.objects.filter(column=column2check,type=type2filter,configuration=self.config_id)
        if self.instance.id:
            queryset = queryset.exclude(id=self.instance.id)
        if queryset.exists():
            raise ValidationError(
                message=_('Selected column is already occupied.'),
                code='column_occupied'
            )
        return column2check
    
    def clean_value(self):
        value2check = self.cleaned_data.get('value')
        type2filter = self.file_type if not self.instance.id else self.instance.type
        queryset = Template.objects.filter(value=value2check,type=type2filter,configuration=self.config_id)
        if self.instance.id:
            queryset = queryset.exclude(id=self.instance.id)
        if queryset.exists():
            raise ValidationError(
                message=_('Model field selected is already configure on the XLSX file.'),
                code='value_occupied'
            )
        return value2check
    
class ExportParamsForm(forms.Form):
    app = forms.CharField(
        label='app', 
        max_length=255,
        validators=[
            RegexValidator(
                regex='^[a-z][a-z0-9_]*$',
                message='App name provide is invalid',
                code='invalid_app'
            )
        ]
    )
    
    model = forms.CharField(
        label='model', 
        max_length=255,
        validators=[
            RegexValidator(
                regex='^[A-Z][a-zA-Z0-9]*$',
                message='Model name provide is invalid',
                code='invalid_model'
            )
        ]
    )
    
    '''
    template_type = forms.ChoiceField(
        label='template_type', 
        choices=[
            ('1','export'),
            ('2','import')
        ], 
    )
    '''
            
    def clean_model(self):
        try:
            model = apps.get_model(app_label=self.cleaned_data['app'], model_name=self.cleaned_data['model'])
        except LookupError:
            raise ValidationError(
                message='The app or model provide are not valid',
                code='model_not_found'
        )
        else:
            return self.cleaned_data['model']

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