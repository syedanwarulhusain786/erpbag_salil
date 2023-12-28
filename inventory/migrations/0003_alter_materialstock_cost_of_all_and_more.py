# Generated by Django 4.2.4 on 2023-12-23 07:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_productstock_materialstock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materialstock',
            name='cost_of_all',
            field=models.DecimalField(decimal_places=2, max_digits=50),
        ),
        migrations.AlterField(
            model_name='materialstock',
            name='cost_of_single',
            field=models.DecimalField(decimal_places=2, max_digits=40),
        ),
        migrations.AlterField(
            model_name='materialstock',
            name='material',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.material'),
        ),
        migrations.AlterField(
            model_name='materialstock',
            name='total_value',
            field=models.DecimalField(decimal_places=2, max_digits=50),
        ),
        migrations.AlterField(
            model_name='productstock',
            name='cost_of_all',
            field=models.DecimalField(decimal_places=2, max_digits=50),
        ),
        migrations.AlterField(
            model_name='productstock',
            name='cost_of_single',
            field=models.DecimalField(decimal_places=2, max_digits=50),
        ),
        migrations.AlterField(
            model_name='productstock',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.product'),
        ),
        migrations.AlterField(
            model_name='productstock',
            name='total_value',
            field=models.DecimalField(decimal_places=2, max_digits=50),
        ),
        migrations.AlterField(
            model_name='service',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.productcategory'),
        ),
    ]