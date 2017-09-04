# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-04 00:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20170904_0007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='piece',
            name='composer',
            field=models.ForeignKey(db_column='composer_id', default=12, on_delete=django.db.models.deletion.CASCADE, to='main.Composer'),
        ),
    ]
