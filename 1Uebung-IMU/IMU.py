import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

# Load separate files
accel_df = pd.read_csv('1Uebung-IMU\data\Huemer-Accel.csv')
gyro_df = pd.read_csv('1Uebung-IMU\data\Huemer-gyro.csv')

# MATLAB Mobile typically uses columns: Time, X, Y, Z
# Rename for consistency
accel_df.rename(columns={'timestamp': 'time', 'X': 'accel_x', 'Y': 'accel_y', 'Z': 'accel_z'}, inplace=True)
gyro_df.rename(columns={'timestamp': 'time', 'X': 'gyro_x', 'Y': 'gyro_y', 'Z': 'gyro_z'}, inplace=True)

# Merge on timestamp (or use nearest time if sampling rates differ slightly)
df = pd.merge_asof(accel_df.sort_values('time'), 
                   gyro_df.sort_values('time'), 
                   on='time', 
                   direction='nearest',
                   tolerance=20)  # 20ms tolerance for sampling rate variations

# Normalize time to start at zero
df['time'] = (df['time'] - df['time'].iloc[0])/1000.0  # Convert ms to seconds



# Calculate sampling rate (use median for robustness against jitter)
dt = df['time'].diff().median()
sampling_rate = 1 / dt

print(f"Total samples: {len(df)}")
print(f"Duration: {df['time'].max():.2f} seconds")
print(f"Sampling rate: {sampling_rate:.1f} Hz")
print(f"Average time step: {dt:.4f} seconds")

print(df.columns)
# Common patterns:
# - accelX, accelY, accelZ or ax, ay, az
# - gyroX, gyroY, gyroZ or gx, gy, gz
# - acceleration_x, acceleration_y, acceleration_z

df.rename(columns={
    'acceleration_x': 'accel_x',
    'acceleration_y': 'accel_y', 
    'acceleration_z': 'accel_z',
    'gyroscope_x': 'gyro_x',
    'gyroscope_y': 'gyro_y',
    'gyroscope_z': 'gyro_z'
}, inplace=True)


# --- OFFSET KORREKTUR ---

offset_x = 0.8
offset_y = -0.16 
offset_z = 0

print(f"Applying manual offsets: X={offset_x}, Y={offset_y}, Z={offset_z}")

df['accel_x'] = df['accel_x'] - offset_x
df['accel_y'] = df['accel_y'] - offset_y
df['accel_z'] = df['accel_z'] - offset_z

# Überprüfung für Gyroskop (Drift hier ist noch schlimmer für die Orientierung!)
gyro_offset_x = 0.0 # Falls das Gyro nicht 0 anzeigt im Stillstand
gyro_offset_y = 0.0
gyro_offset_z = 0.0

df['gyro_x'] = df['gyro_x'] - gyro_offset_x
df['gyro_y'] = df['gyro_y'] - gyro_offset_y
df['gyro_z'] = df['gyro_z'] - gyro_offset_z



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
plt.show()


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
#plt.show()



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
#plt.show()


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
#plt.show()


# Calculate time step for each sample
dt_array = df['time'].diff().fillna(0).values

# Initialize velocity and position arrays
velocity = np.zeros((len(df), 3))
position = np.zeros((len(df), 3))

# Extract acceleration arrays for efficient indexing
accel_x = df['accel_motion_x'].values
accel_y = df['accel_motion_y'].values
accel_z = df['accel_motion_z'].values

# Numerical integration using trapezoidal rule
for i in range(1, len(df)):
    # First integration: Acceleration → Velocity (trapezoidal rule)
    accel_current = np.array([accel_x[i], accel_y[i], accel_z[i]])
    accel_previous = np.array([accel_x[i-1], accel_y[i-1], accel_z[i-1]])
    velocity[i] = velocity[i-1] + 0.5 * (accel_previous + accel_current) * dt_array[i]
    
    # Second integration: Velocity → Position (trapezoidal rule)
    position[i] = position[i-1] + 0.5 * (velocity[i-1] + velocity[i]) * dt_array[i]

# Store results
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
plt.show()



plt.figure(figsize=(10, 10))
plt.plot(df['pos_x'], df['pos_y'], linewidth=2, label='Trajectory')
plt.scatter(df['pos_x'].iloc[0], df['pos_y'].iloc[0], 
            c='green', s=200, marker='o', label='Start', zorder=5)
plt.scatter(df['pos_x'].iloc[-1], df['pos_y'].iloc[-1], 
            c='red', s=200, marker='X', label='End', zorder=5)
plt.xlabel('X Position (m)')
plt.ylabel('Y Position (m)')
plt.title('Reconstructed Trajectory (Top View)')
plt.axis('equal')
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


