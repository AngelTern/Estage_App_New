import re


def separate_location_and_number(location_full):
    match = re.search(r"(\d+\S*)$", location_full)
    if match:
        number = match.group(1)
        location = location_full[:match.start()].strip()
    else:
        number = '\u200B'
        location = location_full.strip()
    return location, number
