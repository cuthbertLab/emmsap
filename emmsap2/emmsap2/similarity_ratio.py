from django.core.exceptions import ObjectDoesNotExist

from .models import Piece, Segment, Ratio


class SimilaritySearcher(object):
    def __init__(
        self,
        start_piece: int = 1,
        end_piece: int = 4000,
        min_threshold: int = 8000,
        max_to_show: int = 2,
        *,
        segment_type: str = 'dia_rhy',
        max_threshold: int = 10001,
        ignore_known_skips: bool = True,
    ):
        self.start_piece = start_piece
        self.end_piece = end_piece
        self.min_threshold = min_threshold
        self.max_threshold = max_threshold
        # start at 3898 when going to dia_rhy again...
        self.segment_type = 'dia_rhy'
        # start at 3896 when going to int_dia_diff again...
        # self.segment_type = 'int_dia_diff'
        self.max_to_show = max_to_show
        # 0 or 300 after skipping one, the odds of a good match goes down.
        self.skipped_match_penalty = 0
        self.ignore_known_skips = ignore_known_skips

        # look out for M2, m2 that are the same rhythm and adjust down
        self.anti_noodle_protection = True

        self.tenor_threshold_add = 1900
        self.tenor_part_number = 2
        self.tenor_other_part_number = 2
        self.print_output = True
        self.fragments_only = False


    def run_pieces(self, start_piece=None, end_piece=None):
        '''
        The main algorithm to search for pieces to match

        min_threshold, max_threshold, and tenor_threshold_add are numbers from
        0 to 10,000+ which scale to 0 - 1 (by dividing by 10000) to find similarity.

        Because of their rhythmic similarity, tenors match far too often,
        so a crude metric is used to identify tenors and raise the min_threshold
        for those matches: basically, parts 2+ (=3rd part
        and beyond) are considered tenors. Not very good, but the best so far.
        '''
        if start_piece is None:
            start_piece = self.start_piece
        if end_piece is None:
            end_piece = self.end_piece

        for piece_id in range(start_piece, end_piece):
            self.run_one_piece(piece_id)
        print('Done.')

    def run_one_piece(self, piece_id):
        skipped_pieces = []
        p: Piece
        try:
            p = Piece.objects.get(id=piece_id)
        except ObjectDoesNotExist:
            print(f'Piece {piece_id} does not exist.  Skipping')
            return
            
        if self.fragments_only is True and p.frag is not True:
            return

        print('Running piece %d (%s)' % (piece_id, p.filename))
        skips = p.skip_piece_ids() if self.ignore_known_skips else set()
        ratios = Ratio.objects.select_related('segment1', 'segment2').filter(
            encoding_type=self.segment_type,
            segment1__piece_id=piece_id,
            ratio__gte=self.min_threshold,
            ratio__lte=self.max_threshold
        ).exclude(segment2__piece_id__in=skips).order_by('-ratio')
        total_shown = 0
        
        ratio_obj: Ratio
        for ratio_obj in ratios:
            return_code = self.check_one_match(ratio_obj, total_shown, skipped_pieces)

            if return_code is not None:
                total_shown = return_code

    def check_one_match(self, ratio_obj: Ratio, total_shown, skipped_pieces):
        matches, adjusted_ratio = self.check_for_show(ratio_obj, skipped_pieces)
        if matches is False:
            return
        total_shown += 1
        s1 = ratio_obj.segment1
        s2 = ratio_obj.segment2
        showInfo = 'part %2d, m. %3d; (%4d) %30s, part %2d, m. %3d (ratio %5d adjusted to %5d)' % (
            s1.part_id,
            s1.measure_start,
            s2.piece.id,
            s2.piece.filename,
            s2.part_id,
            s2.measure_start,
            ratio_obj.ratio,
            adjusted_ratio
        )

        if total_shown > self.max_to_show:
            print('   Not showing (too many matches): ' + showInfo)
            return total_shown

        print('Showing ' + showInfo)
        try:
            ratio_obj.stream().show()
        except Exception as e:
            print(f'ratio_obj {ratio_obj.id} failed to show')
            raise e
        return total_shown

    def check_for_show(self, ratio_obj: Ratio, skipped_pieces=None):
        if skipped_pieces is None:
            skipped_pieces = []
        if ratio_obj.ratio >= self.max_threshold:
            return (False, 'max_threshold')
        if (ratio_obj.segment1.part_id >= self.tenor_part_number or
                ratio_obj.segment2.part_id >= self.tenor_other_part_number):
            # tenor
            if ratio_obj.ratio - self.tenor_threshold_add < self.min_threshold:
                return(False, 'TenorBelowThreshold')

        total_penalty = 0
        if self.anti_noodle_protection:
            total_penalty = self.run_anti_noodle_protection(ratio_obj.ratio, ratio_obj.segment1)

        total_penalty += len(skipped_pieces) * self.skipped_match_penalty
        if ratio_obj.ratio - total_penalty < self.min_threshold:
            print('   below threshold for (%d) %s: ratio %d (adjusted to %d)' %
                  (ratio_obj.segment2.piece.id, ratio_obj.segment2.piece.filename,
                   ratio_obj.ratio, ratio_obj.ratio - total_penalty))
            skipped_pieces.append(ratio_obj.segment2.piece_id)
            return(False, 'TooCommonPenaltyThreshold')

        return (True, ratio_obj.ratio - total_penalty)

    def run_anti_noodle_protection(self, ratio: int, seg: Segment):
        '''
        If anti_noodle_protection, adjust the difference between the ratio and
        10000 by adding in the percentage of noodles -- that is, ascending or
        descending seconds (or unisons) with the same rhythm.  Quick and dirty.
        '''
        ratio_off_100 = 10000 - ratio
        segment_data = seg.segment_data
        segment_length = len(segment_data)
        num_noodles = 0
        for i in range(segment_length - 1):
            this_n = segment_data[i]
            next_n = segment_data[i + 1]
            if self.segment_type == 'dia_rhy':
                # noinspection SpellCheckingInspection
                if this_n in 'ABCDEFG':
                    ascii_diff = abs(ord(this_n) - ord(next_n))
                    if ascii_diff < 2:
                        num_noodles += 1
            elif self.segment_type == 'int_rhy':
                # 41+32 = 73 -- basis.
                this_ord = ord(this_n)
                if 75 >= this_ord >= 71:
                    num_noodles += 1
            elif self.segment_type == 'int_dia_diff':
                # 41+32 = 73 -- basis.
                this_ord = ord(this_n)
                # unison or diatonic second up or down.
                if 74 >= this_ord >= 72:
                    num_noodles += 1
            else:
                print('run_anti_noodle_protection: Unknown segment type ' + self.segment_type)

        noodle_fraction = num_noodles / segment_length
        total_penalty = int(ratio_off_100 * noodle_fraction)
        # print('           Noodle Penalty: ', total_penalty, 'num_noodles', num_noodles)
        return total_penalty

