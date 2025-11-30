import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
import glob
import os



# Pfad zu deinem raw-Ordner
data_path = "data/raw"

# Alle CSV-Dateien im Ordner finden
csv_files = glob.glob(os.path.join(data_path, "*.csv"))

# Nur jene behalten, die IMU-Daten sind
imu_files = [f for f in csv_files if any(key in f.lower() for key in
                                         ["acc", "gyro", "angvel", "accel", "linear"])]
# Nach Änderungszeit sortieren (neueste zuerst)
imu_files.sort(key=os.path.getmtime, reverse=True)

# Die letzten zwei Dateien wählen
accel_file, gyro_file = imu_files[:2]

print("ACC File:", accel_file)
print("GYRO File:", gyro_file)

# Laden
accel_df = pd.read_csv(accel_file)
gyro_df = pd.read_csv(gyro_file)





# MATLAB Mobile typically uses columns: Time, X, Y, Z
# Rename for consistency
accel_df.rename(columns={'timestamp': 'time', 'X': 'ax', 'Y': 'ay', 'Z': 'az'}, inplace=True)
gyro_df.rename(columns={'timestamp': 'time', 'X': 'gx', 'Y': 'gy', 'Z': 'gz'}, inplace=True)

# Millisekunden -> Sekunden (float)
accel_df['time'] = accel_df['time'] / 1000.0
gyro_df['time']  = gyro_df['time']  / 1000.0

# Merge on timestamp (or use nearest time if sampling rates differ slightly)
df = pd.merge_asof(accel_df.sort_values('time'), 
                   gyro_df.sort_values('time'), 
                   on='time', 
                   direction='nearest',
                   tolerance=0.02)  # 20ms tolerance for sampling rate variations

# Normalize time to start at zero
df['time'] = df['time'] - df['time'].iloc[0]



# Calculate sampling rate (use median for robustness against jitter)
dt = df['time'].diff().median()
sampling_rate = 1 / dt

print(f"Total samples: {len(df)}")
print(f"Duration: {df['time'].max():.2f} seconds")
print(f"Sampling rate: {sampling_rate:.1f} Hz")
print(f"Average time step: {dt:.4f} seconds")


print(df.columns)

df.rename(columns={
    'ax': 'accel_x',
    'ay': 'accel_y', 
    'az': 'accel_z',
    'gx': 'gyro_x',
    'gy': 'gyro_y',
    'gz': 'gyro_z'
}, inplace=True)

print(df.columns)


# Check gyroscope units - many apps export deg/s, but Madgwick expects rad/s
gyro_cols = ['gyro_x', 'gyro_y', 'gyro_z']
max_gyro_value = df[gyro_cols].abs().quantile(0.95).max()

if max_gyro_value > 20:  # Heuristic: >20 likely means deg/s
    print(f"Gyroscope values appear to be in deg/s (max: {max_gyro_value:.1f})")
    df[gyro_cols] = np.deg2rad(df[gyro_cols])
    print("Converted gyroscope data from deg/s to rad/s.")
else:
    print(f"Gyroscope values appear to be in rad/s (max: {max_gyro_value:.2f})")



    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

# Acceleration
ax1.plot(df['time'], df['accel_x'], label='X', alpha=0.7)
ax1.plot(df['time'], df['accel_y'], label='Y', alpha=0.7)
ax1.plot(df['time'], df['accel_z'], label='Z', alpha=0.7)
ax1.set_ylabel('Acceleration (m/s²)')
ax1.set_title('Raw Accelerometer Data')
ax1.legend()
ax1.grid(True)

# Gyroscope
ax2.plot(df['time'], df['gyro_x'], label='X', alpha=0.7)
ax2.plot(df['time'], df['gyro_y'], label='Y', alpha=0.7)
ax2.plot(df['time'], df['gyro_z'], label='Z', alpha=0.7)
ax2.set_ylabel('Angular Velocity (rad/s)')
ax2.set_xlabel('Time (s)')
ax2.set_title('Raw Gyroscope Data')
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.savefig('01_raw_sensor_data.png', dpi=300)
# plt.show()

from scipy.signal import butter, filtfilt

def butter_lowpass_filter(data, cutoff, fs, order=2):
    """Apply a Butterworth low-pass filter to the data."""
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    filtered_data = filtfilt(b, a, data)
    return filtered_data

# Filter parameters
cutoff_frequency = 5  # Hz (adjust based on your movement speed)
fs = sampling_rate

# Apply filter to accelerometer data
df['accel_x_filt'] = butter_lowpass_filter(df['accel_x'], cutoff_frequency, fs)
df['accel_y_filt'] = butter_lowpass_filter(df['accel_y'], cutoff_frequency, fs)
df['accel_z_filt'] = butter_lowpass_filter(df['accel_z'], cutoff_frequency, fs)

