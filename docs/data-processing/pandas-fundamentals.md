---
title: Pandas Fundamentals
---

# Pandas Fundamentals

## Introduction to Pandas

Pandas is Python's premier data manipulation and analysis library, built on top of NumPy. It provides two primary data structures that are perfect for engineering applications: Series (1-dimensional) and DataFrame (2-dimensional).

## Core Data Structures

### Series: One-Dimensional Data
```python
import pandas as pd
import numpy as np

# Create a Series for acceleration data
acceleration_x = pd.Series([0.1, 0.2, 0.15, 0.3], 
                          index=['t1', 't2', 't3', 't4'])
print(acceleration_x)

# Series with automatic index
sensor_readings = pd.Series([9.81, 9.79, 9.82, 9.80])
print(f"Mean: {sensor_readings.mean():.3f}")
print(f"Std: {sensor_readings.std():.3f}")
```

### DataFrame: Two-Dimensional Data
```python
# Create DataFrame for IMU data
imu_data = pd.DataFrame({
    'timestamp': [0.0, 0.001, 0.002, 0.003],
    'ax': [0.1, 0.2, 0.15, 0.3],
    'ay': [9.81, 9.80, 9.82, 9.79],
    'az': [0.05, 0.03, 0.08, 0.06],
    'gx': [0.001, 0.002, 0.001, 0.003],
    'gy': [0.02, 0.025, 0.018, 0.022],
    'gz': [0.003, 0.005, 0.002, 0.008]
})

print(imu_data.head())
print(f"Shape: {imu_data.shape}")
```

## Essential Operations

### Data Loading and Inspection
```python
# Load racing session data
sessions = pd.read_csv('data/racing_sessions.csv')
print(sessions.info())
print(sessions.head())

# Load lap time data
laps = pd.read_csv('data/lap_times.csv')
print(f"Total laps: {len(laps)}")
print(f"Fastest lap: {laps['lap_time_s'].min():.3f}s")

# Load detailed telemetry
telemetry = pd.read_csv('data/telemetry_detailed.csv')
print(f"Telemetry points: {len(telemetry)}")
print(f"Speed range: {telemetry['speed_kmh'].min()}-{telemetry['speed_kmh'].max()} km/h")
```

### Additional Data Loading Examples
```python
# Using the course dataset files
sessions = pd.read_csv('data/racing_sessions.csv')
laps = pd.read_csv('data/lap_times.csv') 
telemetry = pd.read_csv('data/telemetry_detailed.csv')

# Excel format (multi-sheet)
excel_data = pd.read_excel('data/nova_paka_racing_data.xlsx', sheet_name='Sessions')
all_sheets = pd.read_excel('data/nova_paka_racing_data.xlsx', sheet_name=None)

# Basic information about the session data
print(f"Dataset shape: {sessions.shape}")
print(f"Columns: {sessions.columns.tolist()}")
print(f"Data types:\n{sessions.dtypes}")

# Statistical summary
print(sessions.describe())

# Missing values
print(f"Missing values:\n{sessions.isnull().sum()}")

# First and last rows
print("First 5 rows:")
print(sessions.head())
print("Last 5 rows:")
print(sessions.tail())
```

### Data Selection and Filtering
```python
# Using the telemetry dataset for examples
telemetry = pd.read_csv('data/telemetry_detailed.csv')

# Column selection
speed_data = telemetry['speed_kmh']
position_data = telemetry[['distance_m', 'time_s']]

# Row selection by index
first_100_samples = telemetry.iloc[:100]
specific_rows = telemetry.iloc[100:200]

# Boolean indexing (filtering)
high_speed = telemetry[telemetry['speed_kmh'] > 35]
heavy_braking = telemetry[telemetry['brake_pressure_bar'] > 50]

# Multiple conditions
fast_braking = telemetry[(telemetry['speed_kmh'] > 30) & (telemetry['brake_pressure_bar'] > 40)]

# Query method (alternative syntax)
high_rpm = telemetry.query('rpm > 7000')
```

### Data Modification
```python
# Using telemetry data for transformations
telemetry = pd.read_csv('data/telemetry_detailed.csv')

# Add new columns (using telemetry data)
telemetry['speed_ms'] = telemetry['speed_kmh'] / 3.6  # Convert km/h to m/s
telemetry['total_g'] = (telemetry['lateral_g']**2 + telemetry['longitudinal_g']**2)**0.5

# Modify existing columns
telemetry['time_minutes'] = telemetry['time_s'] / 60

# Zero-start time (relative to first timestamp)
telemetry['time_relative'] = telemetry['time_s'] - telemetry['time_s'].iloc[0]

# Drop columns (example with hypothetical unused columns)
# telemetry_reduced = telemetry.drop(['unused_column1', 'unused_column2'], axis=1)

# Rename columns (example with existing columns)
telemetry_renamed = telemetry.rename(columns={
    'speed_kmh': 'velocity_kmh',
    'time_s': 'timestamp_seconds',
    'distance_m': 'position_meters'
})
```

