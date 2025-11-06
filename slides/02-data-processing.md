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
- **Why data processing matters** 🏎️
- **Pandas fundamentals** 🐼
- **Vehicle dynamics case study** 📊
- **IMU data analysis** 🚗
- **Hands-on coding** ⚡
- **Preview: Visualization pipeline** 👀

---

## The Racing Data Challenge

![bg right:40% 80%](https://img.redbull.com/images/c_crop,w_3039,h_1518,x_0,y_489/c_auto,w_1200,h_630/f_auto,q_auto/redbullcom/2015/08/19/1331772435696_4/wrc-legende-walter-rohrl)

**Scenario:** Analyzing a racing car's cornering maneuver
- **Raw sensor data:** 6-DOF IMU readings
- **Goal:** Understand vehicle dynamics
- **Challenge:** Transform noisy signals → meaningful motion

> <sub> *„Wenn es nur ein Geheimnis beim Autofahren gibt, dann ist es, so wenig wie möglich zu lenken, Es geht um Linien und man muss begreifen, wann man zu lenken beginnen muss – eher früh als spät."* — Walter Röhrl</sub>

---

## Why Data Processing?

### From Sensors to Insights
```
Raw IMU Data → Clean Data → Vehicle Motion → Performance Analysis
```

### Real Engineering Challenges
- **Sensor noise** and measurement errors
- **Data drift** over time
- **Missing values** and outliers
- **Multiple coordinate systems**
- **High-frequency data** (1000+ Hz)

---

## Pandas: Your Data Swiss Army Knife

### What is Pandas?
- **Python library** for data manipulation and analysis
- Built on **NumPy** for numerical operations
- **DataFrame**: Excel-like data structure in code
- **Series**: Single column of data

### Why Pandas for Engineering?

<style scoped>
.small-list {
  font-size: 0.8em;
}
</style>

<div class="small-list">

- ✅ **Time series** analysis (perfect for sensor data)
- ✅ **File I/O**: CSV, Excel, JSON, **HDF5**, Parquet
- ✅ **Data cleaning** and transformation and built-in **Statistical operations**
- ✅ **Memory efficient** for large datasets with **high-performance** binary formats for big data

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

### The Big Data Challenge in Racing
- **Data volume**: 1000 Hz × 50+ channels = 50,000 values/second
- **Race duration**: 2-hour endurance race = 360 million data points
- **File size**: CSV format ≈ 3.6 GB, **HDF5 format ≈ 0.7 GB**
- **Access speed**: Random access to time ranges

---

### HDF5: Hierarchical Data Format
```python
# Store racing data efficiently
import pandas as pd
import h5py

# Save to HDF5 (compressed, fast access)
df.to_hdf('data/racing_data.h5', key='telemetry', mode='w', 
          complib='zlib', complevel=9)

# Read specific time range (fast!)
df_segment = pd.read_hdf('data/racing_data.h5', key='telemetry', where='time_s >= 30 & time_s <= 60')
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
# Hierarchical structure for race weekend
with pd.HDFStore('data/racing_data.h5') as store:
    store['practice/session1'] = practice1_df
    store['practice/session2'] = practice2_df
    store['qualifying/q1'] = qualifying_df
    store['race/stint1'] = race_stint1_df
    store['race/stint2'] = race_stint2_df

# Query specific sessions
q1_data = pd.read_hdf('data/racing_data.h5', 'sessions')
```

---

### Time Series Indexing & Resampling
```python
# Set timestamp as index for powerful time operations
df_time = df.set_index('timestamp')

# Resample to different frequencies
df_100hz = df_time.resample('10ms').mean()  # 100 Hz
df_10hz = df_time.resample('100ms').mean()  # 10 Hz

# Rolling statistics for trend analysis
df_time['lateral_g_rms'] = df_time['lateral_g'].rolling('1s').std()
```

---

## Vehicle IMU Dataset Structure

```python
# 6-DOF IMU data from a cornering maneuver
columns = [
    'timestamp',     # Time in seconds
    'ax', 'ay', 'az', # Linear acceleration [m/s²]
    'gx', 'gy', 'gz', # Angular velocity [rad/s]
    'speed',         # Vehicle speed [km/h]
    'steering_angle' # Steering input [degrees]
]
```

### Sample Data Preview
| timestamp | ax   | ay    | az   | gx    | gy   | gz    | speed | steering |
|-----------|------|-------|------|-------|------|-------|-------|----------|
| 0.000     | 0.12 | 9.81  | 0.05 | 0.001 | 0.02 | 0.003 | 45.2  | 0.0      |
| 0.001     | 0.15 | 9.79  | 0.08 | 0.002 | 0.02 | 0.005 | 45.3  | 2.1      |

---

## Reading and Exploring Data

### Loading the Dataset
```python
import pandas as pd
import numpy as np

# Load IMU data from CSV
df = pd.read_csv('data/telemetry_detailed.csv')

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

# Check acceleration outliers
outliers_ax = find_outliers(df['ax'])
print(f"Found {len(outliers_ax)} outliers in ax")
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
df_clean['ax'] = df_clean['ax'].interpolate(method='linear')

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

# Apply to acceleration data
df_clean = remove_outliers_iqr(df, 'ax')
```

---

## Time-Based Operations

### Setting Time Index
```python
# Convert timestamp to datetime and set as index
df_clean['datetime'] = pd.to_datetime(df_clean['timestamp'], unit='s')
df_indexed = df_clean.set_index('datetime')

# Now we can use powerful time-based operations
hourly_stats = df_indexed.resample('100ms').mean()
```

---

### Moving Averages for Noise Reduction
```python
# Smooth noisy sensor data
window_size = 10  # 10ms window at 1000Hz

df_smooth = df_clean.copy()
df_smooth['ax_smooth'] = df_clean['ax'].rolling(window=window_size).mean()
df_smooth['ay_smooth'] = df_clean['ay'].rolling(window=window_size).mean()
df_smooth['az_smooth'] = df_clean['az'].rolling(window=window_size).mean()
```

---

## Engineering Calculations

### Coordinate Transformations
```python
# Remove gravity component (assuming vehicle is level initially)
gravity = df_clean['ay'].iloc[:100].mean()  # Estimate from stationary period
df_clean['ay_vehicle'] = df_clean['ay'] - gravity

# Calculate lateral acceleration (important for cornering analysis)
df_clean['lateral_g'] = df_clean['ay_vehicle'] / 9.81
```

---

### Integration: Acceleration → Velocity
```python
# Numerical integration using cumulative trapezoidal rule
dt = df_clean['timestamp'].diff().fillna(0)

# Integrate acceleration to get velocity
df_clean['vx'] = np.cumsum(df_clean['ax'] * dt)
df_clean['vy'] = np.cumsum(df_clean['ay_vehicle'] * dt)

# Integrate velocity to get position
df_clean['pos_x'] = np.cumsum(df_clean['vx'] * dt)
df_clean['pos_y'] = np.cumsum(df_clean['vy'] * dt)
```

---

## Performance Analysis

### Cornering Metrics
```python
# Calculate cornering radius
df_clean['yaw_rate'] = df_clean['gz']  # rad/s
df_clean['speed_ms'] = df_clean['speed'] / 3.6  # Convert km/h to m/s

# Radius of curvature
df_clean['corner_radius'] = df_clean['speed_ms'] / np.abs(df_clean['yaw_rate'])

# Maximum lateral acceleration during maneuver
max_lateral_g = df_clean['lateral_g'].max()
print(f"Maximum lateral acceleration: {max_lateral_g:.2f} g")
```

---

### Statistical Analysis
```python
# Cornering phase detection (high steering angle)
cornering_mask = np.abs(df_clean['steering_angle']) > 10

# Performance metrics during cornering
cornering_data = df_clean[cornering_mask]
avg_corner_speed = cornering_data['speed'].mean()
peak_lateral_g = cornering_data['lateral_g'].max()

print(f"Average cornering speed: {avg_corner_speed:.1f} km/h")
print(f"Peak lateral acceleration: {peak_lateral_g:.2f} g")
```

---

## Advanced Data Operations

### GroupBy for Lap Analysis
```python
# Identify laps using sector markers or lap time
df['lap_number'] = (df['distance'] // track_length).astype(int)

# Analyze performance by lap
lap_stats = df.groupby('lap_number').agg({
    'speed': ['mean', 'max'],
    'lateral_g': 'max',
    'corner_radius': 'min',
    'timestamp': lambda x: x.max() - x.min()  # lap time
})

# Compare fastest vs average lap
fastest_lap = lap_stats['timestamp'].idxmin()
avg_performance = lap_stats.mean()
```

---

### Window Functions & Rolling Calculations
```python
# Sector-based analysis (rolling windows)
df['speed_trend'] = df['speed'].rolling(window=50).mean()
df['accel_variance'] = df['ax'].rolling(window=100).var()

# Performance relative to session average
df['speed_vs_avg'] = df['speed'] / df['speed'].expanding().mean()

# Tire degradation analysis
df['grip_proxy'] = df.groupby('lap_number')['lateral_g'].transform('max')
```

---

### Memory Optimization
```python
# Optimize data types for large datasets
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
with pd.HDFStore('data/racing_data.h5', complevel=9) as store:
    store['raw_data'] = df_raw
    store['processed_data'] = df_clean
    store['cornering_segments'] = cornering_segments
    store['performance_summary'] = pd.DataFrame([performance_metrics])
    
    # Add metadata
    store.get_storer('processed_data').attrs.metadata = {
        'sampling_rate': 1000,
        'vehicle': 'Autocross Single Seater',
        'track': 'Nova Paka Circuit',
        'driver': 'Test Driver',
        'processing_date': pd.Timestamp.now()
    }

# 2. CSV for external tools (MATLAB, Excel)
df_clean.to_csv('data/telemetry_processed.csv', index=False)

# 3. JSON for web applications
summary_stats.to_json('performance_api.json', orient='records')
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
# Professional data structure
/data/racing_data.h5
├── /raw_data              # Original sensor readings
├── /processed_data        # Cleaned and calibrated
├── /derived_parameters    # Calculated values (g-forces, etc.)
├── /cornering_analysis    # Segment-specific data
├── /performance_metrics   # Summary statistics
└── /metadata              # Calibration, units, processing log
```

---

## Live Demo: Racing Data Analysis

### 🏎️ **Hands-On Coding Session**

**Task:** Analyze a racing car's cornering maneuver
1. Load synthetic IMU data
2. Clean and validate the dataset  
3. Calculate vehicle motion parameters
4. Extract performance metrics
5. Prepare data for visualization

**Dataset:** `data/telemetry_detailed.csv`

---

### Key Takeaways

<style scoped>
.small-list {
  font-size: 0.8em;
}
</style>

### HDF5 Advantages for Engineering

### Pandas Essentials for Engineers

<div class="small-list">

- ✅ **DataFrames** are your primary tool for structured data
- ✅ **Time-based indexing** simplifies sensor data analysis
- ✅ **HDF5 storage** for high-performance big data workflows
- ✅ **GroupBy operations** for segment and lap analysis
- ✅ **Rolling functions** for trend and statistical analysis
- ✅ **Memory optimization** for large datasets
- ✅ **Built-in statistical functions** accelerate analysis
- ✅ **Integration capabilities** for motion calculations
- ✅ **Export options** maintain data pipeline flow

</div>

--- 

### Data Processing Workflow
```
Raw Data → Clean → Transform → Analyze → Store (HDF5) → Visualize
```

### Racing Engineering Insights
- **Data quality** directly impacts analysis reliability
- **Coordinate systems** and reference frames matter
- **Integration drift** requires correction strategies
- **Storage format** choice affects performance and compatibility

---

### HDF5 Best Practices
- ✅ **Compress data** for storage efficiency
- ✅ **Use hierarchical structure** for organization
- ✅ **Store metadata** with datasets
- ✅ **Query capabilities** for large datasets
- ✅ **Cross-platform compatibility**

---

## Coming Up Next: Visualization

### Next Session Preview
- **Matplotlib**: Creating publication-ready plots
- **Time series visualization**: Racing telemetry plots
- **3D trajectory plotting**: Vehicle path analysis

### Your Mission
- Practice with the racing dataset
- Try additional calculations (jerk, path curvature)
- Prepare questions for visualization session

**📁 All code examples:** Available in course repository
