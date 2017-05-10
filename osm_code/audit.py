#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import string
import xml.etree.cElementTree as ET
import unicodedata as ud

from utils.translate import make_translation


OSMFILE = "shanghai.osm"
EXPECTED = "路".decode('utf-8')
APP_ID = "YOUR_APP_ID"
SECRET_KEY = "YOUR_SECRET_KEY"


def audit():
    """
    audit the OSMFILE and
    return a list of street names that does not ends with the EXPECTED word
    """

    osm_file = open(OSMFILE, "r")
    invalid_street_names = set([])

    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    value = tag.attrib['v']
                    if not is_valid_street_name(value):
                        invalid_street_names.add(value)
    osm_file.close()
    return invalid_street_names


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def is_valid_street_name(name):
    """
    return True only when the street name ends with the EXPECTED word
    """

    if name.find(EXPECTED) == len(name)-1:
        return True
    return False


def update_name(name):
    """
    1 If string contains chinese characters
        1.1 remove all english characters from string
        1.2 remove anything behind EXPECTED word
        1.3 return result.
    2 Else
        2.1 translate processed english string to chinese
        2.2 remove anything behind EXPECTED word
        2.3 return result
    3 do nothing if the name is empty
    """

    if not name:
        pass

    print "[-]" + name

    if contains_chinese_chars(name):
        # remove all english characters from string
        updated_name = strip_ascii_chars(name)
    else:
        # translate processed english string to chinese
        updated_name = make_translation(name, APP_ID, SECRET_KEY)

    # remove anything behind EXPECTED word
    name = strip_detailed_name(updated_name)
    return name


def contains_chinese_chars(name):
    """
    check if there is any chinese characters
    """

    # remove line breaker to avoid exception
    name = name.strip('\n')

    for n in name:
        try:
            letter_name = ud.name(unicode(n, 'utf-8'))
            if letter_name.startswith('CJK UNIFIED'):
                return True
        except UnicodeDecodeError:
            return True
        except TypeError:
            return True
    return False


def strip_ascii_chars(name):
    """
    remove all the ascii letters, punctuation, digits and whitespaces
    """

    def isAscii(s):
        for c in s:
            if c not in string.ascii_letters and \
               c not in string.punctuation and \
               c not in string.digits and \
               c not in string.whitespace:
                return False
        return True

    char_array = []
    for n in name:
        if not isAscii(n):
            char_array.append(n)

    return "".join(n for n in char_array)


def strip_detailed_name(name):
    """
    remove anything behind EXPECTED word
    """
    if name.find(EXPECTED) > 0:
        return name[0:name.find(EXPECTED)+1]
    return name


def main():
    # parse args for baidu translate api
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-a', dest='app_id',
        help='specify app id for baidu translate api')
    parser.add_argument(
        '-s', dest='secret_key',
        help='specify secret key for baidu translate api')
    args = parser.parse_args()
    if (args.app_id is None) | (args.secret_key is None):
        parser.print_help()
        exit(0)
    else:
        globals()['APP_ID'] = args.app_id
        globals()['SECRET_KEY'] = args.secret_key

    # audit the OSMFILE
    invalid_street_names = audit()

    # fix the invalid street names
    for name in invalid_street_names:
        better_name = update_name(name)
        print "[+]" + better_name


if __name__ == '__main__':
    main()