# Optional: Filter gyroscope data as well
df['gyro_x_filt'] = butter_lowpass_filter(df['gyro_x'], cutoff_frequency, fs)
df['gyro_y_filt'] = butter_lowpass_filter(df['gyro_y'], cutoff_frequency, fs)
df['gyro_z_filt'] = butter_lowpass_filter(df['gyro_z'], cutoff_frequency, fs)



fig, axes = plt.subplots(3, 1, figsize=(12, 10))

for i, axis in enumerate(['x', 'y', 'z']):
    axes[i].plot(df['time'], df[f'accel_{axis}'], 
                 label='Raw', alpha=0.5, linewidth=0.5)
    axes[i].plot(df['time'], df[f'accel_{axis}_filt'], 
                 label='Filtered', linewidth=2)
    axes[i].set_ylabel(f'Acceleration {axis.upper()} (m/s²)')
    axes[i].legend()
    axes[i].grid(True)

axes[2].set_xlabel('Time (s)')
plt.suptitle('Raw vs. Filtered Acceleration')
plt.tight_layout()
plt.savefig('02_filtered_acceleration.png', dpi=300)
# plt.show()


from ahrs.filters import Madgwick

# Initialize the Madgwick filter
madgwick = Madgwick(frequency=sampling_rate, gain=0.1)

# Prepare arrays for orientation storage
quaternions = np.zeros((len(df), 4))
quaternions[0] = np.array([1.0, 0.0, 0.0, 0.0])  # Initial orientation (identity)

# Iterate through sensor measurements
for i in range(1, len(df)):
    # Extract accelerometer and gyroscope values
    accel = df[['accel_x_filt', 'accel_y_filt', 'accel_z_filt']].iloc[i].values
    gyro = df[['gyro_x_filt', 'gyro_y_filt', 'gyro_z_filt']].iloc[i].values
    
    # Normalize accelerometer (Madgwick uses it as direction reference)
    accel_norm = accel / (np.linalg.norm(accel) + 1e-12)
    
    # Update orientation estimate
    quaternions[i] = madgwick.updateIMU(quaternions[i-1], gyr=gyro, acc=accel_norm)

# Store quaternions in dataframe
df['q_w'] = quaternions[:, 0]
df['q_x'] = quaternions[:, 1]
df['q_y'] = quaternions[:, 2]
df['q_z'] = quaternions[:, 3]



from scipy.spatial.transform import Rotation as R

# Convert quaternions to Euler angles
# Note: R.from_quat expects [x, y, z, w] format, but our quaternions are [w, x, y, z]
# We need to reorder: take columns [1,2,3,0] to convert from [w,x,y,z] to [x,y,z,w]
quaternions_scipy = quaternions[:, [1, 2, 3, 0]]
rotations = R.from_quat(quaternions_scipy)
euler_angles = rotations.as_euler('xyz', degrees=True)

df['roll'] = euler_angles[:, 0]
df['pitch'] = euler_angles[:, 1]
df['yaw'] = euler_angles[:, 2]

# Plot orientation over time
fig, axes = plt.subplots(3, 1, figsize=(12, 8))

axes[0].plot(df['time'], df['roll'])
axes[0].set_ylabel('Roll (degrees)')
axes[0].grid(True)

axes[1].plot(df['time'], df['pitch'])
axes[1].set_ylabel('Pitch (degrees)')
axes[1].grid(True)

axes[2].plot(df['time'], df['yaw'])
axes[2].set_ylabel('Yaw (degrees)')
axes[2].set_xlabel('Time (s)')
axes[2].grid(True)

plt.suptitle('Device Orientation Over Time')
plt.tight_layout()
plt.savefig('03_orientation_euler.png', dpi=300)
# plt.show()






from scipy.spatial.transform import Rotation as R

# Create array for global accelerations
accel_global = np.zeros((len(df), 3))

for i in range(len(df)):
    # Get local acceleration (in phone frame)
    accel_local = df[['accel_x_filt', 'accel_y_filt', 'accel_z_filt']].iloc[i].values
    
    # Get rotation at this time step
    q = quaternions[i]  # Our format: [w, x, y, z]
    rotation = R.from_quat([q[1], q[2], q[3], q[0]])  # scipy expects [x, y, z, w]
    
    # Rotate acceleration to global frame
    accel_global[i] = rotation.apply(accel_local)

# Store global accelerations
df['accel_global_x'] = accel_global[:, 0]
df['accel_global_y'] = accel_global[:, 1]
df['accel_global_z'] = accel_global[:, 2]





# Gravity is approximately 9.81 m/s² in the negative Z direction
# Estimate gravity from the mean during stationary periods
baseline_global = df.iloc[:int(2*sampling_rate)]  # First 2 seconds
gravity_global = baseline_global[['accel_global_x', 'accel_global_y', 'accel_global_z']].mean()

