# um pandas als pd und numpy als np "abzukürzen"
import pandas as pd
import numpy as np
from pathlib import Path

Path('data').mkdir(exist_ok=True)

sessions = pd.DataFrame({
    'session_id': [1,2],
    'date': ['2025-01-01','2025-01-02'],
    'track': ['Nova Paka','Nové Město'],
    'driver': ['A. Fahrer','B. Fahrer']
})
sessions.to_csv('data/racing_sessions.csv', index=False)

laps = pd.DataFrame({
    'lap_id': [1,2,3],
    'session_id': [1,1,2],
    'lap_time_s': [60.123, 59.987, 61.456]
})
laps.to_csv('data/lap_times.csv', index=False)

telemetry = pd.DataFrame({
    'timestamp': [0.0, 0.1, 0.2, 0.3],
    'speed_kmh': [50.0, 52.5, 48.7, 51.0],
    'ax': [0.1,0.2,0.15,0.3],
    'ay': [9.81,9.80,9.82,9.79]
})
telemetry.to_csv('data/telemetry_detailed.csv', index=False)

# Excel with a Sessions sheet (optional)
with pd.ExcelWriter('data/nova_paka_racing_data.xlsx') as w:
    sessions.to_excel(w, sheet_name='Sessions', index=False)
    laps.to_excel(w, sheet_name='Laps', index=False)

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