---
title: Racing Data Case Study
---

# Racing Data Case Study: Vehicle Dynamics Analysis

This comprehensive case study demonstrates a complete data processing workflow using racing vehicle telemetry data. We'll analyze IMU data from a cornering maneuver to extract meaningful engineering insights.

## Dataset Overview

### Vehicle and Scenario
- **Vehicle**: European Autocross Championship car (synthetic data)
- **Scenario**: Tight autocross course section with chicane
- **Duration**: 30 seconds of data
- **Sampling Rate**: 1000 Hz
- **Maneuver**: Left-right-left chicane section typical of autocross

> **Note**: This dataset is synthetically generated to provide clean, educational examples. Later in the course, we'll work with 3D geometry data from the same championship car for visualization and analysis.

### Data Structure
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Dataset columns (Nova Paka telemetry data)
columns = [
    'time_s',            # Time in seconds from start
    'speed_kmh',         # Vehicle speed [km/h]
    'lateral_g',         # Lateral acceleration [g] (positive = right turn)
    'longitudinal_g',    # Longitudinal acceleration [g] (positive = acceleration)
    'steering_angle_deg', # Steering wheel angle [degrees]
    'throttle_percent',  # Throttle position [0-100%]
    'brake_pressure_bar', # Brake pressure [bar]
    'distance_m',        # Cumulative distance [m]
    'rpm',               # Engine RPM
    'gear'               # Current gear
]

# Load the dataset
df = pd.read_csv('data/telemetry_detailed.csv')
print(f"Dataset: {df.shape[0]} samples over {df['time_s'].max():.1f} seconds")
print(f"Columns: {list(df.columns)}")
```

## Data Quality Assessment

### Initial Data Exploration
```python
# Basic information
print("=== Dataset Overview ===")
print(f"Shape: {df.shape}")
print(f"Time range: {df['time_s'].min():.3f} - {df['time_s'].max():.3f} seconds")
print(f"Sample rate: {1/df['time_s'].diff().mean():.0f} Hz")

# Statistical summary
print("\n=== Statistical Summary ===")
print(df.describe())

# Data types and missing values
print("\n=== Data Quality ===")
print(f"Data types:\n{df.dtypes}")
print(f"Missing values:\n{df.isnull().sum()}")

# Check for duplicates
duplicates = df.duplicated().sum()
print(f"Duplicate rows: {duplicates}")
```

### Time Series Validation
```python
# Check sampling consistency
time_diffs = df['time_s'].diff()
mean_dt = time_diffs.mean()
std_dt = time_diffs.std()

print(f"Mean sampling interval: {mean_dt:.6f} s ({1/mean_dt:.1f} Hz)")
print(f"Sampling variation: ±{std_dt:.6f} s")

# Identify timing issues
large_gaps = time_diffs[time_diffs > mean_dt * 2]
if len(large_gaps) > 0:
    print(f"Found {len(large_gaps)} timing gaps > {mean_dt*2:.6f} s")
    print("Gap locations:", large_gaps.index.tolist()[:5])

# Visualize timing consistency
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(df['time_s'], time_diffs * 1000)
plt.ylabel('Sample Interval [ms]')
plt.xlabel('Time [s]')
plt.title('Sampling Interval Over Time')

plt.subplot(1, 2, 2)
plt.hist(time_diffs * 1000, bins=50)
plt.xlabel('Sample Interval [ms]')
plt.ylabel('Count')
plt.title('Sample Interval Distribution')
plt.tight_layout()
plt.show()
```

### Physical Validation
```python
def validate_sensor_ranges(df):
    """Validate sensor readings against physical limits for autocross racing"""
    
    validation_rules = {
        'speed_kmh': (0, 60, 'km/h'),  # Autocross typical max speed
        'lateral_g': (-2.0, 2.0, 'g'),  # Lateral acceleration limits
        'longitudinal_g': (-1.5, 1.0, 'g'),  # Braking/acceleration limits
        'steering_angle_deg': (-720, 720, 'degrees'),  # Steering wheel range
        'throttle_percent': (0, 100, '%'),  # Throttle position
        'brake_pressure_bar': (0, 80, 'bar'),  # Brake pressure for Formula Student
        'rpm': (800, 12000, 'rpm'),  # Engine RPM range
        'gear': (1, 6, ''),  # Gear numbers
        'distance_m': (0, 1000, 'm')  # Distance on autocross course
    }
    
    validation_results = {}
    
    for column, (min_val, max_val, unit) in validation_rules.items():
        if column in df.columns:
            out_of_range = df[(df[column] < min_val) | (df[column] > max_val)]
            validation_results[column] = {
                'valid_range': f"[{min_val}, {max_val}] {unit}",
                'actual_range': f"[{df[column].min():.3f}, {df[column].max():.3f}]",
                'violations': len(out_of_range),
                'violation_percentage': len(out_of_range) / len(df) * 100
            }
    
    return validation_results

