import unittest
from names import NameJoiner


class TestNameJoiner(unittest.TestCase):

    def setUp(self):
        self.countries = ['Argentina', 'Ecuador']
        self.name_joiner = NameJoiner(self.countries[0], self.countries[1])

    def test_initial_values_are_correctly_set(self):
        self.assertTrue(self.name_joiner.first_country in self.countries)
        self.assertTrue(self.name_joiner.second_country in self.countries)
        self.assertNotEqual(self.name_joiner.first_country, self.name_joiner.second_country)

    def test_normalizing_names_with_parenthesis(self):
        name = 'Micronesia (Federated States of)'
        expected = 'Federated States of Micronesia'
        result = self.name_joiner.normalize_name(name)
        self.assertEqual(expected, result)

    def test_returning_same_name_if_no_normalization_required(self):
        expected = self.countries[0]
        result = self.name_joiner.normalize_name(expected)
        self.assertEqual(expected, result)

    def test_normalizing_names_with_commas(self):
        name = 'Bonaire, Sint Eustatius and Saba'
        expected = 'Sint Eustatius and Saba Bonaire'
        result = self.name_joiner.normalize_name(name)
        self.assertEqual(expected, result)

    def test_initial_names_are_normalized(self):
        countries = ['Micronesia (Federated States of)', self.countries[1]]
        name_joiner = NameJoiner(countries[0], countries[1])

        expected = 'Federated States of Micronesia'
        self.assertTrue(expected in [name_joiner.first_country, name_joiner.second_country])

    def test_get_split_index(self):
        country = 'Uzbekistan'
        expected = [0, 3, 5, 8]  # Vowels or 'y' followed by a consonant indexes
        splits = self.name_joiner.get_key_vocal_positions(country)
        self.assertEqual(expected, splits)

    def test_get_split_index_country_with_y(self):
        country = 'Cyprus'
        expected = [1, 4]  # Vowels or 'y' followed by a consonant indexes
        splits = self.name_joiner.get_key_vocal_positions(country)
        self.assertEqual(expected, splits)

    def test_join_names_with_first_multi_word_country(self):
        first_country = 'Kyrgyz Soviet Socialist Republic'
        second_country = 'Kuwait'
        cut_country = " ".join(first_country.split()[:-1])
        expected = cut_country + " " + second_country  # Kyrgyz Soviet Socialist Kuwait

        name = self.name_joiner.join_names(first_country, second_country)
        self.assertEqual(expected, name)

    def test_join_names_with_second_multi_word_country(self):
        first_country = 'Kuwait'
        second_country = 'Kyrgyz Soviet Socialist Republic'
        cut_country = " ".join(second_country.split()[:-1])
        expected = cut_country + " " + first_country  # Kyrgyz Soviet Socialist Kuwait

        name = self.name_joiner.join_names(first_country, second_country)
        self.assertEqual(expected, name)

    def test_join_names_with_single_word_countries(self):
        first_country = 'Cuba'
        second_country = 'Bari'
        posible_mashups = ['Curi', 'Baba']

        name = self.name_joiner.join_names(first_country, second_country)
        self.assertIn(name, posible_mashups)

    def test_get_random_split_index(self):
        country = 'Uzbekistan'
        splits = self.name_joiner.get_key_vocal_positions(country)
        random_index = self.name_joiner.get_split_index(country)
        # returned index is a member of splits + 1
        self.assertIn(random_index, [x + 1 for x in splits])

    def test_get_0_from_split_index(self):
        # Don't know how to fire this with an actual country. Maybe it is not required?
        country = 'Khe'
        random_index = self.name_joiner.get_split_index(country)
        # returned index is a member of splits + 1
        self.assertEqual(random_index, 0)

    def test_return_correct_name_if_country_names_are_equal(self):
        countries = ['Uganda', 'Uganda']
        name_joiner = NameJoiner(countries[0], countries[1])

        expected = 'Uganda 2'
        mashup_name = name_joiner.get_mashup_name()
        self.assertEqual(mashup_name, expected)

    def test_capitalize_mashup_name_if_no_uppercase(self):
        first_country = 'cuba'
        second_country = 'bari'
        name_joiner = NameJoiner(first_country, second_country)

        name = name_joiner.get_mashup_name()
        self.assertEqual(name[0], name[0].upper())

    def test_get_new_names_if_mashup_in_original_names(self):
        # Not sure how to trigger this with actual countries
        first_country = 'Segl'
        second_country = 'Pagl'
        name = NameJoiner(first_country, second_country).get_mashup_name()
        self.assertNotIn(name, [first_country, second_country])
