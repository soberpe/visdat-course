---
title: High-Performance Data Storage with HDF5
---

# High-Performance Data Storage with HDF5


## The Big Data Challenge in Engineering

Modern engineering applications generate massive amounts of sensor data. For example:
- **Sampling rates**: 1000+ Hz per channel
- **Channel count**: 60+ sensors (IMU, temperature, pressure, etc.)
- **Run duration**: Hours of continuous measurement
- **Data volume**: Hundreds of millions of data points per experiment

**Storage Challenge Example:**
- 60 channels × 1000 Hz × 3600 seconds (1 hour) = 216 million values
- CSV format: ~3 GB per experiment
- Memory requirements: Several GB RAM for analysis
- Query time: Minutes to find specific time ranges

## Introduction to HDF5

HDF5 (Hierarchical Data Format version 5) is a binary file format designed for storing and organizing large amounts of scientific data.

### Key Advantages for Engineering Data

#### 1. **Compression and Storage Efficiency**
- **5-10x smaller** files compared to CSV
- **Built-in compression** algorithms (gzip, lzf, szip)
- **Chunked storage** for efficient access patterns

#### 2. **Performance**
- **Fast random access** to data subsets
- **Parallel I/O** capabilities
- **Memory mapping** for large datasets
- **Optimized for time series** queries

#### 3. **Data Organization**
- **Hierarchical structure** like a file system
- **Groups and datasets** for logical organization
- **Metadata storage** with attributes
- **Self-describing** format

#### 4. **Cross-Platform Compatibility**
- Works on **Windows, Linux, macOS**
- **Language support**: Python, MATLAB, R, C/C++, Java
- **Long-term archival** format

## HDF5 with Pandas

### Installation and Setup
```python
# Install required packages
# pip install pandas tables h5py

import pandas as pd
import numpy as np
import h5py
```


> **Info**
> **Table format in HDF5 (with pandas):**
> When saving a DataFrame to HDF5, you can choose `format='table'` or `format='fixed'` (the default). Table format enables advanced features:
> - Row-wise access and partial reads
> - Powerful `where` queries for filtering data during loading
> - Appending new data to the file
> Table format is slightly slower to write and uses more space than fixed format, but is essential for large datasets where you need flexible queries and efficient access to subsets of data.


#### Writing Data to HDF5
```python
# Create sample sensor data
np.random.seed(42)
n_samples = 10000  # 10 seconds at 1000 Hz
timestamps = np.linspace(0, 10, n_samples)

# Generate generic sensor measurements
sensor_data = pd.DataFrame({
    'timestamp': timestamps,
    'sensor_1': np.random.normal(0, 1, n_samples),
    'sensor_2': np.random.normal(10, 2, n_samples),
    'sensor_3': np.random.normal(100, 5, n_samples),
    'steering_angle': 50 * np.sin(0.07 * timestamps) + np.random.normal(0, 8, n_samples),
    'throttle_position': np.clip(55 + 35 * np.sin(0.09 * timestamps) + np.random.normal(0, 12, n_samples), 0, 100),
    'brake_pressure': np.maximum(0, 25 * np.sin(0.13 * timestamps + np.pi) + np.random.normal(0, 6, n_samples)),
    'suspension_travel_fl': 50 + 30 * np.sin(0.12 * timestamps) + np.random.normal(0, 8, n_samples),  # Front left
    'suspension_travel_fr': 50 + 30 * np.sin(0.12 * timestamps + 0.1) + np.random.normal(0, 8, n_samples)  # Front right
})

sensor_data['speed'] = np.clip(sensor_data['sensor_1'], 0, 75)  # Example: limit speed to realistic range
sensor_data['suspension_travel_fl'] = np.clip(sensor_data['suspension_travel_fl'], 0, 100)  # 0-100mm travel
sensor_data['suspension_travel_fr'] = np.clip(sensor_data['suspension_travel_fr'], 0, 100)

# Save to HDF5 with compression
# Key arguments for pandas' to_hdf:
#   - 'path_or_buf': filename to save to
#   - 'key': name of the dataset/group in the HDF5 file
#   - 'mode': file mode ('w' for write, 'a' for append, etc.)
#   - 'format': 'fixed' (default, fast, no queries) or 'table' (slower, supports queries)
#   - 'complib': compression library (e.g., 'zlib', 'lzf')
#   - 'complevel': compression level (0-9, higher is more compressed)
#   - 'data_columns': columns to make queryable (only for table format)
sensor_data.to_hdf('data/sensor_data.h5', 
                  key='telemetry', 
                  mode='w',
                  complib='zlib',    # Compression algorithm
                  complevel=9)       # Maximum compression

print(f"Saved {len(sensor_data)} samples to HDF5")
```

