import pandas as pd
import numpy as np

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

