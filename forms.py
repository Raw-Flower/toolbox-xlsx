from django import forms
from .models import Product, Category, Supplier

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
