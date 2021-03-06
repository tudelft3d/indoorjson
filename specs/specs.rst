
==============================
IndoorJSON specifications v0.2
==============================


.. image:: figs/logo.svg
   :width: 300px


.. contents:: :local:


-----------------
IndoorJSON Object
-----------------

An IndoorJSON object represents one indoor model of a given building.

- An IndoorJSON object is a JSON object.
- An IndoorJSON object must have the following 5 members: 

  #. one member with the name ``"type"``, whose value must be ``"IndoorJSON"``;
  #. one member with the name ``"version"``, whose value must be a string with the version (X.Y) of IndoorJSON used;
  #. one member with the name ``"PrimalSpaceFeatures"``, whose value is a JSON object with 2 properties: ``"CellSpace"`` and ``"CellSpaceBoundaries"``. 
  #. one member with the name ``"SpaceLayers"``. This is used to represent each of the dual graphs (there can be many). The value of this member is a collection of key-value pairs, where the key is the ID of a dual graph, and the value is a collection of key-value pairs in which each node (also called 'States') is represented. The ID of a Cell Space should be unique (within one dataset/file).
  #. one member with the name ``"vertices"``, whose value is an array of coordinates of each vertex of the city model. Their position in this array (0-based) is used as an index to be referenced by the Geometric Objects. The indexing mechanism of the format `Wavefront OBJ <https://en.wikipedia.org/wiki/Wavefront_.obj_file>`_ is basically reused.

- An IndoorJSON may have one member with the name ``"InterLayerConnections"``, whose value is a list of JSON objects describing the relationships between different SpaceLayers.
- An IndoorJSON may have one member with the name ``"metadata"``, whose value may contain JSON objects describing the coordinate reference system used, the extent of the dataset, its creator, etc.

An "empty" IndoorJSON object looks like this:

.. code-block:: js

  {
    "type": "IndoorJSON",
    "version": "0.2",
    "metadata": {},
    "PrimalSpaceFeatures": {},
    "SpaceLayers": {},
    "InterLayerConnections": [],
    "vertices": []
  }

.. note::
  While the order of the member values of an IndoorJSON should preferably be as above, not all JSON generators allow one to do this, thus the order is not prescribed.


-------------------
PrimalSpaceFeatures
-------------------

The primal space may have 2 members: ``"CellSpace"`` and ``"CellSpaceBoundaries"``.

CellSpace
*********

The value of this member is a collection of key-value pairs, where the key is the ID of the CellSpace. 
The ID of a Cell Space should be unique (within one dataset/file).
The CellSpace Objects (which subdivides the space; also called the primal space):

- must have a member named ``"type"``, whose value is the type of the CellSpace. For IndoorGML files core, this value is ``"CellSpace"``, but for Extension (eg the Navigation Extension) this value can be any string (it must be the type of the cell);
- may have a member named ``"name"``, whose value is a string describing the name of CellSpace;
- may have one member named ``"duality"``, whose value is the ID of the Node in the dual graph;
- may have a member named ``"duality-spacelayer"``, whose value is the ID of the dual graph (``"SpaceLayers"``). Both ``"duality-spacelayer"`` and and ``"duality"`` are necessary to identify a node since there can be more than one dual graph.
- may have one member named ``"geometry"``, whose value is Geometry Objects. 
- may have one member named ``"partialboundedBy"``, whose value is array containing the IDs of the CellSpaceBoundaries partially bounding the cell (eg the doors).
- may have one member named ``"attributes"``, whose value is JSON object containing extra properties that are used in IndoorGML Extensions. 
- may have a member name ``"externalReference"``, whose value is a JSON object that must contain 2 members (both stings): ``"informationSystem"`` (URI of the file) and ``"externalObject"`` (ID of the object in the file).

.. code-block:: js

  "PrimalSpaceFeatures": {
    "CellSpace": {
      "Cell01": {
        "type": "CellSpace",
        "name": "myCell_01",
        "duality": "R1",
        "duality-spacelayer": "dualgraph_01",
        "partialboundedBy": ["Boundary0", "Boundary34", "Boundary15"],
        "geometry": {
          "type": "Solid",
          "boundaries": [...]
        }
      },
      "Cell87": {
        "type": "CellSpace",
        "name": "myCell_87",
        "duality": "node234",
        "duality-spacelayer": "IS1",
        "geometry": {
          "type": "Solid",
          "boundaries": [...]
        }
      }
    }
  }

If an Extension is used, then the ``"type"`` will be the semantic value (the meaning) of the cell, for instance for the Navigation Extension:

.. code-block:: js

  "PrimalSpaceFeatures": {
    "CellSpace": {
      "CORRIDOR1": {
        "type": "TransitionSpace",
        "duality": "S1",
        "duality-spacelayer": "base",
        "attributes": {
          "class": "1000",
          "function": "1000",
          "usage": "1000"
        },
        "geometry": {...}
      },
      "DOOR1": {
        "type": "ConnectionSpace",
        "duality": "S120",
        "duality-spacelayer": "base",
        "attributes": {
            "class": "1010",
            "function": "1010",
            "usage": "1010"
        },
        "geometry": {...}
      }
    }
  }


CellSpaceBoundaries
*******************

The value of this member is a collection of key-value pairs, where the key is the ID of the CellSpaceBoundary. 
The ID of a CellSpaceBoundary should be unique (within one dataset/file).
The CellSpaceBoundary Object:

- must have a member named ``"type"``, whose value is the type of the CellSpaceBoundary;
- may have one member named ``"geometry"``, whose value is a Geometry Object (a CompositeSurface for 3D surfaces).

.. code-block:: js

  "PrimalSpaceFeatures": {
    "CellSpaceBoundary": {
      "Boundary0": {
        "type": "ConnectionBoundary",
        "geometry": {
          "type": "CompositeSurface",
          "boundaries": [...]
        }
      },
      "Boundary762": {
        "type": "ConnectionBoundary",
        "geometry": {
          "type": "CompositeSurface",
          "boundaries": [...]
        }
      }
    }
  }




-----------
SpaceLayers
-----------

``"SpaceLayers"`` is one JSON object, it is a collection of key-value pairs, where the key is the ID of a dual graph, and the value is a collection of key-value pairs in which each node (Node Object; also called "States") is represented.

.. code-block:: js

  "SpaceLayers": {
    "dualgraph_01": {
      "R1": {
        "type": "Node",
        "duality": "C1",
        ...
      },
      ...
    },
    "dualgraph_02": {
      "anode_92": {
        "type": "Node",
        "duality": "C1",
        ...
      },
      ...
    }
  }


Node Object (State)
*******************

A Node Object, also called 'State' in IndoorGML, represents one node of the dual graph. It:

- must have a member named ``"type"``, whose value must be ``"Node"``;
- may have a member named ``"name"``, whose value is a string describing its name;
- may have one member named ``"duality"``, whose value is the ID (of type string) of the CellSpace object in the PrimalSpaceFeatures;
- may have one member named ``"geometry"``, whose value is Geometry Objects of type ``"Point"``;
- may have one member named ``"edges"``, whose value is an array of Edge Objects.


Edge Object (Transition)
************************

An Edge Object, also called 'Transition' in IndoorGML, represents implicitly one edge having a given Node Object as its origin. 

An Edge Object:

- must have a member named ``"type"``, whose value must be ``"Edge"``;
- may have a member named ``"name"``, whose value is a string describing its name;
- may have a member named ``"description"``, whose value is a string describing it;
- must have a member named ``"destination"``, whose value the ID of the Node Object of the destination (end node) of the edge. Its origin is the Node Object who is its JSON parent;
- may have one member named ``"weight"``, whose value is the weight of the Edge Object (a float value);
- may have one member named ``"extra_nodes"``. This is used for line segments that are not straight (between the origin and the destination). Only the intermediate Nodes Objects (their IDs) are listed in the array, to save space and avoid repetition.

.. code-block:: js

  {
    "type": "Node",
    "name": "mycell01",
    "duality": "C1",
    "geometry": {
      "type": "Point",
      "boundaries": 874
    },
    "edges": [
      {
        "type": "Edge",
        "destination": "R3",
        "weight": 1.0,
        "extra_nodes": [153, 123]
      }
    ]
  }


---------------------
InterLayerConnections
---------------------

An IndoorJSON object may have one key-value pair named ``"InterLayerConnections"`` whose value is an array of InterLayerConnect Objects.

.. code-block:: js

  "InterLayerConnections": [
    {
      "type": "InterLayerConnection",
      "node1": {
        "spacelayer": "dualgraph_01",
        "id": "R1"
      },
      "node2": {
        "spacelayer": "dualgraph_02",
        "id": "R3"
      },
      "typeOfTopoExpression": "CONTAINS"      
    },
    {
      "type": "InterLayerConnection",
      ...
    }
  ]


An InterLayerConnection Object:

