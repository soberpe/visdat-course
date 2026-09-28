---
title: Python External Libraries
---

# Python External Libraries

## Overview

Python's strength lies in its extensive ecosystem of libraries for data processing, analysis, and visualization. This guide covers the most important libraries for our course.

## NumPy - Numerical Computing

NumPy provides powerful array operations and mathematical functions.

```python
import numpy as np

# Create arrays
data = np.array([1.2, 2.3, 3.4, 4.5, 5.6])
matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

print(f"Array: {data}")
print(f"Matrix:\n{matrix}")

# Array operations
squared = data ** 2
normalized = (data - np.mean(data)) / np.std(data)

print(f"Squared: {squared}")
print(f"Normalized: {normalized}")

# Statistical functions
print(f"Mean: {np.mean(data):.2f}")
print(f"Standard deviation: {np.std(data):.2f}")
print(f"Min/Max: {np.min(data):.2f} / {np.max(data):.2f}")

# Matrix operations
print(f"Matrix sum: {np.sum(matrix)}")
print(f"Column means: {np.mean(matrix, axis=0)}")
print(f"Row means: {np.mean(matrix, axis=1)}")
```

### Advanced NumPy Operations

```python
# Generate synthetic sensor data
np.random.seed(42)  # For reproducible results

# Temperature data with trend and noise
time_points = np.linspace(0, 24, 100)  # 24 hours, 100 measurements
base_temp = 20 + 5 * np.sin(2 * np.pi * time_points / 24)  # Daily cycle
noise = np.random.normal(0, 0.5, 100)  # Random noise
temperature = base_temp + noise

# Humidity data
humidity = 60 + 10 * np.sin(2 * np.pi * time_points / 24 + np.pi/4) + np.random.normal(0, 2, 100)

print(f"Temperature range: {np.min(temperature):.1f} to {np.max(temperature):.1f}°C")
print(f"Humidity range: {np.min(humidity):.1f} to {np.max(humidity):.1f}%")

# Array operations for data analysis
def analyze_sensor_array(data, name):
    """Analyze sensor data using NumPy operations."""
    print(f"\n{name} Analysis:")
    print(f"  Count: {len(data)}")
    print(f"  Mean: {np.mean(data):.2f}")
    print(f"  Median: {np.median(data):.2f}")
    print(f"  Std Dev: {np.std(data):.2f}")
    print(f"  25th/75th percentile: {np.percentile(data, 25):.2f} / {np.percentile(data, 75):.2f}")
    
    # Find outliers (beyond 2 standard deviations)
    mean = np.mean(data)
    std = np.std(data)
    outliers = data[np.abs(data - mean) > 2 * std]
    print(f"  Outliers: {len(outliers)} values")

analyze_sensor_array(temperature, "Temperature")
analyze_sensor_array(humidity, "Humidity")
```

## Pandas - Data Analysis

Pandas excels at handling structured data and time series.

```python
import pandas as pd
from datetime import datetime, timedelta

# Create DataFrame from sensor data
sensor_data = pd.DataFrame({
    'timestamp': pd.date_range('2023-10-01 10:00:00', periods=100, freq='15min'),
    'temperature': temperature,
    'humidity': humidity,
    'sensor_id': ['SENSOR_001'] * 100
})

print("Sensor Data Summary:")
print(sensor_data.head())
print(f"\nDataFrame shape: {sensor_data.shape}")
print(f"Data types:\n{sensor_data.dtypes}")

# Data analysis with Pandas
print(f"\nTemperature statistics:")
print(sensor_data['temperature'].describe())

# Time-based operations
sensor_data.set_index('timestamp', inplace=True)

# Resample to hourly averages
hourly_avg = sensor_data.resample('H')[['temperature', 'humidity']].mean()
print(f"\nHourly averages:")
print(hourly_avg.head())

# Find correlations
correlation = sensor_data[['temperature', 'humidity']].corr()
print(f"\nTemperature-Humidity correlation:")
print(correlation)

# Filter data
high_temp_periods = sensor_data[sensor_data['temperature'] > 22]
print(f"\nHigh temperature periods: {len(high_temp_periods)} measurements")
```

