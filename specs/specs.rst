
==============================
IndoorJSON specifications v0.1
==============================


.. image:: logo2.svg
   :width: 300px



.. contents:: :local:


-----------------
IndoorJSON Object
-----------------

A IndoorJSON object represents one indoor model of a given building.

- A IndoorJSON object is a JSON object.
- A IndoorJSON object must have the following 4 members: 

  #. one member with the name ``"type"``, whose value must be ``"IndoorJSON"``;
  #. one member with the name ``"version"``, whose value must be a string with the version (X.Y) of IndoorJSON used;
  #. one member with the name ``"PrimalSpaceFeatures"``. The value of this member is a collection of key-value pairs, where the key is the ID of the CellSpace, and the value is one CellSpace. The ID of a Cell Space should be unique (within one dataset/file).
  #. one member with the name ``"SpaceLayers"``. This is used to represent each of the dual graphs. The value of this member is a collection of key-value pairs, where the key is the ID of a dual graph, and the value is a collection of key-value pairs in which each nodes/States is represented. The ID of a Cell Space should be unique (within one dataset/file).
  #. one member with the name ``"vertices"``, whose value is an array of coordinates of each vertex of the city model. Their position in this array (0-based) is used as an index to be referenced by the Geometric Objects. The indexing mechanism of the format `Wavefront OBJ <https://en.wikipedia.org/wiki/Wavefront_.obj_file>`_ is basically reused.

- A IndoorJSON may have one member with the name ``"metadata"``, whose value may contain JSON objects describing the coordinate reference system used, the extent of the dataset, its creator, etc.

The minimal valid IndoorJSON object is thus:

.. code-block:: js

  {
    "type": "IndoorJSON",
    "version": "0.1",
    "PrimalSpaceFeatures": {},
    "SpaceLayers": {},
    "InterLayerConnections": {},
    "vertices": []
  }

An "empty" IndoorJSON will look like this:

.. code-block:: js

  {
    "type": "IndoorJSON",
    "version": "0.1",
    "metadata": {},
    "PrimalSpaceFeatures": {},
    "SpaceLayers": {},
    "InterLayerConnections": {},
    "vertices": []
  }

.. note::
  While the order of the member values of a IndoorJSON should preferably be as above, not all JSON generators allow one to do this, thus the order is not prescribed.


----------------
Geometry Objects
----------------

IndoorJSON defines the following geometric primitives. 

The indexing mechanism of the format `Wavefront OBJ <https://en.wikipedia.org/wiki/Wavefront_.obj_file>`_ is reused, ie a geometry does not store the locations of its vertices, but points to a vertex in a list (in the IndoorJSON member object ``"vertices"``).

Only linear and planar primitives are allowed (no curves or parametric surfaces for instance).

A Geometry object is a JSON object for which the type member’s value is one of the following:

#. ``"Point"``
#. ``"CompositeSurface"``
#. ``"Solid"``
#. ``"CompositeSolid"``


A Geometry object:

- must have one member with the name ``"type"``, whose value is one of the strings above 
- must have one member with the name ``"boundaries"``, whose value is either a single integer for a ``"Point"``, or a hierarchy of arrays (the depth depends on the Geometry object) with integers. The integers refer to the index in the ``"vertices"`` array of the IndoorJSON object, and it is 0-based (ie the first element in the array has the index "0", the second one "1").



The coordinates of the vertices
*******************************

A IndoorJSON must have one member named ``"vertices"``, whose value is an array of coordinates of each vertex of the city model. 
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

- A ``"Point"`` has one integer value (index of the vertex).
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
