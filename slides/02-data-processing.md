---
marp: true
theme: visdat
paginate: true
footer: "FH OÖ Wels · Visualisierung & Datenaufbereitung"
---

<!-- _class: title -->

# Data Processing

## Getting measurement data into a shape you can trust

Lecture 2 · pandas, NumPy, HDF5

<!--
Second session. The data files are in data/ in the course repository, everyone
should have them locally. Today is mostly hands on: we work through one real
sensor file from loading to storage.
-->

---

# Today

1. **What goes wrong** with measurement data, and how to find it
2. **pandas**: the two objects you need, and the operations that matter
3. **Engineering**: calibration, filtering, integration, and the drift that follows
4. **Storage**: why CSV stops working and what replaces it

<p class="note">Data: <code>data/sensor_data.csv</code> and <code>data/sensor_data.h5</code> in the course repository.</p>

---

<!-- _class: ask -->

# Your rig logged for three hours at 1 kHz. Excel refuses to open the file. Now what?

<!--
Let them work it out. 10.8 million rows. Excel stops at roughly a million, and
would be unusable long before that. This is the moment where a script stops
being optional, which is the honest reason this course exists.
-->

---

# What is actually wrong with the data

<div class="boxes">
<div><b>Gaps</b>The logger dropped samples. The time column has holes you will not see in a plot.</div>
<div><b>Units</b>Degrees or radians, bar or pascal, g or m/s². Nobody wrote it down.</div>
<div><b>Drift</b>The sensor has an offset that changes over the run.</div>
<div><b>Outliers</b>A spike. Is it a fault, or is it the event you are looking for?</div>
</div>

<p class="note">Every one of these is invisible in <code>df.head()</code>. You have to go looking.</p>

---

# Two objects, that is all

<div class="cols">
<div>

**Series**: one labelled column

```python
s = pd.Series([22.5, 22.6, 22.4],
              name="temperature")
```

</div>
<div>

**DataFrame**: a table of Series

```python
df = pd.DataFrame({
    "time": [0.0, 0.001, 0.002],
    "temperature": [22.5, 22.6, 22.4],
})
```

</div>
</div>

Every pandas operation returns one of these two. Once that clicks, the
documentation becomes navigable.

---

<!-- _class: live -->

# First contact

```python
import pandas as pd

df = pd.read_csv("data/sensor_data.csv")
print(df.shape)
df.head()
df.info()          # dtypes and missing values
df.describe()      # min, max, mean, quartiles
```

Read the output together. What is suspicious?

<!--
Do not skip describe(). Ask what a minimum of -273 in a temperature column
would mean, and what a maximum of exactly 1023 usually means (an ADC rail).
Reading describe() critically is the actual skill here.
-->

---

# Is the sampling rate really constant?

```python
dt = df["timestamp"].diff()

print(f"nominal rate: {1 / dt.median():.0f} Hz")
print(f"jitter:       {dt.std() * 1e6:.1f} µs")

gaps = dt[dt > dt.median() * 2]
print(f"gaps: {len(gaps)}")
```

> Everything downstream assumes even spacing: filters, FFT, integration. If the
> spacing is uneven and you do not know it, every result after this point is
> wrong by an amount nobody can estimate.

---

# Missing values: three strategies, three assumptions

```python
df.fillna(method="ffill", limit=5)          # hold the last value
df["temperature"].interpolate("linear")      # assume it changed smoothly
df.dropna(thresh=len(df.columns) * 0.8)      # give up on the row
```

<div class="boxes">
<div><b>Forward fill</b>Right for a slow signal, wrong for a step.</div>
<div><b>Interpolate</b>Right for a smooth physical quantity, wrong across a real gap.</div>
<div><b>Drop</b>Honest, but it changes your time spacing.</div>
</div>

<p class="note">Whatever you choose, write down which one and why. That sentence belongs in your README.</p>

---

# Outliers

```python
Q1, Q3 = df["temperature"].quantile([0.25, 0.75])
iqr = Q3 - Q1
mask = df["temperature"].between(Q1 - 1.5 * iqr, Q3 + 1.5 * iqr)
```

> The method finds points that are unusual. It cannot tell you whether they are
> faults or findings. A pressure spike is an outlier and might also be the
> event the whole test was built to capture.

<p class="note">Never delete silently. Mark, count, and report how many you removed.</p>

<!--
Good moment for a story from practice: a measurement where the "outliers" were
the only real content. Ask them what would have happened if a script had
dropped them automatically.
-->

---

# Time as an index

```python
df["datetime"] = pd.to_datetime(df["timestamp"], unit="s")
df = df.set_index("datetime")

df.resample("100ms").mean()          # downsample
df["temperature"].rolling("1s").mean()   # smooth over a window
df["temperature"].rolling("1s").std()    # noise over a window
```

