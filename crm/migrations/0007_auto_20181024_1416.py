# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-10-24 11:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0006_auto_20181022_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flat_obj',
            name='vid',
            field=models.CharField(choices=[('На море', 'На море'), ('На горы', 'На горы'), ('На море и горы', 'На море и горы')], default='--', max_length=125, verbose_name='Вид'),
        ),
    ]
