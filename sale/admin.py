from django.contrib import admin
from .models import *


class DepotModel(admin.ModelAdmin):
    list_display = ('name', 'code')
    list_filter = ('name',)
    search_fields = ['name', 'code']

class CustomerModel(admin.ModelAdmin):
    list_display = ('name', 'code', 'depot')
    list_filter = ('depot',)
    search_fields = ['name', 'code', 'depot__name']
    autocomplete_fields = ['depot']


class SubcategoryModel(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']

class ProductModel(admin.ModelAdmin):
    list_display = ('name', 'code', 'category_name', 'subcategory', 'rate')
    list_filter = ('category_name',)
    search_fields = ['name', 'code', 'category_id', 'size', 'rate']
    autocomplete_fields = ['subcategory']    

class BalanceModel(admin.ModelAdmin):
    list_display = ('customer', 'transaction_id', 'transaction_time', 'category', 'amount')
    list_filter = ('customer__depot',)
    search_fields = ['customer__name', 'transaction_id']
    autocomplete_fields = ['customer']


class StockModel(admin.ModelAdmin):
    list_display = ('depot', 'product', 'quantity')
    list_filter = ('depot',)
    search_fields = ('depot__name', 'product__name')
    autocomplete_fields = ('depot', 'product')


class LineItemInline(admin.TabularInline):
    model = LineItem
    extra = 1

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('custom_invoice_id', 'customer_id', 'invoice_date', 'total_amount', 'payment_amount')
    list_filter = ('payment_status',)
    search_fields = ('custom_invoice_id', 'customer_id__name', 'invoice_date')
    inlines = [LineItemInline]

@admin.register(LineItem)
class LineItemAdmin(admin.ModelAdmin):
    list_display = ('line_item_id', 'invoice', 'product', 'quantity', 'unit_price', 'total_price')
    list_filter = ('invoice__payment_status',)
    search_fields = ('invoice__custom_invoice_id', 'product__name')


# Register your models here.
admin.site.register(Depot, DepotModel)
admin.site.register(Customer, CustomerModel)
admin.site.register(Product, ProductModel)
admin.site.register(Subcategory, SubcategoryModel)
admin.site.register(Balance, BalanceModel)
admin.site.register(Stock, StockModel)