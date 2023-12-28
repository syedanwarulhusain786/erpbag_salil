# Generated by Django 4.2.4 on 2023-12-23 11:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_materialstock_total_value_productstock_total_value'),
        ('accounting', '0010_ledgerentry'),
    ]

    operations = [
        migrations.RenameField(
            model_name='purchaseinvoice',
            old_name='billing_address',
            new_name='BillingAddress',
        ),
        migrations.RenameField(
            model_name='purchaseinvoice',
            old_name='csgst_total',
            new_name='FinalAmount',
        ),
        migrations.RenameField(
            model_name='purchaseinvoice',
            old_name='final_amt',
            new_name='InvoiceNumber',
        ),
        migrations.RenameField(
            model_name='purchaseinvoice',
            old_name='notes_comments',
            new_name='NotesComments',
        ),
        migrations.RenameField(
            model_name='purchaseinvoice',
            old_name='quotation_date',
            new_name='PurchaseVoucherDate',
        ),
        migrations.RenameField(
            model_name='purchaseinvoice',
            old_name='quotation_number',
            new_name='PurchaseVoucherNumber',
        ),
        migrations.RenameField(
            model_name='purchaseinvoice',
            old_name='shipping_address',
            new_name='ShippingAddress',
        ),
        migrations.RenameField(
            model_name='purchaseinvoice',
            old_name='sgst_total',
            new_name='SubTotal',
        ),
        migrations.RenameField(
            model_name='purchaseinvoice',
            old_name='sub_total',
            new_name='SupplierAddress',
        ),
        migrations.RenameField(
            model_name='purchaseinvoice',
            old_name='terms_and_conditions',
            new_name='Terms_and_conditions',
        ),
        migrations.RemoveField(
            model_name='purchaseinvoice',
            name='Others',
        ),
        migrations.RemoveField(
            model_name='purchaseinvoice',
            name='tax_rate',
        ),
        migrations.RemoveField(
            model_name='purchaseinvoiceitemrow',
            name='entry_type',
        ),
        migrations.AddField(
            model_name='purchaseinvoice',
            name='InvoiceDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='purchaseinvoice',
            name='SupplierEmail',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='purchaseinvoice',
            name='SupplierMobile',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='purchaseinvoice',
            name='Vat',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='purchaseinvoiceitemrow',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='inventory.product'),
        ),
    ]