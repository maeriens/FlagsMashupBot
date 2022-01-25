import random
import unittest
from names import get_mashup_name, get_ends, get_starts, get_min_mashup_length, normalize_mashup


class TestNameJoiner(unittest.TestCase):

    def setUp(self):
        self.country = 'Argentina'.lower()
        self.country2 = 'Ukraine'.lower()
        self.long_country = 'Papua New Guinea'.lower()
        self.long_country2 = 'New Zealand'.lower()
        self.no_split = 'Niue'.lower()

    def test_get_starts(self):
        starts = get_starts(self.country)
        expected = ['a', 'arge', 'argenti']
        self.assertEqual(starts, expected)

    def test_get_ends(self):
        ends = get_ends(self.country)
        expected = ['rgentina', 'ntina', 'na']
        self.assertEqual(ends, expected)

    def test_return_country_if_no_starts(self):
        starts = get_starts(self.no_split)
        expected = [self.no_split]
        self.assertEqual(starts, expected)

    def test_return_country_if_no_ends(self):
        ends = get_ends(self.no_split)
        expected = [self.no_split]
        self.assertEqual(ends, expected)

    def test_get_min_mashup_length_name_if_one_word_country_or_one_has_spaces(self):
        length = get_min_mashup_length(self.country, self.country2)
        expected = max(len(self.country), len(self.country2)) - 1
        self.assertEqual(length, expected)
        # Inverting order should yield same result
        self.assertEqual(length, expected)

        # Same if one has a space in it
        length = get_min_mashup_length(self.country, self.long_country)
        expected = max(len(self.country), len(self.long_country)) - 1
        self.assertEqual(length, expected)
        # Inverting order should yield same result
        self.assertEqual(length, expected)

    def test_get_min_mashup_length_name_if_both_have_spaces(self):
        length = get_min_mashup_length(self.long_country, self.long_country2)
        minimum = min(len(self.long_country), len(self.long_country2))
        expected = minimum + 1
        self.assertEqual(length, expected)

        # Inverting order should yield same result
        length = get_min_mashup_length(self.long_country2, self.long_country2)
        self.assertEqual(length, expected)

    def test_normalize_single_word_mashup(self):
        normalized = normalize_mashup('ecuadortina')
        expected = 'Ecuadortina'
        self.assertEqual(normalized, expected)

    def test_normalize_multi_word_mashup(self):
        normalized = normalize_mashup('islands faway')
        expected = 'Islands Faway'
        self.assertEqual(normalized, expected)

    def test_normalize_with_parenthesis(self):
        normalized = normalize_mashup('islands (far) faway')
        expected = 'Islands (Far) Faway'
        self.assertEqual(normalized, expected)

    def test_skip_normalizing_articles(self):
        for word in ['the', 'of', 'and']:
            no_normalize = normalize_mashup(word)
            self.assertEqual(no_normalize, word)

        skip_article = normalize_mashup('Islands of the Sun')
        expected = 'Islands of the Sun'
        self.assertEqual(skip_article, expected)

    def test_get_mashup_name_single_countries(self):
        mashup = get_mashup_name(self.country, self.country2)
        mashup_length = get_min_mashup_length(self.country, self.country2)

        self.assertGreaterEqual(len(mashup), mashup_length,
                                f'Mashup length is {len(mashup)}, should be greater or equal than {mashup_length}')

        self.assertEqual(mashup.capitalize(), mashup, 'Mashup should be capitalized')

    def test_get_mashup_name_multi_word_country(self):
        mashup = get_mashup_name(self.country, self.long_country2)
        mashup_length = get_min_mashup_length(self.country, self.long_country2)

        self.assertGreaterEqual(len(mashup), mashup_length,
                                f'Mashup length is {len(mashup)}, should be greater or equal than {mashup_length}')
        normalized = normalize_mashup(mashup)
        self.assertEqual(normalized, mashup, 'Mashup normalization was incorrect')

    def test_return_if_both_countries_are_the_same(self):
        mashup = get_mashup_name(self.country, self.country)
        self.assertEqual(mashup, f'{self.country} 2')
        # Same for multi-word countries

        mashup = get_mashup_name(self.long_country, self.long_country)
        self.assertEqual(mashup, f'{self.long_country} 2')


if __name__ == '__main__':
    unittest.main()
