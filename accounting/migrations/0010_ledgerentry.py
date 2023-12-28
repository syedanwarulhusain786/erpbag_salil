# Generated by Django 4.2.4 on 2023-12-23 11:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0009_purchaseinvoice_purchaseinvoiceitemrow'),
    ]

    operations = [
        migrations.CreateModel(
            name='LedgerEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('narration', models.CharField(max_length=499)),
                ('debit_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('credit_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('transaction_date', models.DateField(auto_now_add=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.ledger')),
            ],
        ),
    ]