# Perform validation
validation = validate_sensor_ranges(df)

print("=== Physical Validation Results ===")
for sensor, results in validation.items():
    if results['violations'] > 0:
        print(f"{sensor}: {results['violations']} violations ({results['violation_percentage']:.2f}%)")
        print(f"  Valid: {results['valid_range']}")
        print(f"  Actual: {results['actual_range']}")
```

## Data Cleaning Pipeline

### Outlier Detection and Removal
```python
def detect_outliers_iqr(data, column, factor=1.5):
    """Detect outliers using Interquartile Range method"""
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - factor * IQR
    upper_bound = Q3 + factor * IQR
    
    outliers_mask = (data[column] < lower_bound) | (data[column] > upper_bound)
    outliers = data[outliers_mask]
    
    return outliers, lower_bound, upper_bound, outliers_mask

# Detect outliers in acceleration channels
acceleration_columns = ['lateral_g', 'longitudinal_g']
outlier_summary = {}

for column in acceleration_columns:
    outliers, lower, upper, mask = detect_outliers_iqr(df, column)
    outlier_summary[column] = {
        'count': len(outliers),
        'percentage': len(outliers) / len(df) * 100,
        'bounds': (lower, upper)
    }
    
    print(f"{column}: {len(outliers)} outliers ({len(outliers)/len(df)*100:.2f}%)")
    print(f"  Valid range: [{lower:.3f}, {upper:.3f}] g")

# Remove outliers (conservative approach)
def remove_outliers_conservative(data, columns, factor=2.0):
    """Remove extreme outliers only"""
    clean_data = data.copy()
    
    for column in columns:
        _, _, _, outlier_mask = detect_outliers_iqr(clean_data, column, factor)
        clean_data = clean_data[~outlier_mask]
    
    return clean_data

df_clean = remove_outliers_conservative(df, acceleration_columns)
print(f"\nData after outlier removal: {len(df_clean)} samples ({len(df_clean)/len(df)*100:.1f}% retained)")
```

### Signal Filtering
```python
# Apply moving average filter to reduce noise
def apply_moving_average_filter(data, columns, window_size=10):
    """Apply moving average filter to specified columns"""
    filtered_data = data.copy()
    
    for column in columns:
        # Keep original data
        filtered_data[f'{column}_raw'] = filtered_data[column]
        
        # Apply moving average
        filtered_data[column] = filtered_data[column].rolling(
            window=window_size, center=True
        ).mean()
        
        # Fill NaN values at edges
        filtered_data[column] = filtered_data[column].fillna(method='bfill').fillna(method='ffill')
    
    return filtered_data

# Apply filtering to sensor data
sensor_columns = ['lateral_g', 'longitudinal_g', 'speed_kmh', 'steering_angle_deg']]
df_filtered = apply_moving_average_filter(df_clean, sensor_columns, window_size=10)

# Visualize filtering effect
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
axes = axes.ravel()

