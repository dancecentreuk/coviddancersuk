# Generated by Django 3.1.1 on 2020-11-15 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0005_auto_20201115_2018'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='slug',
            field=models.SlugField(blank=True, max_length=250),
        ),
    ]
