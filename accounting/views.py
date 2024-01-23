from django.shortcuts import render
from django.shortcuts import render, redirect 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from inventory.forms import ProductBrandForm
from datetime import datetime
from .filters import JournalEntryFilter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from django.http import JsonResponse
from django.db.models import Max
from django.db import transaction
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from commonApp.models import *
from accounting.models import *
from django.db.models import Q
from login.models import *
from accounting.currency import currency_symbols
# Create your views here.
# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from inventory.models import *
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from inventory.models import Product
from inventory.forms import ProductDetailsForm  # Replace 'YourProductForm' with your actual form class

from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

from inventory.forms import ProductCategoryForm

from django.shortcuts import render, redirect
from inventory.models import Service
from inventory.forms import ServiceForm


from django.contrib.auth.decorators import user_passes_test
from login.models import CustomUser

def department_check(user, allowed_departments):
    """
    Check if the user's department is in the allowed list.
    """
    return user.department.name in allowed_departments

def department_required(allowed_departments):
    """
    Decorator to restrict access based on the user's department.
    """
    return user_passes_test(lambda u: department_check(u, allowed_departments))

class GeneratePDF(View):
    template_name = 'bills/PurchaseOrder1.html'

    def get(self, request, *args, **kwargs):
        template = get_template(self.template_name)
        context = {'data': 'Your data goes here'}  # Replace with your actual data

        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="output.pdf"'

        # Create PDF for a specific area (e.g., element with ID 'table-container')
        pisa.CreatePDF(html, dest=response)

        return response





def find_max_rows(query):
    row_keys = [key for key in query.keys() if key.startswith(('cat', 'sub', 'ref', 'qty', 'amt'))]

    # Extract the row numbers from the keys and convert them to integers
    row_numbers = [int(key[3:]) for key in row_keys]

    # Find the maximum row number
    max_row_number = max(row_numbers, default=0)

    return max_row_number





#######################Ledgers Create and Chart Of account###################

@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def Account_chart(request):
    Category_list=Group.objects.all()
    # category_data = serializers.serialize('json', Category_list)
    accounts = Ledger.objects.all()

    return render(request, 'accountsCharts.html', context={
        'username':request.user,'IndividualAccount_list':accounts,'account_subcategory':Category_list
    })

from .filters import LedgerEntryFilter

@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def primaryGroup(request):
    IndividualAccount_list=Primary_Group.objects.all()

    currency=[{'key':cur,'value':cur+'-'+currency_symbols[cur]} for cur in currency_symbols]
    
    if request.method=="POST":
        if 'save' in request.POST:
            data = request.POST # Replace with your actual QueryDict data
            primaryType = data.get(f'primaryType', '')
            GroupName = data.get(f'GroupName', '')
            prime=Primary_Group(primary_group_name=GroupName,
                        primary_group_type=primaryType)
            prime.save()
    if request.method=="POST":
        if 'delete' in request.POST:
            account_numberc = request.POST.get('accountNumberc', '')
            # Assuming Primary_Group is your model
            prime_del = get_object_or_404(Primary_Group, primary_group_number=account_numberc)
            prime_del.delete()
    
    
    return render(request, 'master/accountingPrimaryGroup.html', context={
        'username':request.user,'IndividualAccount_list':IndividualAccount_list,'currency':currency,
    })

@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login') 
def groupPage(request):
    IndividualAccount_list=Group.objects.all()
    account_subcategory=Primary_Group.objects.all()
    

    currency=[{'key':cur,'value':cur+'-'+currency_symbols[cur]} for cur in currency_symbols]
    
    if request.method=="POST":
        if 'save' in request.POST:
            data = request.POST # Replace with your actual QueryDict data
            primaryGroupName = data.get(f'primaryGroupName', '')
            GroupName = data.get(f'GroupName', '')
            dr=Primary_Group.objects.get(primary_group_name=primaryGroupName)
            print(dr)
            prime=Group(group_name=GroupName,
                        primary_group=dr)
            prime.save()
    if request.method=="POST":
        if 'delete' in request.POST:
            account_numberc = request.POST.get('accountNumberc', '')
            print(account_numberc,'hhhhhhhhhhh')
            # Assuming Primary_Group is your model
            prime_del = get_object_or_404(Group, group_number=account_numberc)
            prime_del.delete()
    
    
    return render(request, 'master/accountingroup.html', context={
        
        'account_subcategory':account_subcategory,'username':request.user,'IndividualAccount_list':IndividualAccount_list,'currency':currency,
    })
@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def journalEntries(request):
    normalized_data = []
    journal_page_obj=JournalEntryRow.objects.all()

    for journal_entry in journal_page_obj:
        entry_data = {
            
            'voucherNo': journal_entry.entryFk.voucherNo,
            'voucherCode': journal_entry.entryFk.voucherCode,
            'date': journal_entry.entryFk.date,
            'invoice_no': journal_entry.entryFk.invoice_no,
            'invoice_date': journal_entry.entryFk.invoice_date,
            'narration': journal_entry.entryFk.narration,
            'debit_total': journal_entry.entryFk.debit_total,
            'credit_total': journal_entry.entryFk.credit_total,
            
            'ledger_name': journal_entry.ledger.ledger_name,
            'comment': journal_entry.comment,
            'debit': journal_entry.debit,
            'credit': journal_entry.credit,
        }

  

        normalized_data.append(entry_data)
    return render(request, 'vouchers/Journal/journalEntries.html', context={'journal_page_obj':normalized_data})
@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def Gernal_Ledger(request):
    
    accounts = Ledger.objects.all()
    q = request.GET.get('q')
    types = ''
    led = ''
    lis = []
    result = {}
    cat = ''
    subcat = ''
    total_debit = 0
    total_credit = 0
    total_balance = 0

    if q:
        # Assuming you have a ForeignKey relationship between LedgerEntry and DeliveryDetails
        # and LedgerEntry has fields like debit_amount, credit_amount, and date
        ledgers = LedgerEntry.objects.filter(account=Ledger.objects.get(ledger_number=q))

        # Calculate running balances and totals
        running_balance = 0
        for entry in ledgers:
            entry.balance = running_balance + entry.debit_amount - entry.credit_amount
            running_balance = entry.balance

            # Update total debit and credit
            total_debit += entry.debit_amount
            total_credit += entry.credit_amount

            if entry.balance < 0:
                entry.balance = entry.balance * -1
                types = 'Cr'
            else:
                types = 'Dr'

        # Calculate total balance
        total_balance = total_debit - total_credit
        if total_balance<0:
            total_balance=total_balance*-1
        # Pass the ledger entries and totals to the template
        lis = ledgers
        
        led = Ledger.objects.get(ledger_number=q)
        

    return render(request, 'ledgers/ledger.html', context={'heading': led, 'cat': cat, 'subcat': subcat,
                                                             'username': request.user, 'account_list': accounts,
                                                             'led': lis, 'result': result,
                                                             'types': types,
                                                             'total_debit': total_debit,
                                                             'total_credit': total_credit,
                                                             'total_balance': total_balance})


# views.py
from django.shortcuts import render
from .models import LedgerEntry
from .filters import LedgerEntryFilter
@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def LedgerEntries(request):
    
    ledger_entries = LedgerEntry.objects.all()

    # Apply the date range filter
    ledger_filter = LedgerEntryFilter(request.GET, queryset=ledger_entries)

    return render(request, 'ledgers/ledgerEntries.html', context={'ledger_filter': ledger_filter})


@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def  accountingledger(request):
    IndividualAccount_list=Ledger.objects.all()
    group=Group.objects.all()
    primarGroup=Primary_Group.objects.all()
    
    
    currency=[{'key':cur,'value':cur+'-'+currency_symbols[cur]} for cur in currency_symbols]
    
    if request.method=="POST":
        if 'save' in request.POST:
            data = request.POST # Replace with your actual QueryDict data
            primaryGroupName = data.get(f'primaryGroupName', '')
            GroupName= data.get(f'GroupName', '')
            dr=Group.objects.get(group_number=primaryGroupName)
     
            prime=Ledger(group=dr,
                         ledger_name=GroupName)
            prime.save()
    if request.method=="POST":
        if 'delete' in request.POST:
            account_numberc = request.POST.get('accountNumberc', '')
            
            # Assuming Primary_Group is your model
            prime_del = get_object_or_404(Ledger, ledger_number=account_numberc)
            prime_del.delete()
    
    return render(request, 'master/accountingledger.html', context={
            'username':request.user,'IndividualAccount_list':IndividualAccount_list,
            'group':group,'primaryGroup':primarGroup,'currency':currency
        })
###############################################################################

#######################Customers Start##################

@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def accountingcustomer(request):
    IndividualAccount_list=Ledger.objects.all()
    group=Group.objects.all()
    primarGroup=Primary_Group.objects.all()
    Supplier_List=Customer.objects.all()
    
    if request.method == 'POST':
        accountNumberc = request.POST.get('accountNumberc', '')
        Supp=Customer.objects.get(supplier_id=accountNumberc)
        Supp.delete()
    return render(request,'customer/customers.html',context={
            'username':request.user,'IndividualAccount_list':IndividualAccount_list,
            'group':group,'primaryGroup':primarGroup,'cust_List':Supplier_List
        })

