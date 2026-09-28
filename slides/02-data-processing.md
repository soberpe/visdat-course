---
marp: true
paginate: true
footer: "FH OÖ Wels · Visualization & Data Processing (VIS3VO)"
---

# Data Processing with Pandas
Master Mechanical Engineering · 3rd Semester

**Lecture 2: From Raw Sensor Data to Engineering Insights**  
Instructor: Stefan Oberpeilsteiner

---

## Today's Agenda

- Why data processing matters
- Pandas fundamentals
- Data selection & transformation
- Efficient storage (HDF5)
- Hands-on coding

---

## Why Data Processing?

### From Sensors to Insights
```
Raw Sensor Data → Clean Data → Extract Features → Analyze Trends
```

### Common Data Challenges
- **Sensor noise** and measurement errors
- **Data drift** over time
- **Missing values** and outliers
- **Multiple sensor types**
- **High-frequency data** (1000+ Hz)

---

## Pandas: Your Data Swiss Army Knife

<style scoped>
.small-list {
  font-size: 0.8em;
}
</style>
### What is Pandas?

<div class="small-list">

- **Python library** for data manipulation and analysis
- Built on **NumPy** for numerical operations
- **DataFrame**: Table-like structure for sensor data
- **Series**: Single column of data

</div>

### Why Pandas for Sensor Data?

<div class="small-list">

- ✅ **Time series** analysis (ideal for sensor data)
- ✅ **File I/O**: CSV, Excel, JSON, **HDF5**, Parquet
- ✅ **Data cleaning** and transformation
- ✅ **Statistical operations** built-in
- ✅ **Efficient storage** for large datasets

</div>

---

## Core Pandas Concepts

### Series vs DataFrame
```python
import pandas as pd

# Series: 1D labeled array
acceleration = pd.Series([2.1, 1.8, 2.5], 
                        index=['x', 'y', 'z'])

# DataFrame: 2D labeled table
imu_data = pd.DataFrame({
    'timestamp': [0.0, 0.001, 0.002],
    'ax': [0.1, 0.2, 0.15],
    'ay': [9.81, 9.8, 9.82],
    'az': [0.05, 0.03, 0.08]
})
```

---

## High-Performance Data Storage

### The Big Data Challenge in Sensor Experiments
- **Data volume**: 1000 Hz × 50+ channels = 50,000 values/second
- **Experiment duration**: 2 hours = 360 million data points
- **File size**: CSV ≈ 3.6 GB, **HDF5 ≈ 0.7 GB**
- **Access speed**: Fast random access to time ranges

---

### HDF5: Hierarchical Data Format
```python
# Store sensor data efficiently
import pandas as pd

# Save to HDF5 (compressed, fast access)
df.to_hdf('sensor_data.h5', key='experiment', mode='w', 
          complib='zlib', complevel=9)

# Read specific time range (fast!)
df_segment = pd.read_hdf('sensor_data.h5', key='experiment', where='timestamp >= 30 & timestamp <= 60')
```

<style scoped>
.small-list {
  font-size: 0.8em;
}
</style>

### HDF5 Advantages for Engineering

<div class="small-list">

- ✅ **Compression**: 5-10x smaller than CSV
- ✅ **Hierarchical**: Organize data in groups/datasets
- ✅ **Partial loading**: Read only what you need
- ✅ **Metadata**: Store units, calibrations, descriptions

</div>

---

## Advanced Pandas Features

### Multi-Level Data Organization
```python
# Hierarchical structure for sensor experiments
with pd.HDFStore('sensor_data.h5') as store:
    store['experiment1'] = exp1_df
    store['experiment2'] = exp2_df
    store['calibration'] = calib_df

# Query specific experiment
exp1_data = pd.read_hdf('sensor_data.h5', 'experiment1')
```

---

### Time Series Indexing & Resampling
```python
# Set timestamp as index for time-based operations
df_time = df.set_index('timestamp')

# Resample to different frequencies
df_100hz = df_time.resample('10ms').mean()  # 100 Hz
df_10hz = df_time.resample('100ms').mean()  # 10 Hz

# Rolling statistics for trend analysis
df_time['sensor_rms'] = df_time['sensor_value'].rolling('1s').std()
```

