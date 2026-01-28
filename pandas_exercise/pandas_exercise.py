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

data = {
    'speed_kmh': [10, 35, 50, 80, 120],
    'distance_m': [0, 100, 200, 300, 400],
    'time_s': [0, 1, 2, 3, 4],
    'brake_pressure_bar': [0, 10, 20, 30, 40],
    'rpm': [1000, 3000, 5000, 7000, 9000]
}
telemetry = pd.DataFrame(data)
print(telemetry)

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
#```python
