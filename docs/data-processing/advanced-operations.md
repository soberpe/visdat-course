---
title: Advanced Pandas Operations
---

# Advanced Pandas Operations

This document covers sophisticated pandas operations for complex data analysis tasks, including time series analysis, groupby operations, window functions, and advanced transformations.

## Time Series Analysis

### Setting Up Time-Based Index

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Load racing telemetry data
df = pd.read_csv('data/telemetry_detailed.csv')

# Convert timestamp to datetime (assuming start time is a reference point)
base_time = datetime(2016, 7, 3, 14, 30, 0)  # Nova Paka qualifying start
df['datetime'] = base_time + pd.to_timedelta(df['time_s'], unit='s')

# Set datetime as index for time series operations
df_ts = df.set_index('datetime')

print(f"Time range: {df_ts.index.min()} to {df_ts.index.max()}")
print(f"Sampling frequency: {1/df['time_s'].diff().mean():.0f} Hz")

# For frequency inference to work, we need regular intervals
# Let's check the actual sampling rate
time_diff = df['time_s'].diff().dropna()
print(f"Average time step: {time_diff.mean():.6f} seconds")
print(f"Time step std: {time_diff.std():.6f} seconds")

# Try to infer frequency (this works better with regular intervals)
try:
    freq = pd.infer_freq(df_ts.index)
    print(f"Inferred frequency: {freq}")
except:
    print("Could not infer frequency - irregular sampling detected")
```

### Resampling and Frequency Conversion

```python
# Resample to different frequencies (only numeric columns)
numeric_cols = df_ts.select_dtypes(include=[np.number]).columns
df_numeric = df_ts[numeric_cols]

df_1s = df_numeric.resample('1s').mean()      # 1 Hz (1-second intervals)
df_100ms = df_numeric.resample('100ms').mean()  # 10 Hz
df_10ms = df_numeric.resample('10ms').mean()    # 100 Hz

print(f"Original data: {df_ts.shape}")
print(f"Numeric columns: {list(numeric_cols)}")
print(f"1s resampled: {df_1s.shape}")

# Different aggregation methods per column
df_resampled = df_numeric.resample('1s').agg({
    'speed_kmh': 'mean',
    'rpm': 'mean',
    'lateral_g': 'mean',
    'longitudinal_g': 'mean',
    'steering_angle_deg': 'mean',
    'brake_pressure_bar': 'max',
    'throttle_percent': 'mean'
})

print(f"Resampled with different aggregations: {df_resampled.shape}")

# Upsampling with interpolation (only on numeric data)
df_upsampled = df_numeric.resample('1ms').interpolate(method='linear')

# Handle irregular time series  
df_regular = df_numeric.asfreq('10ms', method='ffill')  # Forward fill gaps

print(f"Upsampled to 1ms: {df_upsampled.shape}")
print(f"Regular 10ms grid: {df_regular.shape}")

# Custom resampling function
def rms_resample(series):
    """Calculate RMS (Root Mean Square) for resampling"""
    return np.sqrt(np.mean(series**2))

df_rms = df_numeric.resample('1s').agg({
    'lateral_g': rms_resample,
    'longitudinal_g': rms_resample
})
```

### Rolling Window Operations

```python
# Simple rolling averages
window_size = 100  # 100 samples
df_ts['speed_ma'] = df_ts['speed_kmh'].rolling(window=window_size).mean()
df_ts['speed_std'] = df_ts['speed_kmh'].rolling(window=window_size).std()

# Time-based windows
df_ts['speed_ma_1s'] = df_ts['speed_kmh'].rolling('1s').mean()
df_ts['lateral_g_rms'] = df_ts['lateral_g'].rolling('1s').apply(lambda x: np.sqrt(np.mean(x**2)))

# Multiple statistics in one operation
rolling_stats = df_ts['speed_kmh'].rolling('5s').agg({
    'mean': 'mean',
    'std': 'std',
    'min': 'min',
    'max': 'max',
    'range': lambda x: x.max() - x.min()
})

# Centered windows (look ahead and behind)
df_ts['speed_centered'] = df_ts['speed_kmh'].rolling(window=50, center=True).mean()

print(f"Rolling statistics shape: {rolling_stats.shape}")
print("Speed rolling stats sample:")
print(rolling_stats.head())

# Custom rolling functions
def rolling_percentile(series, percentile=95):
    return series.quantile(percentile/100)

df_ts['speed_95th'] = df_ts['speed_kmh'].rolling('10s').apply(
    lambda x: rolling_percentile(x, 95)
)

