
# IndoorJSON


<img src="specs/figs/logo.svg" width="300">

IndoorJSON is a format for encoding the [IndoorGML](http://indoorgml.net) data model using [JavaScript Object Notation (JSON)](http://json.org).

> Warning: everything here is work-in-progress, and will surely change as we test it with different parsers and software.


```json
  {
    "type": "IndoorJSON",
    "version": "0.1",
    "PrimalSpaceFeatures": {
      "CellSpace": {
        "Cell01": {
          "type": "CellSpace",
          "duality": "N1",
          "duality-spacelayer": "mydualgraph",
          "geometry": {
            "type": "Solid",
            "boundaries": [...]
          }
        },
        "Cell87": {...}
      },
      "CellSpaceBoundaries": {...}
    },
    "SpaceLayers": {
      "mydualgraph": {
        "N1": {
          "type": "Node",
          "duality": "Cell01",
          ...
        },
        ...
      },
    },
    "vertices": [
      [1.1, 2.3, 56.0],
      [34.7, 2.3, 6.9],
      ...
      [99.3, 22.3, 24.2]
    ]
  }
```


