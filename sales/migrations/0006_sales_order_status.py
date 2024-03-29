# Generated by Django 4.2.4 on 2024-01-17 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0005_sales_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='sales',
            name='Order_Status',
            field=models.CharField(blank=True, choices=[('pending', 'pending'), ('approved', 'approved'), ('inProduction', 'inProduction'), ('produced', 'produced'), ('deliverPending', 'deliverPending'), ('completed', 'completed')], default='pending', max_length=20, null=True),
        ),
    ]