@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def addaccountingcustomer(request):
    IndividualAccount_list=Customer.objects.all()
    group=Group.objects.all()
    primarGroup=Primary_Group.objects.all()
    Supplier_List=Customer.objects.all()
    
    if request.method == 'POST':
        voucher_no = request.POST.get('voucher_no', '')
        customerName = request.POST.get('customerName', '')
        customerCode = request.POST.get('customerCode', '')
        creditPeriod = request.POST.get('creditPeriod', 0)
        credit_limit = request.POST.get('creditLimit', 0)
        mailing_name = request.POST.get('mailingName', '')
        phone = request.POST.get('phone', '')
        mobile = request.POST.get('mobile', '')
        email = request.POST.get('email', '')
        bank_account = request.POST.get('bankAccount', '')
        branch_name = request.POST.get('branch_name', '') 
        tin = request.POST.get('tin', '')
        narration = request.POST.get('narration', '')
        gst_no = request.POST.get('GstNo', '')
        pan = request.POST.get('pan', '')
        opening_balance = request.POST.get('openingBalance', 0)
        route_id = request.POST.get('routeId', '')
        area_id = request.POST.get('areaCode', '')
        address = request.POST.get('address', '')

        # Check if the "Add To Ledger" checkbox is selected
        add_to_ledger = request.POST.get('enable_options', False)
        ledger=None
        if add_to_ledger:
            primary_group_number = request.POST.get('primaryGroupName', '')
            group_number = request.POST.get('GroupName', '')
            primary=Primary_Group.objects.get(primary_group_number=primary_group_number)
            groups=Group.objects.get(group_number=group_number)
            ledger=Ledger.objects.create(
                group=groups,
                ledger_name=customerName,
                ledger_limit = credit_limit ,
                opening_balance = opening_balance,

            )
        supp=Customer(
            legder= ledger,
            customer_id=voucher_no,
            customer_name=customerName,
            customer_code=customerCode,
            credit_period=creditPeriod,
            credit_limit=credit_limit,
            mailing_name=mailing_name,            
            phone=phone,
            email=email,
            bank_account=bank_account,
            tin=tin,
            
            narration=narration,
            gst_no=gst_no,
            pan=pan,
            opening_balance=opening_balance,
            route_id=route_id,
            area_id=area_id,
            branch_name=branch_name,
            address=address,
            mobile=mobile,
            
        )
        
        supp.save()
    
    
    
    
    
    
    

    latest_quotation = Customer.objects.order_by().last()
    next_Supplier_number = latest_quotation.customer_id + 1 if latest_quotation else 100    
    return render(request,'customer/addcustomer.html',context={
            'username':request.user,'IndividualAccount_list':IndividualAccount_list,
            'group':group,'primaryGroup':primarGroup,'Supplier_List':Supplier_List,
            'next_Supplier_number':next_Supplier_number
        })
#######################Customers Finished##################



################Supplier Start##############


@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def addaccountingsupplier(request):
    IndividualAccount_list=Ledger.objects.all()
    group=Group.objects.all()
    primarGroup=Primary_Group.objects.all()
    
    if request.method == 'POST':
        voucher_no = request.POST.get('voucher_no', '')
        supplier_name = request.POST.get('supplierName')
        supplier_code = request.POST.get('supplierCode', '')
        credit_period = request.POST.get('creditPeriod', 0)
        credit_limit = request.POST.get('creditLimit', 0)
        mailing_name = request.POST.get('mailingName', '')
        phone = request.POST.get('phone', '')
        mobile = request.POST.get('mobile', '')
        email = request.POST.get('email', '')
        bank_account = request.POST.get('bankAccount', '')
        branch_name = request.POST.get('branch_name', '') 
        tin = request.POST.get('tin', '')
        narration = request.POST.get('narration', '')
        gst_no = request.POST.get('GstNo', '')
        pan = request.POST.get('pan', '')
        opening_balance = request.POST.get('openingBalance', 0)
        route_id = request.POST.get('routeId', '')
        area_id = request.POST.get('areaCode', '')
        address = request.POST.get('address', '')

        # Check if the "Add To Ledger" checkbox is selected
        add_to_ledger = request.POST.get('enable_options', False)
        ledger=None
        if add_to_ledger:
            # primary_group_number = request.POST.get('primaryGroupName', '')
            group_number = request.POST.get('GroupName', '')
            # primary=Primary_Group.objects.get(primary_group_number=primary_group_number)
            groups=Group.objects.get(group_number=group_number)
            ledger=Ledger.objects.create(
                group=groups,
                ledger_name=supplier_name,
                ledger_limit = credit_limit ,
                opening_balance = opening_balance,

            )
            
        supp=Supplier(
            ledger= ledger,
            supplier_id=voucher_no,
            supplier_name=supplier_name,
            supplier_code=supplier_code,
            credit_period=credit_period,
            credit_limit=credit_limit,
            mailing_name=mailing_name,            
            phone=phone,
            mobile=mobile,
            email=email,
            bank_account=bank_account,
            tin=tin,
            narration=narration,
            gst_no=gst_no,
            pan=pan,
            opening_balance=opening_balance,
            route_id=route_id,
            area_id=area_id,
            branch_name=branch_name,
            address=address,
            
        )
        
        supp.save()
    
    
    
    latest_quotation = Supplier.objects.order_by().last()
    next_Supplier_number = latest_quotation.supplier_id + 1 if latest_quotation else 100
    return render(request,'suppliers/addsupplier.html',context={
            'username':request.user,'IndividualAccount_list':IndividualAccount_list,
            'group':group,'primaryGroup':primarGroup,'next_Supplier_number':next_Supplier_number
        })



@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def accountingsupplier(request):
    IndividualAccount_list=Customer.objects.all()
    group=Group.objects.all()
    primarGroup=Primary_Group.objects.all()
    Supplier_List=Supplier.objects.all()
    if request.method == 'POST':
        # Supplier_List=Supplier.objects.get()
        accountNumberc = request.POST.get('accountNumberc', '')
        Supp=Supplier.objects.get(supplier_id=accountNumberc)
        Supp.delete()
        
    return render(request,'suppliers/suppliers.html',context={
            'username':request.user,'IndividualAccount_list':IndividualAccount_list,
            'group':group,'primaryGroup':primarGroup,'Supplier_List':Supplier_List
        })


#######################Suppliers Finished##################





































##################Purchase################
from decimal import Decimal
@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login') 
def purchaseEntry(request):
    suppliers=Supplier.objects.all()
    sundry_creditor_ledgers = Ledger.objects.filter(group__group_name='SUNDRY CREDITORS')
    purchase_ledgers = Ledger.objects.filter(group__group_name='PURCHASE ACCOUNTS')
    tax_ledgers = Ledger.objects.filter(group__group_name='DUTIES & TAXES')

    setting=CompanySettings.objects.all().first()
    products=Product.objects.filter(category__name='purchase')
    materials=Material.objects.all()
    services=Service.objects.filter(category__name='purchase')
    
    
    # services=Service.objects.filter(category=ProductCategory.objects.get(name='Purchase'))
    
    if request.method=='POST':
        # Extract keys that match the pattern 'cat{number}', 'sub{number}', 'ref{number}', etc.
        
        # Handle POST request and process the form data
        purchase_ledgers = request.POST.get('purchase_ledgers')
        tax_ledgers = request.POST.get('tax_ledgers')
        purchaseVdate = request.POST.get('purchaseVdate')
        
        voucher_no = request.POST.get('quotation_number')
        
        invoice_no = request.POST.get('InvNo')
        InvDate = request.POST.get('InvDate')
        if not InvDate:
            InvDate=None
        supplier_id = request.POST.get('supplier_name')
        supplier_mobile = request.POST.get('supplier_mobile')
        supplier_email = request.POST.get('supplier_email')
        supplier_address = request.POST.get('supplier_address')
        billing_address = request.POST.get('billing_address')
        shipping_address = request.POST.get('shipping_address')
        terms = request.POST.get('terms')
        notes = request.POST.get('notes')
        final = request.POST.get('final')     
        tax2 = float(request.POST.get('tax2'))
        s_total = float(request.POST.get('s_total'))
        count=int(request.POST.get('count'))
        quote=PurchaseInvoice(
            supplier = Supplier.objects.get(ledger__id=int(supplier_id)) ,
            PurchaseVoucherNumber = voucher_no, 
            PurchaseVoucherDate = purchaseVdate,
            InvoiceNumber =invoice_no ,
            InvoiceDate = InvDate,
            SupplierMobile = supplier_mobile,
            SupplierEmail = supplier_email,
            SupplierAddress = supplier_address,
            BillingAddress = billing_address,
            ShippingAddress = shipping_address,
            Terms_and_conditions = terms,
            NotesComments = notes,
            SubTotal = s_total,
            Vat = tax2,
            FinalAmount = final,
        )
        quote.save()
        # Add a discount field if you intend to use it
        
 
        for index in range(1,count+1):
                transaction = request.POST.get(f'dropdown{index}')
                transactionType=transaction.split('-')[0]
                
                led=transaction.split('-')[1].strip()
             
                cat=request.POST.get(f'cat{index}')
    
        
                sub=request.POST.get(f'sub{index}')
        
                ref=float(request.POST.get(f'ref{index}'))
            
        
                qty=float(request.POST.get(f'qty{index}'))
    
                amt=float(request.POST.get(f'amt{index}'))
                taxPerProduct=float(request.POST.get(f'tx{index}'))
                # In the view where the purchase is created
                if transactionType=='prod':
                    try:
                        name=Product.objects.get(id=led)
                      
                    except:
                        name=None
                    
        
                
                    # Extract the index from the key (e.g., dropdown1, dropdown2, etc.)
                    PurchaseInvoiceItemRow.objects.create(
                        product=name,
                        quotation=quote,
                        product_name=cat,
                        product_description=sub,
                        quantity=qty,
                        unit_price=ref,
                        total_price=amt,
                        taxPerPiece=taxPerProduct

                        # Add other fields as needed
                    )
                    # Get or create MaterialStock instance
                    # material_stock = ProductStock.objects.get_or_create(
                    #     type='purchase',
                    #     product=name,
                    #     quantity=Decimal(qty),
                    #     cost_of_single=Decimal(ref),
                    # )
                elif transactionType=='mat':
                    try:
                     name=Material.objects.get(id=led)
                    except:
                        name=None
                    
        
                
                    # Extract the index from the key (e.g., dropdown1, dropdown2, etc.)
                    PurchaseInvoiceItemRow.objects.create(
                        material=name,
                        quotation=quote,
                        product_name=cat,
                        product_description=sub,
                        quantity=qty,
                        unit_price=ref,
                        total_price=amt,
                        taxPerPiece=taxPerProduct
                        
                    )
                    # Get or create MaterialStock instance
                    # material_stock = MaterialStock.objects.get_or_create(
                    #     type='purchase',
                    #     material=name,
                    #     quantity=Decimal(qty),
                    #     cost_of_single=Decimal(ref),
                    # )
                else:
                    try:
                        name=Service.objects.get(id=led)
                        
                    except:
                        name=None
                    
        
                
                    # Extract the index from the key (e.g., dropdown1, dropdown2, etc.)
                    PurchaseInvoiceItemRow.objects.create(
                        service=name,
                        quotation=quote,
                        product_name=cat,
                        product_description=sub,
                        quantity=qty,
                        unit_price=ref,
                        total_price=amt,
                        taxPerPiece=taxPerProduct
                        
                    )
                    
                    
                
        
        purchase_account = Ledger.objects.get(id=purchase_ledgers)  # Replace with the actual name or identifier of your purchase account
        accounts_payable_account = Ledger.objects.get(id=supplier_id)  # Replace with the actual name or identifier of your accounts payable account
        tax_paid_account = Ledger.objects.get(id=tax_ledgers)  # Replace with the actual name or identifier of your tax paid account

        # Create a ledger entry for the purchase
        purchase_entry = LedgerEntry.objects.create(
            account=purchase_account,
            narration=f'Purchase Invoice #{quote.PurchaseVoucherNumber}',
            debit_amount=quote.FinalAmount,  # Assuming FinalAmount represents the total purchase amount
            transaction_date=quote.PurchaseVoucherDate,  # Replace with the actual date of the purchase
        )
        # Create a ledger entry for tax paid
        tax_paid_entry = LedgerEntry.objects.create(
            account=tax_paid_account,
            narration=f'Tax for Purchase Invoice #{quote.PurchaseVoucherNumber}',
            debit_amount=quote.Vat,  # Assuming Vat represents the tax amount paid
            transaction_date=quote.PurchaseVoucherDate,  # Replace with the actual date of the purchase
        )
        # Create a ledger entry for accounts payable
        accounts_payable_entry = LedgerEntry.objects.create(
            account=accounts_payable_account,
            narration=f' Sundry Creditor- {accounts_payable_account.ledger_name}  PI #{quote.PurchaseVoucherNumber}',
            credit_amount=quote.FinalAmount,  # Assuming FinalAmount represents the total purchase amount
            transaction_date=quote.PurchaseVoucherDate,  # Replace with the actual date of the purchase
        )

    



        # Redirect to the detail view for the created quotation
        return redirect('purchase-invoices')
        
    
    
    
    
    latest_quotation = PurchaseInvoice.objects.order_by().last()
    next_quotation_number = latest_quotation.PurchaseVoucherNumber + 1 if latest_quotation else 10000
    company = get_object_or_404(Company, name=request.user.company)
    currency=[{'key':cur,'value':cur+'-'+currency_symbols[cur]} for cur in currency_symbols]
    terms = TermsAndCondition.objects.get(company=company,name='SHIPPING')
    return render(request, 'purchase/PurchaseInvoice_Voucher/purchaseVoucher.html', context={
        'username':request.user,'sundry_creditor_ledgers':sundry_creditor_ledgers,'purchase_ledgers':purchase_ledgers
        ,'tax_ledgers':tax_ledgers,'currency':currency,
        'products':products,'next_quotation_number':next_quotation_number,'services':services,'terms':terms,'materials':materials,
        'setting':setting
       
    })  
