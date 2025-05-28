from django.urls import path
from .views import *

app_name = 'xlsx'
urlpatterns = [
    #BASIC
    path(route='index/',view=IndexView.as_view(),name='index'),
    path(route='form/<str:model>',view=FormBasicView.as_view(),name='form_view'),
    
    #PRODUCT
    path(route='product/add',view=ProductCreateView.as_view(),name='product_add'),
    path(route='product/grid',view=ProductListView.as_view(),name='product_grid'),
    
    #CATEGORY
    path(route='category/add',view=CategoryCreateView.as_view(),name='category_add'),
    path(route='category/grid',view=CategoryListView.as_view(),name='category_grid'),
    
    #SUPPLIER
    path(route='supplier/add',view=SupplierCreateView.as_view(),name='supplier_add'),
    path(route='supplier/grid',view=SupplierListView.as_view(),name='supplier_grid'),
]
