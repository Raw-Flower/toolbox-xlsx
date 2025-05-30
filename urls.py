from django.urls import path
from .views import *

app_name = 'xlsx'
urlpatterns = [
    #BASIC
    path(route='index/',view=IndexView.as_view(),name='index'),
    path(route='config/',view=StartConfig.as_view(),name='config'),
    path(route='get-models/<str:app_name>', view=get_models),
    
    #PRODUCT
    path(route='product/grid',view=ProductListView.as_view(),name='product_grid'),
    path(route='product/add',view=ProductCreateView.as_view(),name='product_add'),
    path(route='product/update/<int:pk>',view=ProductUpdateView.as_view(),name='product_update'),
    
    #CATEGORY
    path(route='category/grid',view=CategoryListView.as_view(),name='category_grid'),
    path(route='category/add',view=CategoryCreateView.as_view(),name='category_add'),
    path(route='category/update/<int:pk>',view=CategoryUpdateView.as_view(),name='category_update'),
    
    #SUPPLIER
    path(route='supplier/grid',view=SupplierListView.as_view(),name='supplier_grid'),
    path(route='supplier/add',view=SupplierCreateView.as_view(),name='supplier_add'),
    path(route='supplier/update/<int:pk>',view=SupplierUpdateView.as_view(),name='supplier_update'),
]
