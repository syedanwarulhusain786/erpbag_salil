from django.shortcuts import render
from commonApp.models import *

from inventory.models import *
from accounting.models import *
from login.models import *

# Create your views here.
from django.contrib.auth.decorators import login_required
from .models import *
from accounting.models import *
from django.db.models import Q
from login.models import *

from django.shortcuts import render, redirect, get_object_or_404
from inventory.models import *

from django.template.loader import get_template


from django.shortcuts import render, redirect


from django.contrib.auth.decorators import user_passes_test
from login.models import CustomUser
@login_required(login_url='login')
def hrd_home(request):
    return render(request, 'hrd_home.html')

# Create your views here.
@login_required(login_url='login')
def addaccountingsupplier(request):
    IndividualAccount_list=Ledger.objects.all()
    group=Group.objects.all()
    primarGroup=Primary_Group.objects.all()
    accountType=AccountType.objects.all()
    latest_quotation = Supplier.objects.order_by().last()
    next_Supplier_number = latest_quotation.supplier_id + 1 if latest_quotation else 100
    latestCustomer_quotation = Customer.objects.order_by().last()
    next_Customer_number = latestCustomer_quotation.customer_id + 1 if latestCustomer_quotation else 100
    if request.method == 'POST':
        voucher_no = request.POST.get('voucher_no')
        account_type = request.POST.get('account_type')
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('firstName')
        
        last_name = request.POST.get('lastName')
        supplier_code = request.POST.get('supplierCode')
        
        credit_period = request.POST.get('creditPeriod', 0)
        credit_limit = request.POST.get('creditLimit', 0)
        mailing_name = request.POST.get('mailingName')
        phone = request.POST.get('phone')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        bank_account = request.POST.get('bankAccount')
        branch_name = request.POST.get('branch_name') 
        tin = request.POST.get('tin')
        narration = request.POST.get('narration')
        gst_no = request.POST.get('GstNo')
        pan = request.POST.get('pan')
        opening_balance = request.POST.get('openingBalance', 0)
        route_id = request.POST.get('routeId')
        area_id = request.POST.get('areaCode')
        address = request.POST.get('address')
        user=CustomUser()
        user.is_superuser=False
        user.username=username
        user.first_name=first_name
        user.last_name=last_name
        user.email=email
        user.is_staff=False
        user.is_active=True
        user.account_type=AccountType.objects.get(name=account_type)
        user.company=Company.objects.get(id=request.user.company.id)
        user.department=Department.objects.get(name='NONE')
        user.set_password(password)
        user.save()

    
    latest_quotation = Supplier.objects.order_by().last()
    next_Supplier_number = latest_quotation.supplier_id + 1 if latest_quotation else 100
    return render(request,'suppliers/addsupplier.html',context={
            'username':request.user,'IndividualAccount_list':IndividualAccount_list,
            'group':group,'primaryGroup':primarGroup,'next_Supplier_number':next_Supplier_number,'accountType':accountType
        })


# views.py

from django.shortcuts import render, redirect
from .forms import EmployeeForm,CustomUserCreationForm,  WorkForm, DocumentTypeForm, DocumentForm, EmployeeDocumentForm

# views.py
from django.shortcuts import render, redirect
from .forms import EmployeeForm,CustomUserUpdateForm,EmployeeUpdateForm

def create_employee(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST, request.FILES)
        employee_form = EmployeeForm(request.POST, request.FILES)
        print("User form errors:", user_form.errors)
        print("Employee form errors:", employee_form.errors)
        if user_form.is_valid() and employee_form.is_valid():
            # Save the user object
            user = user_form.save()
            
            # Save the employee object with the user reference
            employee = employee_form.save(commit=False)
            employee.user = user
            employee.save()

            # Log the user in

            return redirect('user_details', employee_id=employee_form.id)

    else:
        user_form = CustomUserCreationForm()
        employee_form = EmployeeForm()

    return render(request, 'employee/add_employee.html', {'form': user_form, 'employee_form': employee_form})



def user_list(request):
    users = CustomUser.objects.all()
    return render(request, 'employee/all_employee.html', {'users': users})


# def user_details(request, user_id):
#     user = get_object_or_404(CustomUser, id=user_id)
#     employee = get_object_or_404(Employee, user=user)
#     return render(request, 'employee/user_details.html', {'user': user, 'employee': employee})

def user_details(request, user_id):
    # Get the existing user object
    user = get_object_or_404(CustomUser, id=user_id)
    employee = Employee.objects.get(user=user)

    if request.method == 'POST':
        # Populate the forms with existing data
        user_form = CustomUserUpdateForm(request.POST,request.FILES, instance=user)
        employee_form = EmployeeUpdateForm(request.POST, request.FILES, instance=employee)
        
        print("User form errors:", user_form.errors)
        print("Employee form errors:", employee_form.errors)
        if user_form.is_valid() and employee_form.is_valid():
            # Save the updated user and employee data
            user_form.save()
            employee_form.save()

            return redirect('user_list')

    else:
        # Populate the forms with existing data
        user_form = CustomUserUpdateForm(instance=user)
        employee_form = EmployeeUpdateForm(instance=employee)

    return render(request, 'employee/user_details.html', {'user_form': user_form, 'employee_form': employee_form, 'user': user})











def create_department(request):
    if request.method == 'POST':
        form = WorkForm(request.POST)
        if form.is_valid():
            department = form.save()
            return redirect('department_detail', department_id=department.id)
    else:
        form = DepartmentForm()

    return render(request, 'your_template_path/create_department.html', {'form': form})

def create_position(request):
    if request.method == 'POST':
        form = WorkForm(request.POST)
        if form.is_valid():
            position = form.save()
            return redirect('position_detail', position_id=position.id)
    else:
        form = WorkForm()

    return render(request, 'your_template_path/create_position.html', {'form': form})

def create_document_type(request):
    if request.method == 'POST':
        form = DocumentTypeForm(request.POST)
        if form.is_valid():
            document_type = form.save()
            return redirect('document_type_detail', document_type_id=document_type.id)
    else:
        form = DocumentTypeForm()

    return render(request, 'your_template_path/create_document_type.html', {'form': form})

def create_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save()
            return redirect('document_detail', document_id=document.id)
    else:
        form = DocumentForm()

    return render(request, 'your_template_path/create_document.html', {'form': form})

def add_documents_to_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)

    if request.method == 'POST':
        form = EmployeeDocumentForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_detail', employee_id=employee.id)
    else:
        form = EmployeeDocumentForm(instance=employee)

    return render(request, 'your_template_path/add_documents_to_employee.html', {'form': form, 'employee': employee})