- must have a member named ``"type"``, whose value must be ``"InterLayerConnection"``;
- must have a member named ``"node1"``, whose value is a JSON object having two members: (1) ``"id"`` is the ID of the Node/State (a string) involved in the connection; (2) ``"spacelayer" is the ID of the SpaceLayer;
- must have a member named ``"node2"``, whose value is like that of ``"node1"`` but the other Node/State (a string) involved in the connection;
- may have a member named ``"typeOfTopoExpression"`` that qualifies the topological relationships between the 2 Nodes. Its value is a string that must be either: "CONTAINS", "OVERLAPS", "EQUALS", "WITHIN", "CROSSES", or "INTERSECTS".

.. code-block:: js

  {
    "type": "InterLayerConnection",
    "node1": {
      "spacelayer": "dualgraph_01",
      "id": "R1"
    },
    "node2": {
      "spacelayer": "dualgraph_02",
      "id": "R3"
    },
    "typeOfTopoExpression": "CONTAINS"      
  }


----------------
Geometry Objects
----------------

IndoorJSON defines the following geometric primitives. 

The indexing mechanism of the format `Wavefront OBJ <https://en.wikipedia.org/wiki/Wavefront_.obj_file>`_ is reused, ie a geometry does not store the locations of its vertices, but points to a vertex in a list (in the IndoorJSON member object ``"vertices"``).

Only linear and planar primitives are allowed (no curves or parametric surfaces for instance).

A Geometry object is a JSON object for which the type member’s value is one of the following:

#. ``"Point"``
#. ``"LineString"``
#. ``"CompositeSurface"``
#. ``"Solid"``
#. ``"CompositeSolid"``


A Geometry object:

- must have one member with the name ``"type"``, whose value is one of the strings above 
- must have one member with the name ``"boundaries"``, whose value is either a single integer for a ``"Point"``, or a hierarchy of arrays (the depth depends on the Geometry object) with integers. The integers refer to the index in the ``"vertices"`` array of the IndoorJSON object, and it is 0-based (ie the first element in the array has the index "0", the second one "1").



The coordinates of the vertices
*******************************

An IndoorJSON must have one member named ``"vertices"``, whose value is an array of coordinates of each vertex of the city model. 
Their position in this array (0-based) is used to represent the Geometric Objects.

- one vertex must be an array with exactly 3 values, representing the *(x,y,z)* location of the vertex.
- the array of vertices may be empty.
- vertices may be repeated


.. code-block:: js

  "vertices": [
    [0.0, 0.0, 0.0],
    [1.0, 0.0, 0.0],
    [0.0, 0.0, 0.0],
    ...
    [1.0, 0.0, 0.0],
    [8523.134, 487625.134, 2.03]
  ]


Representations of boundaries
*****************************

- A ``"Point"`` has one integer value (index of the node).
- A ``"LineString"``, has an array containing the nodes ordered from origin to destination.
- A ``"CompositeSurface"``, has an array containing surfaces, each surface is modelled by an array of array, the first array being the exterior boundary of the surface, and the others the interior boundaries.
- A ``"Solid"`` has an array of shells, the first array being the exterior shell of the solid, and the others the interior shells. Each shell has an array of surfaces, modelled in the exact same way as a MultiSurface/CompositeSurface.
- A ``"CompositeSolid"``, has an array containing solids, each solid is modelled as above.

.. note::

  JSON does not allow comments, the comments in the example below (C++ style: ``//-- my comments``) are only to explain the cases, and should be removed

.. code-block:: js

  {
    "type": "Point",
    "boundaries": 666
  }

.. code-block:: js

  {
    "type": "LineString",
    "boundaries": [33, 232, 0, 72]
  }

.. code-block:: js

  {
    "type": "CompositeSurface",
    "boundaries": [
      [[0, 3, 2, 1]], [[4, 5, 6, 7]], [[0, 1, 5, 4]]
    ]
  }

.. code-block:: js

  {
    "type": "Solid",
    "boundaries": [
      [ [[0, 3, 2, 1, 22]], [[4, 5, 6, 7]], [[0, 1, 5, 4]], [[1, 2, 6, 5]] ], //-- exterior shell
      [ [[240, 243, 124]], [[244, 246, 724]], [[34, 414, 45]], [[111, 246, 5]] ] //-- interior shell
    ]
  }

.. code-block:: js

  {
    "type": "CompositeSolid",
    "boundaries": [
      [ //-- 1st Solid
        [ [[0, 3, 2, 1, 22]], [[4, 5, 6, 7]], [[0, 1, 5, 4]], [[1, 2, 6, 5]] ],
        [ [[240, 243, 124]], [[244, 246, 724]], [[34, 414, 45]], [[111, 246, 5]] ]
      ],
      [ //-- 2st Solid
        [ [[666, 667, 668]], [[74, 75, 76]], [[880, 881, 885]], [[111, 122, 226]] ] 
      ]    
    ]
  }
