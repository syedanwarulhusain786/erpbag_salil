# Generated by Django 4.2.4 on 2024-01-23 08:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0026_joblist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joblist',
            name='material_received',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='material_received', to='inventory.material'),
        ),
        migrations.AlterField(
            model_name='joblist',
            name='price_received',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=50, null=True),
        ),
        migrations.AlterField(
            model_name='joblist',
            name='quantity_received',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='joblist',
            name='received_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
