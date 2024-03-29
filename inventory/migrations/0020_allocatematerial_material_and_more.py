# Generated by Django 4.2.4 on 2024-01-18 23:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0006_sales_order_status'),
        ('inventory', '0019_remove_allocatematerial_pending'),
    ]

    operations = [
        migrations.AddField(
            model_name='allocatematerial',
            name='Material',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='production_product', to='inventory.material'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='allocatematerial',
            name='sales_order',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='sales.sales'),
            preserve_default=False,
        ),
    ]
