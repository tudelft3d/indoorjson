
=======================
IndoorJSON specifications
=======================


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

An "empty" CityJSON will look like this:

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

CityJSON defines the following 3D geometric primitives, ie all of them are embedded in 3D space (and therefore their vertices have *(x, y, z)* coordinates). 
The indexing mechanism of the format `Wavefront OBJ <https://en.wikipedia.org/wiki/Wavefront_.obj_file>`_ is reused, ie a geometry does not store the locations of its vertices, but points to a vertex in a list (in the CityJSON member object ``"vertices"``).

As is the case in CityGML, only linear and planar primitives are allowed (no curves or parametric surfaces for instance).

A Geometry object is a JSON object for which the type member’s value is one of the following:

#. ``"MultiPoint"``
#. ``"MultiLineString"``
#. ``"MultiSurface"``
#. ``"CompositeSurface"``
#. ``"Solid"``
#. ``"MultiSolid"``
#. ``"CompositeSolid"``


A Geometry object:

  - must have one member with the name ``"lod"``, whose value is a number identifying the level-of-detail (LoD) of the geometry. This can be either an integer (following the CityGML standards), or a number following the `improved LoDs by TU Delft <https://www.citygml.org/ongoingdev/tudelft-lods/>`_
  - must have one member with the name ``"boundaries"``, whose value is a hierarchy of arrays (the depth depends on the Geometry object) with integers. An integer refers to the index in the ``"vertices"`` array of the CityJSON object, and it is 0-based (ie the first element in the array has the index "0", the second one "1").
  - may have one member ``"semantics"``, whose value is a hierarchy of nested arrays (the depth depends on the Geometry object). The value of each entry is a string, and the values allowed are depended on the CityObject (see below).
  - may have one member ``"material"``, whose value is a hierarchy of nested arrays (the depth depends on the Geometry object). The value of each entry is an integer referring to the material used (see below).
  - may have one member ``"texture"``, whose value is a hierarchy of nested arrays (the depth depends on the Geometry object). The value of each entry is explained below.


.. note::

  There is **no** Geometry Object for MultiGeometry. 
  Instead, for the ``"geometry"`` member of a CityObject, the different geometries may be enumerated in the array (all with the same value for the member ``"lod"``).


The coordinates of the vertices
*******************************

A CityJSON must have one member named ``"vertices"``, whose value is an array of coordinates of each vertex of the city model. 
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


Arrays to represent boundaries
******************************

- A ``"MultiPoint"`` has an array with the indices of the vertices; this array can be empty.
- A ``"MultiLineString"`` has an array of arrays, each containing the indices of a LineString
- A ``"MultiSurface"``, or a ``"CompositeSurface"``, has an array containing surfaces, each surface is modelled by an array of array, the first array being the exterior boundary of the surface, and the others the interior boundaries.
- A ``"Solid"`` has an array of shells, the first array being the exterior shell of the solid, and the others the interior shells. Each shell has an array of surfaces, modelled in the exact same way as a MultiSurface/CompositeSurface.
- A ``"MultiSolid"``, or a ``"CompositeSolid"``, has an array containing solids, each solid is modelled as above.

.. note::

  JSON does not allow comments, the comments in the example below (C++ style: ``//-- my comments``) are only to explain the cases, and should be removed

.. code-block:: js

  {
    "type": "MultiPoint",
    "lod": 1,
    "boundaries": [2, 44, 0, 7]
  }



.. code-block:: js

  {
    "type": "MultiSurface",
    "lod": 2,
    "boundaries": [
      [[0, 3, 2, 1]], [[4, 5, 6, 7]], [[0, 1, 5, 4]]
    ]
  }

.. code-block:: js

  {
    "type": "Solid",
    "lod": 2,
    "boundaries": [
      [ [[0, 3, 2, 1, 22]], [[4, 5, 6, 7]], [[0, 1, 5, 4]], [[1, 2, 6, 5]] ], //-- exterior shell
      [ [[240, 243, 124]], [[244, 246, 724]], [[34, 414, 45]], [[111, 246, 5]] ] //-- interior shell
    ]
  }


