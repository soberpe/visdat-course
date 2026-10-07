---
title: High-Performance Data Storage with HDF5
---

# High-Performance Data Storage with HDF5

## The Big Data Challenge in Engineering

Test rigs and vehicles produce data quickly. A typical setup records dozens of
channels at a thousand samples per second or more, for hours.

- 60 channels at 1000 Hz for one hour are 216 million values.
- As CSV, that is roughly 2 GB of text.
- Loading it takes minutes, and finding one interesting minute means loading
  everything first.

CSV is a good format for exchanging data, because every program can read it.
It is a poor format for working with large data, and HDF5 is one of the
standard answers to that.

## Introduction to HDF5

HDF5 (Hierarchical Data Format version 5) is a binary file format for large
amounts of scientific data. Three properties make it useful for engineering
measurements.

**It stores binary numbers.** A CSV file stores every number as text, and
reading it means parsing every number from its characters. HDF5 stores the
bytes the way they sit in memory, so reading is mostly copying.

**It can read parts of a file.** With the right layout, you can load one minute
out of three hours without touching the rest of the file.

**It organises data like a file system.** One file can hold many datasets in
groups, for example raw data, cleaned data and results, each with metadata
such as units and calibration dates attached.

HDF5 is supported by Python, MATLAB, C, C++, Julia and many other languages,
on every common operating system, and it is widely used for archiving
measurement data.

## HDF5 with Pandas

Pandas writes and reads HDF5 through the package PyTables, which is installed
with the course requirements as `tables`.

```python
import numpy as np
import pandas as pd

ride = pd.read_csv("data/motorcycle_ride.csv", dtype={"ride_mode": "category"})
```

The examples use the motorcycle ride described on the page
[Sample Datasets](./sample-datasets.md). `ride_mode` is read as a category
right away. The reason is explained in the section on performance below.

### Fixed and Table Format

Pandas offers two layouts inside an HDF5 file.

:::info fixed or table
`format="fixed"` is the default. It writes the DataFrame as a block, and it can
only be read back as a whole.

`format="table"` writes the data as a table of rows. It is slightly slower to
write, but it can be queried with `where` while reading, and new rows can be
appended later. For measurement data you want to slice, this is the format to
use.
:::

### Writing

```python
ride.to_hdf(
    "data/motorcycle_ride.h5",
    key="ride01",                  # name of the dataset inside the file
    mode="w",                      # overwrite the file
    format="table",                # queryable layout
    data_columns=["timestamp", "speed_kmh"],   # columns you can use in where
)
```

### Reading

```python
# Everything
everything = pd.read_hdf("data/motorcycle_ride.h5", key="ride01")
print(len(everything))

# Only one minute, selected while reading
minute = pd.read_hdf("data/motorcycle_ride.h5", key="ride01",
                     where="timestamp >= 60 & timestamp < 120")
print(len(minute))

# Only fast sections, and only two columns
fast = pd.read_hdf("data/motorcycle_ride.h5", key="ride01",
                   where="speed_kmh > 90 & speed_kmh < 200",
                   columns=["timestamp", "speed_kmh"])
print(len(fast))
```

A `where` condition can only use columns listed in `data_columns`, plus the
index. Conditions on other columns raise an error.

## Organising Several Datasets in One File

`HDFStore` opens an HDF5 file like a dictionary. Keys with slashes create
groups, much like folders.

```python
clean = ride[ride["speed_kmh"] <= 250].copy()
clean["coolant_c"] = clean["coolant_c"].ffill(limit=300)

per_gear = clean.groupby("gear")[["speed_kmh", "rpm"]].mean()

with pd.HDFStore("data/motorcycle_project.h5", mode="w") as store:
    store.put("raw/ride01", ride, format="table", data_columns=["timestamp"])
    store.put("processed/ride01", clean, format="table", data_columns=["timestamp"])
    store.put("results/per_gear", per_gear)

with pd.HDFStore("data/motorcycle_project.h5", mode="r") as store:
    for key in store.keys():
        if "/meta/" in key:   # internal nodes that store the categories
            continue
        print(key, store[key].shape)
    summary = store["results/per_gear"]
```

### Metadata

A dataset can carry attributes. Units, the sampling rate and a record of the
processing steps belong next to the data, not in a separate document that gets
lost.