## Data Cleaning

### Handling Missing Values
```python
# Using telemetry data for missing value examples
telemetry = pd.read_csv('data/telemetry_detailed.csv')

# Check for missing values
missing_summary = telemetry.isnull().sum()
print("Missing values per column:")
print(missing_summary[missing_summary > 0])

# Strategy 1: Drop rows with any missing values
telemetry_dropna = telemetry.dropna()

# Strategy 2: Drop rows with too many missing values
threshold = len(telemetry.columns) * 0.7  # Keep rows with at least 70% data
telemetry_threshold = telemetry.dropna(thresh=threshold)

# Strategy 3: Forward fill for short gaps
telemetry_ffill = telemetry.fillna(method='ffill', limit=5)

# Strategy 4: Linear interpolation for sensor data
telemetry_interpolated = telemetry.copy()
telemetry_interpolated['speed_kmh'] = telemetry_interpolated['speed_kmh'].interpolate(method='linear')
telemetry_interpolated['rpm'] = telemetry_interpolated['rpm'].interpolate(method='linear')

# Strategy 5: Fill with specific values
telemetry_filled = telemetry.fillna({
    'speed_kmh': 0,
    'steering_angle_deg': 0,
    'throttle_percent': telemetry['throttle_percent'].mean()
})
```

### Outlier Detection and Removal
```python
# Using telemetry data for transformations
telemetry = pd.read_csv('data/telemetry_detailed.csv')

def detect_outliers_iqr(data, column):
    """Detect outliers using Interquartile Range method"""
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = data[(data[column] < lower_bound) | 
                   (data[column] > upper_bound)]
    return outliers, lower_bound, upper_bound

# Detect outliers using telemetry data
telemetry = pd.read_csv('data/telemetry_detailed.csv')
outliers, lower, upper = detect_outliers_iqr(telemetry, 'lateral_g')
print(f"Found {len(outliers)} outliers in lateral_g")
print(f"Valid range: [{lower:.3f}, {upper:.3f}] g")

# Remove outliers
def remove_outliers_iqr(data, columns):
    """Remove outliers from specified columns using IQR method"""
    telemetry_clean = data.copy()
    
    for column in columns:
        Q1 = telemetry_clean[column].quantile(0.25)
        Q3 = telemetry_clean[column].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        
        # Keep only values within bounds
        mask = (telemetry_clean[column] >= lower) & (telemetry_clean[column] <= upper)
        telemetry_clean = telemetry_clean[mask]
    
    return telemetry_clean

# Apply to g-force channels
gforce_columns = ['lateral_g', 'longitudinal_g']
telemetry_clean = remove_outliers_iqr(telemetry, gforce_columns)
print(f"Removed {len(telemetry) - len(telemetry_clean)} outlier samples")
```

## Basic Statistical Operations

### Descriptive Statistics
```python
# Using telemetry data for statistical examples
telemetry = pd.read_csv('data/telemetry_detailed.csv')

# Single column statistics
print(f"Speed - Mean: {telemetry['speed_kmh'].mean():.2f} km/h")
print(f"Speed - Median: {telemetry['speed_kmh'].median():.2f} km/h")
print(f"Speed - Std: {telemetry['speed_kmh'].std():.2f} km/h")
print(f"Speed - Min/Max: {telemetry['speed_kmh'].min():.1f} / {telemetry['speed_kmh'].max():.1f} km/h")

# Multiple columns
stats_summary = telemetry[['speed_kmh', 'lateral_g', 'longitudinal_g', 'rpm']].describe()
print(stats_summary)

# Custom percentiles
percentiles = telemetry['speed_kmh'].quantile([0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99])
print("Speed percentiles:")
print(percentiles)
```

### Correlation Analysis
```python
# Using telemetry data for transformations
telemetry = pd.read_csv('data/telemetry_detailed.csv')

# Correlation matrix using telemetry data
correlation_matrix = telemetry[['speed_kmh', 'lateral_g', 'longitudinal_g', 'steering_angle_deg']].corr()
print("Correlation matrix:")
print(correlation_matrix)

# Specific correlations
speed_steering_corr = telemetry['speed_kmh'].corr(telemetry['steering_angle_deg'])
print(f"Speed-Steering correlation: {speed_steering_corr:.3f}")
```

