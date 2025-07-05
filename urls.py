from django.urls import path
from .views import *

app_name = 'xlsx'
urlpatterns = [
    #BASIC
    path(route='index/',view=IndexView.as_view(),name='index'),
    path(route='new-config/',view=ConfigAdd.as_view(),name='config_add'),
    path(route='config-grid/',view=ConfigGrid.as_view(),name='config_grid'),
    path(route='import-template-request/<int:config_id>',view=ConfigImportTemplate_Request.as_view(),name='config_import_template'),
    path(route='template/<int:config_id>',view=TemplateGrid.as_view(),name='template_grid'),
    path(route='template/<int:config_id>/create',view=TemplateCreateView.as_view(),name='template_create'),
    path(route='template/<int:config_id>/update/<int:pk>',view=TemplateUpdateView.as_view(),name='template_update'),
    path(route='template/<int:config_id>/delete/<int:pk>',view=TemplateDeleteView.as_view(),name='template_delete'),
    path(route='get-models/<str:app_name>', view=get_models),
    path(route='get-xlsx-file/', view=generate_xlsx_file),
    path(route='async-def/', view=async_testing),
    path(route='import-panel/<str:app>/<str:model>', view=ImportPanel.as_view(), name='import_panel'),
    path(route='import-template-error-details/<int:log_id>', view=import_error_download, name='import_error_download'),
    
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