---

## Sensor Dataset Structure

```python
# Example sensor dataset columns
columns = [
    'timestamp',     # Time in seconds
    'temperature',   # Sensor reading [°C]
    'pressure',      # Sensor reading [Pa]
    'accel_x', 'accel_y', 'accel_z', # Acceleration [m/s²]
]
```

### Sample Data Preview
| timestamp | temperature | pressure | accel_x | accel_y | accel_z |
|-----------|-------------|----------|---------|---------|---------|
| 0.000     | 22.5        | 101325   | 0.12    | 9.81    | 0.05    |
| 0.001     | 22.6        | 101320   | 0.15    | 9.79    | 0.08    |

---

## Reading and Exploring Data

### Loading the Dataset
```python
import pandas as pd
import numpy as np

# Load sensor data from CSV
df = pd.read_csv('sensor_data.csv')

# Quick data exploration
print(f"Dataset shape: {df.shape}")
print(f"Time span: {df['timestamp'].max():.2f} seconds")
print(f"Sample rate: {1/df['timestamp'].diff().mean():.0f} Hz")
```

---

### First Look at the Data
```python
# Display first/last rows
df.head()
df.tail()

# Statistical summary
df.describe()

# Data types and missing values
df.info()
```

---

## Data Quality Assessment

### Checking for Issues
```python
# Missing values
print("Missing values per column:")
print(df.isnull().sum())

# Outlier detection (simple approach)
def find_outliers(series, threshold=3):
    z_scores = np.abs((series - series.mean()) / series.std())
    return series[z_scores > threshold]

# Check temperature outliers
outliers_temp = find_outliers(df['temperature'])
print(f"Found {len(outliers_temp)} outliers in temperature")
```

---

### Time Series Validation
```python
# Check for regular sampling
dt = df['timestamp'].diff()
print(f"Sampling rate variation: {dt.std():.6f} seconds")

# Look for time gaps
gaps = dt[dt > dt.median() * 2]
if len(gaps) > 0:
    print(f"Found {len(gaps)} potential data gaps")
```

---

## Data Cleaning Operations

### Handling Missing Values
```python
# Strategy 1: Forward fill for short gaps
df_clean = df.fillna(method='ffill', limit=5)

# Strategy 2: Interpolation for sensor data
df_clean['temperature'] = df_clean['temperature'].interpolate(method='linear')

# Strategy 3: Drop rows with too many missing values
df_clean = df_clean.dropna(thresh=len(df.columns) * 0.8)
```

---

### Filtering and Smoothing
```python
# Remove outliers using IQR method
def remove_outliers_iqr(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    return df[(df[column] >= lower) & (df[column] <= upper)]

# Apply to temperature data
df_clean = remove_outliers_iqr(df, 'temperature')
```

---

## Time-Based Operations

### Setting Time Index
```python
# Convert timestamp to datetime and set as index
df_clean['datetime'] = pd.to_datetime(df_clean['timestamp'], unit='s')
df_indexed = df_clean.set_index('datetime')

# Now we can use powerful time-based operations
stats_100ms = df_indexed.resample('100ms').mean()
```

---

### Moving Averages for Noise Reduction
```python
# Smooth noisy sensor data
window_size = 10  # 10ms window

df_smooth = df_clean.copy()
df_smooth['temperature_smooth'] = df_clean['temperature'].rolling(window=window_size).mean()
df_smooth['pressure_smooth'] = df_clean['pressure'].rolling(window=window_size).mean()
```

---

## Engineering Calculations

### Sensor Calibration Example
```python
# Remove offset from temperature sensor (calibration)
offset = df_clean['temperature'].iloc[:100].mean()  # Estimate from baseline
df_clean['temperature_calibrated'] = df_clean['temperature'] - offset
```

---

### Integration: Acceleration → Velocity
```python
# Numerical integration using cumulative trapezoidal rule
dt = df_clean['timestamp'].diff().fillna(0)

# Integrate acceleration to get velocity
df_clean['vel_x'] = np.cumsum(df_clean['accel_x'] * dt)
df_clean['vel_y'] = np.cumsum(df_clean['accel_y'] * dt)

# Integrate velocity to get position
df_clean['pos_x'] = np.cumsum(df_clean['vel_x'] * dt)
df_clean['pos_y'] = np.cumsum(df_clean['vel_y'] * dt)
```

