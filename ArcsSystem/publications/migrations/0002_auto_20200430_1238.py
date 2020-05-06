# Generated by Django 2.2.12 on 2020-04-30 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='authors',
            field=models.CharField(default='Author', max_length=500),
        ),
        migrations.AddField(
            model_name='article',
            name='doi',
            field=models.CharField(default='doi', max_length=200),
        ),
        migrations.AddField(
            model_name='article',
            name='py',
            field=models.IntegerField(default='0'),
        ),
    ]