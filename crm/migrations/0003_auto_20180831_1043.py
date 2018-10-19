# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-08-31 07:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0002_auto_20180830_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flat_obj',
            name='h_isp_uch',
            field=models.CharField(choices=[('Поселений (ИЖС)', 'Поселений (ИЖС)'), ('Садовое некоммерческое товарищество', 'Садовое некоммерческое товарищество'), ('Земля промназначения', 'Земля промназначения'), ('ДНП', 'ДНП'), ('Размещение эллингов', 'Размещение эллингов')], default='n/a', max_length=55, verbose_name='Использование участка:'),
        ),
    ]
