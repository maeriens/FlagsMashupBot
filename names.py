import random
import re
import sys

DEBUG = False
SPLIT_PATTERN = r'[aeiouy][^aeiou]'


def get_min_mashup_length(first: str, last: str):
    if ' ' in first and ' ' in last:
        return min(len(first), len(last)) + 1
    else:
        return max(len(first), len(last)) - 1


def get_starts(country: str):
    # Handle cases like Niue that produce no splits
    if re.search(SPLIT_PATTERN, country) is not None:
        regex_iter = re.finditer(SPLIT_PATTERN, country)
        return [country[0:x.start() + 1] for x in regex_iter]
    else:
        return [country]


def get_ends(country: str):
    # Handle cases like Niue that produce no splits
    if re.search(SPLIT_PATTERN, country) is not None:
        regex_iter = re.finditer(SPLIT_PATTERN, country)
        return [country[x.start() + 1:] for x in regex_iter]
    else:
        return [country]


def normalize_mashup(mashup_to_normalize: str):
    # Remove parenthesis, like the case of "Cocos (Keeling) islands"
    local_mashup = mashup_to_normalize.replace('(', '').replace(')', '')
    # Do not capitalize these words
    no_cap = ['and', 'of', 'the']
    parsed_list = [word if word in no_cap else word.capitalize() for word in local_mashup.split(' ')]
    parsed = ' '.join(parsed_list)
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

    # Only set when running the script manually
    if DEBUG:
        print(f"Start options are: {', '.join(first_starts)}")
        print(f"End options are: {', '.join(last_ends)}\n")
        print(f"Combinations are: {', '. join(mixes)}")

    selected = random.choice(mixes)

    if ' ' in selected:
        return normalize_mashup(selected)

    return selected.capitalize()


if __name__ == '__main__':
    try:
        first_option, last_option = sys.argv[1], sys.argv[2]
        if first_option is None or last_option is None:
            raise ValueError

        print(f"Using {first_option} and {last_option}")
        DEBUG = True
        print(get_mashup_name(first_option, last_option))
    except ValueError:
        print('Two extra arguments are required. If it is a multi word country, surround it with quotation marks')
        exit(1)
    except IndexError:
        print(f'Two extra arguments are required, {len(sys.argv) - 1} provided.')
        exit(1)
