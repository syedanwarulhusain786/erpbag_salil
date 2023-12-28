from django.db import models

# Create your models here.
# models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from login.models import *


class Work(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class DocumentType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Employee(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    
    work = models.ForeignKey(Work, on_delete=models.SET_NULL, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    emergency_contact_name = models.CharField(max_length=255, null=True, blank=True)
    emergency_contact_number = models.CharField(max_length=20, null=True, blank=True)
    joining_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Bank Account Details
    account_holder_name = models.CharField(max_length=255, null=True, blank=True)
    account_number = models.CharField(max_length=20, null=True, blank=True)
    bank_name = models.CharField(max_length=255, null=True, blank=True)
    branch_name = models.CharField(max_length=255, null=True, blank=True)
    ifsc_code = models.CharField(max_length=20, null=True, blank=True)

    # Document Upload (Multiple Documents)
    
    
    email = models.EmailField(unique=True)
    pan = models.CharField(max_length=20, null=True, blank=True)
    documents = models.ManyToManyField('Document', blank=True)
    
    # Add more fields as needed

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class Document(models.Model):
    employe = models.ForeignKey(Employee, on_delete=models.CASCADE)
    document_type = models.ForeignKey(DocumentType, on_delete=models.SET_NULL, null=True, blank=True)
    file = models.FileField(upload_to='employee_documents/')
    upload_date = models.DateTimeField(auto_now_add=True)  # Added field

    def __str__(self):
        return f"{self.employe.user.get_full_name()}'s Document - {self.document_type.name}"