@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')    
def purchaseList(request):
    purchase_invoices = PurchaseInvoice.objects.prefetch_related('items').all()
    return render(request, 'purchase/PurchaseInvoice_Voucher/purchaseVouchers.html', context={
      'purchase_invoices':purchase_invoices  
    })
@login_required(login_url='login')
def purchaseDelete(request, pk):
    purchase_invoice = get_object_or_404(PurchaseInvoice, pk=pk)
    if request.method=='POST':
        # Get the PurchaseInvoice instance
        purchase_invoice = get_object_or_404(PurchaseInvoice, pk=pk)

        # Delete the instance
        purchase_invoice.delete()

        # Redirect to the purchase list page or another appropriate page
        return redirect('purchase-invoices')
    return render(request, 'purchase/PurchaseInvoice_Voucher/purchaseVoucherConfirmDelet.html', context={
      'purchase_invoices':purchase_invoice 
    })
@login_required(login_url='login')
def purchaseDetail(request, pk):
    # Get the PurchaseInvoice instance
    purchase_invoice = get_object_or_404(PurchaseInvoice, pk=pk)
    # purchase = get_object_or_404(PurchaseQuotation, quotation_number=pk)
    company = get_object_or_404(Company, name=request.user.company)
    # Render the details template
    return render(request, 'purchase/PurchaseInvoice_Voucher/purchase_invoice_detail.html', {'purchase_invoice': purchase_invoice,'company':company})





from .forms import PurchaseReturnForm, PurchaseReturnItemForm
def create_purchase_return(request):
    if request.method == 'POST':
        form = PurchaseReturnForm(request.POST)
        if form.is_valid():
            # Check if PurchaseReturn already exists for the selected purchase
            purchase = form.cleaned_data['purchase']
            existing_return = PurchaseReturn.objects.filter(purchase=purchase).first()

            if existing_return:
                # Redirect to the detail page if it already exists
                return redirect('purchase_return_detail', purchase_return_id=existing_return.id)
            else:
                # Create a new PurchaseReturn if it doesn't exist
                purchase_return = form.save()
                return redirect('purchase_return_detail', purchase_return_id=purchase_return.id)
    else:
        form = PurchaseReturnForm()

    return render(request, 'purchase/purchase_return/create_purchase_return.html', {'form': form})
def delete_purchase_return_item(request, item_id):
    item = get_object_or_404(PurchaseReturnItem, id=item_id)
    purchase_return_id = item.purchase_return.id
    item.delete()
    return redirect('purchase_return_detail', purchase_return_id=purchase_return_id)
def purchase_return_list(request):
    purchase_returns = PurchaseReturn.objects.all()
    return render(request, 'purchase/purchase_return/purchase_return_list.html', {'purchase_returns': purchase_returns})
# def purchase_return_detail(request, purchase_return_id):
#     purchase_return = get_object_or_404(PurchaseReturn, id=purchase_return_id)
#     return render(request, 'purchase/purchase_return/purchase_return_detail.html', {'purchase_return': purchase_return})
def purchase_return_detail(request, purchase_return_id):
    purchase_return = get_object_or_404(PurchaseReturn, id=purchase_return_id)
    purchaseRow=PurchaseInvoiceItemRow.objects.filter(quotation=purchase_return.purchase)
    print(purchaseRow)
    if request.method == 'POST':
        form = PurchaseReturnItemForm(request.POST)
        if form.is_valid():
            purchase_return_item = form.save(commit=False)
            purchase_return_item.purchase_return = purchase_return
            purchase_return_item.save()

            return redirect('purchase_return_detail', purchase_return_id=purchase_return_id)
    else:
        form = PurchaseReturnItemForm()

    return render(request, 'purchase/purchase_return/purchase_return_detail.html', {'purchaseRow':purchaseRow,'purchase_return': purchase_return, 'form': form})
def add_purchase_return_item(request, purchase_return_id):
    purchase_return = get_object_or_404(PurchaseReturn, id=purchase_return_id)

    if request.method == 'POST':
        form = PurchaseReturnItemForm(request.POST)
        if form.is_valid():
            purchase_return_item = form.save(commit=False)
            purchase_return_item.purchase_return = purchase_return
            purchase_return_item.save()
            # Get or create MaterialStock instance
            try:
                name=Material.objects.get(id=purchase_return_item.material.id)
                print(name)
                material_stock = MaterialStock.objects.get_or_create(
                type='return',
                material=name,
                quantity=Decimal(purchase_return_item.quantity),
                cost_of_single=Decimal(purchase_return_item.cost_of_single),
                )
            except:
                name=None
            try:
                name=Product.objects.get(id=purchase_return_item.product.id)              
                
                # Get or create MaterialStock instance
                material_stock = ProductStock.objects.get_or_create(
                    type='return',
                    product=name,
                    quantity=Decimal(purchase_return_item.quantity),
                    cost_of_single=Decimal(purchase_return_item.cost_of_single),
                )
            except Exception as e:
                name=None
                
            # amt=float(Decimal(purchase_return_item.quantity)*Decimal(purchase_return_item.cost_of_single))
       
            # purchase_account = Ledger.objects.get(ledger_name='Purchase')  # Replace with the actual name or identifier of your purchase account
            # accounts_payable_account = Ledger.objects.get(ledger_number=purchase_return_item.purchase_return.purchase.supplier.ledger.ledger_number)  # Replace with the actual name or identifier of your accounts payable account
            # tax_paid_account = Ledger.objects.get(ledger_name='Total Tax Paid')  # Replace with the actual name or identifier of your tax paid account

            # # Create a ledger entry for the purchase
            # purchase_entry = LedgerEntry.objects.create(
            #     account=purchase_account,
            #     narration=f'Purchase Invoice #{purchase_return_item.purchase_return.purchase.PurchaseVoucherNumber}',
            #     credit_amount=amt,  # Assuming FinalAmount represents the total purchase amount
            #     transaction_date=purchase_return.purchase.PurchaseVoucherDate,  # Replace with the actual date of the purchase
            # )

            # # Create a ledger entry for accounts payable
            # accounts_payable_entry = LedgerEntry.objects.create(
            #     account=accounts_payable_account,
            #     narration=f'Purchase Invoice #{purchase_return_item.purchase_return.purchase.PurchaseVoucherNumber}',
            #     debit_amount=amt,  # Assuming FinalAmount represents the total purchase amount
            #     transaction_date=purchase_return.purchase.PurchaseVoucherDate,  # Replace with the actual date of the purchase
            # )

        
            # # Create a ledger entry for tax paid
            # tax_paid_entry = LedgerEntry.objects.create(
            #     account=tax_paid_account,
            #     narration=f'Tax Paid for Purchase Invoice #{purchase_return_item.purchase_return.purchase.PurchaseVoucherNumber}',
            #     credit_amount=(0.18*amt),  # Assuming Vat represents the tax amount paid
            #     transaction_date=purchase_return.purchase.PurchaseVoucherDate,  # Replace with the actual date of the purchase
            # )

            return redirect('purchase_return_detail', purchase_return_id=purchase_return_id)
    else:
        form = PurchaseReturnItemForm()

    return render(request, 'purchase/purchase_return/add_purchase_return_item.html', {'form': form, 'purchase_return': purchase_return})



  
  
