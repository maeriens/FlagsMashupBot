import re
import random

SPLIT_PATTERN = r'[aeiouy][^aeiou]'


def get_min_mashup_length(first: str, last: str):
    if ' ' in first and ' ' in last:
        return min(len(first), len(last)) + 1
    else:
        return max(len(first), len(last)) - 1


def get_starts(country: str):
    # The search is to handle cases like Niue that produce no splits
    if re.search(SPLIT_PATTERN, country) is not None:
        regex_iter = re.finditer(SPLIT_PATTERN, country)
        return [country[0:x.start() + 1] for x in regex_iter]
    else:
        return [country]


def get_ends(country: str):
    # The search is to handle cases like Niue that produce no splits
    if re.search(SPLIT_PATTERN, country) is not None:
        regex_iter = re.finditer(SPLIT_PATTERN, country)
        return [country[x.start() + 1:] for x in regex_iter]
    else:
        return [country]


def normalize_mashup(mashup_to_normalize: str):
    # Do not capitalize these words
    no_cap = ['and', 'of', 'the']
    parsed_list = [x if x in no_cap else x.capitalize() for x in mashup_to_normalize.split(' ')]
    parsed = ' '.join(parsed_list)

    # I think this only happens with "Cocos (Keeling) Islands"
    if '(' in parsed:
        index = parsed.index('(') + 1
        parsed = parsed[:index] + parsed[index].upper() + parsed[index+1:]

    return parsed


def get_mashup_name(first_country: str, last_country: str):
    first = first_country.lower()
    last = last_country.lower()

    if first == last:
        return f'{first_country} 2'

    first_starts = get_starts(first)
    last_ends = get_ends(last)

    min_length = get_min_mashup_length(first, last)

    # Remove anything that is shorter than any of the names. Also remove the original countries if they reappear.
    mixes = [x + y for x in first_starts for y in last_ends if len(x + y) >= min_length and x + y not in [first, last]]

    selected = random.choice(mixes)

    if ' ' in selected:
        return normalize_mashup(selected)

    return selected.capitalize()
