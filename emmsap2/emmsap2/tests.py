from django.test import SimpleTestCase

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
