# Generated by Django 4.2.4 on 2023-12-23 08:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_materialstock_entry_date_productstock_entry_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='materialstock',
            name='total_value',
        ),
        migrations.RemoveField(
            model_name='productstock',
            name='total_value',
        ),
    ]
