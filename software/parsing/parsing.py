
import os
import sys
import json

fin = open('../../data/FJK-Haus_IndoorGML_withEXR-corrected_1_0_3.json')

def main():
    j = json.loads(fin.read())

    print ("IndoorJSON version:", j['version'])
    print ("Number CellSpace:", len(j['PrimalSpaceFeatures']))
    print ("Number dual graphs (SpaceLayers):", len(j['SpaceLayers']))

    #-- are Cell C1 and C8 adjacent? [either edge C1->C8 or C8->C1]
    print ("C1 and C8 adjacent?", are_cells_adjacent('C1', 'C8', j))
    #-- are Cell C1 and C8 adjacent? 
    print ("C1 and C3 adjacent?", are_cells_adjacent('C1', 'C3', j))
    #-- are Cell C1 and C9 adjacent? 
    print ("C1 and C9 adjacent?", are_cells_adjacent('C1', 'C9', j))


    #-- what is the dual of Node R10?
    dual_r10 = None
    for graphid in j['SpaceLayers']:
        if ('R10' in j['SpaceLayers'][graphid]):
            dual_r10 = j['SpaceLayers'][graphid]['R10']['duality']
    print ('Dual of R10:', str(dual_r10))


def are_cells_adjacent(a, b, j):
    if a not in j['PrimalSpaceFeatures']:
        return False
    if b not in j['PrimalSpaceFeatures']:
        return False
    ca = j['PrimalSpaceFeatures'][a]
    cb = j['PrimalSpaceFeatures'][b]
    # find the dual node
    dual_ca = j['SpaceLayers'][ca['duality-spacelayer']][ca['duality']]
    dual_cb = j['SpaceLayers'][cb['duality-spacelayer']][cb['duality']]
    bFound = False
    # iterate over the edges to see whether b is in a
    for e in dual_ca['edges']:
        if (e['destination'] == cb['duality']):
            bFound = True
            break
    if (bFound == False):
        # iterate over the edges to see whether a is in b
        for e in dual_cb['edges']:
            if (e['destination'] == ca['duality']):
                bFound = True
                break
    return bFound


if __name__ == '__main__':
    main()
