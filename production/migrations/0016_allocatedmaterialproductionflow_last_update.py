# Generated by Django 4.2.4 on 2024-01-22 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0015_producedrow_totalleft_producedrow_totalprocessed_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='allocatedmaterialproductionflow',
            name='last_update',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
