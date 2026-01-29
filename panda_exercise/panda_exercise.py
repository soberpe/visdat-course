#Core Data Structures

import pandas as pd # Importieren der Datenbank und speichern unter neuen Namen
import numpy as np


# Series: One-Dimensional Data
# Create a Series for acceleration data mit .Series
acceleration_x = pd.Series([0.1, 0.2, 0.15, 0.3], 
                    index=['t1', 't2', 't3', 't4'])
print(acceleration_x)

# Series with automatic index
sensor_readings = pd.Series([9.81, 9.79, 9.82, 9.80])
print(f"Mean: {sensor_readings.mean():.3f}") # Mittelwert als float mit drei Nachkommastellen
print(f"Std: {sensor_readings.std():.3f}") # Standardabweichung


# DataFrame: Two-Dimensional Data
# Create DataFrame for IMU data mit .DataFrame
imu_data = pd.DataFrame({
    'timestamp': [0.0, 0.001, 0.002, 0.003],
    'ax': [0.1, 0.2, 0.15, 0.3],
    'ay': [9.81, 9.80, 9.82, 9.79],
    'az': [0.05, 0.03, 0.08, 0.06],
    'gx': [0.001, 0.002, 0.001, 0.003],
    'gy': [0.02, 0.025, 0.018, 0.022],
    'gz': [0.003, 0.005, 0.002, 0.008]
})

print(imu_data.head()) # .head meint ganze Tabelle
print(f"Shape: {imu_data.shape}") # .shape gibt größer wieder (Spalten, Zeilen)


# Essential Operations

# Data Loading and Insprection
# Load racing session data
sessions = pd.read_csv('data/racing_sessions.csv') # liest Datei aus Datenbank ein
print(sessions.info()) # gibt infos zu Daten an wie Zeilenanzahl und Spalteninfos (Anzahl, Name, Datentyp, Einträge ungleich Null) und Speicherplatz an
print(sessions.head()) # darstellung der ganzen Tabelle mit .head

# Load lap time data
laps = pd.read_csv('data/lap_times.csv')
print(f"Total laps: {len(laps)}")
print(f"Fastest lap: {laps['lap_time_s'].min():.3f}s")

# Load detailed telemetry
telemetry = pd.read_csv('data/telemetry_detailed.csv')
print(f"Telemetry points: {len(telemetry)}")
print(f"Speed range: {telemetry['speed_kmh'].min()}-{telemetry['speed_kmh'].max()} km/h")


# Additional Data Loading Examples
# Using the course dataset files
sessions = pd.read_csv('data/racing_sessions.csv')
laps = pd.read_csv('data/lap_times.csv') 
telemetry = pd.read_csv('data/telemetry_detailed.csv')


""" Hat nicht funktioniert!!!
# Excel format (multi-sheet)
excel_data = pd.read_excel('data/nova_paka_racing_data.xlsx', sheet_name='Sessions')
all_sheets = pd.read_excel('data/nova_paka_racing_data.xlsx')

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
"""

# Data Selection an Filtering
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


# Data Modification
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


# Data Cleaning

# Handling Missing Values
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


# Outlier Detection and Removal
# Definieren einer neuen Funktion mit Beschreibung
# Eingabeparameter ist Dateiname und Spaltenname
# Definieren des oberen und unteren 25% Quantils
# Definition der oberen und unteren Grenze der Außreiser anhand der Datenbreite und der Quantile
# Rückgabewert: Außreiser (ganze Spalte) und untere bzw. obere Grenze
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









