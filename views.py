from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, ListView, UpdateView, TemplateView
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from .models import Product, Category, Supplier
from .forms import ProductForm, ProductFilterForm, CategoryForm, CategoryFilterForm, SupplierForm, SupplierFilterForm
from core.utils import get_query_conditions

# BASIC
class IndexView(TemplateView):
    template_name = 'xlsx/basic/index.html'
    
# PRODUCT
class ProductListView(ListView):
    model = Product
    template_name = 'xlsx/product/grid.html'
    context_object_name = 'products_records'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = ProductFilterForm(self.request.GET)
        return context
    
    def get_queryset(self):
        queryset = Product.objects.filter(status=1)
        if self.request.GET:
            filter_form = ProductFilterForm(self.request.GET)
            if filter_form.is_valid():
                #Prepare filters dict
                filters_dict = {
                    'code':'iexact',
                    'name':'icontains',
                    'category':'exact',
                    'supplier':'exact',
                    'status':'exact'
                }
                query_filters = get_query_conditions(filter_form.cleaned_data,filters_dict) #Get conditions
                query_filters &= Q(status = 1) #Add aditional filter
                queryset = Product.objects.filter(query_filters)
                return queryset
            else:
                messages.error(request=self.request,message='Your filters present some issues, please check and try again.')
        return queryset

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
    
class ProductUpdateView(UpdateView):
    form_class = ProductForm
    queryset = Product.objects.filter(status=1)
    model = Product
    template_name = 'xlsx/product/update.html'
    success_url = reverse_lazy('xlsx:product_grid')
    
    def form_valid(self, form):
        messages.success(request=self.request,message=_('Your product has been updated successfully.'))
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(request=self.request,message=_('Your data has some errors, please check and try again.'))
        return super().form_invalid(form)

# CATEGORY
class CategoryListView(ListView):
    model = Category
    template_name = 'xlsx/category/grid.html'
    context_object_name = 'category_records'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = CategoryFilterForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = Category.objects.filter(status=1)
        if self.request.GET:
            filter_form = CategoryFilterForm(self.request.GET)
            if filter_form.is_valid():
                #Prepare filters dict
                filters_dict = {
                    'name':'icontains',
                    'status':'exact'
                }
                query_filters = get_query_conditions(filter_form.cleaned_data,filters_dict) #Get conditions
                query_filters &= Q(status = 1) #Add aditional filter
                queryset = Category.objects.filter(query_filters)
                return queryset
            else:
                messages.error(request=self.request,message='Your filters present some issues, please check and try again.')
        return queryset

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

class CategoryUpdateView(UpdateView):
    form_class = CategoryForm
    queryset = Category.objects.filter(status=1)
    model = Category
    template_name = 'xlsx/category/update.html'
    success_url = reverse_lazy('xlsx:category_grid')
    
    def form_valid(self, form):
        messages.success(request=self.request,message=_('Your category has been updated successfully.'))
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(request=self.request,message=_('Your data has some errors, please check and try again.'))
        return super().form_invalid(form)

# SUUPPLIER
class SupplierListView(ListView):
    model = Supplier
    template_name = 'xlsx/supplier/grid.html'
    context_object_name = 'supplier_records'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = SupplierFilterForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = Supplier.objects.filter(status=1)
        if self.request.GET:
            filter_form = SupplierFilterForm(self.request.GET)
            if filter_form.is_valid():
                #Prepare filters dict
                filters_dict = {
                    'name':'icontains',
                    'status':'exact'
                }
                query_filters = get_query_conditions(filter_form.cleaned_data,filters_dict) #Get conditions
                query_filters &= Q(status = 1) #Add aditional filter
                queryset = Supplier.objects.filter(query_filters)
                return queryset
            else:
                messages.error(request=self.request,message='Your filters present some issues, please check and try again.')
        return queryset

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

class SupplierUpdateView(UpdateView):
    form_class = SupplierForm
    queryset = Supplier.objects.filter(status=1)
    model = Supplier
    template_name = 'xlsx/supplier/update.html'
    success_url = reverse_lazy('xlsx:supplier_grid')
    
    def form_valid(self, form):
        messages.success(request=self.request,message=_('Your supplier has been updated successfully.'))
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(request=self.request,message=_('Your data has some errors, please check and try again.'))
        return super().form_invalid(form)