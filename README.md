# Import Tiff File
This plugin allows to import 3D tiff file by splitting them into equal or smaller 2D image. Two modes are availabe: sliding window, random sampling.

```
.
├── scan_01.tiff
├── scan_02.tiff
└── scan_03.tiff
```

### Settings config

```json
    {
        "axis": [0],
        "size": [256,256],
        "mode": "sliding_window",
        "overlap" : 10,
        "n_sample" : 100,
        "skip" : 2
    }
```

Configuration options:
* `axis`: which axis is flattened
* `size`: size of the image
* `mode`: mode to use, either "sliding_window" or "random"
* `overlap`: in sliding window, overlapping pixel between each window
* `n_sample`: in random sampling, number of sample to generate 