### Advanced Pandas Operations

```python
# Create multi-sensor dataset
sensors = ['TEMP_01', 'TEMP_02', 'TEMP_03']
all_sensor_data = []

for sensor_id in sensors:
    # Generate slightly different data for each sensor
    offset = np.random.uniform(-1, 1)
    sensor_temps = temperature + offset + np.random.normal(0, 0.2, 100)
    
    sensor_df = pd.DataFrame({
        'timestamp': pd.date_range('2023-10-01 10:00:00', periods=100, freq='15min'),
        'temperature': sensor_temps,
        'humidity': humidity + np.random.normal(0, 1, 100),
        'sensor_id': sensor_id
    })
    all_sensor_data.append(sensor_df)

# Combine all sensor data
combined_data = pd.concat(all_sensor_data, ignore_index=True)
print(f"Combined dataset shape: {combined_data.shape}")

# Group operations
sensor_stats = combined_data.groupby('sensor_id').agg({
    'temperature': ['mean', 'std', 'min', 'max'],
    'humidity': ['mean', 'std']
}).round(2)

print(f"\nSensor statistics:")
print(sensor_stats)

# Pivot table for cross-analysis
combined_data['hour'] = combined_data['timestamp'].dt.hour
hourly_pivot = combined_data.pivot_table(
    values='temperature', 
    index='hour', 
    columns='sensor_id', 
    aggfunc='mean'
)

print(f"\nHourly temperature by sensor (first 10 hours):")
print(hourly_pivot.head(10))

# Export processed data
combined_data.to_csv('processed_sensor_data.csv', index=False)
print(f"\nExported {len(combined_data)} records to processed_sensor_data.csv")
```

## Matplotlib - Data Visualization

Create charts and plots for data exploration.

```python
import matplotlib.pyplot as plt

# Simple time series plot
plt.figure(figsize=(12, 8))

# Temperature subplot
plt.subplot(2, 1, 1)
plt.plot(time_points, temperature, 'b-', linewidth=1, alpha=0.7)
plt.title('Temperature Over 24 Hours')
plt.ylabel('Temperature (°C)')
plt.grid(True, alpha=0.3)

# Humidity subplot
plt.subplot(2, 1, 2)
plt.plot(time_points, humidity, 'g-', linewidth=1, alpha=0.7)
plt.title('Humidity Over 24 Hours')
plt.xlabel('Time (hours)')
plt.ylabel('Humidity (%)')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('sensor_timeseries.png', dpi=150, bbox_inches='tight')
plt.show()

# Multi-sensor comparison
plt.figure(figsize=(10, 6))

for sensor_id in sensors:
    sensor_subset = combined_data[combined_data['sensor_id'] == sensor_id]
    plt.plot(sensor_subset['timestamp'], sensor_subset['temperature'], 
             label=sensor_id, linewidth=1, alpha=0.8)

plt.title('Temperature Comparison - Multiple Sensors')
plt.xlabel('Time')
plt.ylabel('Temperature (°C)')
plt.legend()
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('multi_sensor_comparison.png', dpi=150, bbox_inches='tight')
plt.show()

# Statistical plots
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))

# Histogram
ax1.hist(temperature, bins=20, alpha=0.7, color='blue', edgecolor='black')
ax1.set_title('Temperature Distribution')
ax1.set_xlabel('Temperature (°C)')
ax1.set_ylabel('Frequency')

# Box plot by sensor
combined_data.boxplot(column='temperature', by='sensor_id', ax=ax2)
ax2.set_title('Temperature Distribution by Sensor')
ax2.set_xlabel('Sensor ID')
ax2.set_ylabel('Temperature (°C)')

# Scatter plot
ax3.scatter(combined_data['temperature'], combined_data['humidity'], 
           alpha=0.6, c=combined_data['sensor_id'].astype('category').cat.codes, cmap='viridis')
ax3.set_title('Temperature vs Humidity')
ax3.set_xlabel('Temperature (°C)')
ax3.set_ylabel('Humidity (%)')

# Correlation heatmap (using matplotlib)
corr_matrix = combined_data[['temperature', 'humidity']].corr()
im = ax4.imshow(corr_matrix, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
ax4.set_xticks(range(len(corr_matrix.columns)))
ax4.set_yticks(range(len(corr_matrix.columns)))
ax4.set_xticklabels(corr_matrix.columns)
ax4.set_yticklabels(corr_matrix.columns)
ax4.set_title('Correlation Matrix')

# Add correlation values as text
for i in range(len(corr_matrix.columns)):
    for j in range(len(corr_matrix.columns)):
        ax4.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}', 
                ha='center', va='center')

plt.tight_layout()
plt.savefig('sensor_analysis_plots.png', dpi=150, bbox_inches='tight')
plt.show()
```

