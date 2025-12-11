import pandas as pd
import numpy as np

#Create acceleration_x Series for acceleration data
acceleration_x = pd.Series([0.1, 0.2, 0.15, 0.3], 
                          index=['t1', 't2', 't3', 't4'])
print(acceleration_x)

#Series with automatic index
sensor_readings = pd.Series([9.81, 9.79, 9.82, 9.80])
print(f"Mean: {sensor_readings.mean():.3f}")
print(f"Std: {sensor_readings.std():.3f}")

 #Create DataFrame for IMU data
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

#------------------------------------------------------------------
#One dimensional Data
#------------------------------------------------------------------


speed_series = pd.Series([10, 35, 50, 80, 120], name='speed_kmh')
print(speed_series)


#------------------------------------------------------------------
#Two dimensional Data
#------------------------------------------------------------------


data = {
    'speed_kmh': [10, 35, 50, 80, 120],
    'distance_m': [0, 100, 200, 300, 400],
    'time_s': [0, 1, 2, 3, 4],
    'brake_pressure_bar': [0, 10, 20, 30, 40],
    'rpm': [1000, 3000, 5000, 7000, 9000]
}
telemetry = pd.DataFrame(data)
print(telemetry)


#------------------------------------------------------------------
#Data Selection and Filtering
#------------------------------------------------------------------


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
# python


#------------------------------------------------------------------
#Data Modification
#------------------------------------------------------------------


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


#------------------------------------------------------------------
#Data selection and filtering
#------------------------------------------------------------------


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


#------------------------------------------------------------------
#Data modification
#------------------------------------------------------------------


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