@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def submitpurchase(request):
    # Category_list=Primary_Group.objects.all()
    # Subcategory_list = Group.objects.all()
    # debit = Ledger.objects.filter(group__group_name__in=["Sales"])
    # accounts = Ledger.objects.exclude(group__group_name__in=["Sales"])
    # currency=[{'key':cur,'value':cur+'-'+currency_symbols[cur]} for cur in currency_symbols]
    
    
    # try:
    data = request.POST # Replace with your actual QueryDict data
    bankDr = data.get(f'bankDr', '')
    
    voucher_no = data.get(f'invoice_no', '')
    invoicedate = data.get(f'invoice_date', '')
    debit_led = data.get(f'debit_led', '')
    total = data.get(f'd_total', '')
    
    deb_category = Primary_Group.objects.get(primary_group_name='EXPENSES')
    deb_subcategory = Group.objects.get(group_name='Purchase')
    deb_account = Ledger.objects.get(ledger_name=debit_led.split('-')[-1])  # Replace with the appropriate field
            
    
    
    try:
    # Loop through the data to create and save JournalEntries instances
        for i in range(1, 10):  # Assuming you have four sets of data (1 to 4)
            # Replace 'voucher' with the actual key in your QueryDict
            # narration = data.get(f'nar{i}', '')  # Replace 'nar' with the actual key in your QueryDict
            category_name = data.get(f'cat{i}', '')
            subcategory_name = data.get(f'sub{i}', '')
            desc = data.get(f'ref{i}', 0)
            amt = data.get(f'amt{i}', 0)
            bill_no = data.get(f'bill{i}', 0)
            
            
            

            account_num=data.get(f'dropdown{i}', 0)  # Default to 0 if not present or invalid
            print(account_num)
            
            try:
                    # Fetch the corresponding Category, Subcategory, and IndividualAccount instances
                
                cre_account = Ledger.objects.get(ledger_number=account_num)  # Replace with the appropriate field
                cre_subcategory = cre_account.group
                cre_category = cre_account.group.primary_group
                print(voucher_no)
                
                # Create and save the JournalEntries instance
                entry = PurchaseReceipt(
                    date=invoicedate,
                    voucherNo=voucher_no.split('-')[-1],
                    voucherCode=voucher_no,
                    deb_primary_group=deb_category,
                    deb_group=deb_subcategory,
                    deb_ledger=deb_account,
                    cred_primary_group=cre_category,
                    cred_group=cre_subcategory,
                    cred_ledger=cre_account,
                    description=desc,
                    amount=float(amt),
                    total=float(total),
                    bill_no=bill_no
                    
                        # You can set comments as needed
                )
                entry.save()
            except Primary_Group.DoesNotExist:
                pass
            except Group.DoesNotExist:
                pass
            except Ledger.DoesNotExist:
                pass
        entry_response = {
                    "voucherNo": entry.voucherNo,
                    "voucherCode": entry.voucherCode,  # Assuming you have a 'voucherCode' field in your model
                    "account": entry.deb_ledger.ledger_name,  # Assuming 'account_name' is the relevant field in 'IndividualAccount'
                }

        return JsonResponse({'success': True, 'message': 'Sucess'})            
    except Exception as e:
        print(e)
        return JsonResponse({'success': False, 'message': 'Invalid request'})
        
    
    



@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def purchase_quote(request):
    setting=CompanySettings.objects.all().first()
    supplier=Supplier.objects.all()
    
    
    products=Product.objects.all()
    materials=Material.objects.all()
    services=Service.objects.all()
    if request.method=='POST':
        # Extract keys that match the pattern 'cat{number}', 'sub{number}', 'ref{number}', etc.
        rows=find_max_rows(request.POST)
        
        entry='PurchaseQuotation'
        
        # Handle POST request and process the form data
        quotation_number = request.POST.get('quotation_number')
        supplier_name = request.POST.get('supplier_name')
        
        billing_address = request.POST.get('billing_address')
        shipping_address = request.POST.get('shipping_address')
        totalTax = request.POST.get('tax2')
        
        
      
        
        
        sub_total_s = float(request.POST.get('s_total',0))
        final_amt_s = float(request.POST.get('final',0))
        terms = request.POST.get('terms')
        comment = request.POST.get('notes')
        Others=request.POST.get('other',0)
        count=int(request.POST.get('count'))
        
        
        
        quote=PurchaseQuotation(
            quotation_number = quotation_number,
            supplier=Supplier.objects.get(supplier_id=supplier_name),
            billing_address = billing_address,
            shipping_address = shipping_address,
            sub_total = sub_total_s,
            final_amt = final_amt_s,
            tax=totalTax,
            terms_and_conditions=terms,
            notes_comments=comment,
            Others=Others
        )
        quotation=quote.save()
        # Add a discount field if you intend to use it

        # quotation
        # Process Quotation Items

        for index in range(1,count+1):
                # Extract the index from the key (e.g., dropdown1, dropdown2, etc.)
            PurchaseItemRow.objects.create(
                # quotation=quotation,
                entry_type=entry,
                quotation=quote,
                product_name=request.POST.get(f'cat{index}'),
                product_description=request.POST.get(f'sub{index}'),
                quantity=request.POST.get(f'qty{index}'),
                unit_price=request.POST.get(f'ref{index}'),
                total_price=request.POST.get(f'amt{index}'),
                taxPerproduct=request.POST.get(f'tx{index}'),
                
                
                # Add other fields as needed
            )


        messages.success(request, f'''Purchase Order Successfully Submited  #{quote.quotation_number} --
                                    Total Product - {count} --
                                    Total Price - {sub_total_s} --
                                    Total Tax - {totalTax} --
                                    Total Amount - {final_amt_s} --
                                    ''')
    
        
        
        
        # Redirect to the detail view for the created quotation
        return redirect('purchase-orders')
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    latest_quotation = PurchaseQuotation.objects.order_by().last()
    next_quotation_number = latest_quotation.quotation_number + 1 if latest_quotation else 10000
    company = get_object_or_404(Company, name=request.user.company)
    terms = get_object_or_404(TermsAndCondition,company=company,name='SHIPPING')
    tax = Tax.objects.all()
    
    
    
    context = {'PurchaseQuotation': next_quotation_number,'suppliers':supplier,
               'products':products,'services':services,'terms':terms,
               'materials':materials,'terms':terms,'setting':setting}
    return render(request, 'purchase\PurchaseOrder\purchaseOrder.html',context)
@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def quotepurchaseList(request):
    success_messages = messages.get_messages(request)
    quotes=PurchaseQuotation.objects.all()
    return render(request,'purchase\PurchaseOrder\PurchaseOrders.html',{'quotes':quotes,'success_messages':success_messages})

@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def PurchaseQuotationDetailView(request,pk):
    print(request.user.company)
    purchase = get_object_or_404(PurchaseQuotation, quotation_number=pk)
    company = get_object_or_404(Company, name=request.user.company)
    quote = PurchaseItemRow.objects.filter(quotation=purchase)
    
    


    return render(request,'bills\PurchaseOrder1.html',{'purchase':purchase,'company':company,'quotes':quote})

@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def PurchaseQuotationDeleteView(request,pk):
        
    product = get_object_or_404(PurchaseQuotation, quotation_number=pk)
    if request.method == 'POST':
        product.delete()
        # Add any additional processing or redirect as needed
        return redirect('purchase-orders')  # Redirect to the product list view

    return render(request,'purchase\PurchaseOrder\purchaseOrdersConfirmDelet.html',{'object':product})

    


















@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def accountingDashboard(request):
    return render(request,'accountingDashboard.html')

















@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def Journal_entry(request):
                
    Category_list=Primary_Group.objects.all()
    Subcategory_list = Group.objects.all()
    account = VoucherLedgerVisibility.objects.get(voucher_type='JV')

    # Get all ledgers under the selected groups
    selected_group_numbers = account.selected_groups.values_list('group_number', flat=True)
    ledgers_under_selected_groups = Ledger.objects.filter(
        Q(group__group_number__in=selected_group_numbers) |
        Q(group__primary_group__primary_group_number__in=selected_group_numbers)
    )


    if request.method=='POST':
        # Extract keys that match the pattern 'cat{number}', 'sub{number}', 'ref{number}', etc.
        
        # Handle POST request and process the form data
        journal_date = request.POST.get('journal_date')
        voucher_no = request.POST.get('voucher_no')
        
        invoice_no = request.POST.get('invoice_no')
        notes = request.POST.get('notes')
        
        invoice_date = request.POST.get('invoice_date')
        
        
        d_total = float(request.POST.get('d_total'))
        c_total = float(request.POST.get('c_total'))

        count=int(request.POST.get('count'))
        quote=JournalEntry(
            date = journal_date,
            voucherNo=voucher_no,
            invoice_no=invoice_no,
            invoice_date=invoice_date,
            
            narration = notes,
            debit_total = d_total,  
            credit_total = c_total, 
        )
        quote.save()
        # Add a discount field if you intend to use it

 
        for index in range(1,count+1):
                led = request.POST.get(f'dropdown{index}')
                comment=request.POST.get(f'nar{index}')
                
                try:
                    cred=float(request.POST.get(f'deb{index}'))
                except:
                    cred=0.00
                try:
                    deb=float(request.POST.get(f'cre{index}'))
                except:
                    deb=0.00
                
                # Extract the index from the key (e.g., dropdown1, dropdown2, etc.)
                JournalEntryRow.objects.create(
                    # quotation=quotation,
                    entryFk=quote,
                    ledger=Ledger.objects.get(ledger_number=led),
                    comment=comment,
                    debit=cred,
                    credit=deb,

                    # Add other fields as needed
                )



        # Redirect to the detail view for the created quotation
        return redirect('journal-entries')
        
        
                  
    latest_quotation = JournalEntry.objects.order_by().last()
    next_quotation_number = latest_quotation.voucherNo + 1 if latest_quotation else 100
    return render(request, 'vouchers\journal\journalEntry.html',  context={
        'username':request.user,'Category_list':Category_list,'Subcategory_list':Subcategory_list,'account_list':ledgers_under_selected_groups,
    'next_quotation_number':next_quotation_number})
    
    



