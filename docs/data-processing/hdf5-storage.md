---
title: High-Performance Data Storage with HDF5
---

# High-Performance Data Storage with HDF5

## The Big Data Challenge in Engineering

Modern engineering applications generate massive amounts of sensor data. Consider an autocross car's data acquisition system competing at the famous Nova Paka track in Czech Republic:

- **Track specifications**: 930m length, clay-sandy surface, 37m elevation change
- **Sampling rates**: 1000+ Hz per channel
- **Channel count**: 60-80+ sensors (engine, suspension, steering, IMU, GPS, surface grip)
- **Run duration**: Competition runs (60-90 sec for 930m track)
- **Event duration**: European Championship event (2-3 days with practice and competition)
- **Data volume**: ~800 million data points per championship event

**Storage Challenge Example:**
- 75 channels × 1000 Hz × 25200 seconds (7 hours event) = 1.89 billion values
- CSV format: ~28 GB per championship event
- Memory requirements: 10-18 GB RAM for comparative analysis across runs
- Query time: Minutes to find specific track sections or surface conditions

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

### Basic HDF5 Operations with Pandas

#### Writing Data to HDF5
```python
# Create sample autocross racing data for Nova Paka track
np.random.seed(42)
n_samples = 75000  # 75 seconds at 1000 Hz (typical run time for 930m track)
timestamps = np.linspace(0, 75, n_samples)

# Generate realistic Nova Paka autocross telemetry data
# Clay-sandy surface allows for different driving characteristics
racing_data = pd.DataFrame({
    'timestamp': timestamps,
    'speed': 35 + 25 * np.sin(0.085 * timestamps) + np.random.normal(0, 4, n_samples),
    'ax': 1.8 * np.sin(0.11 * timestamps) + np.random.normal(0, 1.2, n_samples),
    'ay': np.random.normal(0, 2.5, n_samples),  # Higher lateral g's on clay-sand
    'az': 9.81 + np.random.normal(0, 0.4, n_samples),
    'steering_angle': 50 * np.sin(0.07 * timestamps) + np.random.normal(0, 8, n_samples),
    'throttle_position': np.clip(55 + 35 * np.sin(0.09 * timestamps) + np.random.normal(0, 12, n_samples), 0, 100),
    'brake_pressure': np.maximum(0, 25 * np.sin(0.13 * timestamps + np.pi) + np.random.normal(0, 6, n_samples)),
    'suspension_travel_fl': 50 + 30 * np.sin(0.12 * timestamps) + np.random.normal(0, 8, n_samples),  # Front left
    'suspension_travel_fr': 50 + 30 * np.sin(0.12 * timestamps + 0.1) + np.random.normal(0, 8, n_samples)  # Front right
})

# Ensure realistic speed limits for 930m clay-sand autocross track
racing_data['speed'] = np.clip(racing_data['speed'], 0, 75)  # Max ~75 km/h for clay-sand surface
racing_data['suspension_travel_fl'] = np.clip(racing_data['suspension_travel_fl'], 0, 100)  # 0-100mm travel
racing_data['suspension_travel_fr'] = np.clip(racing_data['suspension_travel_fr'], 0, 100)

# Save to HDF5 with compression
racing_data.to_hdf('data/racing_data.h5', 
                  key='telemetry', 
                  mode='w',
                  complib='zlib',    # Compression algorithm
                  complevel=9)       # Maximum compression

print(f"Saved {len(racing_data)} samples to HDF5")
```

#### Reading Data from HDF5
```python
# Read entire dataset
df_loaded = pd.read_hdf('data/racing_data.h5', 'telemetry')
print(f"Loaded {len(df_loaded)} samples")

# Method 1: Filter after loading (works with fixed format)
high_speed_data = df_loaded[df_loaded['speed'] > 40]
print(f"Found {len(high_speed_data)} high-speed samples")

# Read time range (using actual column names)
time_segment = df_loaded[(df_loaded['timestamp'] >= 30) & (df_loaded['timestamp'] <= 60)]
print(f"30-60 second segment: {len(time_segment)} samples")

# Method 2: Use table format for where queries (requires recreation)
# First convert to table format with queryable columns
df_loaded.to_hdf('data/racing_data_table.h5', 
                key='telemetry', 
                mode='w',
                format='table',  # Enables where queries
                data_columns=['speed', 'timestamp', 'throttle_position'],  # Specify queryable columns
                complib='zlib', 
                complevel=9)

# Now where queries work!
high_speed_query = pd.read_hdf('data/racing_data_table.h5', 'telemetry', 
                              where='speed > 40')
print(f"Where query result: {len(high_speed_query)} high-speed samples")
```

### Hierarchical Data Organization

