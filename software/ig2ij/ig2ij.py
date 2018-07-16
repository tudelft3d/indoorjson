
import sys
import json
from lxml import etree


inputfile = "/Users/hugo/Dropbox/data/indoorgml/FJK-Haus_IndoorGML_withEXR-corrected_1_0_3.gml"

ns = {}

def main():
    fIn = open(inputfile)
    # try:
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
    print ("File ID:", theid)

    j = {}
    j['type'] = 'IndoorJSON'
    j['version'] = '0.1'
    j['PrimalSpaceFeatures'] = {}
    j['SpaceLayers'] = {}
    j['vertices'] = []


    for sl in root.findall(".//{%s}SpaceLayer" % ns['indoorgml']):
        slid, jgraph = read_dual_graph(sl, j)
        j['SpaceLayers'][slid] = jgraph

    read_cells(root, j)

    #-- save and be-bye
    json_str = json.dumps(j, indent=2)
    # print (json_str)
    fo = open('/Users/hugo/temp/z.json', 'w')
    fo.write(json_str)



    # except:
    #     print ("ERROR: problems while parsing the XML file.")
    #     return 0
    # return 1


def read_dual_graph(sl, j):
    jgraph = {}
    slid = sl.get("{%s}id" % ns['gml'])
    #-- store all Transitions
    dEdges = {}
    for tr in sl.findall(".//{%s}Transition" % ns['indoorgml']):
        connects = tr.findall("./{%s}connects" % ns['indoorgml'])
        weight = tr.find("./{%s}weight" % ns['indoorgml'])
        if weight is not None:
            weight = float(weight.text)
        # print ('weight:', weight)
        a = connects[0].get("{%s}href" % ns['xlink'])[1:]
        b = connects[1].get("{%s}href" % ns['xlink'])[1:]
        dEdges[tr.get("{%s}id" % ns['gml'])] = (a, b, weight)
    #-- store all nodes/States
    for v in sl.findall(".//{%s}State" % ns['indoorgml']):
        jv = {}
        jv['type'] = 'State'
        vid = v.get("{%s}id" % ns['gml'])
        # print ("vid", vid)
        tmp = v.find("./{%s}duality" % ns['indoorgml'])
        jv['duality'] = tmp.get("{%s}href" % ns['xlink'])[1:] 
        tmp = list(map(float, v.find(".//{%s}pos" % ns['gml']).text.split()))
        # print (tmp)
        j['vertices'].append(tmp)
        jv['geometry'] = len(j['vertices']) - 1
        lsAdj = []
        jv['edges'] = []
        for each in v.findall("./{%s}connects" % ns['indoorgml']):
            s = each.get("{%s}href" % ns['xlink'])[1:]  
            if (dEdges[s][1] != vid):
                lsAdj.append(dEdges[s][1])
                jt = {}
                jt['type'] = 'Transition'
                jt['end'] = dEdges[s][1]
                jt['weight'] = dEdges[s][2]
                # TODO : do the vertices for non-straight edges
                jv['edges'].append(jt)
       
        jgraph[vid] = jv
    return slid, jgraph


def read_cells(root, j):
    for cell in root.findall(".//{%s}CellSpace" % ns['indoorgml']):
        jc = {}
        jc['type'] = 'CellSpace'
        id = cell.get("{%s}id" % ns['gml'])
        # duality
        tmp = cell.find("./{%s}duality" % ns['indoorgml'])
        if tmp is not None:
            duality = tmp.get("{%s}href" % ns['xlink'])
            if duality[0] == '#':
                duality = duality[1:]
            jc['duality'] = duality
            # which of the (potentially) different dual graphs?
            if len(j['SpaceLayers']) == 1:
                key, i = list(j['SpaceLayers'].items())[0]
                jc['duality-spacelayer'] = key
            else:
                for key, value in j['SpaceLayers'].items():
                    if duality in value:
                        jc['duality-spacelayer'] = key
                        break
        # name
        tmp = cell.find("./{%s}name" % ns['gml'])
        if tmp is not None:
            jc['name'] = tmp.text
        # TODO: externalReference
        # tmp = cell.find("./{%s}externalReference" % ns['indoorgml'])
        # if tmp is not None:
            # jc['externalReference'] = tmp.text
        solid = cell.find(".//{%s}Solid" % ns['gml'])
        jc['geometry'] = {}
        j['PrimalSpaceFeatures'][id] = jc



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