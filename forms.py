from django import forms
from django.core.validators import RegexValidator
from .models import Product, Category, Supplier, Status

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
            RegexValidator(regex='^[a-zA-Z0-9   -]+$',message='This field contains invalid characters.')
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