## Data Transformation

### Mathematical Operations
```python
# Using telemetry data for transformations
telemetry = pd.read_csv('data/telemetry_detailed.csv')

# Element-wise operations
telemetry['speed_squared'] = telemetry['speed_kmh'] ** 2
telemetry['g_force_magnitude'] = np.sqrt(telemetry['lateral_g']**2 + telemetry['longitudinal_g']**2)

# Trigonometric functions
telemetry['steering_rad'] = np.radians(telemetry['steering_angle_deg'])
telemetry['steering_sin'] = np.sin(telemetry['steering_rad'])

# Logarithmic transformations
telemetry['speed_log'] = np.log1p(telemetry['speed_kmh'])  # log(1+x) to handle zeros

# Normalization
telemetry['speed_normalized'] = (telemetry['speed_kmh'] - telemetry['speed_kmh'].mean()) / telemetry['speed_kmh'].std()

# Min-max scaling
telemetry['speed_scaled'] = (telemetry['speed_kmh'] - telemetry['speed_kmh'].min()) / (telemetry['speed_kmh'].max() - telemetry['speed_kmh'].min())
```

### Binning and Categorization
```python
# Using telemetry data for transformations
telemetry = pd.read_csv('data/telemetry_detailed.csv')

# Create speed categories using telemetry data
speed_bins = [0, 30, 60, 100, 150, 300]
speed_labels = ['Very Low', 'Low', 'Medium', 'High', 'Very High']
telemetry['speed_category'] = pd.cut(telemetry['speed_kmh'], bins=speed_bins, labels=speed_labels)

# Equal-width binning
telemetry['lateral_g_quartiles'] = pd.qcut(telemetry['lateral_g'], q=4, labels=['Q1', 'Q2', 'Q3', 'Q4'])

# Custom conditions
conditions = [
    (telemetry['speed_kmh'] < 50),
    (telemetry['speed_kmh'] >= 50) & (telemetry['speed_kmh'] < 100),
    (telemetry['speed_kmh'] >= 100)
]
choices = ['City', 'Highway', 'Racing']
telemetry['driving_mode'] = np.select(conditions, choices, default='Unknown')
```

## File I/O Operations

### Reading Data
```python
# CSV with custom parameters (using course dataset)
telemetry = pd.read_csv('data/telemetry_detailed.csv')

# Excel with multiple sheets (using course dataset)
sessions_excel = pd.read_excel('data/nova_paka_racing_data.xlsx', sheet_name='Sessions')
all_sheets = pd.read_excel('data/nova_paka_racing_data.xlsx', sheet_name=None)  # All sheets

# Example with custom CSV parameters (hypothetical)
# df = pd.read_csv('custom_data.csv', 
#                 sep=';',           # Different separator
#                 decimal=',',       # European decimal format
#                 encoding='utf-8',  # Character encoding
#                 skiprows=2,        # Skip header rows
#                 nrows=10000,       # Read only first 10k rows
#                 usecols=['timestamp', 'speed', 'ax', 'ay'],  # Specific columns
#                 dtype={'speed': 'float32'},  # Specify data types
#                 parse_dates=['timestamp'])   # Parse dates
```

### Writing Data
```python
# CSV export (using telemetry data)
telemetry.to_csv('processed_data.csv', 
          index=False,           # Don't save index
          float_format='%.6f',   # Control decimal places
          sep=';',               # Custom separator
          encoding='utf-8')      # Character encoding

# Excel export
telemetry.to_excel('analysis_results.xlsx', 
           sheet_name='Processed_Data',
           index=False,
           float_format='%.3f')

# Multiple sheets
with pd.ExcelWriter('race_analysis.xlsx') as writer:
    telemetry.to_excel(writer, sheet_name='Raw_Data', index=False)

# JSON export
telemetry.to_json('telemetry_export.json', 
          orient='records',      # Array of objects
          date_format='iso',     # ISO date format
          indent=2)              # Pretty formatting
```

## Performance Tips