@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def payment(request):
                

    purchase=PurchaseInvoice.objects.all()
    pay = Ledger.objects.filter(group__group_name__in=['BANK ACCOUNTS', 'CASH-IN-HAND'])
    to_ledger_accounts = Ledger.objects.exclude(group__group_name__in=['BANK ACCOUNTS', 'CASH-IN-HAND'])

   

    if request.method=='POST':
        # Extract keys that match the pattern 'cat{number}', 'sub{number}', 'ref{number}', etc.
        
        # Handle POST request and process the form data
        journal_date = request.POST.get('journal_date')
        voucher_no = request.POST.get('voucher_no')
        
        invoice_no = request.POST.get('invoice_no')
        notes = request.POST.get('notes')
        
        invoice_date = request.POST.get('invoice_date')
        
        from_ledger = request.POST.get(f'dropdown1')
        to_ledger=request.POST.get(f'dropdown2')
  
        
        from_led=Ledger.objects.get(ledger_number=from_ledger)
        to_led=Ledger.objects.get(ledger_number=to_ledger)
        tax_led = Ledger.objects.get(ledger_name='GST Paid')  # Replace with the actual name or identifier of your purchase account
        
        amt=float(request.POST.get(f'amt'))
        tax=float(request.POST.get(f'tax'))
        comment=request.POST.get(f'comment')

        quote=PaymentEntry(
            date = journal_date,
            voucherNo=voucher_no,
            invoice_no = invoice_no,
            invoice_date = invoice_date,
            narration = notes,
            comment=comment,
            from_ledger = from_led,
            to_ledger = to_led,
            tax_ledger = tax,
            debit_total = amt,
            credit_total=amt,
        )
        quote.save()

 
       
  
       

        # Create a ledger entry for the purchase
        LedgerEntry.objects.create(
            account=from_led,
            narration=f'Purchase Invoice #{invoice_no}',
            credit_amount=amt,  # Assuming FinalAmount represents the total purchase amount
            transaction_date=invoice_date,  # Replace with the actual date of the purchase
        )

        # Create a ledger entry for accounts payable
        LedgerEntry.objects.create(
            account=to_led,
            narration=f'Purchase Invoice #{invoice_no}',
            debit_amount=amt,  # Assuming FinalAmount represents the total purchase amount
            transaction_date=invoice_date,  # Replace with the actual date of the purchase
        )

    
        # # Create a ledger entry for tax paid
        # LedgerEntry.objects.create(
        #     account=tax_led,
        #     narration=f'Tax Paid for Purchase Invoice #{invoice_no}',
        #     credit_amount=(0.18*amt),  # Assuming Vat represents the tax amount paid
        #     transaction_date=invoice_date,  # Replace with the actual date of the purchase
        # )


        # Get the PurchaseInvoice instance
        purchase_invoice = PurchaseInvoice.objects.get(PurchaseVoucherNumber=invoice_no.split('-')[-1])
        # Update the balance attribute
        tr = purchase_invoice.balance- amt
        purchase_invoice.balance=tr
        # Save the changes
        purchase_invoice.save()
        

        # Redirect to the detail view for the created quotation
        return redirect('payment-entries')
        
        
                  
    latest_quotation = PaymentEntry.objects.order_by().last()
    next_quotation_number = latest_quotation.voucherNo + 1 if latest_quotation else 100
    return render(request, 'vouchers\Payment\payment.html',  context={
        'username':request.user,'account_list':to_ledger_accounts,
    'next_quotation_number':next_quotation_number,'purchases':purchase,'pay':pay})
def payment_list(request):
    payments = PaymentEntry.objects.all()
    return render(request, 'vouchers\Payment\paymentList.html', {'payments': payments})
from sales.models import *
@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def reciept(request):
    purchase=Sales.objects.all()
    pay = Ledger.objects.filter(group__group_name__in=['BANK ACCOUNTS', 'CASH-IN-HAND'])
    to_ledger_accounts = Ledger.objects.exclude(group__group_name__in=['BANK ACCOUNTS', 'CASH-IN-HAND'])
    if request.method=='POST':
        # Extract keys that match the pattern 'cat{number}', 'sub{number}', 'ref{number}', etc.
        
        # Handle POST request and process the form data
        journal_date = request.POST.get('journal_date')
        voucher_no = request.POST.get('voucher_no')
        
        invoice_no = request.POST.get('invoice_no')
        notes = request.POST.get('notes')
        
        invoice_date = request.POST.get('invoice_date')
        
        from_ledger = request.POST.get(f'dropdown1')
        to_ledger=request.POST.get(f'dropdown2')
  
        
        from_led=Ledger.objects.get(ledger_number=from_ledger)
        to_led=Ledger.objects.get(ledger_number=to_ledger)
        tax_led = Ledger.objects.get(ledger_name='GST Paid')  # Replace with the actual name or identifier of your purchase account
        
        amt=float(request.POST.get(f'amt'))
        tax=float(request.POST.get(f'tax'))
        comment=request.POST.get(f'comment')

        quote=PaymentEntry(
            date = journal_date,
            voucherNo=voucher_no,
            invoice_no = invoice_no,
            invoice_date = invoice_date,
            narration = notes,
            comment=comment,
            from_ledger = from_led,
            to_ledger = to_led,
            tax_ledger = tax,
            debit_total = amt,
            credit_total=amt,
        )
        quote.save()

 
       
  
       

        # Create a ledger entry for the purchase
        LedgerEntry.objects.create(
            account=from_led,
            narration=f'Purchase Invoice #{invoice_no}',
            credit_amount=amt,  # Assuming FinalAmount represents the total purchase amount
            transaction_date=invoice_date,  # Replace with the actual date of the purchase
        )

        # Create a ledger entry for accounts payable
        LedgerEntry.objects.create(
            account=to_led,
            narration=f'Purchase Invoice #{invoice_no}',
            debit_amount=amt,  # Assuming FinalAmount represents the total purchase amount
            transaction_date=invoice_date,  # Replace with the actual date of the purchase
        )

    
        # # Create a ledger entry for tax paid
        # LedgerEntry.objects.create(
        #     account=tax_led,
        #     narration=f'Tax Paid for Purchase Invoice #{invoice_no}',
        #     credit_amount=(0.18*amt),  # Assuming Vat represents the tax amount paid
        #     transaction_date=invoice_date,  # Replace with the actual date of the purchase
        # )


        # Get the PurchaseInvoice instance
        purchase_invoice = PurchaseInvoice.objects.get(PurchaseVoucherNumber=invoice_no.split('-')[-1])
        # Update the balance attribute
        tr = purchase_invoice.balance- amt
        purchase_invoice.balance=tr
        # Save the changes
        purchase_invoice.save()
        

        # Redirect to the detail view for the created quotation
        return redirect('reciept-entries')
        
        
                  
    latest_quotation = PaymentEntry.objects.order_by().last()
    next_quotation_number = latest_quotation.voucherNo + 1 if latest_quotation else 100
    return render(request, 'vouchers/Reciept/reciept.html',  context={
        'username':request.user,'account_list':to_ledger_accounts,
    'next_quotation_number':next_quotation_number,'purchases':purchase,'pay':pay})
def reciept_list(request):
    payments = PaymentEntry.objects.all()
    return render(request, 'vouchers/Reciept/recieptList.html', {'payments': payments})


@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def contra(request):
                
    Category_list=Primary_Group.objects.all()
    Subcategory_list = Group.objects.all()
    account = VoucherLedgerVisibility.objects.get(voucher_type='CV')

    # Get all ledgers under the selected groups
    selected_group_numbers = account.selected_groups.values_list('group_number', flat=True)
    ledgers_under_selected_groups = Ledger.objects.filter(
        Q(group__group_number__in=selected_group_numbers) |
        Q(group__primary_group__primary_group_number__in=selected_group_numbers)
    )

    # Now `ledgers_under_selected_groups` contains all ledgers under the selected groups
    for ledger in ledgers_under_selected_groups:
        print(ledger.ledger_name)
    if request.method=='POST':
        # Extract keys that match the pattern 'cat{number}', 'sub{number}', 'ref{number}', etc.
        
        # Handle POST request and process the form data
        journal_date = request.POST.get('journal_date')
        voucher_no = request.POST.get('voucher_no')
        
        invoice_no = request.POST.get('invoice_no')
        notes = request.POST.get('notes')
        
        invoice_date = request.POST.get('invoice_date')
        
        
        d_total = float(request.POST.get('d_total'))
        c_total = float(request.POST.get('c_total'))

        count=int(request.POST.get('count'))
        quote=ContraEntry(
            date = journal_date,
            voucherNo=voucher_no,
            invoice_no=invoice_no,
            invoice_date=invoice_date,
            narration = notes,
            debit_total = d_total,  
            credit_total = c_total, 
        )
        quote.save()
        # Add a discount field if you intend to use it

 
        for index in range(1,count+1):
                print(index)
                led = request.POST.get(f'dropdown{index}')
                try:
                    cred=float(request.POST.get(f'deb{index}'))
                except:
                    cred=0.00
                try:
                    deb=float(request.POST.get(f'cre{index}'))
                except:
                    deb=0.00
                comment=request.POST.get(f'nar{index}')
                
                # Extract the index from the key (e.g., dropdown1, dropdown2, etc.)
                ContraEntryRow.objects.create(
                    # quotation=quotation,
                    entryFk=quote,
                    ledger=Ledger.objects.get(ledger_number=led),
                    comment=comment,
                    
                    debit=cred,
                    credit=deb,

                    # Add other fields as needed
                )



        # Redirect to the detail view for the created quotation
        return redirect('contra')
        
        
                  
    latest_quotation = ContraEntry.objects.order_by().last()
    next_quotation_number = latest_quotation.voucherNo + 1 if latest_quotation else 100
    return render(request, 'vouchers\Contra\contra.html',  context={
        'username':request.user,'Category_list':Category_list,'Subcategory_list':Subcategory_list,'account_list':ledgers_under_selected_groups,
    'next_quotation_number':next_quotation_number})




