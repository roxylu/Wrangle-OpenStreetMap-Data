#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import re
import codecs
import json

from audit import update_name, is_valid_street_name

OSM_FILE = "shanghai.osm"
CREATED = ["version", "changeset", "timestamp", "user", "uid"]
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def shape_element(element):
    """
    return a dictionary, containing the shaped data for the given element.
    """
    node = {}
    pos = {}

    # all attributes of "node" and "way" should be turned into regular key/value pairs
    if element.tag == "node" or element.tag == "way":
        # node type
        node['type'] = element.tag

        for tag in element.iter(element.tag):
            for key in tag.attrib:
                value = tag.attrib[key]

                # attributes in the CREATED array should be added under a key "created"
                if key in CREATED:
                    node.setdefault('created', {}).update({key: value})
                # attributes for latitude and longitude should be added to a "pos" dict
                # make sure the values inside "pos" array are floats
                elif key in ['lon', 'lat']:
                    pos.update({key: float(value)})
                # turned into regular key/value pairs
                else:
                    node[key] = value

        for ele in element.getchildren():
            # for "tag" specifically
            if ele.tag == "tag":
                for tag in element.iter("tag"):
                    key_name = tag.attrib["k"]

                    # if the second level tag "k" value contains problematic characters, it should be ignored
                    if re.search(problemchars, key_name):
                        pass
                    # if the second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
                    elif key_name.startswith('addr:'):
                        # split first_tag, second_tag by ":", for example addr:street
                        key_names = key_name.split(':')
                        # if there is a second ":", the tag should be ignored
                        if len(key_names) == 2:
                            first_tag, second_tag = key_names
                            value = tag.attrib["v"]
                            if second_tag == 'street' and not is_valid_street_name(value):
                                value = update_name(value)

                            try:
                                node.setdefault('address', {}).update({second_tag: value})
                            except:
                                # Sometimes we have <tag k="address" v="SOMETHING"/>
                                # Here we need to convert the string type to dict for address key
                                node['address'] = {}
                                node.setdefault('address', {}).update({second_tag: value})
                    else:
                        node[key_name] = tag.attrib["v"]

            # for "tag" specifically
            if ele.tag == "nd":
                # refs should be turned into items in "node_refs" list
                node['node_refs'] = []
                for nd in element.iter("nd"):
                    node['node_refs'].append(nd.attrib["ref"])

        # change pos dict into geospacial indexing array
        if 'lon' in pos and 'lat' in pos:
            node['pos'] = [pos['lat'], pos['lon']]

        return node
    else:
        return None


def process_map(file_in, pretty=False):
    """
    1. Parse the map file, and shape each element in it.
    2. Save the data in a file, and could later on
    import the shaped data into MongoDB.
    """
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data


def main():
    data = process_map(OSM_FILE, True)


if __name__ == "__main__":
    main()
