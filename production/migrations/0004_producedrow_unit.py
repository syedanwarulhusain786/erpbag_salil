# Generated by Django 4.2.4 on 2024-01-18 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0003_remove_producedrow_package_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='producedrow',
            name='unit',
            field=models.DecimalField(decimal_places=2, default=450, max_digits=50),
            preserve_default=False,
        ),
    ]
