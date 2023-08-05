from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Depot)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Subcategory)