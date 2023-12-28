from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Production)
class MaterialStockAdmin(admin.ModelAdmin):
    list_display = ('sales_order', 'cutting', 'printing', 'stitching', 'packing', 'ready_to_dispatch','created_at','updated_at')
