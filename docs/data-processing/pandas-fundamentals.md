---
title: Pandas Fundamentals
---

# Pandas Fundamentals

## Introduction to Pandas

Pandas was created in 2008 by Wes McKinney to address the lack of flexible,
high-performance data analysis tools in Python. Before pandas, data
manipulation in Python relied on basic lists, dictionaries, and NumPy arrays,
which are powerful for numerical work but cumbersome for tabular, labeled, or
time series data.

**The leap:** Pandas introduced the DataFrame and the Series, bringing
spreadsheet-like, labeled, and relational data handling to Python. This made
tasks like filtering, grouping, joining, and time series analysis much easier
and more expressive, and it is a large part of why Python became a leading
language for data science and engineering.

:::info The dataset used on this page
All examples use `data/motorcycle_ride.csv` from the course repository, the log
of a motorcycle ride of about nine minutes recorded at 100 Hz. The columns are
described on the page [Sample Datasets](./sample-datasets.md). The file
contains deliberate defects, such as gaps, missing values and impossible
readings. Some examples on this page run into them on purpose.
:::

Every code block on this page assumes these two imports:

```python
import numpy as np
import pandas as pd
```

## Core Data Structures

Pandas represents data with two objects. Everything else in the library is an
operation on one of them, and every operation returns one of them again.

### Series: One-Dimensional Data

A **Series** is a one-dimensional labeled array, similar to a column in a
spreadsheet. A single sensor channel is a Series: a sequence of values with an
index and a name.

```python
speed = pd.Series([0.0, 12.4, 31.0, 48.7, 50.2], name="speed_kmh")
print(speed)
print(speed.mean())
```

### DataFrames: Two-Dimensional Data

A **DataFrame** is a two-dimensional table, like an entire spreadsheet. Each
column is a Series, and all columns share the same index. DataFrames are the
structure you will work with most of the time.

```python
sample = pd.DataFrame({
    "timestamp": [0.00, 0.01, 0.02, 0.03, 0.04],
    "speed_kmh": [0.0, 12.4, 31.0, 48.7, 50.2],
    "rpm": [1250, 2400, 3600, 3900, 4000],
    "gear": [0, 1, 2, 3, 3],
})
print(sample)
print(sample.dtypes)
```

## Loading and Inspecting

The first thing to do with a new file is to load it and look at it critically,
before computing anything.

```python
ride = pd.read_csv("data/motorcycle_ride.csv")

print(ride.shape)       # rows and columns
print(ride.head())      # the first five rows
ride.info()             # data types and non-null counts
print(ride.describe())  # min, max, mean and quartiles per column
```

:::tip Read describe() like a reviewer
`describe()` is where impossible values show up first. A minimum or maximum
that is suspiciously round, or physically impossible, is rarely a measurement.
In this file, three columns have exactly such a value. Finding them is one of
the exercises of the data processing lecture.
:::

## Selecting and Filtering

Selection means picking columns, rows, or both. Filtering means keeping the
rows that satisfy a condition.

```python
ride = pd.read_csv("data/motorcycle_ride.csv")

# Column selection: one column gives a Series, a list gives a DataFrame
speed = ride["speed_kmh"]
engine = ride[["timestamp", "rpm", "gear"]]

# Row selection by position
first_second = ride.iloc[:100]          # 100 Hz, so the first second
some_rows = ride.iloc[1000:1010]

# Boolean indexing: keep rows where the condition is True
fast = ride[ride["speed_kmh"] > 90]
braking = ride[ride["brake_front_bar"] > 5]

# Multiple conditions need & and |, and parentheses around each condition
hard_braking_fast = ride[(ride["speed_kmh"] > 80) & (ride["brake_front_bar"] > 8)]

# The query method expresses the same with a string
leaning = ride.query("lean_deg > 20 or lean_deg < -20")
print(len(fast), len(braking), len(hard_braking_fast), len(leaning))
```

## Adding and Changing Columns

New columns are created by assignment. The calculation runs on the whole
column at once, there is no loop.

```python
ride = pd.read_csv("data/motorcycle_ride.csv")

# Unit conversion
ride["speed_ms"] = ride["speed_kmh"] / 3.6
ride["time_min"] = ride["timestamp"] / 60

# A derived physical quantity: in a steady bend, the lateral acceleration
# follows from the lean angle as a_lat = g * tan(lean)
ride["lateral_g"] = np.tan(np.radians(ride["lean_deg"]))

# Renaming and dropping columns return a new DataFrame
renamed = ride.rename(columns={"speed_kmh": "wheel_speed_kmh"})
reduced = ride.drop(columns=["brake_rear_bar", "ride_mode"])
print(reduced.columns.tolist())
```

