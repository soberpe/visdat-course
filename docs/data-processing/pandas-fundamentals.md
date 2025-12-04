---
title: Pandas Fundamentals
---

# Pandas Fundamentals


## Introduction to Pandas



Pandas was created in 2008 by Wes McKinney to address the lack of flexible, high-performance data analysis tools in Python. Before pandas, data manipulation in Python relied on basic lists, dictionaries, and NumPy arrays—powerful for numerical work, but cumbersome for tabular, labeled, or time series data.

**The leap:** Pandas introduced the DataFrame and Series, bringing spreadsheet-like, labeled, and relational data handling to Python. This made tasks like filtering, grouping, joining, and time series analysis much easier and more expressive, and enabled Python to become a leading language for data science and engineering.


> **Info**
> All code examples use the provided dummy sensor dataset (`sensor_data.csv`). Column names (e.g. `speed_kmh`, `lateral_g`, etc.) are illustrative and may differ in your own data.

## Core Data Structures
Learn how pandas represents and organizes data. Series and DataFrames are the foundation for all analysis and manipulation.



### Series: One-Dimensional Data
A **Series** is a one-dimensional labeled array, similar to a column in a spreadsheet. Use Series for handling single columns or sensor channels with labels and fast operations.

**Series Example:**
```python
import pandas as pd
speed_series = pd.Series([10, 35, 50, 80, 120], name='speed_kmh')
print(speed_series)
```

### DataFrames: Two-Dimensional Data
A **DataFrame** is a two-dimensional table of data, like an entire spreadsheet, with rows and columns. DataFrames are the core structure in pandas for working with tabular data.

DataFrames allow you to organize, inspect, and manipulate data efficiently. Once you understand their structure, you can select, filter, and transform data for analysis.

**DataFrame Example:**
```python
data = {
    'speed_kmh': [10, 35, 50, 80, 120],
    'distance_m': [0, 100, 200, 300, 400],
    'time_s': [0, 1, 2, 3, 4],
    'brake_pressure_bar': [0, 10, 20, 30, 40],
    'rpm': [1000, 3000, 5000, 7000, 9000]
}
telemetry = pd.DataFrame(data)
print(telemetry)
```

### Data Selection and Filtering
Select columns, rows, and filter data using conditions.
```python
# Column selection
speed_data = telemetry['speed_kmh']
position_data = telemetry[['distance_m', 'time_s']]

# Row selection by index
first_3_samples = telemetry.iloc[:3]
specific_rows = telemetry.iloc[2:4]

# Boolean indexing (filtering)
high_speed = telemetry[telemetry['speed_kmh'] > 35]
heavy_braking = telemetry[telemetry['brake_pressure_bar'] > 20]

# Multiple conditions
fast_braking = telemetry[(telemetry['speed_kmh'] > 30) & (telemetry['brake_pressure_bar'] > 10)]

# Query method (alternative syntax)
```python
```


### Data Modification
Add, change, or remove columns to create new features or clean up your dataset.
```python
# Add new columns
telemetry['speed_ms'] = telemetry['speed_kmh'] / 3.6  # Convert km/h to m/s
telemetry['total_g'] = (telemetry.get('lateral_g', 0)**2 + telemetry.get('longitudinal_g', 0)**2)**0.5

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

### Data Selection and Filtering
Extract relevant rows and columns to focus your analysis on the data that matters.
```python
# Using the telemetry dataset for examples
telemetry = pd.read_csv('data/sensor_data.csv')

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
Add, change, or remove columns to create new features or clean up your dataset.
```python
# Using telemetry data for transformations
telemetry = pd.read_csv('data/sensor_data.csv')

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
Prepare your data by handling missing values and removing outliers for reliable analysis.


### Handling Missing Values
Deal with gaps in your data using strategies like dropping, filling, or interpolation.
```python
# Using telemetry data for missing value examples
telemetry = pd.read_csv('data/sensor_data.csv')

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
Identify and remove extreme values that could distort your analysis.
```python
# Using telemetry data for transformations
telemetry = pd.read_csv('data/sensor_data.csv')

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
telemetry = pd.read_csv('data/sensor_data.csv')
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
Summarize your data and discover patterns using descriptive statistics and correlations.


### Descriptive Statistics
Calculate means, medians, percentiles, and more to understand your data’s distribution.
```python
# Using telemetry data for statistical examples
telemetry = pd.read_csv('data/sensor_data.csv')

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
Find relationships between variables to reveal dependencies and trends.
```python
# Using telemetry data for transformations
telemetry = pd.read_csv('data/sensor_data.csv')

# Correlation matrix using telemetry data
correlation_matrix = telemetry[['speed_kmh', 'lateral_g', 'longitudinal_g', 'steering_angle_deg']].corr()
print("Correlation matrix:")
print(correlation_matrix)

