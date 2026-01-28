import pandas as pd

data = {
    'speed_kmh': [10, 35, 50, 80, 120],
    'distance_m': [0, 100, 200, 300, 400],
    'time_s': [0, 1, 2, 3, 4],
    'brake_pressure_bar': [0, 10, 20, 30, 40],
    'rpm': [1000, 3000, 5000, 7000, 9000]
}
telemetry = pd.DataFrame(data)
print(telemetry)