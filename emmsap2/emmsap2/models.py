from __future__ import annotations

import pathlib

from django.db import models

from music21 import converter
from music21 import expressions
from music21 import layout
from music21 import stream

from . import files


class Chords(models.Model):
    piece = models.OneToOneField('Piece', on_delete=models.CASCADE)
    chord_data = models.TextField(blank=True, null=True)


class Country(models.Model):
    name = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'countries'


class Composer(models.Model):
    is_canonical = models.BooleanField(blank=True, null=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    sort_year = models.IntegerField(blank=True, null=True)
    earliest_year = models.IntegerField(blank=True, null=True)
    latest_year = models.IntegerField(blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE) 

    def __str__(self):
        return self.name


class Intervals(models.Model):
    piece = models.ForeignKey('Piece', on_delete=models.CASCADE)
    part_id = models.IntegerField(blank=True, null=True)
    intervals = models.TextField(blank=True, null=True)
    intervals_no_unisons = models.TextField(blank=True, null=True)
    intervals_with_rests = models.TextField(blank=True, null=True)
    intervals_one_char = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.fn + ':' + str(self.part_id)

    class Meta:
        unique_together = (('piece', 'part_id'),)


class Piece(models.Model):
    filename = models.CharField(unique=True, max_length=255, blank=True, null=True)
    piece_name = models.CharField(max_length=255, blank=True, null=True)
    composer = models.ForeignKey(Composer, blank=False, null=False, default=1,
                                 on_delete=models.CASCADE)
    frag = models.BooleanField(blank=True, null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stream = None

    def __str__(self):
        return self.filename

    @property
    def filepath(self) -> pathlib.Path:
        return files.emmsapDir / self.filename

    def stream(self) -> stream.Score|None:
        '''
        returns a music21 Score object from this piece
        '''
        if self._stream is not None:
            return self._stream
        if self.filename is not None:
            # noinspection PyBroadException
            s = converter.parse(self.filepath)
            self._stream = s
            return s
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
    measure_start = models.IntegerField(blank=True, null=True)
    measure_end = models.IntegerField(blank=True, null=True)
    encoding_type = models.CharField(max_length=20)
    segment_data = models.CharField(max_length=40, blank=True, null=True)
    ratio_searched = models.BooleanField(default=False)

    def show(self):
        p = self.piece.stream()
        part = p.parts[self.part_id]
        excerpt = part.measures(self.measure_start, self.measure_end)
        for el in list(excerpt[layout.LayoutBase]):
            excerpt.remove(el, recurse=True)

        express = expressions.TextExpression(
            f'{self.piece.filename} part {self.part_id}, '
            + f'mm. {self.measure_start}-{self.measure_end}'
        )
        excerpt[stream.Measure][0].insert(0, express)
        excerpt.show()

    class Meta:
        indexes = [
            models.Index(fields=['piece']),
            models.Index(fields=['encoding_type']),
            models.Index(fields=['part_id']),
        ]


class Ratio(models.Model):
    segment1 = models.ForeignKey(Segment, on_delete=models.CASCADE, related_name='segment1s')
    segment2 = models.ForeignKey(Segment, on_delete=models.CASCADE, related_name='segment2s')
    ratio = models.SmallIntegerField()
    encoding_type = models.CharField(max_length=20)

    def __repr__(self):
        return f'<Ratio {self.ratio} {self.encoding_type} {self.segment1_id} {self.segment2_id}>'

    class Meta:
        indexes = [
            models.Index(fields=['encoding_type']),
        ]


class Text(models.Model):
    piece = models.OneToOneField(Piece, on_delete=models.CASCADE)
    language = models.CharField(max_length=4, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    text_reg = models.TextField(blank=True, null=True)
    text_no_space = models.TextField(blank=True, null=True)


class TinyNotation(models.Model):
    piece = models.ForeignKey(Piece, on_delete=models.CASCADE)
    part_id = models.IntegerField(blank=True, null=True)
    ts_ratio = models.CharField(max_length=10, blank=True, null=True)
    tn = models.TextField(blank=True, null=True)
    tn_strip = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = (('piece', 'part_id'),)


class SkipGroupCategory(models.Model):
    category = models.CharField(max_length=255)


class SkipGroup(models.Model):
    reason = models.TextField(blank=True, default='')
    category = models.ForeignKey(SkipGroupCategory, blank=True, null=True, on_delete=models.SET_NULL)


class SkipPiece(models.Model):
    skip_group = models.ForeignKey(SkipGroup, on_delete=models.CASCADE)
    piece = models.ForeignKey(Piece, on_delete=models.CASCADE)

