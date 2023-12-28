from django.contrib import admin

# Register your models here.
# admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,  Work, DocumentType, Employee, Document


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['user', 'work', 'joining_date', 'salary']
    list_filter = ['user__department', 'work']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'user__email']

class DocumentAdmin(admin.ModelAdmin):
    list_display = ['employee', 'document_type', 'upload_date']
    list_filter = ['employee', 'document_type']
    search_fields = ['employee__user__username', 'employee__user__first_name', 'employee__user__last_name', 'employee__user__email']

# Register the models and admins
admin.site.register(Work)
admin.site.register(DocumentType)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Document, DocumentAdmin)
