# Generated by Django 4.2.4 on 2024-01-23 08:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0022_purchaseinvoiceitemrow_service_and_more'),
        ('inventory', '0025_allocatematerial_idx'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_sent', models.PositiveIntegerField()),
                ('price_send', models.DecimalField(decimal_places=2, max_digits=50)),
                ('sent_date', models.DateField()),
                ('price_received', models.DecimalField(decimal_places=2, max_digits=50)),
                ('quantity_received', models.PositiveIntegerField()),
                ('received_date', models.DateField()),
                ('material_received', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='material_received', to='inventory.material')),
                ('material_send', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='material_send', to='inventory.material')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.supplier')),
            ],
        ),
    ]