#### Race Weekend Structure
```python
# Organize complete Nova Paka European Championship event data
with pd.HDFStore('data/racing_data.h5', mode='w') as store:
    # Practice sessions on different days
    store['practice/friday_morning'] = friday_morning_practice
    store['practice/friday_afternoon'] = friday_afternoon_practice
    store['practice/saturday_warmup'] = saturday_warmup
    
    # European Championship competition runs
    store['championship/qualifying_run1'] = qualifying_run1_data
    store['championship/qualifying_run2'] = qualifying_run2_data
    store['championship/semifinal_run1'] = semifinal_run1_data
    store['championship/semifinal_run2'] = semifinal_run2_data
    store['championship/final_run'] = final_run_data
    
    # Different surface conditions (clay-sand changes with weather)
    store['conditions/dry_clay'] = dry_conditions_runs
    store['conditions/wet_clay'] = wet_conditions_runs
    store['conditions/optimal_grip'] = optimal_grip_runs
    
    # Post-processed analysis results
    store['analysis/run_times'] = run_analysis_df
    store['analysis/sector_times'] = sector_analysis_df
    store['analysis/surface_grip_analysis'] = grip_analysis_df
    store['analysis/elevation_performance'] = elevation_analysis_df
    
    # Setup and configuration data
    store['metadata/vehicle_setup'] = setup_parameters_df
    store['metadata/weather_conditions'] = weather_data_df
    store['metadata/track_conditions'] = track_surface_df
    store['metadata/european_championship_rules'] = championship_rules_df

print("Nova Paka European Championship event data structure created")
```

#### Querying the Hierarchical Structure
```python
# List all available datasets
with pd.HDFStore('data/racing_data.h5', mode='r') as store:
    print("Available datasets:")
    for key in store.keys():
        # For fixed format, we need to read the shape instead of using nrows
        try:
            nrows = store.get_storer(key).nrows
            if nrows is None:
                # For fixed format, get the shape directly
                data_shape = store[key].shape
                nrows = data_shape[0]
            print(f"  {key}: {nrows} rows")
        except Exception as e:
            print(f"  {key}: Unable to get row count ({e})")

# Load specific championship run data
high_speed_sections = pd.read_hdf('data/racing_data.h5', 'telemetry')
# Filter for high-speed sections (using actual column names)
high_speed_sections = high_speed_sections[high_speed_sections['speed'] > 50]
```

### Advanced HDF5 Features

#### Metadata and Attributes
```python
# load telemetry out of racing data racing data
telemetry = pd.read_hdf('data/racing_data.h5', 'telemetry')

# Add metadata to datasets
with pd.HDFStore('data/racing_data.h5', mode='w') as store:
    # Store the main telemetry data
    store['telemetry'] = telemetry
    
    # Add comprehensive metadata
    store.get_storer('telemetry').attrs.metadata = {
        'vehicle': 'Autocross Championship Car 2016',
        'driver': 'Philipp Höglinger',
        'track': 'Nova Paka Autocross Track',
        'track_location': 'Štikovská rokle, Nova Paka, Czech Republic',
        'track_length': 930,  # meters (official track length)
        'track_width': '10-20m',  # variable width
        'track_elevation_change': 37,  # meters (cant)
        'track_surface': 'Clay-sandy (aluminous-sandy)',
        'track_type': 'European Championship level',
        'weather': 'Partly cloudy, 18°C, Wind: 8 km/h NE',
        'tire_compound': 'All-terrain (suitable for clay-sand)',
        'fuel_load': 'Competition level (15L)',
        'session_type': 'European Championship Qualifying',
        'session_date': '2016-07-03',
        'sampling_rate_hz': 1000,
        'coordinate_system': 'vehicle_body_frame',
        'units': {
            'timestamp': 'seconds',
            'speed': 'km/h',
            'acceleration': 'm/s²',
            'angular_velocity': 'rad/s',
            'steering_angle': 'degrees'
        },
        'calibration_date': '2014-09-01',
        'sensor_serial_numbers': {
            'imu': 'IMU-2014-007',
            'gps': 'GPS-2014-008',
            'wheel_speed': 'WS-2014-009'
        },
        'track_notes': 'Unique European track in ravine terrain, clay-sandy surface, double barrier protection, FIA fence, asphalt start section'
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
with pd.HDFStore('data/racing_data.h5', mode='r') as store:
    metadata = store.get_storer('telemetry').attrs.metadata
    processing_info = store.get_storer('telemetry').attrs.processing
    
    print("Vehicle:", metadata['vehicle'])
    print("Track:", metadata['track'])
    print("Location:", metadata['track_location'])
    print("Processing date:", processing_info['processing_date'])
```

#### Efficient Querying Strategies
```python
# Note: These examples require table format with data_columns specified
# Convert to table format first if needed:
# df.to_hdf('data.h5', 'telemetry', format='table', data_columns=['speed', 'steering_angle', 'timestamp'])

# For fixed format (default), use post-load filtering:
df = pd.read_hdf('data/racing_data.h5', 'telemetry')

# Complex filtering with multiple conditions for clay-sand surface
cornering_data = df[(abs(df['steering_angle']) > 20) &  # More steering on clay-sand
                   (df['speed'] > 35) &
                   (df['timestamp'] >= 20)]

# Time-based filtering for 930m track
run_start = 3.5   # seconds (after asphalt start section)
run_end = 62.4    # seconds (typical completion time)
run_data = df[(df['timestamp'] >= run_start) & (df['timestamp'] <= run_end)]

# Surface-specific filtering for clay-sand conditions
high_grip_samples = df[abs(df['ay']) > 1.5]  # High lateral g on good grip sections
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