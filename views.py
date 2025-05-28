from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, TemplateView, FormView
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import Product, Category, Supplier
from .forms import ProductForm, CategoryForm, SupplierForm

# BASIC
class IndexView(TemplateView):
    template_name = 'xlsx/basic/index.html'
    
class FormBasicView(FormView):
    template_name = 'xlsx/basic/form.html'
    
    #Based on the parameters, form will return and render
    def get_form_class(self):
        #return super().get_form_class()
        return ProductForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = 'product'
        return context

# PRODUCT
class ProductListView(ListView):
    queryset = Product.objects.filter(status=1)
    model = Product
    template_name = 'xlsx/product/grid.html'

class ProductCreateView(CreateView):
    form_class = ProductForm
    model = Product
    success_url = reverse_lazy('xlsx:product_grid')
    template_name = 'xlsx/product/create.html'
    
    def form_valid(self, form):
        messages.success(request=self.request,message=_('Your product has been created successfully.'))
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(request=self.request,message=_('Your data has some errors, please check and try again.'))
        return super().form_invalid(form)

# CATEGORY
class CategoryListView(ListView):
    queryset = Category.objects.filter(status=1)
    model = Category
    template_name = 'xlsx/category/grid.html'
    context_object_name = 'category_records'

class CategoryCreateView(CreateView):
    form_class = CategoryForm
    model = Category
    success_url = reverse_lazy('xlsx:category_add')
    template_name = 'xlsx/category/create.html'
    
    def form_valid(self, form):
        messages.success(request=self.request,message=_('Your category has been created successfully.'))
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(request=self.request,message=_('Your data has some errors, please check and try again.'))
        return super().form_invalid(form)

# SUUPPLIER
class SupplierListView(ListView):
    queryset = Supplier.objects.filter(status=1)
    model = Supplier
    template_name = 'xlsx/supplier/grid.html'
    context_object_name = 'supplier_records'

class SupplierCreateView(CreateView):
    form_class = SupplierForm
    model = Supplier
    success_url = reverse_lazy('xlsx:supplier_add')
    template_name = 'xlsx/supplier/create.html'
    
    def form_valid(self, form):
        messages.success(request=self.request,message=_('Your category has been created successfully.'))
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(request=self.request,message=_('Your data has some errors, please check and try again.'))
        return super().form_invalid(form)