With a time index, pandas understands windows in seconds instead of rows, and
uneven spacing stops silently corrupting your averages.

---

# Smoothing costs something

```python
df["temp_smooth"] = df["temperature"].rolling(window=10, center=True).mean()
```

<div class="cols">
<div>

**You gain**

Less noise, a readable curve, stable derivatives.

</div>
<div>

**You pay**

Edges get cut, real peaks get shorter, fast events disappear entirely.

</div>
</div>

<p class="note">Always plot raw and filtered together, at least once, before you trust the filtered one.</p>

---

# Calibration is subtraction, with a decision in it

```python
baseline = df["temperature"].iloc[:100].mean()   # first 100 samples, rig at rest
df["temperature_cal"] = df["temperature"] - baseline
```

The code is trivial. The decision is not: those first 100 samples have to be a
state you can defend as zero.

---

# Integration, and what it does to your error

```python
import numpy as np

dt = df["timestamp"].diff().fillna(0)

df["vel_x"] = np.cumsum(df["accel_x"] * dt)   # acceleration → velocity
df["pos_x"] = np.cumsum(df["vel_x"] * dt)     # velocity → position
```

> A constant offset in acceleration becomes a linear error in velocity and a
> quadratic error in position. That is why the IMU workshop asks you to walk a
> measured distance and compare.

---

<!-- _class: live -->

# Watch the drift appear

```python
fig, axs = plt.subplots(3, 1, sharex=True, figsize=(9, 7))
axs[0].plot(df["timestamp"], df["accel_x"]); axs[0].set_ylabel("a [m/s²]")
axs[1].plot(df["timestamp"], df["vel_x"]);   axs[1].set_ylabel("v [m/s]")
axs[2].plot(df["timestamp"], df["pos_x"]);   axs[2].set_ylabel("s [m]")
axs[2].set_xlabel("Time [s]")
```

Then: subtract the mean of the acceleration and run it again.

<!--
The three stacked axes make the point better than any explanation. Show it
first without removing the offset, so the position curve runs off the screen,
then with. This is the preview of the IMU workshop.
-->

---

<!-- _class: section -->

# Storage

## When the CSV stops being a good idea

---

# Formats, and what each is for

| Format | Good at | Falls over when |
|---|---|---|
| **CSV** | Anything can read it | Large files, types, structure |
| **Excel** | Colleagues open it | Row limits, silent type changes |
| **HDF5** | Large arrays, fast partial reads | You want to open it by hand |
| **Parquet** | Columnar analysis, compression | Row-wise access |

<p class="note">CSV is a good interchange format and a bad working format. Both things are true.</p>

---

# HDF5 in practice

```python
# write, compressed, with a queryable structure
df.to_hdf("data/sensor_data.h5", key="run01/sensors",
          format="table", complevel=5)

# read only what you need, without loading the file
part = pd.read_hdf("data/sensor_data.h5", key="run01/sensors",
                   where="index >= 100 and index < 200")
```

One file can hold many runs under different keys, with metadata, and you read a
slice of it without touching the rest.

---

<!-- _class: live -->

# Compare it yourself

```python
import time, os

t0 = time.perf_counter(); pd.read_csv("data/sensor_data.csv"); t_csv = time.perf_counter() - t0
t0 = time.perf_counter(); pd.read_hdf("data/sensor_data.h5"); t_hdf = time.perf_counter() - t0

print(f"CSV  {os.path.getsize('data/sensor_data.csv')/1e6:.1f} MB  {t_csv:.3f} s")
print(f"HDF5 {os.path.getsize('data/sensor_data.h5')/1e6:.1f} MB  {t_hdf:.3f} s")
```

<!--
Numbers in front of them beat any claim from me. Run it twice, the second run
is warm cache, and say so, because that is the kind of honesty a measurement
deserves.
-->

---

# Memory: the cheapest optimisation you will ever make

```python
df["sensor_id"] = df["sensor_id"].astype("category")
df["temperature"] = df["temperature"].astype("float32")

print(df.memory_usage(deep=True).sum() / 1e6, "MB")
```

float64 to float32 halves the memory and is almost always enough for sensor
data. A repeated string column as `category` can save 90 percent.

---

# Recap

- Look for **gaps, units, drift and outliers** before you compute anything
- **Series and DataFrame** are the only two objects
- Cleaning is a **decision**, so write down which one you made
- Integration turns a small offset into a **large error**
- CSV to exchange, **HDF5 to work**

---

<!-- _class: section -->

# Next

## Visualization

<p>From this table to a picture someone can act on.</p>

<p>Bring your cleaned sensor data.</p>
