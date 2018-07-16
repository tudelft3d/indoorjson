
=======================
IndoorJSON specifications
=======================


.. contents:: :local:


-----------------
IndoorJSON Object
-----------------

A CityJSON object represents one 3D city model of a given area, this model may contain features of different types, as defined in the CityGML data model.

- A CityJSON object is a JSON object.
- A CityJSON object must have the following 4 members: 

  #. one member with the name ``"type"``, whose value must be ``"CityJSON"``;
  #. one member with the name ``"version"``, whose value must be a string with the version (X.Y) of CityJSON used;
  #. one member with the name ``"CityObjects"``. The value of this member is a collection of key-value pairs, where the key is the ID of the object, and the value is one City Object. The ID of a City Object should be unique (within one dataset/file).
  #. one member with the name ``"vertices"``, whose value is an array of coordinates of each vertex of the city model. Their position in this array (0-based) is used as an index to be referenced by the Geometric Objects. The indexing mechanism of the format `Wavefront OBJ <https://en.wikipedia.org/wiki/Wavefront_.obj_file>`_ is basically reused.

- A CityJSON may have one member with the name ``"metadata"``, whose value may contain JSON objects describing the coordinate reference system used, the extent of the dataset, its creator, etc.
- A CityJSON may have one member with the name ``"extensions"``, used if there are Extensions used in the file, see the page :doc:`extensions` for all the details.
- A CityJSON may have one member with the name ``"transform"``, whose value must contain 2 JSON objects describing how to *decompress* the coordinates. Transform is used to reduce the file size only.
- A CityJSON may have one member with name ``"appearance"``, the value may contain JSON objects representing the textures and/or materials of surfaces.
- A CityJSON may have one member with name ``"geometry-templates"``, the value may contain JSON objects representing the templates that can be reused by different City Objects (usually for trees). This is the concept of "implicit geometries" in CityGML.
- A CityJSON may have other members, and their value is not prescribed. Because these are not standard in CityJSON, they might be ignored by parsers.

The minimal valid CityJSON object is thus:

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
    "type": "MultiLineString",
    "lod": 1,
    "boundaries": [
      [2, 3, 5], [77, 55, 212]
    ]  
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

.. code-block:: js

  {
    "type": "CompositeSolid",
    "lod": 3,
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


.. _specs_semantics:


Semantic Surface Object
***********************

A Semantics Surface is a JSON object representing the semantics of a surface, and may also represent other attributes of the surface (eg the slope of the roof or the solar potential).
A Semantic Object:
  
  - must have one member with the name ``"type"``, whose value is one of the allowed value. These depend on the City Object, see below.
  - may have other attributes in the form of a JSON key-value pair, where the value must not be a JSON object (but a string/number/integer/boolean). 

.. code-block:: js

  {
    "type": "RoofSurface",
    "slope": 16.4,
    "solar-potential": 5
  }

----

.. rubric:: Values for Semantics

``"Building"``, ``"BuildingPart"``, and ``"BuildingInstallation"`` can have the following semantics for (LoD0 to LoD3; LoD4 is omitted):


  * ``"RoofSurface"`` 
  * ``"GroundSurface"`` 
  * ``"WallSurface"``
  * ``"ClosureSurface"``
  * ``"OuterCeilingSurface"``
  * ``"OuterFloorSurface"``
  * ``"Window"``
  * ``"Door"``

For ``"WaterBody"``:

  * ``"WaterSurface"``
  * ``"WaterGroundSurface"``
  * ``"WaterClosureSurface"``

For Transportation (``"Road"``, ``"Railway"``, ``"TransportSquare"``):

  * ``"TrafficArea"``
  * ``"AuxiliaryTrafficArea"``

----

Because in one given City Object (say a ``"Building"``) several surfaces can have the same semantics (think of a complex building that has been triangulated, there can be dozens of triangles used to model the same surface), a Semantic Surfaces object has to be declared once, and each of the surfaces used to represent it points to it.
This is achieved by first declaring all the Semantic Surfaces in an array, and then having an array where each surface links to Semantic Surfaces (position in the array).

A Geometry object:

  - may have one member with the name ``"semantics"``, whose values are two keys ``"surfaces"`` and ``"values"``. Both have to be present.
  -  the value of ``"surfaces"`` is an array of Semantic Surface Objects.
  -  the value of ``"values"`` is a hierarchy of arrays (the depth depends on the Geometry object; it is two less than the array ``"boundaries"``) with integers. An integer refers to the index in the ``"surfaces"`` array of the same geometry, and it is 0-based. If one surface has no semantics, a value of ``null`` must be used.

.. code-block:: js

  {
    "type": "MultiSurface",
    "lod": 2,
    "boundaries": [
      [[0, 3, 2, 1]], [[4, 5, 6, 7]], [[0, 1, 5, 4], [[0, 2, 3, 8], [[10, 12, 23, 48]]
    ],
    "semantics": {
      "surfaces" : [
        {
          "type": "RoofSurface",
          "slope": 33.4
        }, 
        {
          "type": "RoofSurface",
          "slope": 66.6
        },
        {
          "type": "GroundSurface"
        }
      ],
      "values": [0, 0, null, 1, 2]
    },
  }

.. note::
   A ``null`` value is used to specify that a given surface has no semantics, but to avoid having arrays filled with ``null``, it is also possible to specify ``null`` for a shell or a whole Solid in a MultiSolid, the ``null`` propagates to the nested arrays.

   .. code-block:: js
     
     {
        "type": "CompositeSolid",
        "lod": 2,
        "boundaries": [
          [ //-- 1st Solid
            [ [[0, 3, 2, 1, 22]], [[4, 5, 6, 7]], [[0, 1, 5, 4]], [[1, 2, 6, 5]] ]
          ],
          [ //-- 2nd Solid
            [ [[666, 667, 668]], [[74, 75, 76]], [[880, 881, 885]], [[111, 122, 226]] ] 
          ]    
        ],
        "semantics": {
          "surfaces" : [
            {      
              "type": "RoofSurface",
            }, 
            {
              "type": "WallSurface",
            }
          ],
          "values": [
            [ //-- 1st Solid
              [0, 1, 1, null]
            ],
            [ //-- 2nd Solid get all null values
              null
            ]
          ]
        }
      }  