columns_to_plot = ['lateral_g', 'longitudinal_g', 'speed_kmh', 'steering_angle_deg']
for i, column in enumerate(columns_to_plot):
    if i < 4 and column in df_filtered.columns:
        axes[i].plot(df_filtered['time_s'], df_filtered[f'{column}_raw'], 
                    alpha=0.3, label='Raw', color='gray')
        axes[i].plot(df_filtered['time_s'], df_filtered[column], 
                    label='Filtered', color='blue')
        
        # Set appropriate y-axis labels
        if column == 'lateral_g' or column == 'longitudinal_g':
            ylabel = f'{column} [g]'
        elif column == 'speed_kmh':
            ylabel = 'Speed [km/h]'
        elif column == 'steering_angle_deg':
            ylabel = 'Steering [deg]'
        else:
            ylabel = column
            
        axes[i].set_ylabel(ylabel)
        axes[i].set_xlabel('Time [s]')
        axes[i].legend()
        axes[i].grid(True, alpha=0.3)

plt.tight_layout()
plt.suptitle('Signal Filtering Effect', y=1.02)
plt.show()
```

## Engineering Analysis

### Performance Metrics Calculation
```python
# Calculate additional performance metrics from telemetry data
def calculate_performance_metrics(data):
    """Calculate racing performance metrics"""
    result = data.copy()
    
    # Total acceleration magnitude
    result['total_g'] = np.sqrt(result['lateral_g']**2 + result['longitudinal_g']**2)
    
    # Cornering performance indicators
    result['cornering_speed'] = np.where(
        np.abs(result['lateral_g']) > 0.3,  # During cornering
        result['speed_kmh'],
        np.nan
    )
    
    # Braking and acceleration zones
    result['braking_zone'] = result['longitudinal_g'] < -0.2
    result['acceleration_zone'] = result['longitudinal_g'] > 0.2
    result['cornering_zone'] = np.abs(result['lateral_g']) > 0.3
    
    # Throttle effectiveness (speed change vs throttle input)
    result['speed_change'] = result['speed_kmh'].diff()
    result['throttle_effectiveness'] = result['speed_change'] / (result['throttle_percent'] + 1)
    
    return result

df_metrics = calculate_performance_metrics(df_filtered)

print("Performance metrics calculated:")
print(f"Max total g-force: {df_metrics['total_g'].max():.2f} g")
print(f"Max cornering speed: {df_metrics['cornering_speed'].max():.1f} km/h")
print(f"Time in braking zones: {df_metrics['braking_zone'].sum() * df_metrics['time_s'].diff().mean():.1f} s")
print(f"Time in acceleration zones: {df_metrics['acceleration_zone'].sum() * df_metrics['time_s'].diff().mean():.1f} s")
print(f"Time in cornering zones: {df_metrics['cornering_zone'].sum() * df_metrics['time_s'].diff().mean():.1f} s")
```

## Data Visualization

### Time Series Plots
```python
# Create comprehensive time series visualization
fig, axes = plt.subplots(4, 1, figsize=(15, 12))

# Speed and throttle/brake
axes[0].plot(df_performance['time_s'], df_performance['speed_kmh'], 'b-', label='Speed')
axes[0].set_ylabel('Speed [km/h]', color='b')
axes[0].tick_params(axis='y', labelcolor='b')

ax0_twin = axes[0].twinx()
if 'throttle_percent' in df_performance.columns:
    ax0_twin.plot(df_performance['time_s'], df_performance['throttle_percent'], 'g-', alpha=0.7, label='Throttle')
if 'brake_pressure_bar' in df_performance.columns:
    ax0_twin.plot(df_performance['time_s'], df_performance['brake_pressure_bar']*5, 'r-', alpha=0.7, label='Brake×5')
ax0_twin.set_ylabel('Throttle [%] / Brake×5 [bar]', color='g')
ax0_twin.tick_params(axis='y', labelcolor='g')

# Highlight cornering segments
for corner in corners:
    axes[0].axvspan(corner['start_time'], corner['end_time'], alpha=0.2, color='yellow', label='Cornering' if corner == corners[0] else "")

axes[0].set_title('Speed Profile and Driver Inputs')
axes[0].grid(True, alpha=0.3)

# Lateral and longitudinal acceleration
axes[1].plot(df_performance['time_s'], df_performance['lateral_g'], 'r-', label='Lateral G')
axes[1].plot(df_performance['time_s'], df_performance['longitudinal_g'], 'b-', label='Longitudinal G')
axes[1].set_ylabel('Acceleration [g]')
axes[1].legend()
axes[1].grid(True, alpha=0.3)
axes[1].set_title('Vehicle Accelerations')

