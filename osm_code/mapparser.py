#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET

import pprint


def count_tags(filename):
    """
    Returns a dictionary with the tag name as the key
    and number of times this tag can be encountered in the map as value.
    """
    tags = {}
    with open(filename, 'r') as file:
        for event, elem in ET.iterparse(file, events=("start", )):
            tags[elem.tag] = tags.get(elem.tag, 0) + 1

    return tags


def main():
    tags = count_tags('shanghai.osm')
    pprint.pprint(tags)


if __name__ == "__main__":
    main()