:::warning Methods return new objects
`rename`, `drop`, `dropna`, `fillna` and most other methods do not change the
DataFrame you call them on. They return a new one. If you do not assign the
result, nothing happened. This is the same reference semantics you know from
Python variables in general.
:::

## Data Cleaning

Cleaning is a sequence of decisions. Each method below encodes an assumption
about the signal, and the right choice depends on what the column measures.

### Handling Missing Values

```python
ride = pd.read_csv("data/motorcycle_ride.csv")

# Where are values missing?
missing = ride.isna().sum()
print(missing[missing > 0])

# Strategy 1: drop every row with a missing value
complete_rows = ride.dropna()

# Strategy 2: hold the last value, for a slow signal, at most 3 s at 100 Hz
coolant_filled = ride["coolant_c"].ffill(limit=300)

# Strategy 3: interpolate, for a smooth signal, at most 0.2 s
lean_filled = ride["lean_deg"].interpolate(limit=20)

# Strategy 4: fill with a fixed value, only if that value is justified
throttle_filled = ride["throttle_pct"].fillna(0)   # assumes a closed throttle
```

Each strategy is right for some signals and wrong for others. Holding the last
value suits the coolant temperature, which changes slowly. It does not suit the
throttle, which can jump within a tenth of a second. Interpolating suits the
lean angle, which changes smoothly, but not across a long gap. Dropping rows is
honest, but it creates holes in the time axis. Whatever you choose, write down
which method you used and why.

### Outlier Detection

The interquartile range (IQR) method flags values far outside the middle half
of the data.

```python
ride = pd.read_csv("data/motorcycle_ride.csv")

def detect_outliers_iqr(data, column):
    """Return the rows outside 1.5 IQR, and the bounds that were used."""
    q1 = data[column].quantile(0.25)
    q3 = data[column].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    outliers = data[(data[column] < lower) | (data[column] > upper)]
    return outliers, lower, upper

outliers, lower, upper = detect_outliers_iqr(ride, "speed_kmh")
print(f"speed_kmh: {len(outliers)} outliers outside [{lower:.1f}, {upper:.1f}]")

outliers, lower, upper = detect_outliers_iqr(ride, "lean_deg")
print(f"lean_deg:  {len(outliers)} outliers outside [{lower:.1f}, {upper:.1f}]")
```

On the wheel speed, the method finds a handful of samples, and they are indeed
faulty. On the lean angle it flags thousands, because riding upright is what is
usual and every bend is unusual. The method finds what is rare. It cannot tell
whether a rare value is a fault or the most interesting part of the
measurement.

```python
# Remove outliers only where you have checked that they are faults
outliers, lower, upper = detect_outliers_iqr(ride, "speed_kmh")
ride_clean = ride.drop(index=outliers.index)
print(f"Removed {len(ride) - len(ride_clean)} samples")
```

:::warning Never delete silently
Mark, count and report the values you remove. A script that drops outliers
automatically will one day drop exactly the event the test was built to
capture.
:::

## Statistics

### Descriptive Statistics

```python
ride = pd.read_csv("data/motorcycle_ride.csv")
moving = ride[ride["speed_kmh"].between(3, 200)]   # riding, without error frames

print(f"Mean speed:   {moving['speed_kmh'].mean():.1f} km/h")
print(f"Median speed: {moving['speed_kmh'].median():.1f} km/h")
print(f"Std:          {moving['speed_kmh'].std():.1f} km/h")

print(moving[["speed_kmh", "rpm", "throttle_pct", "lean_deg"]].describe())

print(moving["speed_kmh"].quantile([0.1, 0.5, 0.9, 0.99]))
```

### Grouping

`groupby` splits the table by the values of one column, applies a calculation
to each group, and combines the results.

```python
ride = pd.read_csv("data/motorcycle_ride.csv")

per_gear = ride.groupby("gear").agg(
    samples=("speed_kmh", "size"),
    mean_speed=("speed_kmh", "mean"),
    mean_rpm=("rpm", "mean"),
)
print(per_gear)

print(ride.groupby("ride_mode")["lean_deg"].agg(["min", "max"]))
```

### Correlation

```python
ride = pd.read_csv("data/motorcycle_ride.csv")
moving = ride[ride["speed_kmh"].between(3, 200)]

columns = ["speed_kmh", "rpm", "throttle_pct", "accel_x", "lean_deg"]
print(moving[columns].corr().round(2))
```

A correlation coefficient measures a linear relationship and nothing else. The
lean angle and the speed are clearly related on a motorcycle, but the
coefficient is close to zero, because the bike leans left as often as right.

## Transforming Data

### Mathematical Operations

