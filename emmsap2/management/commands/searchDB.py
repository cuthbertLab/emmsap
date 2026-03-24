from django.core.management.base import BaseCommand, CommandError

from ...index_segments import encodings_to_algorithms
from ...models import Piece
from ...similarity_ratio import SimilaritySearcher


class Command(BaseCommand):
    help = 'Search a range of pieces with SimilaritySearcher'

    def add_arguments(self, parser):
        parser.add_argument(
            '--start',
            dest='start_piece',
            type=int,
            help='First piece ID to search',
        )
        parser.add_argument(
            '--end',
            dest='end_piece',
            type=int,
            help='Last piece ID to search (inclusive)',
        )
        parser.add_argument(
            '--segment-type',
            default='dia_rhy',
            help='Segment encoding type to search',
        )
        parser.add_argument(
            '--min-threshold',
            type=int,
            default=8000,
            help='Minimum similarity threshold',
        )

    def handle(self, *args, **options):
        start_piece = options['start_piece']
        end_piece = options['end_piece']
        segment_type = options['segment_type']
        min_threshold = options['min_threshold']

        if segment_type not in encodings_to_algorithms:
            valid_segment_types = ', '.join(sorted(encodings_to_algorithms))
            raise CommandError(
                f'Unknown --segment-type {segment_type!r}. '
                f'Valid values: {valid_segment_types}.'
            )

        if start_piece is None and end_piece is not None:
            raise CommandError('--end requires --start.')

        highest_piece_id = Piece.objects.order_by('-id').values_list('id', flat=True).first()
        if highest_piece_id is None:
            raise CommandError('No Piece rows exist.')

        if start_piece is None and end_piece is None:
            recent_piece_ids = list(
                Piece.objects.order_by('-id').values_list('id', flat=True)[:10]
            )
            start_piece = recent_piece_ids[-1]
            end_piece = recent_piece_ids[0]
        elif end_piece is None:
            end_piece = highest_piece_id

        if start_piece > end_piece:
            raise CommandError('--start must be less than or equal to --end.')

        searcher = SimilaritySearcher(
            start_piece=start_piece,
            end_piece=end_piece + 1,
            min_threshold=min_threshold,
            segment_type=segment_type,
        )
        searcher.run_pieces()
