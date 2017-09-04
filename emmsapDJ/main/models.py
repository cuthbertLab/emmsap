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


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'



class Chords(models.Model):
    pieceid = models.IntegerField(db_column='pieceId')  # Field name made lowercase.
    chorddata = models.CharField(db_column='chordData', max_length=32765, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'chords'



class Country(models.Model):
    name = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'country'
        verbose_name_plural = 'countries'


class Composer(models.Model):
    iscanonical = models.NullBooleanField(db_column='isCanonical', blank=True, null=True)  # Field name made lowercase.
    canonicallink = models.IntegerField(db_column='canonicalLink', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(max_length=64, blank=True, null=True)
    sortyear = models.IntegerField(db_column='sortYear', blank=True, null=True)  # Field name made lowercase.
    earliestyear = models.IntegerField(db_column='earliestYear', blank=True, null=True)  # Field name made lowercase.
    latestyear = models.IntegerField(db_column='latestYear', blank=True, null=True)  # Field name made lowercase.
    country = models.ForeignKey(Country, on_delete=models.CASCADE) 

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'composer'



class Intervals(models.Model):
    fn = models.CharField(max_length=255, blank=True, null=True)
    partid = models.IntegerField(db_column='partId', blank=True, null=True)  # Field name made lowercase.
    intervals = models.TextField(blank=True, null=True)
    intervalsnounisons = models.TextField(db_column='intervalsNoUnisons', blank=True, null=True) # Field name made lowercase.

    def __str__(self):
        return self.fn + ':' + str(self.partid)


    class Meta:
        managed = False
        db_table = 'intervals'
        unique_together = (('fn', 'partid'),)


class Piecetwopart3Grammapping(models.Model):
    ngramid = models.IntegerField(db_column='ngramId', blank=True, null=True)  # Field name made lowercase.
    pieceid = models.IntegerField(db_column='pieceId', blank=True, null=True)  # Field name made lowercase.
    ngramcount = models.IntegerField(db_column='ngramCount', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'pieceTwoPart3GramMapping'


class Piece(models.Model):
    filename = models.CharField(unique=True, max_length=255, blank=True, null=True)
    piecename = models.CharField(max_length=255, blank=True, null=True)
    composer = models.PositiveIntegerField(blank=False, null=False, default=12) # models.ForeignKey(Composer, blank=False, null=False, default=12, on_delete=models.CASCADE)
    frag = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.filename

    def stream(self):
        '''
        returns a music21 Score object from this piece
        '''
        if hasattr(self, '_stream') and self._stream is not None:
            return self._stream
        if self.filename is not None:
            from music21 import converter
            import os
            from emmsap import files
            try:
                s = converter.parse(os.path.join(files.emmsapDir, self.filename))
                self._stream = s
                return s
            except:
                print("%s Failed in conversion" % self.filename)
                return None
        else:
            return None
    
    def numberOfVoices(self):
        '''
        returns the number of voices in the piece
        
        >>> p = Piece(4)
        >>> p.filename
        u'Ascoli_Piceno_Mater_Digna_Dei_Lux.xml'
        >>> p.numberOfVoices()
        2
        '''
        s = self.stream()
        if s is not None:
            return len(s.parts)
        else:
            return 0


    class Meta:
        db_table = 'pieces'


class Ratiosdiarhy2(models.Model):
    segment1id = models.IntegerField(db_column='segment1Id')  # Field name made lowercase.
    segment2id = models.IntegerField(db_column='segment2Id')  # Field name made lowercase.
    ratio = models.SmallIntegerField(db_index=True)

    class Meta:
        managed = False
        db_table = 'ratiosDiaRhy2'


class Segment(models.Model):
    piece = models.ForeignKey(Piece, on_delete=models.CASCADE) 
    partid = models.IntegerField(db_column='partId', blank=True, null=True)  # Field name made lowercase.
    segmentid = models.IntegerField(db_column='segmentId', blank=True, null=True)  # Field name made lowercase.
    measurestart = models.IntegerField(db_column='measureStart', blank=True, null=True)  # Field name made lowercase.
    measureend = models.IntegerField(db_column='measureEnd', blank=True, null=True)  # Field name made lowercase.
    encodingtype = models.CharField(db_column='encodingType', max_length=20, blank=True, null=True)  # Field name made lowercase.
    segmentdata = models.CharField(db_column='segmentData', max_length=40, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'segment'


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
        unique_together = (('fn', 'partid'),)