NumPy functions work directly on Series, element by element.

```python
ride = pd.read_csv("data/motorcycle_ride.csv")

ride["lean_rad"] = np.radians(ride["lean_deg"])
ride["accel_g"] = ride["accel_x"] / 9.81

# Magnitude of the horizontal acceleration, longitudinal and lateral combined
ride["lateral_g"] = np.tan(ride["lean_rad"])
ride["total_g"] = np.sqrt(ride["accel_g"] ** 2 + ride["lateral_g"] ** 2)

# Standardisation and min-max scaling
rpm = ride["rpm"]
ride["rpm_standardised"] = (rpm - rpm.mean()) / rpm.std()
ride["rpm_scaled"] = (rpm - rpm.min()) / (rpm.max() - rpm.min())
```

### Binning and Categorisation

```python
ride = pd.read_csv("data/motorcycle_ride.csv")

# Fixed bins with labels
ride["speed_band"] = pd.cut(
    ride["speed_kmh"],
    bins=[-1, 3, 55, 85, 300],
    labels=["standstill", "town", "country road", "fast"],
)

# Quantile bins: four groups with the same number of samples
ride["rpm_quartile"] = pd.qcut(ride["rpm"], q=4, labels=["Q1", "Q2", "Q3", "Q4"])

# Conditions, checked in order, the first match wins
conditions = [
    ride["brake_front_bar"] > 1,
    ride["lean_deg"].abs() > 10,
    ride["throttle_pct"] > 30,
]
ride["phase"] = np.select(conditions, ["braking", "cornering", "accelerating"],
                          default="cruising")
print(ride["phase"].value_counts())
```

## Reading and Writing Files

### Reading

`read_csv` has many options. The ones below are the ones you need most often
with measurement files.

```python
ride = pd.read_csv(
    "data/motorcycle_ride.csv",
    usecols=["timestamp", "speed_kmh", "rpm", "ride_mode"],  # only these columns
    dtype={"rpm": "int32", "ride_mode": "category"},          # explicit types
    nrows=6000,                                               # the first minute
)
ride.info()
```

Files from European software often use a semicolon as separator and a comma
as decimal mark. `sep=";"` and `decimal=","` read them correctly.

### Writing

```python
ride = pd.read_csv("data/motorcycle_ride.csv")
first_minute = ride[ride["timestamp"] < 60]

# CSV without the index, which is only a row number here
first_minute.to_csv("ride_first_minute.csv", index=False)

# Excel, with several sheets in one file
summary = ride.groupby("gear")[["speed_kmh", "rpm"]].mean()
with pd.ExcelWriter("ride_report.xlsx") as writer:
    first_minute.to_excel(writer, sheet_name="First minute", index=False)
    summary.to_excel(writer, sheet_name="Per gear")

# Reading it back: one sheet, or all sheets as a dictionary
per_gear = pd.read_excel("ride_report.xlsx", sheet_name="Per gear")
sheets = pd.read_excel("ride_report.xlsx", sheet_name=None)
print(list(sheets))

# JSON, one object per row
first_minute.head(3).to_json("ride_sample.json", orient="records", indent=2)
```

Excel is useful for handing results to colleagues, but it is a poor working
format: it has a limit of about a million rows, and it changes data types
silently. For large files, see [HDF5 Storage](./hdf5-storage.md).

## Performance

### Memory

```python
ride = pd.read_csv("data/motorcycle_ride.csv")
print(f"Before: {ride.memory_usage(deep=True).sum() / 1e6:.1f} MB")

def optimize_dtypes(data):
    """Downcast numbers and turn repeated strings into categories."""
    data = data.copy()
    for col in data.select_dtypes(include="float64"):
        data[col] = pd.to_numeric(data[col], downcast="float")
    for col in data.select_dtypes(include="int64"):
        data[col] = pd.to_numeric(data[col], downcast="integer")
    for col in data.select_dtypes(include="object"):
        data[col] = data[col].astype("category")
    return data

small = optimize_dtypes(ride)
print(f"After:  {small.memory_usage(deep=True).sum() / 1e6:.1f} MB")
```

Most of the saving comes from `ride_mode`. As Python strings, each of its
values costs dozens of bytes. As a category, each value is a small integer
code. float32 instead of float64 halves the rest, and its precision of about
seven digits is more than any sensor in this file delivers.

### Vectorised Operations

A loop over rows runs in Python, one row at a time. A vectorised operation runs
in compiled code over the whole column. The difference is often a factor of a
hundred or more.