#### Reading Data from HDF5
```python

# Read entire dataset
df_loaded = pd.read_hdf('data/sensor_data.h5', 'telemetry')
print(f"Loaded {len(df_loaded)} samples")

# Method 1: Filter after loading (works with fixed format)
high_value_data = df_loaded[df_loaded['sensor_1'] > 40]
print(f"Found {len(high_value_data)} samples with sensor_1 > 40")

# Read time range (using actual column names)
time_segment = df_loaded[(df_loaded['timestamp'] >= 3) & (df_loaded['timestamp'] <= 6)]
print(f"3-6 second segment: {len(time_segment)} samples")


# Method 2: Use table format for where queries (requires recreation)
# First convert to table format with queryable columns
df_loaded.to_hdf('data/sensor_data_table.h5', 
                key='telemetry', 
                mode='w',
                format='table',  # Enables where queries
                data_columns=['sensor_1', 'timestamp', 'throttle_position'],  # Specify queryable columns
                complib='zlib', 
                complevel=9)

# Now where queries work!
high_value_query = pd.read_hdf('data/sensor_data_table.h5', 'telemetry', 
                              where='sensor_1 > 40')
print(f"Where query result: {len(high_value_query)} samples with sensor_1 > 40")
```


> **Info**
> **HDFStore in pandas:**
> `HDFStore` is a high-level interface in pandas for reading, writing, and managing HDF5 files. It allows you to organize data in a hierarchical structure (like folders and files), store multiple DataFrames under different keys, and attach metadata. Use `HDFStore` when you need to:
> - Save or load multiple datasets in one HDF5 file
> - Organize data into logical groups (e.g., sessions, analysis results)
> - Attach metadata or attributes to datasets
> - List available datasets and manage file structure


#### Hierarchical Data Organization Example
```python
# Organize sensor experiment data in a hierarchical structure
with pd.HDFStore('data/sensor_data.h5', mode='w') as store:
    # Example sessions
    store['experiment/session_001'] = session_001_data
    store['experiment/session_002'] = session_002_data
    store['experiment/session_003'] = session_003_data
    
    # Analysis results
    store['analysis/statistics'] = statistics_df
    store['analysis/performance'] = performance_df
    store['analysis/derived_parameters'] = derived_df
    
    # Setup and configuration data
    store['metadata/device_setup'] = setup_parameters_df
    store['metadata/environment_conditions'] = environment_data_df
    store['metadata/experiment_notes'] = experiment_notes_df

print("Sensor experiment data structure created")
```

#### Querying the Hierarchical Structure
```python
# List all available datasets
with pd.HDFStore('data/sensor_data.h5', mode='r') as store:
    print("Available datasets:")
    for key in store.keys():
        try:
            nrows = store.get_storer(key).nrows
            if nrows is None:
                data_shape = store[key].shape
                nrows = data_shape[0]
            print(f"  {key}: {nrows} rows")
        except Exception as e:
            print(f"  {key}: Unable to get row count ({e})")

# Load specific session data
session_data = pd.read_hdf('data/sensor_data.h5', 'telemetry')
# Filter for high values (using actual column names)
high_value_sections = session_data[session_data['sensor_1'] > 50]
```

### Advanced HDF5 Features

#### Metadata and Attributes
```python

# Load telemetry out of sensor data
telemetry = pd.read_hdf('data/sensor_data.h5', 'telemetry')


# Add metadata to datasets
with pd.HDFStore('data/sensor_data.h5', mode='w') as store:
    # Store the main telemetry data
    store['telemetry'] = telemetry
    
    # Add comprehensive metadata (realistic example, but not required for analysis)
    store.get_storer('telemetry').attrs.metadata = {
        'device': 'Multi-sensor Logger 2022',
        'operator': 'Data Acquisition Team',
        'location': 'Test Facility, Example City',
        'experiment_type': 'Sensor Calibration',
        'experiment_date': '2022-05-15',
        'sampling_rate_hz': 1000,
        'coordinate_system': 'device_body_frame',
        'units': {
            'timestamp': 'seconds',
            'sensor_1': 'unitless',
            'sensor_2': 'unitless',
            'sensor_3': 'unitless',
            'steering_angle': 'degrees',
            'throttle_position': 'percent',
            'brake_pressure': 'bar'
        },
        'calibration_date': '2022-05-01',
        'sensor_serial_numbers': {
            'imu': 'IMU-2022-007',
            'gps': 'GPS-2022-008',
            'pressure': 'PR-2022-009'
        },
        'experiment_notes': 'Routine calibration and performance test.'
    }
    
    # Add processing metadata
    store.get_storer('telemetry').attrs.processing = {
        'processing_date': pd.Timestamp.now().isoformat(),
        'software_version': 'DataProcessor v2.1',
        'processing_steps': [
            'outlier_removal_iqr',
            'missing_value_interpolation',
            'moving_average_filter_10ms',
            'coordinate_transformation',
            'gravity_compensation'
        ],
        'quality_metrics': {
            'data_completeness': 0.997,
            'outlier_percentage': 0.003,
            'signal_to_noise_ratio': 45.2
        }
    }

# Read metadata
with pd.HDFStore('data/sensor_data.h5', mode='r') as store:
    metadata = store.get_storer('telemetry').attrs.metadata
    processing_info = store.get_storer('telemetry').attrs.processing
    
    print("Device:", metadata['device'])
    print("Location:", metadata['location'])
    print("Experiment type:", metadata['experiment_type'])
    print("Processing date:", processing_info['processing_date'])
```

