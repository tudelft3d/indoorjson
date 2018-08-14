

import os
import sys
import json
import jsonschema


# fin = open('/Users/hugo/temp/z.json')
fin = open('../../data/FJK-Haus_IndoorGML_withEXR-corrected_1_0_3.json')

def main():
    try:
        j = json.loads(fin.read(), object_pairs_hook=dict_raise_on_duplicates)
    except ValueError as Argument:
        print ("ERROR:   ", Argument)
        isValid = False
        print ("bye bye")
        sys.exit()

    #-- make sure it's a CityJSON file
    if (j["type"] != "IndoorJSON"):
        print ("ERROR:   not a IndoorJSON file")
        isValid = False
        sys.exit()

    schema = '../../schema/indoorjson.schema.json'
    js = json.loads(open(schema).read())
    # print (js)

    try:
        jsonschema.validate(j, js)
    except jsonschema.ValidationError as e:
        print ("ERROR:   ", e.message)
        isValid = False
        sys.exit()
    except jsonschema.SchemaError as e:
        print ("ERROR:   ", e)
        isValid = False
        sys.exit()

    print ("VALID!")


def dict_raise_on_duplicates(ordered_pairs):
    d = {}
    for k, v in ordered_pairs:
        if k in d:
           raise ValueError("Invalid CityJSON file, duplicate key for City Object IDs: %r" % (k))
        else:
           d[k] = v
    return d


if __name__ == '__main__':
    main()