```python
import time

ride = pd.read_csv("data/motorcycle_ride.csv")

# Slow: a Python loop over the rows
t0 = time.perf_counter()
values = []
for _, row in ride.iterrows():
    values.append(row["speed_kmh"] / 3.6 * np.tan(np.radians(row["lean_deg"])))
t_loop = time.perf_counter() - t0

# Fast: the same calculation on whole columns
t0 = time.perf_counter()
vectorised = ride["speed_kmh"] / 3.6 * np.tan(np.radians(ride["lean_deg"]))
t_vec = time.perf_counter() - t0

print(f"loop {t_loop:.2f} s, vectorised {t_vec:.4f} s")
```

#### When a Row-Wise Function Is Unavoidable

Sometimes each row needs a calculation that does not exist as a column
operation. `apply` with `axis=1` calls a function once per row. It is as slow
as a loop, but it keeps the code readable. The example transforms a
body-fixed vector into global coordinates using a reference point and three
orientation angles per row.

```python
df = pd.DataFrame({
    "ref_x": [100, 200], "ref_y": [50, 60], "ref_z": [20, 30],
    "body_x": [1, 0], "body_y": [0, 1], "body_z": [0, 0],
    "yaw_deg": [30, 45], "pitch_deg": [10, 0], "roll_deg": [5, -10],
})

def rotation_matrix(yaw_deg, pitch_deg, roll_deg):
    yaw, pitch, roll = np.radians([yaw_deg, pitch_deg, roll_deg])
    rz = np.array([[np.cos(yaw), -np.sin(yaw), 0],
                   [np.sin(yaw), np.cos(yaw), 0],
                   [0, 0, 1]])
    ry = np.array([[np.cos(pitch), 0, np.sin(pitch)],
                   [0, 1, 0],
                   [-np.sin(pitch), 0, np.cos(pitch)]])
    rx = np.array([[1, 0, 0],
                   [0, np.cos(roll), -np.sin(roll)],
                   [0, np.sin(roll), np.cos(roll)]])
    return rz @ ry @ rx

def transform_row(row):
    p_ref = np.array([row["ref_x"], row["ref_y"], row["ref_z"]])
    v_body = np.array([row["body_x"], row["body_y"], row["body_z"]])
    r = rotation_matrix(row["yaw_deg"], row["pitch_deg"], row["roll_deg"])
    v_global = r @ v_body + p_ref
    return pd.Series({"global_x": v_global[0], "global_y": v_global[1],
                      "global_z": v_global[2]})

df[["global_x", "global_y", "global_z"]] = df.apply(transform_row, axis=1)
print(df[["global_x", "global_y", "global_z"]])
```

## Best Practices

### Reusable Functions with Validation

Loading, checking and cleaning belong in functions, so that every analysis
starts from the same, checked state.

```python
REQUIRED = ["timestamp", "speed_kmh", "rpm", "lean_deg", "accel_x"]

# Physically possible range per column. Anything outside is not a measurement.
LIMITS = {
    "speed_kmh": (0, 250),
    "rpm": (0, 12000),
    "brake_front_bar": (0, 50),
    "lean_deg": (-60, 60),
    "coolant_c": (-20, 130),
}

def load_ride(filename):
    """Load a ride log, check its columns and sort it by time."""
    data = pd.read_csv(filename)
    missing = set(REQUIRED) - set(data.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    return data.sort_values("timestamp").reset_index(drop=True)

def validate_ranges(data):
    """Report every column with values outside its physical range."""
    issues = []
    for column, (low, high) in LIMITS.items():
        bad = data[(data[column] < low) | (data[column] > high)]
        if len(bad) > 0:
            issues.append(f"{column}: {len(bad)} values outside [{low}, {high}]")
    return issues

ride = load_ride("data/motorcycle_ride.csv")
for issue in validate_ranges(ride):
    print(" -", issue)
```

A range check is less clever than an outlier test and often more useful. It
does not flag the bends, because 30 degrees of lean is possible. It does flag
the values that no motorcycle can produce.

### Documenting What You Did

```python
import json

raw = pd.read_csv("data/motorcycle_ride.csv")
processed = raw[raw["speed_kmh"] <= 250].copy()
processed["coolant_c"] = processed["coolant_c"].ffill(limit=300)

processing_log = {
    "source_file": "data/motorcycle_ride.csv",
    "processing_date": pd.Timestamp.now().isoformat(),
    "steps": [
        "removed speed_kmh above 250 (bus error frames)",
        "coolant_c: forward fill, at most 3 s",
    ],
    "samples": {"raw": len(raw), "processed": len(processed)},
}

with open("processing_log.json", "w") as f:
    json.dump(processing_log, f, indent=2)
```

This covers the pandas operations you need for most data processing tasks.
The lecture on data processing builds on them with time indices, filtering,
calibration and integration.
