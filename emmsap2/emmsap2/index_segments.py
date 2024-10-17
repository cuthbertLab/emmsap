import typing as t

from django.db import transaction

from music21 import search as searchBase
from music21.search import segment


from .indexing_methods import translate_diatonic_intervals_and_speed
from .models import Piece, Segment


# change management/commands/updateDB.py when this changes.
encodings_to_algorithms = {
    # 'dia_slower1': searchBase.translateStreamToString,
    'dia_rhy': searchBase.translateDiatonicStreamToString,
    # 'int_rhy_jitter': searchBase.translateIntervalsAndSpeed,
    # 'int_rhy': searchBase.translateIntervalsAndSpeed,
    'int_dia_diff':  translate_diatonic_intervals_and_speed,
}


def main(encoding_type: str):
    print(f'Beginning to index segments for {encoding_type=}')
    missing = find_pieces_without_segments(encoding_type)
    print(f'{len(missing)} piece(s) to index')
    segment_indexes = index_pieces_segments(missing, encoding_type)
    filename_to_piece: dict[str, Piece] = {p.filename: p for p in missing}
    piece_to_segments: dict[Piece, t.Any] = {}
    for filename, seg_data in segment_indexes.items():
        piece_to_segments[filename_to_piece[filename]] = seg_data
    print('Storing segments')
    store_segments(piece_to_segments, encoding_type)


# too short pieces that do not have segments.
ignore_these = {
    'Vienna_922_Gloria_T_end.xml',
    'Fauvel_Monophonic_59.mxl',
    'Fauvel_Monophonic_60.mxl',
    'Fauvel_Monophonic_63.mxl',
    'Fauvel_Monophonic_65.mxl',
}

def find_pieces_without_segments(encoding_type: str) -> list[Piece]:
    missing = []
    for p in Piece.objects.prefetch_related('segment_set'):
        if p.filename in ignore_these:
            continue
        if not p.segment_set.filter(encoding_type=encoding_type).count():
            missing.append(p)
    return missing


def index_pieces_segments(pieces: list[Piece], encoding_type: str):
    try:
        algorithm = encodings_to_algorithms[encoding_type]
    except IndexError as ie:
        raise IndexError(f'Unknown encoding_type: {encoding_type!r}') from ie

    indexed_segments = segment.indexScoreFilePaths(
        [p.filepath for p in pieces],
        segmentLengths=30,
        overlap=25,
        giveUpdates=True,
        algorithm=algorithm,
        jitter=0,
        failFast=False,
    )
    print('done indexing segments')
    return indexed_segments


def store_segments(piece_to_segments: dict[Piece, t.Any], encoding_type: str) -> None:
    for piece_obj, indexed_segments in piece_to_segments.items():
        with transaction.atomic():
            for part_id, part_info in enumerate(indexed_segments):
                ml = part_info['measureList']
                num_segments = len(ml)
                for segment_id in range(num_segments):
                    measure_start = ml[segment_id][0]
                    measure_end = ml[segment_id][1]
                    segment_data = part_info['segmentList'][segment_id]
                    if len(segment_data) < 20 and segment_id > 0:
                        # don't index last few notes, etc. which will be included
                        # in the previous segment.
                        continue
                    if len(segment_data) < 10 and segment_id == 0:
                        # don't index pieces with fewer than 10 notes at all.
                        continue

                    seg = Segment(
                        piece=piece_obj,
                        part_id=part_id,
                        measure_start=measure_start,
                        measure_end=measure_end,
                        encoding_type=encoding_type,
                        segment_data=segment_data,
                    )
                    seg.save()