## Practical Data Processing Pipeline

```python
def create_sensor_analysis_pipeline(data_file, output_dir="analysis_output"):
    """Complete data processing pipeline using multiple libraries."""
    import os
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Step 1: Load data with Pandas
    print("1. Loading data...")
    df = pd.read_csv(data_file)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    print(f"   Loaded {len(df)} records from {data_file}")
    
    # Step 2: Data validation and cleaning
    print("2. Cleaning data...")
    initial_count = len(df)
    
    # Remove invalid values
    df = df.dropna()
    df = df[(df['temperature'] >= -50) & (df['temperature'] <= 100)]
    df = df[(df['humidity'] >= 0) & (df['humidity'] <= 100)]
    
    final_count = len(df)
    print(f"   Removed {initial_count - final_count} invalid records")
    
    # Step 3: Statistical analysis with NumPy
    print("3. Performing statistical analysis...")
    stats_summary = {
        'temperature': {
            'mean': np.mean(df['temperature']),
            'std': np.std(df['temperature']),
            'median': np.median(df['temperature']),
            'q25': np.percentile(df['temperature'], 25),
            'q75': np.percentile(df['temperature'], 75)
        },
        'humidity': {
            'mean': np.mean(df['humidity']),
            'std': np.std(df['humidity']),
            'median': np.median(df['humidity']),
            'q25': np.percentile(df['humidity'], 25),
            'q75': np.percentile(df['humidity'], 75)
        }
    }
    
    # Step 4: Time-based analysis with Pandas
    print("4. Analyzing temporal patterns...")
    df.set_index('timestamp', inplace=True)
    
    # Hourly statistics
    hourly_stats = df.groupby(df.index.hour).agg({
        'temperature': ['mean', 'std'],
        'humidity': ['mean', 'std']
    }).round(2)
    
    # Daily statistics if data spans multiple days
    if df.index.date.nunique() > 1:
        daily_stats = df.groupby(df.index.date).agg({
            'temperature': ['mean', 'std', 'min', 'max'],
            'humidity': ['mean', 'std', 'min', 'max']
        }).round(2)
    else:
        daily_stats = None
    
    # Step 5: Generate visualizations
    print("5. Creating visualizations...")
    
    # Time series plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    ax1.plot(df.index, df['temperature'], 'b-', linewidth=1, alpha=0.7)
    ax1.set_title('Temperature Time Series')
    ax1.set_ylabel('Temperature (°C)')
    ax1.grid(True, alpha=0.3)
    
    ax2.plot(df.index, df['humidity'], 'g-', linewidth=1, alpha=0.7)
    ax2.set_title('Humidity Time Series')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Humidity (%)')\n    ax2.grid(True, alpha=0.3)\n    \n    plt.tight_layout()\n    plt.savefig(f'{output_dir}/timeseries.png', dpi=150, bbox_inches='tight')\n    plt.close()\n    \n    # Statistical distribution plots\n    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))\n    \n    # Temperature histogram\n    ax1.hist(df['temperature'], bins=20, alpha=0.7, color='blue', edgecolor='black')\n    ax1.set_title('Temperature Distribution')\n    ax1.set_xlabel('Temperature (°C)')\n    ax1.set_ylabel('Frequency')\n    \n    # Humidity histogram\n    ax2.hist(df['humidity'], bins=20, alpha=0.7, color='green', edgecolor='black')\n    ax2.set_title('Humidity Distribution')\n    ax2.set_xlabel('Humidity (%)')\n    ax2.set_ylabel('Frequency')\n    \n    # Scatter plot\n    ax3.scatter(df['temperature'], df['humidity'], alpha=0.6)\n    ax3.set_title('Temperature vs Humidity')\n    ax3.set_xlabel('Temperature (°C)')\n    ax3.set_ylabel('Humidity (%)')\n    \n    # Hourly averages\n    hourly_means = df.groupby(df.index.hour).mean()\n    ax4.plot(hourly_means.index, hourly_means['temperature'], 'o-', label='Temperature')\n    ax4_twin = ax4.twinx()\n    ax4_twin.plot(hourly_means.index, hourly_means['humidity'], 's-', color='orange', label='Humidity')\n    ax4.set_title('Hourly Averages')\n    ax4.set_xlabel('Hour of Day')\n    ax4.set_ylabel('Temperature (°C)', color='blue')\n    ax4_twin.set_ylabel('Humidity (%)', color='orange')\n    \n    plt.tight_layout()\n    plt.savefig(f'{output_dir}/distributions.png', dpi=150, bbox_inches='tight')\n    plt.close()\n    \n    # Step 6: Export results\n    print(\"6. Exporting results...\")\n    \n    # Save processed data\n    df.to_csv(f'{output_dir}/cleaned_data.csv')\n    \n    # Save statistical summary\n    with open(f'{output_dir}/statistics_summary.txt', 'w') as f:\n        f.write(\"Sensor Data Analysis Summary\\n\")\n        f.write(\"=\" * 30 + \"\\n\\n\")\n        \n        for variable, stats in stats_summary.items():\n            f.write(f\"{variable.title()} Statistics:\\n\")\n            for stat_name, value in stats.items():\n                f.write(f\"  {stat_name}: {value:.2f}\\n\")\n            f.write(\"\\n\")\n        \n        f.write(\"Hourly Statistics:\\n\")\n        f.write(str(hourly_stats))\n        f.write(\"\\n\\n\")\n        \n        if daily_stats is not None:\n            f.write(\"Daily Statistics:\\n\")\n            f.write(str(daily_stats))\n    \n    # Save hourly statistics as CSV\n    hourly_stats.to_csv(f'{output_dir}/hourly_statistics.csv')\n    \n    if daily_stats is not None:\n        daily_stats.to_csv(f'{output_dir}/daily_statistics.csv')\n    \n    print(f\"   Analysis complete! Results saved to {output_dir}/\")\n    \n    return {\n        'stats_summary': stats_summary,\n        'hourly_stats': hourly_stats,\n        'daily_stats': daily_stats,\n        'processed_data': df\n    }\n\n# Run the complete pipeline\nif os.path.exists('processed_sensor_data.csv'):\n    results = create_sensor_analysis_pipeline('processed_sensor_data.csv')\n    print(\"\\nPipeline completed successfully!\")\nelse:\n    print(\"Please run the Pandas section first to generate the input data file.\")\n```\n\n## Next Steps\n\nNow you have a solid foundation in Python's data processing ecosystem:\n\n- **NumPy** for numerical computations and array operations\n- **Pandas** for data manipulation and analysis\n- **Matplotlib** for data visualization\n- **Integrated workflows** combining all libraries\n\nContinue with:\n- **[C++ Programming](../cpp/cpp-overview)** - Learn C++ for performance-critical tasks\n- **[Programming Fundamentals](../programming/paradigms)** - Understand programming paradigms\n\nThese libraries form the backbone of Python's data science ecosystem!