print(f"Estimated gravity vector: {gravity_global.values}")

# Remove gravity
df['accel_motion_x'] = df['accel_global_x'] - gravity_global['accel_global_x']
df['accel_motion_y'] = df['accel_global_y'] - gravity_global['accel_global_y']
df['accel_motion_z'] = df['accel_global_z'] - gravity_global['accel_global_z']



fig, axes = plt.subplots(3, 1, figsize=(12, 8))

axes[0].plot(df['time'], df['accel_motion_x'])
axes[0].set_ylabel('Global X (m/s²)')
axes[0].grid(True)

axes[1].plot(df['time'], df['accel_motion_y'])
axes[1].set_ylabel('Global Y (m/s²)')
axes[1].grid(True)

axes[2].plot(df['time'], df['accel_motion_z'])
axes[2].set_ylabel('Global Z (m/s²)')
axes[2].set_xlabel('Time (s)')
axes[2].grid(True)

plt.suptitle('Motion Acceleration in Global Coordinates')
plt.tight_layout()
plt.savefig('04_global_acceleration.png', dpi=300)
# plt.show()





# # Calculate time step for each sample
# dt_array = df['time'].diff().fillna(0).values

# # Initialize velocity and position arrays
# velocity = np.zeros((len(df), 3))
# position = np.zeros((len(df), 3))

# # Extract acceleration arrays for efficient indexing
# accel_x = df['accel_motion_x'].values
# accel_y = df['accel_motion_y'].values
# accel_z = df['accel_motion_z'].values

# # Numerical integration using trapezoidal rule
# for i in range(1, len(df)):
#     # First integration: Acceleration → Velocity (trapezoidal rule)
#     accel_current = np.array([accel_x[i], accel_y[i], accel_z[i]])
#     accel_previous = np.array([accel_x[i-1], accel_y[i-1], accel_z[i-1]])
#     velocity[i] = velocity[i-1] + 0.5 * (accel_previous + accel_current) * dt_array[i]
    
#     # Second integration: Velocity → Position (trapezoidal rule)
#     position[i] = position[i-1] + 0.5 * (velocity[i-1] + velocity[i]) * dt_array[i]

# # Store results
# df['vel_x'] = velocity[:, 0]
# df['vel_y'] = velocity[:, 1]
# df['vel_z'] = velocity[:, 2]

# df['pos_x'] = position[:, 0]
# df['pos_y'] = position[:, 1]
# df['pos_z'] = position[:, 2]


# --- Integration mit einfacher Driftkorrektur (ZUPT-artig) ---

# Zeitdifferenzen
dt_array = df['time'].diff().fillna(0).values
t = df['time'].values

# Arrays vorbereiten
velocity = np.zeros((len(df), 3))
position = np.zeros((len(df), 3))

# Beschleunigung (bereits: global, gravitationsfrei)
accel_x = df['accel_motion_x'].values
accel_y = df['accel_motion_y'].values
accel_z = df['accel_motion_z'].values

# 1) Erste Integration: a -> v (wie bisher, trapezoidal)
for i in range(1, len(df)):
    a_curr = np.array([accel_x[i],   accel_y[i],   accel_z[i]])
    a_prev = np.array([accel_x[i-1], accel_y[i-1], accel_z[i-1]])
    velocity[i] = velocity[i-1] + 0.5 * (a_prev + a_curr) * dt_array[i]

# 2) Stationäre Phasen detektieren (sehr grob, aber reicht hier)
acc_norm = np.sqrt(accel_x**2 + accel_y**2 + accel_z**2)
gyro_norm = np.linalg.norm(df[['gyro_x', 'gyro_y', 'gyro_z']].values, axis=1)

# Schwellen kannst du bei Bedarf anpassen:
acc_thresh = 0.1   # m/s²
gyro_thresh = 0.05 # rad/s
stationary = (acc_norm < acc_thresh) & (gyro_norm < gyro_thresh)

print(f"Stationary samples: {stationary.sum()} / {len(df)}")

# 3) Drift als v(t) = a*t + b aus den stationären Punkten schätzen und abziehen
vel_corrected = velocity.copy()
for axis in range(3):
    v = velocity[:, axis]
    t_stat = t[stationary]
    v_stat = v[stationary]
    if len(t_stat) > 2:
        A = np.vstack([t_stat, np.ones_like(t_stat)]).T
        a, b = np.linalg.lstsq(A, v_stat, rcond=None)[0]  # lineares Fit
        drift = a * t + b
        vel_corrected[:, axis] = v - drift
    # In stationären Phasen Geschwindigkeit hart auf 0 setzen
    vel_corrected[stationary, axis] = 0.0

velocity = vel_corrected

