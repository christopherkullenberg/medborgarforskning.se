# Generated by Django 3.0.3 on 2020-02-21 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20200221_1254'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='end_date',
            field=models.DateTimeField(verbose_name='End date'),
        ),
        migrations.AddField(
            model_name='project',
            name='start_date',
            field=models.DateTimeField(verbose_name='Start date'),
        ),
    ]