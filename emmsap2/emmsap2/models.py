from django.db import models


class Chords(models.Model):
    piece_id = models.IntegerField()
    chord_data = models.CharField(max_length=32765, blank=True, null=True)


class Country(models.Model):
    name = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'countries'


class Composer(models.Model):
    is_canonical = models.NullBooleanField(blank=True, null=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    sort_year = models.IntegerField(blank=True, null=True)
    earliest_year = models.IntegerField(blank=True, null=True)
    latest_year = models.IntegerField(blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE) 

    def __str__(self):
        return self.name


class Intervals(models.Model):
    fn = models.CharField(max_length=255, blank=True, null=True)
    part_id = models.IntegerField(db_column='partId', blank=True, null=True)
    intervals = models.TextField(blank=True, null=True)
    intervals_no_unisons = models.TextField(blank=True, null=True)
    intervals_with_rests = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.fn + ':' + str(self.part_id)

    class Meta:
        unique_together = (('fn', 'part_id'),)


class Piece(models.Model):
    filename = models.CharField(unique=True, max_length=255, blank=True, null=True)
    piece_name = models.CharField(max_length=255, blank=True, null=True)
    composer = models.ForeignKey(Composer, blank=False, null=False, default=12, on_delete=models.CASCADE)
    frag = models.BooleanField(blank=True, null=True)

    def __init__(self, *args, **kwargs):
        super(*args, **kwargs)
        self._stream = None

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


class Segment(models.Model):
    piece = models.ForeignKey(Piece, on_delete=models.CASCADE) 
    part_id = models.IntegerField(blank=True, null=True)
    segment_id = models.IntegerField(blank=True, null=True)
    measure_start = models.IntegerField(blank=True, null=True)
    measure_end = models.IntegerField(blank=True, null=True)
    encoding_type = models.CharField(max_length=20, blank=True, null=True)
    segment_data = models.CharField(max_length=40, blank=True, null=True)


class RatiosDiaRhy2(models.Model):
    segment1_id = models.ForeignKey(Segment, on_delete=models.CASCADE)
    segment2_id = models.ForeignKey(Segment, on_delete=models.CASCADE)
    ratio = models.SmallIntegerField(db_index=True)


class Texts(models.Model):
    fn = models.CharField(unique=True, max_length=255, blank=True, null=True)
    language = models.CharField(max_length=4, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    text_reg = models.TextField(blank=True, null=True)
    text_no_space = models.TextField(blank=True, null=True)


class TinyNotation(models.Model):
    fn = models.CharField(max_length=255, blank=True, null=True)
    part_id = models.IntegerField(blank=True, null=True)
    ts_ratio = models.CharField(max_length=10, blank=True, null=True)
    tn = models.TextField(blank=True, null=True)
    tn_strip = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = (('fn', 'part_id'),)
