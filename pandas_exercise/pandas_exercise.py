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