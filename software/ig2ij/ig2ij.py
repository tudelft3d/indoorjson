
import sys
import json
from lxml import etree


inputfile = "/Users/hugo/Dropbox/data/indoorgml/FJK-Haus_IndoorGML_withEXR-corrected_1_0_3.gml"

ns = {}

def main():
    fIn = open(inputfile)
    try:
        parser = etree.XMLParser(ns_clean=True)
        tree = etree.parse(fIn, parser)
        root = tree.getroot()
        for key in root.nsmap.keys():
            if root.nsmap[key].find('www.opengis.net/gml') != -1:
                ns['gml'] = "%s" % root.nsmap[key]
            if root.nsmap[key].find('http://www.opengis.net/indoorgml/1.0/core') != -1:
                ns['indoorgml'] = "%s" % root.nsmap[key]
            if root.nsmap[key].find('www.w3.org/1999/xlink') != -1:
                ns['xlink'] = "%s" % root.nsmap[key]                

        theid = root.get("{%s}id" % ns['gml'])
        print (theid)

        read_cells(root)

    except:
        print ("ERROR: problems while parsing the XML file.")
        return 0
    return 1


def read_cells(root):
    for cell in root.findall(".//{%s}CellSpace" % ns['indoorgml']):
        # print (cell)
        id = cell.get("{%s}id" % ns['gml'])
        print (id)
        
        tmp = cell.find("./{%s}duality" % ns['indoorgml'])
        duality = tmp.get("{%s}href" % ns['xlink'])
        if duality[0] == '#':
            duality = duality[1:]
        print (duality)

        solid = cell.find(".//{%s}Solid" % ns['gml'])
        print (solid)



# def convert(fIn):
#   #-- skip the header
#   l = fIn.next()
#   while (len(l) == 0) or (l[0] == '#') or (l[:3] == 'OFF'):
#     l = fIn.next()
#   numVertices = int(l.split()[0])
#   numFaces    = int(l.split()[1])
#   lstVertices = []
#   for i in range(numVertices):
#     lstVertices.append(map(float, fIn.next().split()))
#   lstFaces = []
#   for i in range(numFaces):
#     lstFaces.append(map(int, fIn.next().split()[1:]))
#   cm = {}
#   cm["type"] = "CityJSON"
#   cm["version"] = "0.6"
#   cm["CityObjects"] = {}
#   cm["vertices"] = []
#   for v in lstVertices:
#     cm["vertices"].append(v)
#   g = {'type': 'Solid'}
#   shell = []
#   for f in lstFaces:
#     shell.append([f])
#   g['boundaries'] = [shell]
#   g['lod'] = 1
#   o = {'type': 'GenericCityObject'}
#   o['geometry'] = [g]
#   cm["CityObjects"]["id-1"] = o
#   return cm


if __name__ == "__main__":
    main()  