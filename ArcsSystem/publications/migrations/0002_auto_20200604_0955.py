# Generated by Django 2.2.13 on 2020-06-04 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyword',
            name='keyword',
            field=models.TextField(),
        ),
    ]