### Memory Optimization
```python
# Check memory usage (using telemetry data)
telemetry = pd.read_csv('data/telemetry_detailed.csv')
print(f"Memory usage: {telemetry.memory_usage(deep=True).sum() / 1e6:.1f} MB")

# Optimize data types
def optimize_dtypes(telemetry_data):
    """Optimize DataFrame memory usage"""
    original_size = telemetry_data.memory_usage(deep=True).sum()
    
    # Optimize float columns
    for col in telemetry_data.select_dtypes(include=['float64']):
        col_min = telemetry_data[col].min()
        col_max = telemetry_data[col].max()
        
        if col_min > np.finfo(np.float32).min and col_max < np.finfo(np.float32).max:
            telemetry_data[col] = pd.to_numeric(telemetry_data[col], downcast='float')
    
    # Optimize integer columns
    for col in telemetry_data.select_dtypes(include=['int64']):
        col_min = telemetry_data[col].min()
        col_max = telemetry_data[col].max()
        
        if col_min > np.iinfo(np.int32).min and col_max < np.iinfo(np.int32).max:
            telemetry_data[col] = pd.to_numeric(telemetry_data[col], downcast='integer')
    
    optimized_size = telemetry_data.memory_usage(deep=True).sum()
    print(f"Memory reduced from {original_size/1e6:.1f} MB to {optimized_size/1e6:.1f} MB")
    print(f"Reduction factor: {original_size/optimized_size:.1f}x")
    
    return telemetry_data

telemetry_optimized = optimize_dtypes(telemetry.copy())
```

### Vectorized Operations
```python
# Using telemetry data for vectorized operations
telemetry = pd.read_csv('data/telemetry_detailed.csv')

# Avoid loops - use vectorized operations
# BAD: Loop through rows
results = []
for index, row in telemetry.iterrows():
    result = row['lateral_g'] * row['speed_kmh'] / 3.6
    results.append(result)
telemetry['bad_calculation'] = results

# GOOD: Vectorized operation
telemetry['good_calculation'] = telemetry['lateral_g'] * telemetry['speed_kmh'] / 3.6

# Use .apply() for complex operations
def complex_calculation(row):
    return np.sqrt(row['lateral_g']**2 + row['longitudinal_g']**2) * row['speed_kmh']

telemetry['complex_result'] = telemetry.apply(complex_calculation, axis=1)

# Even better: Pure vectorized
telemetry['complex_result_vectorized'] = np.sqrt(telemetry['lateral_g']**2 + telemetry['longitudinal_g']**2) * telemetry['speed_kmh']
```

## Best Practices

### Code Organization
```python
# Create reusable functions
def load_telemetry_data(filename):
    """Load and basic preprocessing of telemetry data"""
    telemetry_data = pd.read_csv(filename)
    
    # Basic validation
    required_columns = ['time_s', 'speed_kmh', 'lateral_g', 'longitudinal_g', 'rpm']
    missing_columns = set(required_columns) - set(telemetry_data.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    # Sort by timestamp
    telemetry_data = telemetry_data.sort_values('time_s').reset_index(drop=True)
    
    return telemetry_data

def validate_sensor_data(telemetry_data):
    """Validate sensor data ranges"""
    validation_rules = {
        'speed_kmh': (0, 350),           # km/h
        'lateral_g': (-3, 3),            # g-force
        'longitudinal_g': (-3, 3),       # g-force
        'rpm': (0, 10000),               # engine RPM
        'steering_angle_deg': (-720, 720)  # degrees
    }
    
    issues = []
    for column, (min_val, max_val) in validation_rules.items():
        if column in telemetry_data.columns:
            out_of_range = telemetry_data[(telemetry_data[column] < min_val) | (telemetry_data[column] > max_val)]
            if len(out_of_range) > 0:
                issues.append(f"{column}: {len(out_of_range)} values out of range [{min_val}, {max_val}]")
    
    return issues

# Use the functions
telemetry = load_telemetry_data('data/telemetry_detailed.csv')
validation_issues = validate_sensor_data(telemetry)
if validation_issues:
    print("Data validation issues:")
    for issue in validation_issues:
        print(f"  - {issue}")
```

### Documentation and Metadata
```python
# Document your data processing steps (using telemetry data)
telemetry_raw = pd.read_csv('data/telemetry_detailed.csv')
telemetry_processed = telemetry_raw.copy()  # After processing steps

processing_log = {
    'source_file': 'data/telemetry_detailed.csv',
    'processing_date': pd.Timestamp.now().isoformat(),
    'steps': [
        'loaded_raw_data',
        'removed_outliers_iqr',
        'interpolated_missing_values',
        'applied_moving_average_filter',
        'calculated_derived_parameters'
    ],
    'data_quality': {
        'original_samples': len(telemetry_raw),
        'final_samples': len(telemetry_processed),
        'retention_rate': len(telemetry_processed) / len(telemetry_raw)
    }
}

# Save processing metadata
import json
with open('processing_log.json', 'w') as f:
    json.dump(processing_log, f, indent=2)
```

This covers the fundamental pandas operations you'll need for most data processing tasks. The next documents will build on these basics with more advanced operations and specific use cases.