
import os
import sys
import json

fin = open('../../data/FJK-Haus_IndoorGML_withEXR-corrected_1_0_3.json')

def main():
    j = json.loads(fin.read())

    print ("IndoorJSON version:", j['version'])
    print ("Number CellSpace:", len(j['PrimalSpaceFeatures']))
    print ("Number dual graphs (SpaceLayers):", len(j['SpaceLayers']))

    #-- are Cell C1 and C8 adjacent? either edge C1->C8 or C8->C1
    c1 = j['PrimalSpaceFeatures']['C1']
    c8 = j['PrimalSpaceFeatures']['C8']
    # find the dual node
    dual_c1 = j['SpaceLayers'][c1['duality-spacelayer']][c1['duality']]
    dual_c8 = j['SpaceLayers'][c8['duality-spacelayer']][c8['duality']]
    bFound = False
    # iterate over the edges to see whether C8 is in C1
    for e in dual_c1['edges']:
        if (e['destination'] == 'C8'):
            bFound = True
            break
    if (bFound == False):
        # iterate over the edges to see whether C1 is in C8
        for e in dual_c8['edges']:
            if (e['destination'] == 'C1'):
                bFound = True
                break
    print ("C1 and C8 adjacent?", bFound)


    #-- what is the dual of Node R10?
    dual_r10 = None
    for graphid in j['SpaceLayers']:
        if ('R10' in j['SpaceLayers'][graphid]):
            dual_r10 = j['SpaceLayers'][graphid]['R10']['duality']
    print ('Dual of R10:', str(dual_r10))


if __name__ == '__main__':
    main()
