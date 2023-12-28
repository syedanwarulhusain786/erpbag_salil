# forms.py

from django import forms
from .models import Employee,  Work, DocumentType, Document
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Employee
from login.models import CustomUser
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.forms import PasswordInput
from login.models import *

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'account_type', 'department', 'company', 'phone_number', 'profilePic']
    
    password2 = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control dark-border', 'placeholder': 'Confirm Password'}))
    password1 = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control dark-border', 'placeholder': 'Password'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control dark-border', 'placeholder': 'Username'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control dark-border', 'placeholder': 'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control dark-border', 'placeholder': 'Last Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control dark-border', 'placeholder': 'Email'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control dark-border', 'placeholder': 'Phone Number'}))
    profile_pic = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control dark-border'}))
    account_type = forms.ModelChoiceField(queryset=AccountType.objects.all(), widget=forms.Select(attrs={'class': 'form-control dark-border'}))
    department = forms.ModelChoiceField(queryset=Department.objects.all(), widget=forms.Select(attrs={'class': 'form-control dark-border'}))
    company = forms.ModelChoiceField(queryset=Company.objects.all(), widget=forms.Select(attrs={'class': 'form-control dark-border'}))
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ('user',)
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control dark-border', 'placeholder': 'Date of Birth', 'type': 'date'}),
            'address': forms.Textarea(attrs={'class': 'form-control dark-border', 'placeholder': 'Address'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control dark-border', 'placeholder': 'Phone Number'}),
            'emergency_contact_name': forms.TextInput(attrs={'class': 'form-control dark-border', 'placeholder': 'Emergency Contact Name'}),
            'emergency_contact_number': forms.TextInput(attrs={'class': 'form-control dark-border', 'placeholder': 'Emergency Contact Number'}),
            'joining_date': forms.DateInput(attrs={'class': 'form-control dark-border', 'placeholder': 'Joining Date', 'type': 'date'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control dark-border', 'placeholder': 'Salary'}),
            'account_holder_name': forms.TextInput(attrs={'class': 'form-control dark-border', 'placeholder': 'Account Holder Name'}),
            'account_number': forms.TextInput(attrs={'class': 'form-control dark-border', 'placeholder': 'Account Number'}),
            'bank_name': forms.TextInput(attrs={'class': 'form-control dark-border', 'placeholder': 'Bank Name'}),
            'branch_name': forms.TextInput(attrs={'class': 'form-control dark-border', 'placeholder': 'Branch Name'}),
            'ifsc_code': forms.TextInput(attrs={'class': 'form-control dark-border', 'placeholder': 'IFSC Code'}),
            'email': forms.EmailInput(attrs={'class': 'form-control dark-border', 'placeholder': 'Email'}),
            'pan': forms.TextInput(attrs={'class': 'form-control dark-border', 'placeholder': 'PAN'}),
        }
        labels = {
        'date_of_birth': 'Date of Birth',
        'address': 'Address',
        'phone_number': 'Phone Number',
        'emergency_contact_name': 'Emergency Contact Name',
        'emergency_contact_number': 'Emergency Contact Number',
        'joining_date': 'Joining Date',
        'salary': 'Salary',
        'account_holder_name': 'Account Holder Name',
        'account_number': 'Account Number',
        'bank_name': 'Bank Name',
        'branch_name': 'Branch Name',
        'ifsc_code': 'IFSC Code',
        'email': 'Email',
        'pan': 'PAN',
    }


CustomUser = get_user_model()

class CustomUserUpdateForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'account_type', 'department', 'company', 'phone_number', 'profilePic']

    password2 = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control dark-border', 'placeholder': 'Confirm Password'}), required=False)
    password1 = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control dark-border', 'placeholder': 'Password'}), required=False)
    # username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control dark-border', 'placeholder': 'Username'}), required=False)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control dark-border', 'placeholder': 'First Name'}), required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control dark-border', 'placeholder': 'Last Name'}), required=False)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control dark-border', 'placeholder': 'Email'}), required=False)
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control dark-border', 'placeholder': 'Phone Number'}), required=False)
    profile_pic = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control dark-border'}), required=False)
    account_type = forms.ModelChoiceField(queryset=AccountType.objects.all(), widget=forms.Select(attrs={'class': 'form-control dark-border'}), required=False)
    department = forms.ModelChoiceField(queryset=Department.objects.all(), widget=forms.Select(attrs={'class': 'form-control dark-border'}), required=False)
    company = forms.ModelChoiceField(queryset=Company.objects.all(), widget=forms.Select(attrs={'class': 'form-control dark-border'}), required=False)

class EmployeeUpdateForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ('user','documents','work')
        
        widgets = {
            
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control dark-border', 'placeholder': 'Date of Birth', 'type': 'date'}),
            'address': forms.Textarea(attrs={'class': 'form-control dark-border', 'placeholder': 'Address'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control dark-border', 'placeholder': 'Phone Number'}),
            'emergency_contact_name': forms.TextInput(attrs={'class': 'form-control dark-border', 'placeholder': 'Emergency Contact Name'}),
            'emergency_contact_number': forms.TextInput(attrs={'class': 'form-control dark-border', 'placeholder': 'Emergency Contact Number'}),
            'joining_date': forms.DateInput(attrs={'class': 'form-control dark-border', 'placeholder': 'Joining Date', 'type': 'date'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control dark-border', 'placeholder': 'Salary'}),
            'account_holder_name': forms.TextInput(attrs={'class': 'form-control dark-border', 'placeholder': 'Account Holder Name'}),
            'account_number': forms.TextInput(attrs={'class': 'form-control dark-border', 'placeholder': 'Account Number'}),
            'bank_name': forms.TextInput(attrs={'class': 'form-control dark-border', 'placeholder': 'Bank Name'}),
            'branch_name': forms.TextInput(attrs={'class': 'form-control dark-border', 'placeholder': 'Branch Name'}),
            'ifsc_code': forms.TextInput(attrs={'class': 'form-control dark-border', 'placeholder': 'IFSC Code'}),
            'email': forms.EmailInput(attrs={'class': 'form-control dark-border', 'placeholder': 'Email'}),
            'pan': forms.TextInput(attrs={'class': 'form-control dark-border', 'placeholder': 'PAN'}),
        }
        labels = {
            'date_of_birth': 'Date of Birth',
            'address': 'Address',
            'phone_number': 'Phone Number',
            'emergency_contact_name': 'Emergency Contact Name',
            'emergency_contact_number': 'Emergency Contact Number',
            'joining_date': 'Joining Date',
            'salary': 'Salary',
            'account_holder_name': 'Account Holder Name',
            'account_number': 'Account Number',
            'bank_name': 'Bank Name',
            'branch_name': 'Branch Name',
            'ifsc_code': 'IFSC Code',
            'email': 'Email',
            'pan': 'PAN',
        }







class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['document_type', 'file']

class EmployeeDocumentForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['documents']


class WorkForm(forms.ModelForm):
    class Meta:
        model = Work
        fields = '__all__'

class DocumentTypeForm(forms.ModelForm):
    class Meta:
        model = DocumentType
        fields = '__all__'