# Exponentially weighted moving average
df_ts['speed_ewm'] = df_ts['speed_kmh'].ewm(span=50).mean()
df_ts['speed_ewm_var'] = df_ts['speed_kmh'].ewm(span=50).var()
```

### Expanding Window Operations

```python
# Session-long performance tracking (using available columns)
df_ts['best_speed_so_far'] = df_ts['speed_kmh'].expanding().max()
df_ts['avg_rpm_so_far'] = df_ts['rpm'].expanding().mean()
df_ts['speed_consistency'] = df_ts['speed_kmh'].expanding().std()

# Custom expanding functions
def expanding_efficiency(speed_series):
    """Calculate fuel efficiency trend"""
    return speed_series.mean() / (speed_series.std() + 1e-6)

df_ts['efficiency_trend'] = df_ts['speed_kmh'].expanding().apply(expanding_efficiency)

print("Expanding window operations completed")
print(f"Best speed so far at end: {df_ts['best_speed_so_far'].iloc[-1]:.1f} km/h")
print(f"Final speed consistency: {df_ts['speed_consistency'].iloc[-1]:.2f}")
```

## GroupBy Operations

### Basic Grouping Concepts

```python
# Nova Paka track specifications (from course metadata)
track_length = 930  # meters

# Assume we have lap numbers in our data
df['lap_number'] = (df['distance_m'] // track_length).astype(int)

# Basic groupby operations (using actual column names)
lap_stats = df.groupby('lap_number').agg({
    'speed_kmh': ['mean', 'max', 'std'],
    'lateral_g': ['max', 'mean'],
    'rpm': ['mean', 'max'],
    'time_s': ['min', 'max']  # Start and end times
})

# Flatten multi-level column names
lap_stats.columns = ['_'.join(col).strip() for col in lap_stats.columns]

# Calculate lap times
lap_stats['lap_time'] = lap_stats['time_s_max'] - lap_stats['time_s_min']

print("Lap Statistics:")
print(lap_stats.head())
print(f"\nTrack length: {track_length}m")
print(f"Number of laps detected: {len(lap_stats)}")
```

### Advanced Grouping Strategies

```python
# Multiple grouping variables
# Group by lap and track sector
sector_boundaries = [0, 150, 300, 800]  # meters

def assign_sector(distance):
    for i, boundary in enumerate(sector_boundaries[1:]):
        if distance <= boundary:
            return i + 1
    return len(sector_boundaries) - 1

df['sector'] = df['distance_m'].apply(assign_sector)

# Group by lap and sector (using actual column names)
lap_sector_analysis = df.groupby(['lap_number', 'sector']).agg({
    'speed_kmh': 'mean',
    'lateral_g': 'max',
    'time_s': lambda x: x.max() - x.min()  # Sector time
}).rename(columns={'time_s': 'sector_time'})

# Pivot for easy comparison
sector_times = lap_sector_analysis['sector_time'].unstack(level='sector')
print("Sector times by lap:")
print(sector_times.head())
```

### Filter Operations

```python
# Filter: return entire groups that meet criteria
# Keep only laps with average speed above threshold
fast_laps = df.groupby('lap_number').filter(lambda x: x['speed_kmh'].mean() > 85)

# Keep only complete laps (sufficient data points)
complete_laps = df.groupby('lap_number').filter(lambda x: len(x) > 1000)

# Keep laps with good data quality (no large gaps)
def has_good_data_quality(group):
    time_diffs = group['time_s'].diff()
    max_gap = time_diffs.max()
    return max_gap < 0.1  # Less than 100ms gaps

quality_laps = df.groupby('lap_number').filter(has_good_data_quality)

# Combine filters (using actual column names)
clean_fast_laps = df.groupby('lap_number').filter(
    lambda x: (x['speed_kmh'].mean() > 35) and (len(x) > 50) and has_good_data_quality(x)
)

print(f"Total laps: {df['lap_number'].nunique()}")
print(f"Quality laps: {quality_laps['lap_number'].nunique()}")
print(f"Clean fast laps: {clean_fast_laps['lap_number'].nunique()}")
```

## Window Functions

### Ranking Operations

```python
# Rank within entire dataset
df['speed_rank_global'] = df['speed_kmh'].rank(method='dense', ascending=False)

# Rank within each lap
df['speed_rank_lap'] = df.groupby('lap_number')['speed_kmh'].rank(method='dense', ascending=False)

# Add lateral g ranking
df['lateral_g_rank_global'] = df['lateral_g'].abs().rank(method='dense', ascending=False)

# Percentile ranks
df['speed_percentile'] = df['speed_kmh'].rank(pct=True)  # 0-1 range
df['speed_percentile_lap'] = df.groupby('lap_number')['speed_kmh'].rank(pct=True)

# Multiple ranking criteria (now that both columns exist)
df['combined_rank'] = df.eval('speed_rank_global + lateral_g_rank_global')

print(f"Speed rankings: min={df['speed_rank_global'].min()}, max={df['speed_rank_global'].max()}")
print(f"Lateral G rankings: min={df['lateral_g_rank_global'].min()}, max={df['lateral_g_rank_global'].max()}")
print(f"Combined rankings: min={df['combined_rank'].min()}, max={df['combined_rank'].max()}")
```

### Cumulative Operations

```python
# Basic cumulative operations
df['cumulative_distance'] = df['distance_m'].cumsum()
df['session_max_speed'] = df['speed_kmh'].cummax()
df['session_max_lateral_g'] = df['lateral_g'].abs().cummax()  # Maximum g-force experienced so far

# Group-aware cumulative operations
df['distance_in_lap'] = df.groupby('lap_number')['distance_m'].cumsum()
df['lap_max_speed'] = df.groupby('lap_number')['speed_kmh'].cummax()

print(f"Final cumulative distance: {df['cumulative_distance'].iloc[-1]:.1f}m")
print(f"Session max speed: {df['session_max_speed'].iloc[-1]:.1f} km/h")
print(f"Session max lateral G: {df['session_max_lateral_g'].iloc[-1]:.2f} g")

# Custom cumulative functions
def cumulative_tire_wear(speed_series, lateral_g_series):
    """Calculate cumulative tire wear proxy"""
    wear_rate = speed_series * lateral_g_series.abs()
    return wear_rate.cumsum()

df['tire_wear_estimate'] = cumulative_tire_wear(df['speed_kmh'], df['lateral_g'])

# Conditional cumulative operations
df['overspeed_count'] = (df['speed_kmh'] > 120).cumsum()  # Count overspeeds
```

## Advanced Data Transformations

### Categorical Data Operations

```python
# Create performance categories
df['speed_category'] = pd.cut(df['speed_kmh'], 
                             bins=[0, 50, 100, 150, 200, 300],
                             labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])

