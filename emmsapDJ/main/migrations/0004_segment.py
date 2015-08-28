# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20150827_2332'),
    ]

    operations = [
        migrations.CreateModel(
            name='Segment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('partid', models.IntegerField(null=True, db_column='partId', blank=True)),
                ('segmentid', models.IntegerField(null=True, db_column='segmentId', blank=True)),
                ('measurestart', models.IntegerField(null=True, db_column='measureStart', blank=True)),
                ('measureend', models.IntegerField(null=True, db_column='measureEnd', blank=True)),
                ('encodingtype', models.CharField(max_length=20, null=True, db_column='encodingType', blank=True)),
                ('segmentdata', models.CharField(max_length=40, null=True, db_column='segmentData', blank=True)),
            ],
            options={
                'db_table': 'segment',
                'managed': False,
            },
        ),
    ]
