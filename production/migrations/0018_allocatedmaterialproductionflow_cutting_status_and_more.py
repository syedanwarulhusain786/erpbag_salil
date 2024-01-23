# Generated by Django 4.2.4 on 2024-01-22 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0017_alter_allocatedmaterialproductionflow_last_update'),
    ]

    operations = [
        migrations.AddField(
            model_name='allocatedmaterialproductionflow',
            name='cutting_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending', max_length=20),
        ),
        migrations.AddField(
            model_name='allocatedmaterialproductionflow',
            name='packaginganddispatch_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending', max_length=20),
        ),
        migrations.AddField(
            model_name='allocatedmaterialproductionflow',
            name='printing_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending', max_length=20),
        ),
        migrations.AddField(
            model_name='allocatedmaterialproductionflow',
            name='stitching_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending', max_length=20),
        ),
    ]
