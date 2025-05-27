from django.contrib import admin
from .models import Product, Category, Supplier

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['code','name','income_price','outcome_price','category','supplier','createtime','status']
    readonly_fields = ['createtime','updatetime']
    list_filter = ['status','category','supplier']
    search_fields = ['code','name']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','createtime','status']
    readonly_fields = ['createtime','updatetime']
    list_filter = ['status']
    search_fields = ['name']

class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name','createtime','status']
    readonly_fields = ['createtime','updatetime']
    list_filter = ['status']
    search_fields = ['name']
    
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Supplier, SupplierAdmin)
