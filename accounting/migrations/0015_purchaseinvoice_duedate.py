# Generated by Django 4.2.4 on 2023-12-26 00:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0014_purchasereturnitem_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseinvoice',
            name='dueDate',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