```python
with pd.HDFStore("data/motorcycle_project.h5", mode="a") as store:
    attrs = store.get_storer("processed/ride01").attrs
    attrs.sampling_rate_hz = 100
    attrs.units = {
        "timestamp": "s", "speed_kmh": "km/h", "rpm": "1/min",
        "lean_deg": "deg", "accel_x": "m/s^2", "coolant_c": "degC",
    }
    attrs.processing = [
        "removed speed_kmh above 250 (bus error frames)",
        "coolant_c: forward fill, at most 3 s",
    ]

with pd.HDFStore("data/motorcycle_project.h5", mode="r") as store:
    attrs = store.get_storer("processed/ride01").attrs
    print(attrs.sampling_rate_hz, attrs.units["accel_x"])
```

## Performance

Claims about file formats are easy to make and easy to check. The comparison
below makes three hours of riding out of the nine minute file and measures on
your own machine.

```python
import os
import time

big = pd.concat([ride] * 20, ignore_index=True)   # three hours

big.to_csv("ride_3h.csv", index=False)
big.to_hdf("ride_3h.h5", key="ride", mode="w", format="table")
big.to_hdf("ride_3h_zlib.h5", key="ride", mode="w", format="table", complevel=5)

def measure(label, read, path):
    t0 = time.perf_counter()
    read()
    seconds = time.perf_counter() - t0
    print(f"{label:22s} {os.path.getsize(path) / 1e6:5.0f} MB  {seconds:.2f} s")

measure("CSV", lambda: pd.read_csv("ride_3h.csv"), "ride_3h.csv")
measure("HDF5 table", lambda: pd.read_hdf("ride_3h.h5", "ride"), "ride_3h.h5")
measure("HDF5 table, zlib 5", lambda: pd.read_hdf("ride_3h_zlib.h5", "ride"),
        "ride_3h_zlib.h5")
measure("HDF5, one minute", lambda: pd.read_hdf("ride_3h.h5", "ride",
        where="index < 6000"), "ride_3h.h5")
```

On a typical laptop, the result looks roughly like this:

| Format | Size | Read everything |
|---|---|---|
| CSV | about 60 MB | about 0.6 s |
| HDF5 table | about 100 MB | about 0.2 s |
| HDF5 table, zlib level 5 | about 22 MB | about 0.6 s |
| HDF5, one minute only | | a few hundredths of a second |

Three things are worth noticing.

**Uncompressed HDF5 reads about three times faster than CSV.** Parsing text is
the expensive part of reading a CSV, and HDF5 skips it. With numbers written to
full precision, the CSV gets larger and the advantage grows to a factor of ten
or more.

**Compression is a trade, not a free improvement.** With zlib, the file
shrinks to about a third of the CSV, but decompressing costs about as much
time as parsing the text did. Without compression, the HDF5 file is even larger than
the CSV here, because the logger writes short numbers such as `0.0`, while a
float64 always takes 8 bytes. Choose by what limits you: disk space or reading
time.

**Partial reads are the real advantage.** One minute out of three hours comes
back almost immediately, whatever the size of the file. A CSV has to be read
from the start.

:::warning Text is slow in every format
Read `ride_mode` without `dtype={"ride_mode": "category"}` and run the
comparison again. As a column of Python strings, it takes HDF5 most of its
lead, because strings have to be converted one by one in any format. As a
category, the column is stored as small integer codes.
:::

## Best Practices

### A Structure for Project Files

A clear group structure makes a file understandable years later, by someone
else, without a separate description.

```text
project.h5
├── raw/
│   ├── ride01
│   └── ride02
├── processed/
│   ├── ride01
│   └── ride02
├── results/
│   └── per_gear
└── metadata/
    └── calibration
```

Raw data is written once and never changed. Every processing step writes to a
new place, so you can always return to what was measured.

### Appending Data

Table format can grow. This is useful when a logger delivers data in pieces, or
when a long file is converted in chunks that each fit into memory.

```python
first = ride.iloc[:30000]
second = ride.iloc[30000:]

with pd.HDFStore("data/ride_chunks.h5", mode="w") as store:
    store.append("ride01", first, data_columns=["timestamp"])
    store.append("ride01", second, data_columns=["timestamp"])
    print(store.get_storer("ride01").nrows == len(ride))
```

HDF5 is a robust solution for large engineering datasets. Its strengths are
fast binary reads, partial reads with queries, and a hierarchical structure
with metadata, as long as you know which of them you actually need.
