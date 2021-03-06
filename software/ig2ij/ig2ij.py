#-- small script to convert IndoorGML files to IndoorJSON
#-- h.ledoux@tudelft.nl
#-- 2019-10-15


import sys
import os
import json
from lxml import etree


inputfile = "../../data/FJK-Haus_IndoorGML_withEXR-corrected_1_0_3.gml"
# inputfile = "/Users/hugo/Dropbox/data/indoorgml/KU-EngBuilding-IndoorGML-2019-02-12.gml"

ns = {}

def main():
    ifile = os.path.abspath(inputfile)
    print("Parsing", ifile)
    fIn = open(ifile)
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

    j = {}
    j['type'] = 'IndoorJSON'
    j['version'] = '0.2'
    j['PrimalSpaceFeatures'] = {}
    j['SpaceLayers'] = {}
    j['vertices'] = []

    #-- dual space 
    for sl in root.findall(".//{%s}SpaceLayer" % ns['indoorgml']):
        slid, jgraph = read_dual_graph(sl, j)
        j['SpaceLayers'][slid] = jgraph

    #-- primal space: Cells
    read_cells(root, j)

    #-- primal space: Cell Boundaries
    read_cell_boundaries(root, j)

    #-- save and be-bye
    # json_str = json.dumps(j, indent=2)
    json_str = json.dumps(j, separators=(',',':'))
    fout = os.path.abspath('../../data/out.json')
    fo = open(fout, 'w')
    fo.write(json_str)
    print("IndoorJSON file save to", fout)




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
        a = connects[0].get("{%s}href" % ns['xlink'])[1:]
        b = connects[1].get("{%s}href" % ns['xlink'])[1:]
        #-- look for extra vertices that break the straight line segments... 
        ngeom = tr.find("./{%s}geometry" % ns['indoorgml'])
        extrav = []
        if ngeom != None:
            allpos = ngeom.findall(".//{%s}pos" % ns['gml'])
            if (len(allpos) > 2):
                extrav = allpos[1:-1]
        dEdges[tr.get("{%s}id" % ns['gml'])] = (a, b, weight, extrav)
    #-- store all nodes/States
    for v in sl.findall(".//{%s}State" % ns['indoorgml']):
        jv = {}
        jv['type'] = 'Node'
        vid = v.get("{%s}id" % ns['gml'])
        # print ("vid", vid)
        tmp = v.find("./{%s}duality" % ns['indoorgml'])
        jv['duality'] = tmp.get("{%s}href" % ns['xlink'])[1:] 
        tmp = list(map(float, v.find(".//{%s}pos" % ns['gml']).text.split()))
        j['vertices'].append(tmp)
        jv['geometry'] = {'type': 'Point', 'boundaries': len(j['vertices']) - 1}
        lsAdj = []
        jv['edges'] = []
        for each in v.findall("./{%s}connects" % ns['indoorgml']):
            s = each.get("{%s}href" % ns['xlink'])[1:]  
            if (dEdges[s][1] != vid):
                lsAdj.append(dEdges[s][1])
                jt = {}
                jt['type'] = 'Edge'
                jt['destination'] = dEdges[s][1]
                jt['weight'] = dEdges[s][2]
                jt['extra_nodes'] = None
                # vertices for non-straight edges
                if (len(dEdges[s][3]) > 0):
                    # print("add extra v", dEdges[s][3])
                    jt['extra_nodes'] = []
                    for each in dEdges[s][3]:
                        # print (each.text)
                        v = list(map(float, each.text.split()))
                        j['vertices'].append(v)    
                        jt['extra_nodes'].append(len(j['vertices']) - 1)
                jv['edges'].append(jt)
       
        jgraph[vid] = jv
    return slid, jgraph


