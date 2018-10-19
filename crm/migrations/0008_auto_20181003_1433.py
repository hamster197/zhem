# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-10-03 11:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0007_auto_20180928_1233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otchet_nov',
            name='vneseno_komisii',
            field=models.IntegerField(default='0', verbose_name='Внесенно комисии 1:'),
        ),
        migrations.AlterField(
            model_name='otchet_nov',
            name='vneseno_komisii2',
            field=models.IntegerField(default=0, verbose_name='Внесенно комисии 2:'),
        ),
        migrations.AlterField(
            model_name='otchet_nov',
            name='vneseno_komisii3',
            field=models.IntegerField(default=0, verbose_name='Внесенно комисии: 3'),
        ),
        migrations.AlterField(
            model_name='otchet_nov',
            name='vneseno_komisii4',
            field=models.IntegerField(default=0, verbose_name='Внесенно комисии 4:'),
        ),
        migrations.AlterField(
            model_name='otchet_nov',
            name='vneseno_komisii5',
            field=models.IntegerField(default=0, verbose_name='Внесенно комисии 5:'),
        ),
        migrations.AlterField(
            model_name='otchet_nov',
            name='vneseno_komisii_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата внесения комисии 1:'),
        ),
        migrations.AlterField(
            model_name='otchet_nov',
            name='vneseno_komisii_date2',
            field=models.DateField(blank=True, null=True, verbose_name='Дата внесения комисии 2:'),
        ),
        migrations.AlterField(
            model_name='otchet_nov',
            name='vneseno_komisii_date3',
            field=models.DateField(blank=True, null=True, verbose_name='Дата внесения комисии 3:'),
        ),
        migrations.AlterField(
            model_name='otchet_nov',
            name='vneseno_komisii_date4',
            field=models.DateField(blank=True, null=True, verbose_name='Дата внесения комисии 4:'),
        ),
        migrations.AlterField(
            model_name='otchet_nov',
            name='vneseno_komisii_date5',
            field=models.DateField(blank=True, null=True, verbose_name='Дата внесения комисии 5:'),
        ),
    ]