@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def credit_note(request):
                
    Category_list=Primary_Group.objects.all()
    Subcategory_list = Group.objects.all()
    account = VoucherLedgerVisibility.objects.get(voucher_type='CNV')

    # Get all ledgers under the selected groups
    selected_group_numbers = account.selected_groups.values_list('group_number', flat=True)
    ledgers_under_selected_groups = Ledger.objects.filter(
        Q(group__group_number__in=selected_group_numbers) |
        Q(group__primary_group__primary_group_number__in=selected_group_numbers)
    )

    if request.method=='POST':
        # Extract keys that match the pattern 'cat{number}', 'sub{number}', 'ref{number}', etc.
        
        # Handle POST request and process the form data
        journal_date = request.POST.get('journal_date')
        voucher_no = request.POST.get('voucher_no')
        
        invoice_no = request.POST.get('invoice_no')
        notes = request.POST.get('notes')
        
        invoice_date = request.POST.get('invoice_date')
        
        
        d_total = float(request.POST.get('d_total'))
        c_total = float(request.POST.get('c_total'))

        count=int(request.POST.get('count'))
        quote=CreditNoteEntry(
            date = journal_date,
            voucherNo=voucher_no,
            invoice_no=invoice_no,
            invoice_date=invoice_date,
            
            narration = notes,
            debit_total = d_total,  
            credit_total = c_total, 
        )
        quote.save()
        # Add a discount field if you intend to use it

 
        for index in range(1,count+1):
                led = request.POST.get(f'dropdown{index}')
                try:
                    cred=float(request.POST.get(f'deb{index}'))
                except:
                    cred=0.00
                try:
                    deb=float(request.POST.get(f'cre{index}'))
                except:
                    deb=0.00
                comment=request.POST.get(f'nar{index}')
                
                # Extract the index from the key (e.g., dropdown1, dropdown2, etc.)
                creditNoteEntryRow.objects.create(
                    # quotation=quotation,
                    entryFk=quote,
                    ledger=Ledger.objects.get(ledger_number=led),
                    comment=comment,
                    
                    debit=cred,
                    credit=deb,

                    # Add other fields as needed
                )



        # Redirect to the detail view for the created quotation
        return redirect('credit-note-entries')
        
        
                  
    latest_quotation = CreditNoteEntry.objects.order_by().last()
    next_quotation_number = latest_quotation.voucherNo + 1 if latest_quotation else 100
    return render(request, 'vouchers\Credit\credit_note.html',  context={
        'username':request.user,'Category_list':Category_list,'Subcategory_list':Subcategory_list,'account_list':ledgers_under_selected_groups,
    'next_quotation_number':next_quotation_number})

@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def debit_note(request):
                
    Category_list=Primary_Group.objects.all()
    Subcategory_list = Group.objects.all()
    account = VoucherLedgerVisibility.objects.get(voucher_type='DNV')

    # Get all ledgers under the selected groups
    selected_group_numbers = account.selected_groups.values_list('group_number', flat=True)
    ledgers_under_selected_groups = Ledger.objects.filter(
        Q(group__group_number__in=selected_group_numbers) |
        Q(group__primary_group__primary_group_number__in=selected_group_numbers)
    )

    if request.method=='POST':
        # Extract keys that match the pattern 'cat{number}', 'sub{number}', 'ref{number}', etc.
        
        # Handle POST request and process the form data
        journal_date = request.POST.get('journal_date')
        voucher_no = request.POST.get('voucher_no')
        
        invoice_no = request.POST.get('invoice_no')
        notes = request.POST.get('notes')
        
        invoice_date = request.POST.get('invoice_date')
        
        
        d_total = float(request.POST.get('d_total'))
        c_total = float(request.POST.get('c_total'))

        count=int(request.POST.get('count'))
        quote=DebitNoteEntry(
            date = journal_date,
            voucherNo=voucher_no,
            invoice_no=invoice_no,
            invoice_date=invoice_date,
            
            narration = notes,
            debit_total = d_total,  
            credit_total = c_total, 
        )
        quote.save()
        # Add a discount field if you intend to use it

 
        for index in range(1,count+1):
                led = request.POST.get(f'dropdown{index}')
                try:
                    cred=float(request.POST.get(f'deb{index}'))
                except:
                    cred=0.00
                try:
                    deb=float(request.POST.get(f'cre{index}'))
                except:
                    deb=0.00
                comment=request.POST.get(f'nar{index}')
                
                # Extract the index from the key (e.g., dropdown1, dropdown2, etc.)
                DebitNoteEntryRow.objects.create(
                    # quotation=quotation,
                    entryFk=quote,
                    ledger=Ledger.objects.get(ledger_number=led),
                    comment=comment,
                    
                    debit=cred,
                    credit=deb,

                    # Add other fields as needed
                )



        # Redirect to the detail view for the created quotation
        return redirect('debit-note-entries')
        
        
                  
    latest_quotation = DebitNoteEntry.objects.order_by().last()
    next_quotation_number = latest_quotation.voucherNo + 1 if latest_quotation else 100
    return render(request, 'vouchers\Debit\debit_note.html',  context={
        'username':request.user,'Category_list':Category_list,'Subcategory_list':Subcategory_list,'account_list':ledgers_under_selected_groups,
    'next_quotation_number':next_quotation_number})























    












































def autocomplete(request):
    term = request.GET.get('term', '')
    # Implement your logic to fetch suggestions based on the input term
    suggestions = Ledger.objects.filter(ledger_name__icontains=term).values_list('ledger_name', flat=True)
    return JsonResponse(list(suggestions), safe=False)



@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def journalEntries(request):
    # context = {}
    # q = request.GET.get('q')
    # from_date = request.GET.get('from')
    # to_date = request.GET.get('to')

    # context['username'] = request.user

    # # Parse date inputs (assuming they are in a specific format)
    # try:
    #     from_date = datetime.strptime(from_date, '%Y-%m-%d').date() if from_date else None
    #     to_date = datetime.strptime(to_date, '%Y-%m-%d').date() if to_date else None
    # except ValueError:
    #     from_date = None
    #     to_date = None

    # if q:
    #     multiple_q = (
    #         Q(voucherNo__icontains=q) |
    #         Q(voucherCode__icontains=q) |
    #         Q(rows__ledger__group__primary_group__primary_group_name__icontains=q) |
    #         Q(rows__ledger__group__group_name__icontains=q) |
    #         Q(rows__ledger__ledger_name__icontains=q)
    #     )

    #     # Apply date range filtering if both 'from_date' and 'to_date' are provided
    #     if from_date and to_date:
    #         filtered_entry = JournalEntryFilter(
    #             request.GET,
    #             queryset=JournalEntry.objects.filter(multiple_q, date__range=[from_date, to_date]).distinct()
    #         )
    #     else:
    #         filtered_entry = JournalEntryFilter(request.GET, queryset=JournalEntry.objects.filter(multiple_q).distinct())
    # else:
    #     # Apply date range filtering if both 'from_date' and 'to_date' are provided
    #     if from_date and to_date:
    #         filtered_entry = JournalEntryFilter(
    #             request.GET,
    #             queryset=JournalEntry.objects.filter(date__range=[from_date, to_date]).distinct()
    #         )
    #     else:
    #         filtered_entry = JournalEntryFilter(request.GET, queryset=JournalEntry.objects.all().distinct())

    # context['filtered_journal'] = filtered_entry
    # paginated_filtered_journal = Paginator(filtered_entry.qs, 50)
    # page_number = request.GET.get('page')
    
    # journal_page_obj = paginated_filtered_journal.get_page(page_number)
    # context['journal_page_obj'] = journal_page_obj
    journal_page_obj=JournalEntry.objects.all()
    return render(request, 'vouchers/Journal/journalEntries.html', context={'journal_page_obj':journal_page_obj})

# @department_required(allowed_departments=['ACCOUNT'])
# @login_required(login_url='login')
# def Gernal_Ledger(request):
                
#     accounts = Ledger.objects.all()           
#     q=request.GET.get('q')
#     lis=[]
#     result={}
#     cat=''
#     subcat=''
#     if 'q' in request.GET:
#         ledgers=JournalEntryRow.objects.filter(ledger__ledger_number=q)
#         cred=0
       
#         deb=0
#         bal=0
#         for row in ledgers:
            
#             led={}
#             led['idx']=row.entryFk
#             led['date']=row.entryFk.date
#             led['ledger']=row.ledger
#             led['narration']=row.entryFk.narration
#             led['debit']=row.debit
#             led['credit']=row.credit
#             if row.debit==0.00:
#                 led['Balance']=-1*(row.credit)
#             else:
#                 led['Balance']=row.debit
#             cred=cred+row.credit
#             deb=deb+row.debit
#             bal=bal+led['Balance']
#             lis.append(led)
            
#         result={
#           'deb_result':deb,
#           'cred_result':cred,
#           'bal_result':bal,
        
#         }
#         cat=row.ledger.group.primary_group.primary_group_name
#         subcat=row.ledger.group.group_name
            

         
#     return render(request, 'ledgers\ledger.html', context={'heading':q,'cat':cat,'subcat':subcat,
#         'username':request.user,'account_list':accounts,
#         'led':lis,'result':result
#     }) 

  














