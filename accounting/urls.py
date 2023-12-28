"""
URL configuration for erp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views
from .views import GeneratePDF
urlpatterns = [

    
    
    
    
    
    
    
    
    
    
    path('accountsChart/', views.Account_chart, name="accountsChart"),



    path('primaryGroup/', views.primaryGroup, name="primaryGroup"),
    path('groupage/', views.groupPage, name="groupage"),


    
    
    
    ##############Journal Ledgers###########
    path('generalLedger/', views.Gernal_Ledger, name="generalLedger"),

    
    ###########################################################################################################################
    
    
    
    
    
    
    #################################################Purchase Return ##########################

    

    # path('purchaseReturn/add/', views.add_service, name='add_service'),
    # path('purchaseReturn/', views.list_services, name='list_services'),
    # path('purchaseReturn/add/', views.add_service, name='add_service'),
    
    
    #################################################Journal Entry ##########################

          
    path('journal/', views.Journal_entry, name="journal"),
    path('edit-journal/', views.journalEntries, name="edit-journal"),
    path('journal-entries/', views.journalEntries, name="journal-entries"),
    
    
    ###############Payment Entries#############
             
    path('payment/', views.payment, name="payment"),
    path('payment-entries/', views.payment_list, name="payment-entries"),
    
    ############Reciept Entry#############
             
    path('reciept/', views.reciept, name="reciept"),
    path('reciept-entries/', views.reciept_list, name="reciept-entries"),
    
    #############contra Entry############
             
    path('contra/', views.contra, name="contra"),
    path('edit-contra/', views.Journal_entry, name="edit-contra"),
    path('contra-entries/', views.journalEntries, name="contra-entries"),
    
    ################################################################
    
    #############credit Entry############
    
    path('credit-note/', views.credit_note, name="credit-note"),
    path('edit-credit-note/', views.Journal_entry, name="edit-credit-note"),
    path('credit-note-entries/', views.journalEntries, name="credit-note-entries"),
    
    #############debit Entry############
    
    path('debit-note/', views.debit_note, name="debit-note"),
    path('edit-debit-note/', views.Journal_entry, name="edit-debit-note"),
    path('debit-note-entries/', views.journalEntries, name="debit-note-entries"),
    
    
    
    
    
    
    
    
    
    
    
    
    
    path('account/', views.accountingDashboard, name='account'),
    
    
    path('customer/', views.accountingcustomer, name='customer'),
    path('addcustomer/', views.addaccountingcustomer, name='addcustomer'),
    
    
    path('addsupplier/', views.addaccountingsupplier, name='addsupplier'),
    path('supplier/', views.accountingsupplier, name='supplier'),
    
    
    
    path('group/', views.accountingroup, name='group'),
    path('accountingledger/', views.accountingledger, name='accountingledger'),
    path('voucher/', views.accountingvoucher, name='voucher'),
    path('currency/', views.accountingcurrency, name='currency'),
    

    
    path('trialBalance/', views.Trial_Balance, name="trialBalance"),
    
    path('profitAndLoss/', views.Profit_Loss, name="profitAndLoss"),
    
    path('balanceSheet/', views.Balance_sheet, name="balanceSheet"),
    
  
    
    path('autocomplete/', views.autocomplete, name="autocomplete"),
    
    path('action/', views.action, name="action"),
    path('action_ledger/', views.action_ledger, name="action"),
    
    
    
    
    path('maintain/', views.maintain, name="maintain"),
    
    
    path('paymentEntry/', views.paymentEntry, name="paymentEntry"),
    path('paymentList/', views.paymentList, name="paymentList"),
    path('submit_payment/', views.submit_payment, name="submit_payment"),
    
    path('recieptList/', views.recieptList, name="recieptList"),
    path('recieptEntry/', views.recieptEntry, name="recieptEntry"),
    path('submit_reciept/', views.submit_reciept, name="submit_reciept"),
    
    
    path('salesList/', views.salesList, name="salesList"),
    path('salesEntry/', views.salesEntry, name="salesEntry"),
    path('submitSales/', views.submitSales, name="submitSales"),
    
    # path('purchaseList/', views.purchaseList, name="purchaseList"),
    # # path('purchaseEntry/', views.purchaseEntry, name="purchaseEntry"),
    # path('submitpurchase/', views.submitpurchase, name="submitpurchase"),
    
    
    
    
    
    path('view_salesvoucher/<str:voucher_id>/', views.item_detail, name='item_detail'),
    path('generate_pdf/', views.generate_pdf, name='generate_pdf'),
    
    
    
# path('product-materials-detail/<int:product_id>/', views.product_materials_detail, name='product-materials-detail'),

    
    # Add more URLs as needed
    
    #################################################Quotation Urls##########################
    path('purchase/add/', views.purchase_quote, name='purchase_quote'),
    
    path('purchase-orders/', views.quotepurchaseList, name='purchase-orders'),
    path('purchase/<int:pk>/', views.PurchaseQuotationDetailView, name='quotation-detail'),
    path('purchase/<int:pk>/delete/',views.PurchaseQuotationDeleteView, name='quotation-delete'),
    
    
    
    
    
    
    
    ###################################Purchase Urls##########################
    path('purchase-detail/<int:pk>/',views.purchaseDetail, name='purchase-detail'),
    path('purchase-delete/<int:pk>/', views.purchaseDelete, name='purchase-delete'),
    path('purchase-invoices/', views.purchaseList, name='purchaseOrder'),
    path('purchase-invoices/add/', views.purchaseEntry, name='add_purchase'),
    #####################################################################################################

    
    path('pdfs/', GeneratePDF.as_view(), name='pdfs'),
    path('purchase_return_item/delete/<int:item_id>/', views.delete_purchase_return_item, name='delete_purchase_return_item'),
    path('purchase-return/create/', views.create_purchase_return, name='create_purchase_return'),
    path('purchase-return/<int:purchase_return_id>/', views.purchase_return_detail, name='purchase_return_detail'),
    path('purchase-return/<int:purchase_return_id>/add_item/', views.add_purchase_return_item, name='add_purchase_return_item'),
    path('purchase_return/', views.purchase_return_list, name='purchase_return_list'),
]
