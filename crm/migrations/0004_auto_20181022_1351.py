# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-10-22 10:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0003_remove_flat_obj_apparts1_pr'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flat_obj',
            old_name='apparts_pr',
            new_name='appart_pr',
        ),
    ]