@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def action_ledger(request):
    if request.method == "POST":
        data = request.POST  # Get the POST data
        action = data.get("action")
    

        if action == "delete":
            # Handle delete action
            account_number = data.get("ledger_number")

            # Delete the account using the account number
            try:
                account_to_delete = Ledger.objects.get(ledger_number=account_number)
                account_to_delete.delete()
                return JsonResponse({'success': True, 'message': 'Account deleted successfully'})
            except Ledger.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Account not found'})
        elif action == "save":
            # Handle edit action
            account_num = data.get("account_number")
            new_account_name = data.get("accountname").replace(' ','_')
            category = Group.objects.get(group_number=account_num)
            new_account = Ledger(group=category, ledger_name=new_account_name)

        # Save the new Account object to the database
            new_account.save()
            
            return JsonResponse({'success': True, 'message': 'Account Added successfully'})

    return JsonResponse({'success': False, 'message': 'Invalid request'})

@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def action(request):
    if request.method == "POST":
        data = request.POST  # Get the POST data
        action = data.get("action")
    

        if action == "delete":
            # Handle delete action
            account_number = data.get("account_number")

            # Delete the account using the account number
            try:
                account_to_delete = Ledger.objects.get(ledger_number=account_number)
                account_to_delete.delete()
                return JsonResponse({'success': True, 'message': 'Account deleted successfully'})
            except Ledger.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Account not found'})
        elif action == "save":
            # Handle edit action
            account_num = data.get("account_number")
            new_account_name = data.get("accountname").replace(' ','_')
            category = Group.objects.get(group_number=account_num)
            new_account = Ledger(group=category, ledger_name=new_account_name)

        # Save the new Account object to the database
            new_account.save()
            
            return JsonResponse({'success': True, 'message': 'Account Added successfully'})

    return JsonResponse({'success': False, 'message': 'Invalid request'})








@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def paymentEntry(request):
    Category_list=Primary_Group.objects.all()
    Subcategory_list = Group.objects.all()
    banks = Ledger.objects.filter(group__group_name__in=["BANK ACCOUNTS"])
    cash= Ledger.objects.filter(group__group_name__in=["Cash"])
    accounts = Ledger.objects.exclude(group__group_name__in=["Cash", "BANK ACCOUNTS"])
    currency=[{'key':cur,'value':cur+'-'+currency_symbols[cur]} for cur in currency_symbols]
    return render(request, 'paymentVoucher.html', context={
        'username':request.user,'Category_list':Category_list,'Subcategory_list':Subcategory_list,'account_list':accounts,'currency':currency,'banks':banks,
        'cashs':cash
    })
    
@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def paymentList(request):
    print(request.user.username)    
               

    return render(request, 'paymentList.html', context={
        'username':request.user
    })

@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def submit_payment(request):
    invoicedate=voucher_no=invoicedate=transactionType=bankAmt_inWords=Banknotes=total=None
    cashtransactionType=transactionType=bank_currency=chequeNumber=chequeDate=clearanceDate=None
    bankDr=bank_currency=transaction_type=cheque_no=chequeDate=clearanceDate=None
    
    try:
        data = request.POST # Replace with your actual QueryDict data
        voucher_no = data.get(f'bankvoucher_no', '')
        invoicedate = data.get(f'bankjournal_date', '')
        ttype = data.get(f'ttype', '')
        bankAmt_inWords = data.get(f'bankAmt_inWords', '')
        bankAmt_in_No =data.get(f'bankAmt_in_No', '')
        Banknotes = data.get(f'Banknotes', '')
        RecievedFrom = data.get(f'RecievedFrom', '')
        total = data.get(f'total', '')
        remark = data.get(f'cashTransaction_Id', '')
        
        if ttype=='cash':
            cashtransactionType = data.get(f'cashtransactionType', '')
            
            deb_account = Ledger.objects.get(ledger_name=cashtransactionType.split('-')[-1])  # Replace with the appropriate field
            deb_subcategory = deb_account.group
            deb_category = deb_account.group.primary_group
            method='cash'  
        
        else:
            transactionType =data.get(f'transactionType', '')
            if transactionType=='Cheque':
                chequeNumber =data.get(f'chequeNumber', '')
                chequeDate = data.get(f'chequeDate', '')
                clearanceDate = data.get(f'clearanceDate', 'YYYY-MM-DD')
            bank_currency = data.get(f'bank_currency', '')
            
            bankDr = data.get(f'bankDr', '')
            deb_account = Ledger.objects.get(ledger_name=bankDr)  # Replace with the appropriate field
            deb_subcategory = deb_account.group
            deb_category = deb_account.group.primary_group  
            method='bank'  
            
        try:
            # Loop through the data to create and save JournalEntries instances
            for i in range(1, 10):  # Assuming you have four sets of data (1 to 4)
                # Replace 'voucher' with the actual key in your QueryDict
                # narration = data.get(f'nar{i}', '')  # Replace 'nar' with the actual key in your QueryDict
                category_name = data.get(f'cat{i}', '')
                subcategory_name = data.get(f'sub{i}', '')
                ref = data.get(f'ref{i}', 0)
                bill = data.get(f'bill{i}', 0)
                amt = data.get(f'amt{i}', 0)
                cred = data.get(f'cred{i}', 0)
                account_num=data.get(f'dropdown{i}', 0)  # Default to 0 if not present or invalid
                print(account_num)
                # try:
                        # Fetch the corresponding Category, Subcategory, and IndividualAccount instances
                cre_account = Ledger.objects.get(ledger_number=int(account_num))  # Replace with the appropriate field
                cre_subcategory = cre_account.group
                cre_category = cre_account.group.primary_group
                # Create and save the JournalEntries instance
                entry = Payment(
                    date=invoicedate,
                    voucherNo=voucher_no.split('-')[-1],
                    voucherCode=voucher_no,
                    receipt_method=method,
                    amount_in_words=bankAmt_inWords,
                    amount_in_numbers=bankAmt_in_No,
                    received_from=RecievedFrom,
                    remarks=remark,
                    narration=Banknotes,
                    d_ledger=deb_account,
                    d_primary_group=deb_category,
                    d_group=deb_subcategory,
                    c_ledger=cre_account,
                    c_primary_group=cre_subcategory,
                    c_group=cre_category,
                    reference=ref,
                    reference_bill_number=bill,
                    reference_bill_amount = amt,
                    debit = cred,
                    transaction_currency = bank_currency,
                    clearance_date =clearanceDate,
                    transaction_type = transactionType,
                    cheque_no = chequeNumber,
                    bank_date = chequeDate,

                )
                entry.save()
        except Primary_Group.DoesNotExist:
            pass
        except Group.DoesNotExist:
            pass
        except Ledger.DoesNotExist:
            pass
        entry_response = {
                "voucherNo": entry.voucherNo,
                "voucherCode": entry.voucherCode,  # Assuming you have a 'voucherCode' field in your model
                "account": entry.d_ledger.ledger_name,  # Assuming 'account_name' is the relevant field in 'IndividualAccount'
            }
        print(entry_response)
        return JsonResponse({'success': True, 'message': 'Sucess'})            
    except Exception as e:
        print(e)
        return JsonResponse({'success': False, 'message': 'Invalid request'})
    




@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def recieptEntry(request):
    Category_list=Primary_Group.objects.all()
    Subcategory_list = Group.objects.all()
    banks = Ledger.objects.filter(group__group_name__in=["BANK ACCOUNTS"])
    cash= Ledger.objects.filter(group__group_name__in=["Cash"])
    accounts = Ledger.objects.exclude(group__group_name__in=["Cash", "BANK ACCOUNTS"])
    currency=[{'key':cur,'value':cur+'-'+currency_symbols[cur]} for cur in currency_symbols]
    return render(request, 'recieptVoucher.html', context={
        'username':request.user,'Category_list':Category_list,'Subcategory_list':Subcategory_list,'account_list':accounts,'currency':currency,'banks':banks,
        'cashs':cash
    })
  
