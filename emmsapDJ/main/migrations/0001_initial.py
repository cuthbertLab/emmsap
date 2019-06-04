# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chords',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pieceid', models.IntegerField(db_column='pieceId')),
                ('chorddata', models.CharField(max_length=32765, null=True, db_column='chordData', blank=True)),
            ],
            options={
                'db_table': 'chords',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Intervals',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fn', models.CharField(max_length=255, null=True, blank=True)),
                ('partid', models.IntegerField(null=True, db_column='partId', blank=True)),
                ('intervals', models.TextField(null=True, blank=True)),
            ],
            options={
                'db_table': 'intervals',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Piece',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.CharField(max_length=255, unique=True, null=True, blank=True)),
                ('piecename', models.CharField(max_length=255, null=True, blank=True)),
                ('composer_id', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'pieces',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Piecetwopart3Grammapping',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ngramid', models.IntegerField(null=True, db_column='ngramId', blank=True)),
                ('pieceid', models.IntegerField(null=True, db_column='pieceId', blank=True)),
                ('ngramcount', models.IntegerField(null=True, db_column='ngramCount', blank=True)),
            ],
            options={
                'db_table': 'pieceTwoPart3GramMapping',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Ratiosdiarhy2',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('segment1id', models.IntegerField(db_column='segment1Id')),
                ('segment2id', models.IntegerField(db_column='segment2Id')),
                ('ratio', models.SmallIntegerField()),
            ],
            options={
                'db_table': 'ratiosDiaRhy2',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Segments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pieceid', models.IntegerField(null=True, db_column='pieceId', blank=True)),
                ('partid', models.IntegerField(null=True, db_column='partId', blank=True)),
                ('segmentid', models.IntegerField(null=True, db_column='segmentId', blank=True)),
                ('measurestart', models.IntegerField(null=True, db_column='measureStart', blank=True)),
                ('measureend', models.IntegerField(null=True, db_column='measureEnd', blank=True)),
                ('encodingtype', models.CharField(max_length=20, null=True, db_column='encodingType', blank=True)),
                ('segmentdata', models.CharField(max_length=40, null=True, db_column='segmentData', blank=True)),
            ],
            options={
                'db_table': 'segments',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Texts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fn', models.CharField(max_length=255, unique=True, null=True, blank=True)),
                ('language', models.CharField(max_length=4, null=True, blank=True)),
                ('text', models.TextField(null=True, blank=True)),
                ('textreg', models.TextField(null=True, db_column='textReg', blank=True)),
                ('textnospace', models.TextField(null=True, db_column='textNoSpace', blank=True)),
            ],
            options={
                'db_table': 'texts',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tinynotation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fn', models.CharField(max_length=255, null=True, blank=True)),
                ('partid', models.IntegerField(null=True, db_column='partId', blank=True)),
                ('tsratio', models.CharField(max_length=10, null=True, db_column='tsRatio', blank=True)),
                ('tn', models.TextField(null=True, blank=True)),
                ('tnstrip', models.TextField(null=True, db_column='tnStrip', blank=True)),
            ],
            options={
                'db_table': 'tinyNotation',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Twopart3Grams',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('int1', models.IntegerField()),
                ('int2', models.IntegerField()),
                ('int3', models.IntegerField()),
            ],
            options={
                'db_table': 'twoPart3Grams',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Composer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('iscanonical', models.NullBooleanField(db_column='isCanonical')),
                ('canonicallink', models.IntegerField(null=True, db_column='canonicalLink', blank=True)),
                ('name', models.CharField(max_length=64, null=True, blank=True)),
                ('sortyear', models.IntegerField(null=True, db_column='sortYear', blank=True)),
                ('earliestyear', models.IntegerField(null=True, db_column='earliestYear', blank=True)),
                ('latestyear', models.IntegerField(null=True, db_column='latestYear', blank=True)),
            ],
            options={
                'db_table': 'composer',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40, null=True, blank=True)),
            ],
            options={
                'db_table': 'country',
            },
        ),
        migrations.AddField(
            model_name='composer',
            name='country',
            field=models.ForeignKey(to='main.Country', on_delete=models.CASCADE),
        ),
    ]
