# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-10-22 11:50
from __future__ import unicode_literals

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0004_auto_20181022_1351'),
    ]

    operations = [
        migrations.AddField(
            model_name='flat_obj',
            name='pereferiya',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Электричество', 'Электричество'), ('Газ', 'Газ'), ('Канализация', 'Канализация')], default='--', max_length=15, verbose_name='Переферия:'),
        ),
        migrations.AddField(
            model_name='flat_obj',
            name='relef',
            field=models.CharField(choices=[('Ровный', 'Ровный'), ('Уклон', 'Уклон')], default='--', max_length=15, verbose_name='Вид рельефа:'),
        ),
        migrations.AddField(
            model_name='flat_obj',
            name='vid',
            field=models.CharField(choices=[('На море', 'На море'), ('На горы', 'На горы'), ('На море и горы', 'На море и горы')], default='--', max_length=15, verbose_name='Вид'),
        ),
        migrations.AddField(
            model_name='flat_obj',
            name='vid_prava',
            field=models.CharField(choices=[('Собственность', 'Собственность'), ('Аренда (49лет)', 'Аренда (49лет)')], default='--', max_length=15, verbose_name='Вид права:'),
        ),
        migrations.AddField(
            model_name='flat_obj',
            name='vid_razr',
            field=models.CharField(choices=[('Поселений (ИЖС)', 'Поселений (ИЖС)'), ('Земля промназначения', 'Земля промназначения'), ('Садовое некоммерческое товарищество', 'Садовое некоммерческое товарищество'), ('ДНП', 'ДНП')], default='--', max_length=15, verbose_name='Вид разрешения:'),
        ),
    ]
