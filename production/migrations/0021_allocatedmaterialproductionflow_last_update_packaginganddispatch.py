# Generated by Django 4.2.4 on 2024-01-23 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0020_allocatedmaterialproductionflow_stitching_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='allocatedmaterialproductionflow',
            name='last_update_packaginganddispatch',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
