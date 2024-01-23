from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Production)
class MaterialStockAdmin(admin.ModelAdmin):
    list_display = ('productionUnit', 'created_at', 'updated_at')
from django.contrib import admin
from .models import *
# Register your models here.
from sales.models import *
from accounting.models import *
from .models import *

admin.site.register(ProducedRow)
admin.site.register(ReadyToDispatch)
admin.site.register(AllocatedMaterialProductionFlow)