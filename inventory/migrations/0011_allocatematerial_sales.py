# Generated by Django 4.2.4 on 2023-12-28 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0010_allocatematerial'),
    ]

    operations = [
        migrations.AddField(
            model_name='allocatematerial',
            name='sales',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
