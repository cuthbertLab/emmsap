import concurrent.futures
from functools import partial, cache
import typing as t

from django.db.models.query import QuerySet
from django.db import transaction, connection

try:
    from Levenshtein import ratio as lvRatio
except ImportError as ie:
    raise ImportError(
        'No Levenshtein C program found -- will be much slower; \n'
          + 'run pip3 install python-Levenshtein') from ie


from .models import Segment, Ratio


def update_ratio_table_parallel(encoding_type: str):
    '''
    updates the ratio table in Parallel,
    computing ratios for all segments (against all lower numbered segments)
    that do not have ratios computed
    '''
    max_workers = 3
    missing_segments = find_segments_with_no_ratios(encoding_type)
    num_missing_segments = len(missing_segments)
    print(f'{num_missing_segments} waiting to be indexed')
    partial_commit = partial(commit_ratio_for_one_segment,
                             encoding_type=encoding_type,
                             search_direction='down')
    print('Starting multi-threading index task, will take some time before first results.')
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_seg = {executor.submit(partial_commit, seg): seg
                         for seg in missing_segments}
        total_done = 0
        num_added = 0
        for future in concurrent.futures.as_completed(future_to_seg):
            num_added += future.result()
            total_done += 1
            if not total_done % 30:
                print(f'Done {total_done} segments of {num_missing_segments} -- found {num_added} interesting.')

    # common.runNonParallel(missing_segments, partial_commit, updateMultiply=30, updateFunction=True)


def find_segments_with_no_ratios(encoding_type: str) -> QuerySet[Segment]:
    '''
    returns a QuerySet of Segments which have no ratios in the ratio list
    '''
    missing_ratios = Segment.objects.filter(
        encoding_type=encoding_type,
        ratio_searched=False,
    )
    print(f'There are {len(missing_ratios)} segment ids that should have ratios')
    return missing_ratios


@transaction.atomic
def commit_ratio_for_one_segment(
    seg: Segment,
    search_direction: str = 'down',
    encoding_type: str = 'dia_rhy',
) -> int:
    new_ratios = get_ratios_for_segment(seg, search_direction, encoding_type)
    for rat in new_ratios:
        rat.save()
    seg.ratio_searched = True
    seg.save()
    return len(new_ratios)


@cache
def raw_ratios(encoding_type: str):
    '''
    Perform a raw SQL query for speed and memory:
    '''
    with connection.cursor() as cursor:
        # noinspection SqlResolve
        cursor.execute('SELECT id, segment_data, piece_id '
                       'FROM emmsap2_segment '
                       'WHERE encoding_type = %s',
                       [encoding_type])
        return cursor.fetchall()


def get_ratios_for_segment(
    seg: Segment,
    search_direction: str = 'down',
    encoding_type: str = 'dia_rhy',
) -> t.Sequence[Ratio]:
    minimums = {
        'dia_rhy': 5900,
        'int_rhy': 6500,
    }
    minimum_to_store = minimums[encoding_type]
    others = raw_ratios(encoding_type)
    new_objs: list[Ratio] = []
    my_data = seg.segment_data
    my_id = seg.id
    my_piece_id = seg.piece_id

    for other_id, other_data, other_piece_id in others:
        if other_piece_id == my_piece_id:
            continue  # no internal matches.
        if search_direction == 'up' and other_id <= my_id:
            continue
        elif search_direction == 'down' and other_id >= my_id:
            continue
        elif search_direction == 'both' and other_id == my_id:
            continue

        ratio_int = ratio_from_segment_data(my_data, other_data)
        if ratio_int > minimum_to_store:
            r1 = Ratio(segment1_id=seg.id,
                       segment2_id=other_id,
                       ratio=ratio_int,
                       encoding_type=encoding_type)
            new_objs.append(r1)
            r2 = Ratio(segment1_id=other_id,
                       segment2_id=seg.id,
                       ratio=ratio_int,
                       encoding_type=encoding_type)
            new_objs.append(r2)
    return new_objs


def ratio_from_segment_data(data1: str, data2: str) -> int:
    return int(10_000 * lvRatio(data1, data2))

