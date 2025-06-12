from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, ListView, UpdateView, TemplateView, DeleteView
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from django.apps import apps
from .models import Product, Category, Supplier, Configuration, Template
from .forms import ProductForm, ProductFilterForm, CategoryForm, CategoryFilterForm, SupplierForm, SupplierFilterForm, ConfigurationForm, ConfigurationFilterForm, TemplateForm, ExportParamsForm
from core.utils import get_query_conditions
from .utils import getModelsByApp, prepare_xlsx_export, sync_def
from .mixins import CheckTypeParameter
from asgiref.sync import sync_to_async
import asyncio

# BASIC
class IndexView(TemplateView):
    template_name = 'xlsx/basic/index.html'

# CORE
class ConfigAdd(CreateView):
    model = Configuration
    form_class = ConfigurationForm
    template_name = 'xlsx/core/config_add.html'
    success_url = reverse_lazy('xlsx:config_grid')
    
    def form_valid(self, form):
        messages.success(request=self.request,message=_('Your configuration has been created successfully.'))
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(request=self.request,message=_('Your data has some errors, please check and try again.'))
        return super().form_invalid(form)
    
class ConfigGrid(ListView):
    model = Configuration
    template_name = 'xlsx/core/config_grid.html'
    context_object_name = 'config_records'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = ConfigurationFilterForm(self.request.GET)
        return context
    
    def get_queryset(self):
        queryset = Configuration.objects.filter(status=1)
        if self.request.GET:
            filter_form = ConfigurationFilterForm(self.request.GET)
            if filter_form.is_valid():
                filters_dict = {
                    'app':'icontains',
                    'model':'icontains',
                    'status':'exact'
                }
                query_filters = get_query_conditions(filter_form.cleaned_data,filters_dict)
                queryset = Configuration.objects.filter(query_filters)
                return queryset
            else:
                messages.error(request=self.request,message='Your filters present some issues, please check and try again.')
        return queryset
    
class TemplateGrid(CheckTypeParameter, ListView):
    model = Template
    template_name = 'xlsx/core/template_grid.html'
    context_object_name = 'export_config'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['config'] = get_object_or_404(Configuration,id=self.kwargs['config_id'])
        return context
    
    def get_queryset(self):
        template_type = 1 if self.request.GET.get('type','export')=='export' else 2
        queryset = Template.objects.filter(configuration=self.kwargs['config_id'],type=template_type)
        return queryset.order_by('column')
    
class TemplateCreateView(CheckTypeParameter, CreateView):
    model = Template
    template_name = 'xlsx/core/template_create.html'
    form_class = TemplateForm
    
    def get_success_url(self):
        return reverse_lazy(
            'xlsx:template_grid', 
            kwargs={
                'config_id':self.kwargs['config_id']
            },
            query={
                'type':self.request.GET['type']
            }
        )
    
    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs['config_id'] = self.kwargs['config_id']
        form_kwargs['file_type'] = self.request.GET['type']
        return form_kwargs
    
    def post(self, request, *args, **kwargs):
        type = self.request.GET['type']
        allow_values = ['export','import']
        if type not in allow_values:
            messages.error(request=self.request,message=_('Type parameter is missing or incorrect, please check and try again.'))
            return redirect('xlsx:config_grid')
        return super().post(request, *args, **kwargs)
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.configuration = Configuration.objects.get(id=self.kwargs['config_id'])
        self.object.type = 1 if self.request.GET['type']=='export' else 2
        messages.success(request=self.request,message=_('Template configuration has been created correctly.'))
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(request=self.request,message=_('You data have some issues, please check and try again.'))
        return super().form_invalid(form)
    
class TemplateUpdateView(UpdateView):
    model = Template
    template_name = 'xlsx/core/template_update.html'
    form_class = TemplateForm
    
    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs['config_id'] = self.kwargs['config_id']
        return form_kwargs
    
    def get_success_url(self):
        template_type = 'export' if self.get_object().type == 1 else 'import'
        return reverse_lazy(
            viewname = 'xlsx:template_grid', 
            kwargs={
                'config_id':self.get_object().configuration.id
            },
            query={
                'type':template_type
            }
        )
    
    def form_valid(self, form):
        messages.success(request=self.request,message=_('Template configuration has been updated correctly.'))
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(request=self.request,message=_('You data have some issues, please check and try again.'))
        return super().form_invalid(form)
    
class TemplateDeleteView(DeleteView):
    model = Template
    template_name = 'xlsx/core/template_delete.html'
    
    def get_success_url(self):
        template_type = 'export' if self.get_object().type == 1 else 'import'
        return reverse_lazy(
            viewname = 'xlsx:template_grid', 
            kwargs={
                'config_id':self.get_object().configuration.id
            },
            query={
                'type':template_type
            }
        )
        
    def form_valid(self, form):
        messages.success(request=self.request,message=_('Template column has been deleted correctly.'))
        return super().form_valid(form)
    
# FUNCTIONS
def get_models(request,app_name):
    models = getModelsByApp(app_name)
    return JsonResponse(
        data={
            'models':models
        }
    )
    
async def async_testing(request):
    result = await sync_to_async(sync_def,thread_sensitive=True)('my_parameter')
    if result:
        print('ejecutado correcto...')
        
    return JsonResponse(
        data={
            'result':True
        }
    )
    
def generate_xlsx_file(request):
    print('generando file...')
    if request.method == 'POST':
        form = ExportParamsForm(request.POST)
        if form.is_valid():
            #Get template configuration
            config_instance = Configuration.objects.get(app=form.cleaned_data.get('app'),model=form.cleaned_data.get('model')) # Get config instance
            template_config = Template.objects.filter(configuration=config_instance.id,type=form.cleaned_data.get('template_type')).order_by('column') # Get template config for export
            model = apps.get_model(app_label=form.cleaned_data.get('app'), model_name=form.cleaned_data.get('model')) # Get model for query
            
            #Prepare parameters for get same result as user
            queryparams = {}
            for field in template_config: # Loop template fields
                if field.value in request.POST and request.POST.get(field.value): # If template field found on user request, added to query params 
                    queryparams[field.value] = request.POST.get(field.value)# Query params same as the user
            queryset = model.objects.filter(**queryparams)# Filter the model loaded and apply the same filters as the user
            
            result = asyncio.run(sync_to_async(prepare_xlsx_export)(queryset,template_config,config_instance.id))
            print(result)
            
            #Create xlsx file
                #create dataframe using pandas
                #Transfer this dataframe to real xlsx file
                #Save this file as a log
                #Return log ID
                
            response = HttpResponse(
                result.getvalue(),
                content='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename=export.xlsx'    
            return response
            
        else:
            errors_list = []
            for field,errors in form.errors.items(): 
                for error in errors:
                    errors_list.append(error)
            return JsonResponse(
                data={
                    'result':False,
                    'form_errors':errors_list
                }
            )
    return JsonResponse(
        data={
            'result':False,
            'error':'Only post request are allow.'
        }
    )

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