# 4) Zweite Integration: v -> s mit korrigierter Geschwindigkeit
position = np.zeros_like(velocity)
for i in range(1, len(df)):
    position[i] = position[i-1] + 0.5 * (velocity[i-1] + velocity[i]) * dt_array[i]

# Ergebnisse ins DataFrame schreiben
df['vel_x'] = velocity[:, 0]
df['vel_y'] = velocity[:, 1]
df['vel_z'] = velocity[:, 2]

df['pos_x'] = position[:, 0]
df['pos_y'] = position[:, 1]
df['pos_z'] = position[:, 2]





fig, axes = plt.subplots(3, 1, figsize=(12, 8))

axes[0].plot(df['time'], df['vel_x'])
axes[0].set_ylabel('Velocity X (m/s)')
axes[0].grid(True)

axes[1].plot(df['time'], df['vel_y'])
axes[1].set_ylabel('Velocity Y (m/s)')
axes[1].grid(True)

axes[2].plot(df['time'], df['vel_z'])
axes[2].set_ylabel('Velocity Z (m/s)')
axes[2].set_xlabel('Time (s)')
axes[2].grid(True)

plt.suptitle('Reconstructed Velocity')
plt.tight_layout()
plt.savefig('05_velocity.png', dpi=300)
# plt.show()




plt.figure(figsize=(10, 10))
plt.plot(df['pos_x'], df['pos_y'], linewidth=2, label='Trajectory')

plt.scatter(df['pos_x'].iloc[0], df['pos_y'].iloc[0],
            c='green', s=200, marker='o', label='Start', zorder=5)

plt.scatter(df['pos_x'].iloc[-1], df['pos_y'].iloc[-1],
            c='red', s=200, marker='X', label='End', zorder=5)

plt.xlabel('X Position (m)')
plt.ylabel('Y Position (m)')
plt.title('Reconstructed Trajectory (Top View)')

# --- WICHTIG: gleiche Skalierung für beide Achsen ---
x_min, x_max = df['pos_x'].min(), df['pos_x'].max()
y_min, y_max = df['pos_y'].min(), df['pos_y'].max()

# Gemeinsame Achsenlimits bestimmen
min_lim = min(x_min, y_min)
max_lim = max(x_max, y_max)

plt.xlim(min_lim, max_lim)
plt.ylim(min_lim, max_lim)

plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig('06_trajectory_2d.png', dpi=300)
plt.show()





from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

# Plot trajectory
ax.plot(df['pos_x'], df['pos_y'], df['pos_z'], linewidth=2, label='Trajectory')

# Mark start and end
ax.scatter(df['pos_x'].iloc[0], df['pos_y'].iloc[0], df['pos_z'].iloc[0], 
           c='green', s=200, marker='o', label='Start')
ax.scatter(df['pos_x'].iloc[-1], df['pos_y'].iloc[-1], df['pos_z'].iloc[-1], 
           c='red', s=200, marker='X', label='End')

ax.set_xlabel('X Position (m)')
ax.set_ylabel('Y Position (m)')
ax.set_zlabel('Z Position (m)')
ax.set_title('Reconstructed 3D Trajectory')
ax.legend()

# ------------------------------------------------------
#  GLEICHE SKALIERUNG AUF ALLEN 3 ACHSEN
# ------------------------------------------------------
x = df['pos_x']
y = df['pos_y']
z = df['pos_z']

max_range = max(
    x.max() - x.min(), 
    y.max() - y.min(), 
    z.max() - z.min()
) / 2.0

mid_x = (x.max() + x.min()) / 2.0
mid_y = (y.max() + y.min()) / 2.0
mid_z = (z.max() + z.min()) / 2.0

ax.set_xlim(mid_x - max_range, mid_x + max_range)
ax.set_ylim(mid_y - max_range, mid_y + max_range)
ax.set_zlim(mid_z - max_range, mid_z + max_range)
# ------------------------------------------------------

plt.tight_layout()
plt.savefig('07_trajectory_3d.png', dpi=300)
plt.show()



# Calculate Euclidean distance from start to end
start_pos = np.array([df['pos_x'].iloc[0], df['pos_y'].iloc[0], df['pos_z'].iloc[0]])
end_pos = np.array([df['pos_x'].iloc[-1], df['pos_y'].iloc[-1], df['pos_z'].iloc[-1]])
reconstructed_distance = np.linalg.norm(end_pos - start_pos)

print(f"Reconstructed distance: {reconstructed_distance:.3f} meters")
print(f"Start position: {start_pos}")
print(f"End position: {end_pos}")

# If you measured the actual distance, compare:
# actual_distance = 1.0  # meters (your measurement)
# error = abs(reconstructed_distance - actual_distance)
# print(f"Error: {error:.3f} meters ({error/actual_distance*100:.1f}%)")