def read_cells(root, j):
    j['PrimalSpaceFeatures']['CellSpace'] = {}
    for el in root.findall(".//{%s}cellSpaceMember" % ns['indoorgml']):
        cell = el[0]
        jc = {}
        jc['type'] = remove_ns(cell.tag)
        theid = cell.get("{%s}id" % ns['gml'])
        #-- duality
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
        #-- name
        tmp = cell.find("./{%s}name" % ns['gml'])
        if tmp is not None:
            jc['name'] = tmp.text

        #-- partialboundedBy
        tmp = cell.findall("./{%s}partialboundedBy" % ns['indoorgml'])
        if len(tmp) > 0:
            jc['partialboundedBy'] = []
            for each in tmp:
                # print(each.get("{%s}href" % ns['xlink'])[1:])
                jc['partialboundedBy'].append(each.get("{%s}href" % ns['xlink'])[1:])

        
        #-- other properties (coming from extensions)
        basic_properties = ["duality", 
                            "cellSpaceGeometry", 
                            "externalReference", 
                            "name", 
                            "boundedBy", 
                            "partialboundedBy"]
        jc['attributes'] = {}
        for each in cell:
            if (remove_ns(each.tag) not in basic_properties):
                # print(each.tag)
                jc['attributes'][remove_ns(each.tag)] = each.text
        
        # TODO: externalReference
        # tmp = cell.find("./{%s}externalReference" % ns['indoorgml'])
        # if tmp is not None:
            # jc['externalReference'] = tmp.text
        # Solid
        jc['geometry'] = {'type': 'Solid'}

        nsol = cell.find(".//{%s}Solid" % ns['gml'])
        solid = []
        nsh = nsol.find("./{%s}exterior" % ns['gml'])
        shell = []
        for npoly in nsh.findall(".//{%s}Polygon" % ns['gml']):
            nexterior = npoly.find(".//{%s}exterior" % ns['gml'])
            lr = parse_gml_polygon_ring(nexterior, j['vertices'])
            polygon = [lr]
            ninteriors = npoly.findall(".//{%s}interior" % ns['gml'])
            if len(ninteriors) != 0:
                irings = []
                for i in range(len(ninteriors)):
                    polygon.append(parse_gml_polygon_ring(intnodes[i], j['vertices']))
            shell.append(polygon)
        # TODO : INTERIOR SHELLS
        solid.append(shell)
        jc['geometry']['boundaries'] = solid
        j['PrimalSpaceFeatures']['CellSpace'][theid] = jc


def read_cell_boundaries(root, j):
    j['PrimalSpaceFeatures']['CellSpaceBoundaries'] = {}
    for el in root.findall(".//{%s}cellSpaceBoundaryMember" % ns['indoorgml']):
        cell = el[0]
        jc = {}
        jc['type'] = remove_ns(cell.tag)
        # print (remove_ns(cell.tag))
        theid = cell.get("{%s}id" % ns['gml'])
        #-- Polygon3D
        g3d = cell.find(".//{%s}geometry3D" % ns['indoorgml'])
        cs = []
        for poly in g3d.findall(".//{%s}Polygon" % ns['gml']):
            nexterior = poly.find(".//{%s}exterior" % ns['gml'])
            lr = parse_gml_polygon_ring(nexterior, j['vertices'])
            polygon = [lr]
            ninteriors = poly.findall(".//{%s}interior" % ns['gml'])
            if len(ninteriors) != 0:
                irings = []
                for i in range(len(ninteriors)):
                    polygon.append(parse_gml_polygon_ring(intnodes[i], j['vertices']))
            cs.append(polygon)
        if (len(cs) != 0):
            jc['geometry'] = {'type': 'CompositeSurface'}
            jc['geometry']['boundaries'] = cs
            j['PrimalSpaceFeatures']['CellSpaceBoundaries'][theid] = jc


def remove_ns(tag):
    return tag[tag.rfind('}')+1:]


def parse_gml_polygon_ring(n, jvertices):
    allgmlpos = n.findall(".//{%s}pos" % ns['gml'])
    ring = []
    for i in allgmlpos:
        v = list(map(float, i.text.split()))
        jvertices.append(v)    
        ring.append(len(jvertices) - 1)
    return ring    


if __name__ == "__main__":
    main()  