---

## Performance Analysis

### Sensor Data Metrics
```python
# Calculate max/min temperature and pressure
max_temp = df_clean['temperature'].max()
min_temp = df_clean['temperature'].min()
max_pressure = df_clean['pressure'].max()
print(f"Max temperature: {max_temp:.2f} °C")
print(f"Min temperature: {min_temp:.2f} °C")
print(f"Max pressure: {max_pressure:.0f} Pa")
```

---

### Statistical Analysis
```python
# Detect high-pressure events
high_pressure_mask = df_clean['pressure'] > 102000
high_pressure_data = df_clean[high_pressure_mask]
avg_high_pressure = high_pressure_data['pressure'].mean()
print(f"Average high pressure: {avg_high_pressure:.0f} Pa")
```

---

## Advanced Data Operations

### GroupBy for Sensor Events
```python
# Group by experiment or batch
df['batch'] = (df['timestamp'] // 60).astype(int)  # Each batch = 1 min

# Analyze metrics by batch
batch_stats = df.groupby('batch').agg({
    'temperature': ['mean', 'max'],
    'pressure': ['mean', 'max'],
    'timestamp': lambda x: x.max() - x.min()  # batch duration
})
```

---

### Window Functions & Rolling Calculations
```python
# Rolling analysis for sensor data
df['temp_trend'] = df['temperature'].rolling(window=50).mean()
df['pressure_variance'] = df['pressure'].rolling(window=100).var()

# Relative to session average
df['temp_vs_avg'] = df['temperature'] / df['temperature'].expanding().mean()
```

---

### Memory Optimization
```python
# Optimize data types for large sensor datasets
def optimize_dtypes(df):
    for col in df.select_dtypes(include=['float64']):
        if df[col].min() > np.finfo(np.float32).min and \
           df[col].max() < np.finfo(np.float32).max:
            df[col] = df[col].astype(np.float32)
    for col in df.select_dtypes(include=['int64']):
        if df[col].min() > np.iinfo(np.int32).min and \
           df[col].max() < np.iinfo(np.int32).max:
            df[col] = df[col].astype(np.int32)
    return df

df_optimized = optimize_dtypes(df)
print(f"Memory usage reduced by {df.memory_usage().sum() / df_optimized.memory_usage().sum():.1f}x")
```

---

## Data Export and Pipeline

<style scoped>
pre {
  max-height: 350px;
  overflow-y: auto;
  font-size: 0.8em;
}
</style>

```python
# Multiple export formats for different use cases

# 1. HDF5 for high-performance analysis
with pd.HDFStore('sensor_data.h5', complevel=9) as store:
    store['raw_data'] = df_raw
    store['processed_data'] = df_clean
    store['summary'] = pd.DataFrame([summary_stats])
    # Add metadata
    store.get_storer('processed_data').attrs.metadata = {
        'sampling_rate': 1000,
        'experiment': 'Lab Sensor Test',
        'operator': 'Test Engineer',
        'processing_date': pd.Timestamp.now()
    }

# 2. CSV for external tools (Excel, MATLAB)
df_clean.to_csv('sensor_data_processed.csv', index=False)

# 3. JSON for web applications
summary_stats.to_json('sensor_summary.json', orient='records')
```

---

### HDF5 Data Organization

<style scoped>
pre {
  max-height: 350px;
  overflow-y: auto;
  font-size: 0.8em;
}
</style>

```python
# Example HDF5 data structure
/sensor_data.h5
├── /raw_data              # Original sensor readings
├── /processed_data        # Cleaned and calibrated
├── /derived_parameters    # Calculated values
├── /summary               # Summary statistics
└── /metadata              # Calibration, units, processing log
```

---

## Coming Up Next: Visualization

### Next Session Preview
- **Matplotlib**: Creating publication-ready plots
- **Time series visualization**: Sensor data plots
- **3D trajectory plotting**: Experiment path analysis

### Your Mission
- Practice with the sensor dataset
- Try additional calculations (moving average, event detection)

**📁 All code examples:** Available in course repository