# Steering angle (if available)
if 'steering_angle_deg' in df_performance.columns:
    axes[2].plot(df_performance['time_s'], df_performance['steering_angle_deg'], 'g-', label='Steering Angle')
    axes[2].set_ylabel('Steering [deg]', color='g')
    axes[2].tick_params(axis='y', labelcolor='g')
    axes[2].set_title('Steering Input')
else:
    # Show distance and sector progression
    axes[2].plot(df_performance['time_s'], df_performance['distance_m'], 'purple', label='Distance')
    axes[2].set_ylabel('Distance [m]', color='purple')
    axes[2].tick_params(axis='y', labelcolor='purple')
    axes[2].set_title('Distance Progression')

axes[2].grid(True, alpha=0.3)

# Corner radius and total g-force
axes[3].plot(df_performance['time_s'], df_performance['corner_radius'], 'orange', label='Corner Radius')
axes[3].set_ylabel('Radius [m]', color='orange')
axes[3].tick_params(axis='y', labelcolor='orange')

ax3_twin = axes[3].twinx()
ax3_twin.plot(df_performance['time_s'], df_performance['total_g'], 'purple', alpha=0.7, label='Total G')
ax3_twin.set_ylabel('Total G [g]', color='purple')
ax3_twin.tick_params(axis='y', labelcolor='purple')

axes[3].set_xlabel('Time [s]')
axes[3].set_ylim(0, 100)  # Focus on realistic autocross corner radii
axes[3].set_title('Cornering Metrics')
axes[3].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

### G-G Diagram (Traction Circle)

The G-G diagram, also known as the traction circle, is a fundamental visualization tool in vehicle dynamics analysis that plots lateral acceleration versus longitudinal acceleration to show the vehicle's traction utilization.

```python
# Create G-G diagram (traction circle)
plt.figure(figsize=(10, 10))

# Plot all data points
plt.scatter(df_performance['lateral_g'], df_performance['longitudinal_g'], 
           c=df_performance['speed_kmh'], cmap='viridis', alpha=0.6, s=1)

# Highlight cornering segments
cornering_data = df_performance[df_performance['is_cornering']]
if len(cornering_data) > 0:
    plt.scatter(cornering_data['lateral_g'], cornering_data['longitudinal_g'], 
               c='red', alpha=0.8, s=3, label='Cornering')

# Draw theoretical traction circle for autocross
theta = np.linspace(0, 2*np.pi, 100)
max_g = 1.5  # Typical autocross limit
circle_x = max_g * np.cos(theta)
circle_y = max_g * np.sin(theta)
plt.plot(circle_x, circle_y, 'r--', alpha=0.5, label='Theoretical Limit (1.5g)')

plt.xlabel('Lateral Acceleration [g]')
plt.ylabel('Longitudinal Acceleration [g]')
plt.title('G-G Diagram - Nova Paka Autocross')
plt.colorbar(label='Speed [km/h]')
plt.legend()
plt.grid(True, alpha=0.3)
plt.axis('equal')
plt.show()

# Calculate traction utilization
max_g_utilization = df_performance['total_g'].max()
avg_g_utilization = df_performance['total_g'].mean()

print(f"Traction Utilization Analysis:")
print(f"  Maximum total g-force: {max_g_utilization:.3f} g")
print(f"  Average total g-force: {avg_g_utilization:.3f} g")
print(f"  Peak utilization: {max_g_utilization/1.5*100:.1f}% of theoretical maximum")
```

