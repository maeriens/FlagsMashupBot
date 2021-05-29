import re
import random

TOOBIG = -1
TOOSMALL = -2
NOTNEW = -3
EMPTY = -1

countries = [
    'Afghanistan', 'Åland Islands', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola', 'Anguilla',
    'Antarctica','Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan',
    'Bahamas', 'Bahrain',  'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan',
    'Bolivia (Plurinational State of)', 'Bonaire, Sint Eustatius and Saba', 'Bosnia and Herzegovina', 'Botswana',
    'Bouvet Island', 'Brazil', 'British Indian Ocean Territory', 'United States Minor Outlying Islands',
    'Virgin Islands (British)', 'Virgin Islands (U.S.)', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burundi',
    'Cambodia', 'Cameroon', 'Canada', 'Cabo Verde', 'Cayman Islands', 'Central African Republic', 'Chad', 'Chile',
    'China', 'Christmas Island', 'Cocos (Keeling) Islands', 'Colombia', 'Comoros', 'Congo',
    'Congo (Democratic Republic of the)', 'Cook Islands', 'Costa Rica', 'Croatia', 'Cuba', 'Curaçao', 'Cyprus',
    'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador',
    'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Falkland Islands (Malvinas)', 'Faroe Islands', 'Fiji',
    'Finland', 'France', 'French Guiana', 'French Polynesia', 'French Southern Territories', 'Gabon', 'Gambia',
    'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala',
    'Guernsey', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Heard Island and McDonald Islands', 'Holy See',
    'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', "Côte d'Ivoire", 'Iran (Islamic Republic of)',
    'Iraq', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Jamaica', 'Japan',
    'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Kuwait', 'Kyrgyzstan', "Lao People's Democratic Republic",
    'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macao',
    'Macedonia (the former Yugoslav Republic of)', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta',
    'Marshall Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico',
    'Micronesia (Federated States of)',
    'Moldova (Republic of)', 'Monaco', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar',
    'Namibia',
    'Nauru', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue',
    'Norfolk Island',
    "Korea (Democratic People's Republic of)", 'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau',
    'Palestine, State of', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Pitcairn', 'Poland',
    'Portugal',
    'Puerto Rico', 'Qatar', 'Republic of Kosovo', 'Réunion', 'Romania', 'Russian Federation', 'Rwanda',
    'Saint Barthélemy',
    'Saint Helena, Ascension and Tristan da Cunha', 'Saint Kitts and Nevis', 'Saint Lucia',
    'Saint Martin (French part)',
    'Saint Pierre and Miquelon', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe',
    'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Sint Maarten (Dutch part)',
    'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa',
    'South Georgia and the South Sandwich Islands',
    'Korea (Republic of)', 'South Sudan', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Svalbard and Jan Mayen',
    'Swaziland', 'Sweden', 'Switzerland', 'Syrian Arab Republic', 'Taiwan', 'Tajikistan',
    'Tanzania, United Republic of',
    'Thailand', 'Timor-Leste', 'Togo', 'Tokelau', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan',
    'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates',
    'United Kingdom of Great Britain and Northern Ireland', 'United States of America', 'Uruguay', 'Uzbekistan',
    'Vanuatu',
    'Venezuela (Bolivarian Republic of)', 'Viet Nam', 'Wallis and Futuna', 'Western Sahara', 'Yemen', 'Zambia',
    'Zimbabwe'
]


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
        # print(self.first_country, '|', self.second_country)
        if self.first_country == self.second_country:
            return self.first_country + " 2"

        mashup_name = self.join_names(self.first_country, self.second_country)

        # Prevent for example Senegal/Portugal -> Senegal. Swap name order.
        if mashup_name in [self.first_country, self.second_country]:
            mashup_name = self.join_names(self.second_country, self.first_country)

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
        print('splits', splits, country_name)
        if len(splits) == 0:
            print(f"{country_name} omitted as it has no vowels to split")
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
