from django.core.management.base import CommandError
from django.test import SimpleTestCase

from .management.commands.searchDB import Command as SearchDBCommand
from .similarity_ratio import SimilaritySearcher


class SimilaritySearcherTests(SimpleTestCase):
    def test_existing_attributes_remain_mutable(self):
        searcher = SimilaritySearcher()

        searcher.max_to_show = 5

        self.assertEqual(searcher.max_to_show, 5)

    def test_new_attributes_are_rejected(self):
        searcher = SimilaritySearcher()

        with self.assertRaises(AttributeError):
            searcher.new_attribute = 'not allowed'


class SearchDBCommandTests(SimpleTestCase):
    def test_invalid_segment_type_raises_command_error(self):
        command = SearchDBCommand()

        with self.assertRaisesMessage(
            CommandError,
            "Unknown --segment-type 'bogus'. Valid values: dia_rhy, int_dia_diff.",
        ):
            command.handle(segment_type='bogus', start_piece=None, end_piece=None, min_threshold=8000)
