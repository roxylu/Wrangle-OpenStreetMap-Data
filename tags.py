#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def key_type(element, keys):
    """
    Check the "k" value for each "<tag>"
    and see if there are any potential problems.
    Returns a count of each of four tag categories in a dictionary:
    "lower", for tags that contain only lowercase letters and are valid,
    "lower_colon", for otherwise valid tags with a colon in their names,
    "problemchars", for tags with problematic characters, and
    "other", for other tags that do not fall into the other three categories.
    """
    if element.tag == "tag":
        for tag in element.iter("tag"):
            key_name = tag.attrib["k"]
            if re.search(lower, key_name):
                keys['lower'] += 1
            elif re.search(lower_colon, key_name):
                keys['lower_colon'] += 1
            elif re.search(problemchars, key_name):
                keys['problemchars'] += 1
            else:
                keys['other'] += 1
        
    return keys



def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys



def main():
    keys = process_map('shanghai.osm')
    pprint.pprint(keys)


if __name__ == "__main__":
    main()
