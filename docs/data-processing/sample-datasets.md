---
title: Sample Datasets
---

# Sample Datasets

The `data/` folder of the course repository holds the files used in the
exercises, the demos and the code snippets of this documentation.

## Motorcycle ride

**File:** `data/motorcycle_ride.csv`

This is the time series dataset of the course. The data processing lecture,
the visualization lecture and the chapters on pandas and HDF5 all use it. It is
the log of a motorcycle ride of about nine minutes on a country road, recorded
at 100 Hz: a village, a junction, fast straights, a section of bends, a traffic
light and a stop at the end. The ride starts and ends at standstill.

The file is synthetic, and it is deliberately not clean. It contains the kinds
of problems a real data logger produces: gaps in the time column, missing
values, values that are not measurements at all, and a sensor offset that
drifts. Finding them is part of the exercise, so they are not listed here. The
script that generates the file, `tools/make-motorcycle-ride.py`, documents
every one of them in its docstring, if you want to check your findings.

| Column | Unit | Meaning |
|---|---|---|
| `timestamp` | s | Time since the logger started |
| `speed_kmh` | km/h | Wheel speed sensor |
| `rpm` | 1/min | Engine speed |
| `gear` | - | Selected gear, 0 is neutral |
| `throttle_pct` | % | Throttle opening |
| `brake_front_bar` | bar | Front brake line pressure |
| `brake_rear_bar` | bar | Rear brake line pressure |
| `lean_deg` | deg | Lean angle from the IMU, positive is to the right |
| `accel_x` | m/s² | Longitudinal acceleration from the IMU |
| `coolant_c` | °C | Coolant temperature, updated once per second |
| `ride_mode` | - | Riding mode selected on the dashboard |

## FEM results

**Files:** `data/beam_stress.vtu`, `data/conrod.inp`

`beam_stress.vtu` is a beam computed with CalculiX, with displacements,
stresses and strains on the mesh. The mesh visualization workshop and the Qt
workshop use it. `conrod.inp` is the mesh of a connecting
rod in Abaqus format, the input for the file conversion examples with meshio.
