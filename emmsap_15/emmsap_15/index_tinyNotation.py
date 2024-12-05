import string

from django.db import transaction

import music21.note

from .models import Piece, TinyNotation, Intervals
from .to_tinyNotation import convert


# noinspection SpellCheckingInspection
alphabet = '__BCDEFGHIJKLMNOPQSTUVWXYZ'


def main():
    print('Indexing intervals and tinyNotation:')
    i = 0
    pieces = Piece.objects.exclude(tinynotation__isnull=False)
    for piece in pieces:
        i += 1
        print(f'{piece.filename} ({i}/{pieces.count()})')
        with transaction.atomic():
            for part_id, part in enumerate(piece.stream().parts):
                index_intervals_one_part(piece, part, part_id)
                index_tinyNotation_one_part(piece, part, part_id)
    print(f'Indexed intervals and tinyNotation for {i} piece(s).')


def index_tinyNotation_one_part(piece, part, part_id):
    ts_obj = part[music21.meter.TimeSignature].first()
    if not ts_obj:
        ts_ratio = 'unk'
    else:
        # we use numerator, denominator because
        # it automatically converts 2/2+1/16 to 17/16
        # (or for this project, 9/8+9/8+9/8)
        ts_ratio = f'{ts_obj.numerator}/{ts_obj.denominator}'
    pf = part.flatten().notesAndRests.stream()
    tn = convert(pf)
    pf_strip = pf.stripTies()
    tn_strip = convert(pf_strip)
    tn_obj = TinyNotation(
        piece=piece,
        part_id=part_id,
        tn=tn,
        tn_strip=tn_strip,
        ts_ratio=ts_ratio,
    )
    tn_obj.save()


def index_intervals_one_part(
    piece: Piece,
    part: music21.stream.Part,
    part_id: int,
):
    pf = part.flatten().stripTies().getElementsByClass(music21.note.GeneralNote)
    last_dnn: int = 0
    intervals = []
    intervals_no_unisons = []
    intervals_with_rests = []
    intervals_one_char = []

    for n in pf:
        if not n.pitches:
            intervals_with_rests.append('r')
            intervals_one_char.append('r')
            continue
        dnn = n.pitches[0].diatonicNoteNum
        if not last_dnn:
            last_dnn = dnn
            continue

        intv = dnn - last_dnn
        if intv >= 0:
            intv += 1
        else:
            intv -= 1

        if abs(intv) > 16:
            last_dnn = dnn
            continue  # encoding error

        str_intv = str(intv)
        if abs(intv) >= 10:
            str_intv = string.ascii_uppercase[abs(intv) - 10]
        intervals.append(str_intv)
        intervals_with_rests.append(str_intv)
        if intv != 1:
            intervals_no_unisons.append(str_intv)
        if intv > 0:
            intervals_one_char.append(str_intv)
        else:
            intervals_one_char.append(alphabet[-intv])  # B-W

        last_dnn = dnn

    intv_obj = Intervals(
        piece=piece,
        part_id=part_id,
        intervals=''.join(intervals),
        intervals_no_unisons=''.join(intervals_no_unisons),
        intervals_with_rests=''.join(intervals_with_rests),
        intervals_one_char=''.join(intervals_one_char),
    )
    intv_obj.save()