### Speed vs Distance Analysis
```python
# Plot speed profile vs distance (track map alternative)
plt.figure(figsize=(15, 8))

# Main plot: Speed vs Distance
plt.subplot(2, 1, 1)
plt.plot(df_performance['distance_m'], df_performance['speed_kmh'], 'b-', linewidth=2)

# Mark cornering segments
for i, corner in enumerate(corners):
    corner_data = df_performance[
        (df_performance['time_s'] >= corner['start_time']) & 
        (df_performance['time_s'] <= corner['end_time'])
    ]
    if len(corner_data) > 0:
        plt.plot(corner_data['distance_m'], corner_data['speed_kmh'], 'r-', linewidth=3, alpha=0.7)
        # Add corner labels
        mid_distance = corner_data['distance_m'].mean()
        mid_speed = corner_data['speed_kmh'].mean()
        plt.annotate(f'C{i+1}', (mid_distance, mid_speed), 
                    xytext=(5, 5), textcoords='offset points', fontsize=8)

plt.xlabel('Distance [m]')
plt.ylabel('Speed [km/h]')
plt.title('Speed Profile Along Nova Paka Track (930m)')
plt.grid(True, alpha=0.3)
plt.xlim(0, 930)  # Nova Paka track length

# Secondary plot: G-forces vs Distance
plt.subplot(2, 1, 2)
plt.plot(df_performance['distance_m'], df_performance['lateral_g'], 'r-', alpha=0.7, label='Lateral G')
plt.plot(df_performance['distance_m'], df_performance['longitudinal_g'], 'b-', alpha=0.7, label='Longitudinal G')
plt.plot(df_performance['distance_m'], df_performance['total_g'], 'k-', linewidth=2, label='Total G')

plt.xlabel('Distance [m]')
plt.ylabel('Acceleration [g]')
plt.title('G-Force Profile Along Track')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xlim(0, 930)

plt.tight_layout()
plt.show()

# Track sector analysis
print("Nova Paka Track Analysis:")
print(f"Total track length: {df_performance['distance_m'].max():.0f} m")
for sector in range(1, 5):
    sector_data = df_performance[df_performance['sector'] == sector]
    if len(sector_data) > 0:
        print(f"Sector {sector}: Avg speed {sector_data['speed_kmh'].mean():.1f} km/h, "
              f"Max lateral g {sector_data['lateral_g'].abs().max():.2f}")

print(f"Cornering segments identified: {len(corners)}")
print(f"Total cornering time: {df_performance['is_cornering'].sum() * df_performance['time_s'].diff().mean():.1f}s")
```

## Data Export and Reporting
### Generate Analysis Report
```python
def generate_analysis_report(data):
    """Generate comprehensive Nova Paka analysis report"""
    
    # Calculate basic statistics from the data
    duration = data['time_s'].max() - data['time_s'].min()
    distance = data['distance_m'].max()
    avg_speed = data['speed_kmh'].mean()
    max_speed = data['speed_kmh'].max()
    max_lateral_g = data['lateral_g'].abs().max()
    max_longitudinal_g = data['longitudinal_g'].abs().max()
    
    report = f"""
# Nova Paka Autocross Analysis Report

## Session Overview
- **Track**: Nova Paka (930m autocross circuit)
- **Duration**: {duration:.1f} seconds
- **Distance**: {distance:.1f} meters
- **Average Speed**: {avg_speed:.1f} km/h
- **Maximum Speed**: {max_speed:.1f} km/h

## Performance Highlights
- **Peak Lateral G-Force**: {max_lateral_g:.2f} g
- **Peak Longitudinal G-Force**: {max_longitudinal_g:.2f} g

## Basic Statistics
- **Samples**: {len(data)} data points
- **Sampling Rate**: {len(data)/duration:.0f} Hz
- **Speed Range**: {data['speed_kmh'].min():.1f} - {data['speed_kmh'].max():.1f} km/h
- **G-Force Range**: ±{max(max_lateral_g, max_longitudinal_g):.2f} g maximum

## Data Quality
- **Missing Values**: {data.isnull().sum().sum()} total
- **Complete Data Coverage**: {(1 - data.isnull().sum().sum() / (len(data) * len(data.columns))) * 100:.1f}%
"""
    
    return report

# Generate and save report
report_content = generate_analysis_report(df_filtered)

with open('nova_paka_analysis_report.md', 'w') as f:
    f.write(report_content)

print("Nova Paka analysis report generated: nova_paka_analysis_report.md")
```

## References

1. Milliken, W. F., & Milliken, D. L. (1995). *Race Car Vehicle Dynamics*. SAE International.