@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def submit_reciept(request):
    invoicedate=voucher_no=invoicedate=transactionType=bankAmt_inWords=Banknotes=total=None
    cashtransactionType=transactionType=bank_currency=chequeNumber=chequeDate=clearanceDate=None
    bankDr=bank_currency=transaction_type=cheque_no=chequeDate=clearanceDate=None
    
    try:
        data = request.POST # Replace with your actual QueryDict data
        voucher_no = data.get(f'bankvoucher_no', '')
        invoicedate = data.get(f'bankjournal_date', '')
        ttype = data.get(f'ttype', '')
        bankAmt_inWords = data.get(f'bankAmt_inWords', '')
        bankAmt_in_No =data.get(f'bankAmt_in_No', '')
        Banknotes = data.get(f'Banknotes', '')
        RecievedFrom = data.get(f'RecievedFrom', '')
        total = data.get(f'total', '')
        remark = data.get(f'cashTransaction_Id', '')
        
        if ttype=='cash':
            cashtransactionType = data.get(f'cashtransactionType', '')
            
            deb_account = Ledger.objects.get(ledger_name=cashtransactionType.split('-')[-1])  # Replace with the appropriate field
            deb_subcategory = deb_account.group
            deb_category = deb_account.group.primary_group
            method='cash'  
        
        else:
            transactionType =data.get(f'transactionType', '')
            if transactionType=='Cheque':
                chequeNumber =data.get(f'chequeNumber', '')
                chequeDate = data.get(f'chequeDate', '')
                clearanceDate = data.get(f'clearanceDate', 'YYYY-MM-DD')
            bank_currency = data.get(f'bank_currency', '')
            
            bankDr = data.get(f'bankDr', '')
            deb_account = Ledger.objects.get(ledger_name=bankDr)  # Replace with the appropriate field
            deb_subcategory = deb_account.group
            deb_category = deb_account.group.primary_group  
            method='bank'  
            
        try:
            # Loop through the data to create and save JournalEntries instances
            for i in range(1, 10):  # Assuming you have four sets of data (1 to 4)
                # Replace 'voucher' with the actual key in your QueryDict
                # narration = data.get(f'nar{i}', '')  # Replace 'nar' with the actual key in your QueryDict
                category_name = data.get(f'cat{i}', '')
                subcategory_name = data.get(f'sub{i}', '')
                ref = data.get(f'ref{i}', 0)
                bill = data.get(f'bill{i}', 0)
                amt = data.get(f'amt{i}', 0)
                cred = data.get(f'cred{i}', 0)
                account_num=data.get(f'dropdown{i}', 0)  # Default to 0 if not present or invalid
                print(account_num)
                # try:
                        # Fetch the corresponding Category, Subcategory, and IndividualAccount instances
                cre_account = Ledger.objects.get(ledger_number=int(account_num))  # Replace with the appropriate field
                cre_subcategory = cre_account.group
                cre_category = cre_account.group.primary_group
                # Create and save the JournalEntries instance
                entry = Receipt(
                    date=invoicedate,
                    voucherNo=voucher_no.split('-')[-1],
                    voucherCode=voucher_no,
                    receipt_method=method,
                    amount_in_words=bankAmt_inWords,
                    amount_in_numbers=bankAmt_in_No,
                    received_from=RecievedFrom,
                    remarks=remark,
                    narration=Banknotes,
                    d_ledger=deb_account,
                    d_primary_group=deb_category,
                    d_group=deb_subcategory,
                    c_ledger=cre_account,
                    c_primary_group=cre_subcategory,
                    c_group=cre_category,
                    reference=ref,
                    reference_bill_number=bill,
                    reference_bill_amount = amt,
                    debit = cred,
                    transaction_currency = bank_currency,
                    clearance_date =clearanceDate,
                    transaction_type = transactionType,
                    cheque_no = chequeNumber,
                    bank_date = chequeDate,

                )
                entry.save()
        except Primary_Group.DoesNotExist:
            pass
        except Group.DoesNotExist:
            pass
        except Ledger.DoesNotExist:
            pass
        entry_response = {
                "voucherNo": entry.voucherNo,
                "voucherCode": entry.voucherCode,  # Assuming you have a 'voucherCode' field in your model
                "account": entry.d_ledger.ledger_name,  # Assuming 'account_name' is the relevant field in 'IndividualAccount'
            }
        print(entry_response)
        return JsonResponse({'success': True, 'message': 'Sucess'})            
    except Exception as e:
        print(e)
        return JsonResponse({'success': False, 'message': 'Invalid request'})

@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')    
def recieptList(request):
    print(request.user.username)    
               

    return render(request, 'recieptList.html', context={
        'username':request.user
    })
    
    
    
  
@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')  
def salesEntry(request):
    Category_list=Primary_Group.objects.all()
    Subcategory_list = Group.objects.all()
    debit = Ledger.objects.filter(group__group_name__in=["Sales"])
    accounts = Ledger.objects.exclude(group__group_name__in=["Sales"])
    currency=[{'key':cur,'value':cur+'-'+currency_symbols[cur]} for cur in currency_symbols]
    return render(request, 'sales_voucher.html', context={
        'username':request.user,'Category_list':Category_list,'Subcategory_list':Subcategory_list,'account_list':accounts,'currency':currency,'debit':debit,
    })  

@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def submitSales(request):
    tax_per=10
    Category_list=Primary_Group.objects.all()
    Subcategory_list = Group.objects.all()
    debit = Ledger.objects.filter(group__group_name__in=["Sales"])
    accounts = Ledger.objects.exclude(group__group_name__in=["Sales"])
    currency=[{'key':cur,'value':cur+'-'+currency_symbols[cur]} for cur in currency_symbols]
    
    
    # try:
    data = request.POST # Replace with your actual QueryDict data
    voucher_no = data.get(f'voucher', '')
    invoicedate = data.get(f'invoice_date', '')
    debit_led = data.get(f'debit_led', '')
    total = data.get(f'd_total', '')
    taxed=(10/100)*float(total)
    final=float(total)+taxed
    deb_category = Primary_Group.objects.get(primary_group_name='INCOME')
    deb_subcategory = Group.objects.get(group_name='Sales')
    deb_account = Ledger.objects.get(ledger_name=debit_led.split('-')[-1])  # Replace with the appropriate field
            
    
    
    try:
    # Loop through the data to create and save JournalEntries instances
        for i in range(1, 10):  # Assuming you have four sets of data (1 to 4)
            # Replace 'voucher' with the actual key in your QueryDict
            # narration = data.get(f'nar{i}', '')  # Replace 'nar' with the actual key in your QueryDict
            category_name = data.get(f'cat{i}', '')
            subcategory_name = data.get(f'sub{i}', '')
            desc = data.get(f'ref{i}', 0)
            qty = data.get(f'qty{i}', 0)
            
            unt = data.get(f'unt{i}', 0)
            
            amt = data.get(f'amt{i}', 0)
            
            

            account_num=data.get(f'dropdown{i}', 0)  # Default to 0 if not present or invalid
            
            try:
                    # Fetch the corresponding Category, Subcategory, and IndividualAccount instances
                
                cre_account = Ledger.objects.get(ledger_number=account_num)  # Replace with the appropriate field
                cre_subcategory = cre_account.group
                cre_category = cre_account.group.primary_group
                
                # Create and save the JournalEntries instance
                entry = SalesReceipt(
                    date=invoicedate,
                    voucherNo=voucher_no.split('-')[-1],
                    voucherCode=voucher_no,
                    deb_primary_group=deb_category,
                    deb_group=deb_subcategory,
                    deb_ledger=deb_account,
                    cred_primary_group=cre_category,
                    cred_group=cre_subcategory,
                    cred_ledger=cre_account,
                    decsription=desc,
                    qty=int(qty),
                    untPrice=int(unt),
                    amount=float(amt),
                    total=float(total),
                    taxed=float(taxed),
                    final=float(final),
                    
                    
                        # You can set comments as needed
                )
                entry.save()
            except Primary_Group.DoesNotExist:
                pass
            except Group.DoesNotExist:
                pass
            except Ledger.DoesNotExist:
                pass
        entry_response = {
                    "voucherNo": entry.voucherNo,
                    "voucherCode": entry.voucherCode,  # Assuming you have a 'voucherCode' field in your model
                    "account": entry.deb_ledger.ledger_name,  # Assuming 'account_name' is the relevant field in 'IndividualAccount'
                }

        return JsonResponse({'success': True, 'message': 'Sucess'})            
    except Exception as e:
        print(e)
        return JsonResponse({'success': False, 'message': 'Invalid request'}) 
from django.db.models import F

from django.db.models import Subquery, OuterRef

@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def salesList(request):
    unique_receipts = SalesReceipt.objects.filter(
    s_no=Subquery(
        SalesReceipt.objects.filter(voucherCode=OuterRef('voucherCode')).order_by('s_no').values('s_no')[:1]
    )
)
    # Sale_Receipt=SalesReceipt.objects.all()
    Category_list=Primary_Group.objects.all()
    Subcategory_list = Group.objects.all()
    banks = Ledger.objects.filter(group__group_name__in=["Bank Account"])
    cash= Ledger.objects.filter(group__group_name__in=["Cash"])
    accounts = Ledger.objects.exclude(group__group_name__in=["Cash", "Bank Account"])
    currency=[{'key':cur,'value':cur+'-'+currency_symbols[cur]} for cur in currency_symbols]
    print(unique_receipts)
    return render(request, 'sales_list.html', context={
        'username':request.user,'Category_list':Category_list,'Subcategory_list':Subcategory_list,'account_list':accounts,'currency':currency,'banks':banks,
        'cashs':cash,'SalesReceipt':unique_receipts
    })  
  
  
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import FileResponse
  
  
def generate_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = "inline; filename=your_file.pdf"

    p = canvas.Canvas(response, pagesize=letter)
    p.drawString(100, 750, "Hello, world.")
    # Add more content here using the ReportLab API.

    p.showPage()
    p.save()

    return response
  


@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def item_detail(request, voucher_id):
    print(voucher_id)
    Sale_Receipt=SalesReceipt.objects.filter(voucherCode=voucher_id)
    print(Sale_Receipt)
    # item = get_object_or_404(Item, id=item_id)  # Retrieve the item based on its ID
    return render(request, 'salesvoucher_pdf.html', {'item': Sale_Receipt[0],'items': Sale_Receipt,})
  
  
  
  
  
  
  
  
  
  
  
  
  
  
    
        
        
        
        
        
        

  
  
@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
    
def Trial_Balance(request):
                
    accounts = Ledger.objects.values('ledger_name',)  
    led=[]
    res={}
    resdeb=0
    rescred=0
    resbal=0
    
    for account in accounts:        
        ledgers=JournalEntries.objects.filter(ledger__ledger_name=account['ledger_name'])
        print()
        cred=0
        deb=0
        bal=0
        for row in ledgers:
            
      
 
    
            cred=cred+row.credit
            deb=deb+row.debit
            bal=deb-cred
            
        le={'type':account['ledger_name'],
            'deb':deb,'cred':cred,'bal':bal
        }
        led.append(le)
        resdeb=resdeb+deb
        rescred=rescred+cred
        resbal=resbal+bal
    result={
        'deb_result':resdeb,
        'cred_result':rescred,
        'bal_result':resbal
    }        
    return render(request, 'trial_balance.html', context={
        'username':request.user,'account_list':accounts,
        'data':led,'result':result
    }) 
    
def Profit_Loss(request):
    print(request.user.username)    
               

    return render(request, 'home.html', context={
        'username':request.user
    })
def Balance_sheet(request):
                
    print(request.user.username)    
               

    return render(request, 'home.html', context={
        'username':request.user
    })
    
    
    
def maintain(request):
                
    print(request.user.username)    
               

    return render(request, 'maintain.html', context={
        'username':request.user
    })



@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def accountingroup(request):
    return render(request,'accountingroup.html')

@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def accountingvoucher(request):
    return render(request,'accountingvoucher.html')

@department_required(allowed_departments=['ACCOUNT'])
@login_required(login_url='login')
def accountingcurrency(request):
    return render(request,'accountingcurrency.html')