#### Efficient Querying Strategies
```python
# Note: These examples require table format with data_columns specified
# Convert to table format first if needed:
# df.to_hdf('data.h5', 'telemetry', format='table', data_columns=['speed', 'steering_angle', 'timestamp'])

# For fixed format (default), use post-load filtering:
df = pd.read_hdf('data/racing_data.h5', 'telemetry')

# Generic filtering examples
filtered_data = df[(abs(df['steering_angle']) > 20) &  # Example: large steering angles
                   (df['sensor_1'] > 35) &
                   (df['timestamp'] >= 2)]

# Time-based filtering for a session
session_start = 3.5   # seconds
session_end = 6.4     # seconds
session_data = df[(df['timestamp'] >= session_start) & (df['timestamp'] <= session_end)]

# Value-specific filtering
high_value_samples = df[abs(df['sensor_2']) > 1.5]  # Example: high values in sensor_2
```

### Performance Comparison

#### File Size Comparison
```python
import os

# Create test dataset
large_dataset = pd.DataFrame({
    'timestamp': np.linspace(0, 3600, 3600000),  # 1 hour at 1000 Hz
    'speed': np.random.normal(100, 20, 3600000),
    'ax': np.random.normal(0, 2, 3600000),
    'ay': np.random.normal(9.81, 1, 3600000),
    'az': np.random.normal(0, 0.5, 3600000),
    'gx': np.random.normal(0, 0.1, 3600000),
    'gy': np.random.normal(0, 0.1, 3600000),
    'gz': np.random.normal(0, 0.1, 3600000),
    'steering': np.random.normal(0, 10, 3600000)
})

# Save in different formats
large_dataset.to_csv('large_dataset.csv', index=False)
large_dataset.to_hdf('large_dataset.h5', key='data', mode='w', complib='zlib', complevel=9)

# Compare file sizes
csv_size = os.path.getsize('large_dataset.csv') / 1e6
hdf5_size = os.path.getsize('large_dataset.h5') / 1e6

print(f"File size comparison (3.6M samples):")
print(f"CSV:     {csv_size:.1f} MB")
print(f"HDF5:    {hdf5_size:.1f} MB  ({csv_size/hdf5_size:.1f}x smaller)")
```

#### Query Performance Comparison
```python
import time

# Time different query methods
def time_query(description, query_func):
    start = time.time()
    result = query_func()
    end = time.time()
    print(f"{description}: {end-start:.3f} seconds ({len(result)} rows)")
    return result

# CSV query (load all, then filter)
def csv_query():
    df = pd.read_csv('large_dataset.csv')
    return df[(df['speed'] > 120) & (df['timestamp'] >= 1800)]

# HDF5 query (load all, then filter - works with fixed format)
def hdf5_query():
    df = pd.read_hdf('large_dataset.h5', 'data')
    return df[(df['speed'] > 120) & (df['timestamp'] >= 1800)]

print("Query performance comparison:")
csv_result = time_query("CSV", csv_query)
hdf5_result = time_query("HDF5", hdf5_query)
```

## Best Practices for HDF5 in Engineering

### 1. **Data Organization**
```python
# Recommended hierarchical structure
/project_data.h5
├── /raw_data
│   ├── /session_001
│   ├── /session_002
│   └── /session_003
├── /processed_data
│   ├── /cleaned
│   ├── /calibrated
│   └── /derived_parameters
├── /analysis_results
│   ├── /statistical_summary
│   ├── /performance_metrics
│   └── /comparative_analysis
└── /metadata
    ├── /calibration_data
    ├── /setup_parameters
    └── /processing_logs
```

### 2. **Chunking Strategy**
```python
# Optimize chunking for your access patterns
# For time series data accessed by time ranges
racing_data.to_hdf('optimized_data.h5', 
                  key='telemetry',
                  mode='w',
                  complib='zlib',
                  complevel=6,           # Balance compression vs speed
                  min_itemsize=50,       # Optimize string columns
                  data_columns=True,     # Enable querying on all columns
                  chunksize=10000)       # Optimize for your typical query size
```

HDF5 provides a robust, high-performance solution for managing large engineering datasets. Its combination of compression, hierarchical organization, and fast querying capabilities makes it ideal for racing telemetry, sensor data, and other time-series engineering applications.