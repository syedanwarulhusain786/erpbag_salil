# Generated by Django 4.2.4 on 2024-01-22 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0014_producedrow_alloca'),
    ]

    operations = [
        migrations.AddField(
            model_name='producedrow',
            name='TotalLeft',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='producedrow',
            name='TotalProcessed',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='producedrow',
            name='TotalprocessedNow',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]