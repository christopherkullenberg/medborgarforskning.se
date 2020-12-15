# Generated by Django 2.2.16 on 2020-12-15 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
            ],
            options={
                'verbose_name': 'Author',
                'verbose_name_plural': 'Authors',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField()),
                ('title', models.CharField(db_index=True, default='title', max_length=100)),
                ('title_en', models.CharField(db_index=True, default='title', max_length=100, null=True)),
                ('title_sv', models.CharField(db_index=True, default='title', max_length=100, null=True)),
                ('publishedDate', models.DateField(db_index=True)),
                ('content', models.TextField()),
                ('content_en', models.TextField(null=True)),
                ('content_sv', models.TextField(null=True)),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
            },
        ),
    ]