# Specific correlations
speed_steering_corr = telemetry['speed_kmh'].corr(telemetry['steering_angle_deg'])
print(f"Speed-Steering correlation: {speed_steering_corr:.3f}")
```


## Data Transformation
Apply mathematical operations, scaling, and categorization to create new insights from your data.




### Mathematical Operations
Use arithmetic, trigonometric, and normalization functions to process and analyze sensor data.
```python
# Using telemetry data for transformations
telemetry = pd.read_csv('data/sensor_data.csv')

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
Group continuous data into categories for easier analysis and visualization.
```python
# Using telemetry data for transformations
telemetry = pd.read_csv('data/sensor_data.csv')

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
Read and write data in various formats to share results or work with other tools.

### Reading Data
Import data from CSV, Excel, and other formats with flexible options.
```python
# CSV with custom parameters (using course dataset)
telemetry = pd.read_csv('data/sensor_data.csv')

# Excel with multiple sheets (using course dataset)
sessions_excel = pd.read_excel('data/sensor_data.xlsx', sheet_name='Sessions')
all_sheets = pd.read_excel('data/sensor_data.xlsx', sheet_name=None)  # All sheets

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
Export your processed data for reporting, sharing, or further analysis.
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
Optimize memory usage and speed for large datasets and efficient workflows.


### Memory Optimization
Reduce memory footprint by adjusting data types and using efficient pandas features.
```python
# Check memory usage (using telemetry data)
telemetry = pd.read_csv('data/sensor_data.csv')
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
Speed up calculations by using pandas’ built-in vectorized operations instead of slow loops.
```python
# Using telemetry data for vectorized operations
telemetry = pd.read_csv('data/sensor_data.csv')

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

#### Applying a Function to Each Row: 3D Vector Transformation Example
You can use `.apply()` to perform complex operations on each row of a DataFrame. For example, transforming a body-fixed vector to global coordinates using reference points and orientation angles:
```python
import pandas as pd
import numpy as np

# Example DataFrame: each row has a reference point, body-fixed vector, and orientation angles
df = pd.DataFrame({
    'ref_x': [100, 200],
    'ref_y': [50, 60],
    'ref_z': [20, 30],
    'body_x': [1, 0],
    'body_y': [0, 1],
    'body_z': [0, 0],
    'yaw_deg': [30, 45],
    'pitch_deg': [10, 0],
    'roll_deg': [5, -10]
})

def rotation_matrix(yaw_deg, pitch_deg, roll_deg):
    yaw = np.radians(yaw_deg)
    pitch = np.radians(pitch_deg)
    roll = np.radians(roll_deg)
    Rz = np.array([
        [np.cos(yaw), -np.sin(yaw), 0],
        [np.sin(yaw),  np.cos(yaw), 0],
        [0, 0, 1]
    ])
    Ry = np.array([
        [np.cos(pitch), 0, np.sin(pitch)],
        [0, 1, 0],
        [-np.sin(pitch), 0, np.cos(pitch)]
    ])
    Rx = np.array([
        [1, 0, 0],
        [0, np.cos(roll), -np.sin(roll)],
        [0, np.sin(roll),  np.cos(roll)]
    ])
    return Rz @ Ry @ Rx

def transform_row(row):
    p_ref = np.array([row['ref_x'], row['ref_y'], row['ref_z']])
    v_body = np.array([row['body_x'], row['body_y'], row['body_z']])
    R = rotation_matrix(row['yaw_deg'], row['pitch_deg'], row['roll_deg'])
    v_global = R @ v_body + p_ref
    return pd.Series({'global_x': v_global[0], 'global_y': v_global[1], 'global_z': v_global[2]})

# Apply transformation to each row
df[['global_x', 'global_y', 'global_z']] = df.apply(transform_row, axis=1)
print(df[['ref_x', 'ref_y', 'ref_z', 'body_x', 'body_y', 'body_z', 'global_x', 'global_y', 'global_z']])
```


## Best Practices
Organize your code and document your workflow for reproducible, maintainable analysis.


### Code Organization
Write reusable functions and validate your data for robust analysis.
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
telemetry = load_telemetry_data('data/sensor_data.csv')
validation_issues = validate_sensor_data(telemetry)
if validation_issues:
    print("Data validation issues:")
    for issue in validation_issues:
        print(f"  - {issue}")
```


### Documentation and Metadata
Keep track of your processing steps and data quality for transparency and reproducibility.
```python
# Document your data processing steps (using telemetry data)
telemetry_raw = pd.read_csv('data/sensor_data.csv')
telemetry_processed = telemetry_raw.copy()  # After processing steps

processing_log = {
    'source_file': 'data/sensor_data.csv',
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