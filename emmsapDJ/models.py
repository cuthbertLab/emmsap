# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class Chords(models.Model):
    pieceid = models.IntegerField(db_column='pieceId')  # Field name made lowercase.
    chorddata = models.CharField(db_column='chordData', max_length=32765, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'chords'


class Composers(models.Model):
    iscanonical = models.IntegerField(db_column='isCanonical', blank=True, null=True)  # Field name made lowercase.
    canonicallink = models.IntegerField(db_column='canonicalLink', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(max_length=64, blank=True, null=True)
    sortyear = models.IntegerField(db_column='sortYear', blank=True, null=True)  # Field name made lowercase.
    earliestyear = models.IntegerField(db_column='earliestYear', blank=True, null=True)  # Field name made lowercase.
    latestyear = models.IntegerField(db_column='latestYear', blank=True, null=True)  # Field name made lowercase.
    countryid = models.IntegerField(db_column='countryId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'composers'


class Countries(models.Model):
    name = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'countries'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Intervals(models.Model):
    fn = models.CharField(max_length=255, blank=True, null=True)
    partid = models.IntegerField(db_column='partId', blank=True, null=True)  # Field name made lowercase.
    intervals = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'intervals'
        unique_together = (('fn', 'partId'),)


class Piecetwopart3Grammapping(models.Model):
    ngramid = models.IntegerField(db_column='ngramId', blank=True, null=True)  # Field name made lowercase.
    pieceid = models.IntegerField(db_column='pieceId', blank=True, null=True)  # Field name made lowercase.
    ngramcount = models.IntegerField(db_column='ngramCount', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'pieceTwoPart3GramMapping'


class Pieces(models.Model):
    filename = models.CharField(unique=True, max_length=255, blank=True, null=True)
    piecename = models.CharField(max_length=255, blank=True, null=True)
    composer_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pieces'


class Ratiosdiarhy2(models.Model):
    segment1id = models.IntegerField(db_column='segment1Id')  # Field name made lowercase.
    segment2id = models.IntegerField(db_column='segment2Id')  # Field name made lowercase.
    ratio = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'ratiosDiaRhy2'


class Segments(models.Model):
    pieceid = models.IntegerField(db_column='pieceId', blank=True, null=True)  # Field name made lowercase.
    partid = models.IntegerField(db_column='partId', blank=True, null=True)  # Field name made lowercase.
    segmentid = models.IntegerField(db_column='segmentId', blank=True, null=True)  # Field name made lowercase.
    measurestart = models.IntegerField(db_column='measureStart', blank=True, null=True)  # Field name made lowercase.
    measureend = models.IntegerField(db_column='measureEnd', blank=True, null=True)  # Field name made lowercase.
    encodingtype = models.CharField(db_column='encodingType', max_length=20, blank=True, null=True)  # Field name made lowercase.
    segmentdata = models.CharField(db_column='segmentData', max_length=40, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'segments'


class Texts(models.Model):
    fn = models.CharField(unique=True, max_length=255, blank=True, null=True)
    language = models.CharField(max_length=4, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    textreg = models.TextField(db_column='textReg', blank=True, null=True)  # Field name made lowercase.
    textnospace = models.TextField(db_column='textNoSpace', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'texts'


class Tinynotation(models.Model):
    fn = models.CharField(max_length=255, blank=True, null=True)
    partid = models.IntegerField(db_column='partId', blank=True, null=True)  # Field name made lowercase.
    tsratio = models.CharField(db_column='tsRatio', max_length=10, blank=True, null=True)  # Field name made lowercase.
    tn = models.TextField(blank=True, null=True)
    tnstrip = models.TextField(db_column='tnStrip', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tinyNotation'
        unique_together = (('fn', 'partId'),)


class Twopart3Grams(models.Model):
    int1 = models.IntegerField()
    int2 = models.IntegerField()
    int3 = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'twoPart3Grams'