# Cornering intensity classification
df['cornering_intensity'] = pd.cut(df['lateral_g'].abs(),
                                  bins=[0, 0.3, 0.8, 1.2, 2.0],
                                  labels=['Straight', 'Light', 'Moderate', 'Hard'])

# Custom categorization
def categorize_driving_style(row):
    if row['speed_kmh'] > 150 and row['lateral_g'] > 1.0:
        return 'Aggressive'
    elif row['speed_kmh'] > 100 and row['lateral_g'] > 0.5:
        return 'Sporty'
    elif row['speed_kmh'] < 60:
        return 'Conservative'
    else:
        return 'Normal'

df['driving_style'] = df.apply(categorize_driving_style, axis=1)

# Analyze by categories
category_analysis = df.groupby(['cornering_intensity', 'speed_category']).size()
style_performance = df.groupby('driving_style').agg({
    'speed_kmh': 'mean',
    'lateral_g': 'max'
})
```

## Performance Optimization

### Vectorized Operations

```python
# Avoid loops - use vectorized operations
# BAD: Loop through rows
results = []
for index, row in df.iterrows():
    # Using actual telemetry columns
    result = np.sqrt(row['lateral_g']**2 + row['longitudinal_g']**2)
    results.append(result)
df['magnitude_slow'] = results

# GOOD: Vectorized operation
df['magnitude_fast'] = np.sqrt(df['lateral_g']**2 + df['longitudinal_g']**2)

# Complex vectorized operations
# Estimate cornering force using lateral g-force
df['cornering_force'] = df['speed_kmh'] * df['lateral_g'] / 9.81

# Vehicle mass for Formula Student car (estimated)
vehicle_mass = 250  # kg (typical Formula Student car)
df['power_estimate'] = df['speed_kmh'] * df['longitudinal_g'] * vehicle_mass / 3.6

# Conditional operations - adjusted for autocross racing speeds
df['performance_zone'] = np.where(
    (df['speed_kmh'] > 40) & (df['lateral_g'] > 0.8),
    'High Performance',
    np.where(
        df['speed_kmh'] > 25,
        'Normal',
        'Low Speed'
    )
)

# Multiple conditions with np.select - realistic autocross speeds
conditions = [
    (df['speed_kmh'] < 15),  # Tight corners
    (df['speed_kmh'] >= 15) & (df['speed_kmh'] < 50),  # Technical sections
    (df['speed_kmh'] >= 50) & (df['speed_kmh'] < 120),  # Fast sections
    (df['speed_kmh'] >= 120)  # Straights
]
choices = ['Tight Corner', 'Technical', 'Fast Section', 'Straight']
df['speed_context'] = np.select(conditions, choices, default='Unknown')
```

These advanced pandas operations provide the foundation for sophisticated data analysis workflows. They enable complex time series analysis, detailed groupby operations, and efficient data transformations essential for engineering applications.