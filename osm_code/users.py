#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint

OSM_FILE = "shanghai.osm"


def process_map(filename):
    """
    return a set of unique user IDs ("uid")
    who have contributed to the map in this particular area.
    """
    users = set()
    for _, element in ET.iterparse(filename):
        for node in element.iter(element.tag):
            try:
                users.add(node.attrib['uid'])
            except:
                pass
    return users


def main():
    users = process_map(OSM_FILE)
    pprint.pprint(len(users))


if __name__ == "__main__":
    main()
