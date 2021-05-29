import re
import random


class NameJoiner:
    """
    NameJoiner class. Receives two country names and mixes them into a new one.
    Note that the parameter names are based on the order they are received, not the output, as
    they are randomized before being assigned internally. So the received first_country could be the
    second part of the mashup name.

    :param first_country: the first country name
    :param second_country: the second country name
    """
    def __init__(self, first_country, second_country):
        words = [first_country, second_country]
        random.shuffle(words)
        self.first_country = self.normalize_name(words[0])
        self.second_country = self.normalize_name(words[1])

    def get_key_vocal_positions(self, country_name):
        """
        Returns a List with the index of vowels/groups of vowels
        :param country_name: the string to split
        """
        regex_iter = re.finditer(r'[aeiouy][^aeiou]', country_name.lower())
        positions = [i.start() for i in regex_iter]
        return positions

    def get_mashup_name(self):
        """
        This function is in charge of getting the mashup name and capitalizing it if needed.
        If the names are equal, it adds returns the first name with a 2
        :return: the mashup name
        """
        if self.first_country == self.second_country:
            return self.first_country + " 2"

        mashup_name = self.join_names(self.first_country, self.second_country)

        # Attempt to prevent e.g. Senegal/Portugal -> Senegal. Swap name order.
        if mashup_name in [self.first_country, self.second_country]:
            mashup_name = self.join_names(self.second_country, self.first_country)

        # If not possible somehow, return first country + last split of the second country
        if mashup_name in [self.first_country, self.second_country]:
            mashup_name = self.first_country + \
                          self.second_country[self.get_key_vocal_positions(self.second_country)[-1] + 1]

        # Fix if the first letter is not uppercase
        if mashup_name[0] == mashup_name[0].lower():
            mashup_name = mashup_name[0].upper() + mashup_name[1:]

        return mashup_name

    def join_names(self, first_name, second_name):
        """
        This function joins the two given names
        If the first one has more than one word, it removes the last one and appends the last of the second one
        This is reversed if it happens with the second one (but not the first)

        :param first_name: The first country name to mashup
        :param second_name: The second country name to mashup
        :return: The mashed up name
        """
        if len(first_name.split()) > 1:
            return " ".join(first_name.split()[:-1]) + " " + second_name.split()[-1]
        elif len(second_name.split()) > 1:
            return " ".join(second_name.split()[:-1]) + " " + first_name.split()[-1]
        else:
            first_split = self.get_split_index(first_name)
            second_split = self.get_split_index(second_name)
            return first_name[:first_split] + second_name[second_split:].lower()

    def get_split_index(self, country_name: str) -> int:
        """
        Choose a vowel (or 'y') that is not followed by another vowel index
        from the given country and return the following index to split
        :param country_name: the country to get split position
        :return: the position to split the country
        """
        splits = self.get_key_vocal_positions(country_name)
        if len(splits) == 0:
            print(f"{country_name} omitted as it has no vowel/y + consonant combo to split")
            return 0

        # Adding one prevents not using the name if it starts with a vowel and index is 0
        return random.choice(splits) + 1

    def normalize_name(self, country_name: str) -> str:
        """
        This function swaps the content of the name if it has anything between brackets
        or has text after a comma and returns it
        :param country_name: the name to analyze
        :return: the normalized country name
        """
        if '(' in country_name:
            first_parenthesis = re.findall(r"(.*)\s\((.*?)\)", country_name)[0]

            return first_parenthesis[1] + ' ' + first_parenthesis[0]

        if "," in country_name:
            temp_name = country_name.split(", ")
            return temp_name[1] + " " + temp_name[0]

        return country_name
