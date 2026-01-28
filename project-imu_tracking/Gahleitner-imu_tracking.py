# Importing Libraries and Modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
from ahrs.filters import Madgwick
from scipy.spatial.transform import Rotation as R
from mpl_toolkits.mplot3d import Axes3D

# Load separate files
# Parameter to select which measurement to load
# 1 = Measurement of 2D rectangular trajectory
# 2 = Measurement of Π-shaped trajectory
# 3 = Measurement 3 of circular trajectory
# 4 = Measurement 4 of folding phone trajectory (→↑→↓)
measurement_number = 1

# Map measurement number to file paths
measurement_files = {
    1: ('project-imu_tracking/data/raw/Gahleitner_rectangle_acceleration.csv', 
        'project-imu_tracking/data/raw/Gahleitner_rectangle_gyroscope.csv'),
    2: ('project-imu_tracking/data/raw/Gahleitner_cshape_acceleration.csv', 
        'project-imu_tracking/data/raw/Gahleitner_cshape_gyroscope.csv'),
    3: ('project-imu_tracking/data/raw/Gahleitner_circular_acceleration.csv', 
        'project-imu_tracking/data/raw/Gahleitner_circular_gyroscope.csv'),
    4: ('project-imu_tracking/data/raw/Gahleitner_fold_acceleration.csv', 
        'project-imu_tracking/data/raw/Gahleitner_fold_gyroscope.csv'),
}

# Load data based on selected measurement
accel_file, gyro_file = measurement_files[measurement_number]
accel_df = pd.read_csv(accel_file)
gyro_df = pd.read_csv(gyro_file)

print(f"Loaded measurement {measurement_number}")

# MATLAB Mobile typically uses columns: Time, X, Y, Z
# Rename for consistency
accel_df.rename(columns={'timestamp': 'time', 'X': 'accel_x', 'Y': 'accel_y', 'Z': 'accel_z'}, inplace=True)
gyro_df.rename(columns={'timestamp': 'time', 'X': 'gyro_x', 'Y': 'gyro_y', 'Z': 'gyro_z'}, inplace=True)

# Convert MATLAB Mobile timestamp (ms) into (s)
accel_df['time'] = accel_df['time'] / 1000.0
gyro_df['time']  = gyro_df['time'] / 1000.0

# Merge on timestamp (or use nearest time if sampling rates differ slightly)
df = pd.merge_asof(accel_df.sort_values('time'), 
                   gyro_df.sort_values('time'), 
                   on='time', 
                   direction='nearest',
                   tolerance=0.02)  # 20ms tolerance for sampling rate variations

# Normalize time to start at zero
df['time'] = df['time'] - df['time'].iloc[0]

# Inspect normalized time data
print(df.head())

# Calculate sampling rate (use median for robustness against jitter)
dt = df['time'].diff().median()
sampling_rate = 1 / dt

print(f"Total samples: {len(df)}")
print(f"Duration: {df['time'].max():.2f} seconds")
print(f"Sampling rate: {sampling_rate:.1f} Hz")
print(f"Average time step: {dt:.2f} seconds")

print(df.columns)

# Check gyroscope units - many apps export deg/s, but Madgwick expects rad/s
gyro_cols = ['gyro_x', 'gyro_y', 'gyro_z']
max_gyro_value = df[gyro_cols].abs().quantile(0.95).max()
#if max_gyro_value > 20:  # Heuristic: >20 likely means deg/s
    #print(f"Gyroscope values appear to be in deg/s (max: {max_gyro_value:.1f})")
    #df[gyro_cols] = np.deg2rad(df[gyro_cols])
    #print("Converted gyroscope data from deg/s to rad/s.")
#else:
    #print(f"Gyroscope values appear to be in rad/s (max: {max_gyro_value:.2f})")
print('Gyroscope data is in rad/s.')



#Signal Filtering

def butter_lowpass_filter(data, cutoff, fs, order=2):
    """Apply a Butterworth low-pass filter to the data."""
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    filtered_data = filtfilt(b, a, data)
    return filtered_data

# Filter parameters
cutoff_frequency = 3  # Hz (adjust based on your movement speed)
fs = sampling_rate

# Apply filter to accelerometer data
df['accel_x_filt'] = butter_lowpass_filter(df['accel_x'], cutoff_frequency, fs)
df['accel_y_filt'] = butter_lowpass_filter(df['accel_y'], cutoff_frequency, fs)
df['accel_z_filt'] = butter_lowpass_filter(df['accel_z'], cutoff_frequency, fs)

# Apply filter to gyroscope data
df['gyro_x_filt'] = butter_lowpass_filter(df['gyro_x'], cutoff_frequency, fs)
df['gyro_y_filt'] = butter_lowpass_filter(df['gyro_y'], cutoff_frequency, fs)
df['gyro_z_filt'] = butter_lowpass_filter(df['gyro_z'], cutoff_frequency, fs)

# Create a dedicated figure for raw sensor data
fig_raw = plt.figure(num='Raw Sensor Data', figsize=(12, 8))
ax1 = fig_raw.add_subplot(2, 1, 1)
ax2 = fig_raw.add_subplot(2, 1, 2)

# Acceleration (raw)
ax1.plot(df['time'], df['accel_x'], label='X', alpha=0.7)
ax1.plot(df['time'], df['accel_y'], label='Y', alpha=0.7)
ax1.plot(df['time'], df['accel_z'], label='Z', alpha=0.7)
ax1.set_ylabel('Acceleration (m/s²)')
ax1.set_title('Raw Accelerometer Data')
ax1.legend()
ax1.grid(True)

# Gyroscope (raw)
ax2.plot(df['time'], df['gyro_x'], label='X', alpha=0.7)
ax2.plot(df['time'], df['gyro_y'], label='Y', alpha=0.7)
ax2.plot(df['time'], df['gyro_z'], label='Z', alpha=0.7)
ax2.set_ylabel('Angular Velocity (rad/s)')
ax2.set_xlabel('Time (s)')
ax2.set_title('Raw Gyroscope Data')
ax2.legend()
ax2.grid(True)

plt.tight_layout()
fig_raw.savefig('project-imu_tracking/figures/01_raw_sensor_data.png', dpi=300)

# Create a figure comparing filtered vs raw data side-by-side
fig_comparison = plt.figure(num='Filtered vs Raw Comparison', figsize=(12, 8))
ax1 = fig_comparison.add_subplot(2, 1, 1)
ax2 = fig_comparison.add_subplot(2, 1, 2)

# Filtered acceleration overlaid with raw
ax1.plot(df['time'], df['accel_x'], label='Raw X', alpha=0.7, linewidth=0.8)
ax1.plot(df['time'], df['accel_y'], label='Raw Y', alpha=0.7, linewidth=0.8)
ax1.plot(df['time'], df['accel_z'], label='Raw Z', alpha=0.7, linewidth=0.8)
ax1.plot(df['time'], df['accel_x_filt'], label='Filtered X', linewidth=2,color='blue')
ax1.plot(df['time'], df['accel_y_filt'], label='Filtered Y', linewidth=2,color='orange')
ax1.plot(df['time'], df['accel_z_filt'], label='Filtered Z', linewidth=2,color='green')
ax1.set_ylabel('Acceleration (m/s²)')
ax1.set_title('Filtered vs Raw Accelerometer Data')
ax1.legend(ncol=2)
ax1.grid(True)

# Filtered gyroscope overlaid with raw
ax2.plot(df['time'], df['gyro_x'], label='Raw X', alpha=0.7, linewidth=0.8)
ax2.plot(df['time'], df['gyro_y'], label='Raw Y', alpha=0.7, linewidth=0.8)
ax2.plot(df['time'], df['gyro_z'], label='Raw Z', alpha=0.7, linewidth=0.8)
ax2.plot(df['time'], df['gyro_x_filt'], label='Filtered X', linewidth=2,color='blue')
ax2.plot(df['time'], df['gyro_y_filt'], label='Filtered Y', linewidth=2,color='orange')
ax2.plot(df['time'], df['gyro_z_filt'], label='Filtered Z', linewidth=2,color='green')
ax2.set_ylabel('Angular Velocity (rad/s)')
ax2.set_xlabel('Time (s)')
ax2.set_title('Filtered vs Raw Gyroscope Data')
ax2.legend(ncol=2)
ax2.grid(True)

plt.tight_layout()
fig_comparison.savefig('project-imu_tracking/figures/02_filtered_comparison.png', dpi=300)

# Estimate orientation using Madgwick filter
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

# Convert quaternions to Euler angles
# Note: R.from_quat expects [x, y, z, w] format, but our quaternions are [w, x, y, z]
# We need to reorder: take columns [1,2,3,0] to convert from [w,x,y,z] to [x,y,z,w]
quaternions_scipy = quaternions[:, [1, 2, 3, 0]]
rotations = R.from_quat(quaternions_scipy)
euler_angles = rotations.as_euler('xyz', degrees=True)

df['roll'] = euler_angles[:, 0]
df['pitch'] = euler_angles[:, 1]
df['yaw'] = euler_angles[:, 2]


# Create a Orientation Plot
fig_orient = plt.figure(num='Orientation', figsize=(12, 8))

# Roll
ax1 = fig_orient.add_subplot(3, 1, 1)
ax1.plot(df['time'], df['roll'], label='Roll (degrees)', alpha=0.7)
ax1.set_ylabel('Roll (degrees)')
ax1.set_title('Roll over Time')
ax1.legend()
ax1.grid(True)

# Pitch
ax2 = fig_orient.add_subplot(3, 1, 2)
ax2.plot(df['time'], df['pitch'], label='Pitch (degrees)', alpha=0.7, color='orange')
ax2.set_ylabel('Pitch (degrees)')
ax2.set_title('Pitch over Time')
ax2.legend()
ax2.grid(True)

# Yaw
ax3 = fig_orient.add_subplot(3, 1, 3)
ax3.plot(df['time'], df['yaw'], label='Yaw (degrees)', alpha=0.7, color='green')
ax3.set_ylabel('Yaw (°)')
ax3.set_xlabel('Time (s)')
ax3.set_title('Yaw over Time')
ax3.legend()
ax3.grid(True)

plt.tight_layout()
fig_orient.savefig('project-imu_tracking/figures/03_orientation_data.png', dpi=300)



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

# Create a Orientation Plot
fig_accel_motion = plt.figure(num='Motion Acceleration in Global Coordinates', figsize=(12, 8))

# X
ax1 = fig_accel_motion.add_subplot(3, 1, 1)
ax1.plot(df['time'], df['accel_motion_x'], label='Global X (m/s²)', alpha=0.7)
ax1.set_ylabel('Global X (m/s²)')
ax1.set_title('Global X (m/s²)')
ax1.legend()
ax1.grid(True)

# Y
ax2 = fig_accel_motion.add_subplot(3, 1, 2)
ax2.plot(df['time'], df['accel_motion_y'], label='Global Y (m/s²)', alpha=0.7, color='orange')
ax2.set_ylabel('Global Y (m/s²)')
ax1.set_title('Global Y (m/s²)')
ax2.legend()
ax2.grid(True)

# Z
ax3 = fig_accel_motion.add_subplot(3, 1, 3)
ax3.plot(df['time'], df['accel_motion_z'], label='Global Z (m/s²)', alpha=0.7, color='green')
ax3.set_ylabel('Global Z (m/s²)')
ax3.set_xlabel('Time (s)')
ax1.set_title('Global Accelerations (m/s²)')
ax3.legend()
ax3.grid(True)

plt.tight_layout()
fig_accel_motion.savefig('project-imu_tracking/figures/04_global_acceleration.png', dpi=300)


# Numerical Integration to Reconstruct Trajectory
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

# Create a Velocity Plot
fig_velocity = plt.figure(num='Reconstructed Velocity', figsize=(12, 8))

# Velocity X
ax1 = fig_velocity.add_subplot(3, 1, 1)
ax1.plot(df['time'], df['vel_x'], label='Velocity X (m/s)', alpha=0.7)
ax1.set_ylabel('Velocity X (m/s)')
ax1.set_title('Velocity X (m/s)')
ax1.legend()
ax1.grid(True)

# Velocity Y
ax2 = fig_velocity.add_subplot(3, 1, 2)
ax2.plot(df['time'], df['vel_y'], label='Velocity Y (m/s)', alpha=0.7, color='orange')
ax2.set_ylabel('Velocity Y (m/s)')
ax2.set_title('Velocity Y (m/s)')
ax2.legend()
ax2.grid(True)

# Velocity Z
ax3 = fig_velocity.add_subplot(3, 1, 3)
ax3.plot(df['time'], df['vel_z'], label='Velocity Z (m/s)', alpha=0.7, color='green')
ax3.set_ylabel('Velocity Z (m/s)')
ax3.set_xlabel('Time (s)')
ax3.set_title('Velocity Z (m/s)')
ax3.legend()
ax3.grid(True)

plt.tight_layout()
fig_velocity.savefig('project-imu_tracking/figures/05_velocity.png', dpi=300)

# Create a Trajectory Plot
fig_trajectory = plt.figure(num='Reconstructed Trajectory (Top View)', figsize=(12, 8))
ax = fig_trajectory.add_subplot(1, 1, 1)  # single subplot

# Plot trajectory
ax.plot(df['pos_x'], df['pos_y'], linewidth=2, label='Trajectory')
ax.scatter(df['pos_x'].iloc[0], df['pos_y'].iloc[0], 
           c='green', s=200, marker='o', label='Start', zorder=5)
ax.scatter(df['pos_x'].iloc[-1], df['pos_y'].iloc[-1], 
           c='red', s=200, marker='X', label='End', zorder=5)

# Labels and title
ax.set_xlabel('X Position (m)')
ax.set_ylabel('Y Position (m)')
ax.set_title('Reconstructed Trajectory (Top View)')
ax.axis('equal')
ax.grid(True, alpha=0.3)
ax.legend()

plt.tight_layout()
fig_trajectory.savefig('project-imu_tracking/figures/06_trajectory_2d.png', dpi=300)

# Create a 3D Trajectory Plot
fig_trajectory_3d = plt.figure(num='Reconstructed 3D Trajectory', figsize=(12, 8))
ax = fig_trajectory_3d.add_subplot(1, 1, 1, projection='3d')

# Plot trajectory
ax.plot(df['pos_x'], df['pos_y'], df['pos_z'], linewidth=2, label='Trajectory')

# Mark start and end
ax.scatter(df['pos_x'].iloc[0], df['pos_y'].iloc[0], df['pos_z'].iloc[0], 
           c='green', s=200, marker='o', label='Start')
ax.scatter(df['pos_x'].iloc[-1], df['pos_y'].iloc[-1], df['pos_z'].iloc[-1], 
           c='red', s=200, marker='X', label='End')

# Labels and title
ax.set_xlabel('X Position (m)')
ax.set_ylabel('Y Position (m)')
ax.set_zlabel('Z Position (m)')
ax.set_title('Reconstructed 3D Trajectory')
ax.legend()

plt.tight_layout()
fig_trajectory_3d.savefig('project-imu_tracking/figures/07_trajectory_3d.png', dpi=300)

# Calculate Euclidean distance from start to end
start_pos = np.array([df['pos_x'].iloc[0], df['pos_y'].iloc[0], df['pos_z'].iloc[0]])
end_pos = np.array([df['pos_x'].iloc[-1], df['pos_y'].iloc[-1], df['pos_z'].iloc[-1]])
reconstructed_distance = np.linalg.norm(end_pos - start_pos)

print(f"Reconstructed distance: {reconstructed_distance:.3f} meters")
print(f"Start position: {start_pos}")
print(f"End position: {end_pos}")


# Calculate acceleration magnitude in global frame
accel_magnitude = np.sqrt(
    df['accel_motion_x']**2 + 
    df['accel_motion_y']**2 + 
    df['accel_motion_z']**2
)

# Define stationary threshold
stationary_threshold = 0.2  # m/s²
is_stationary = accel_magnitude < stationary_threshold

# Apply ZUPT: reset velocity during stationary periods
velocity_zupt = velocity.copy()
for i in range(len(df)):
    if is_stationary.iloc[i]:
        velocity_zupt[i] = np.array([0.0, 0.0, 0.0])

# Reintegrate position with ZUPT-corrected velocity using trapezoidal rule
position_zupt = np.zeros((len(df), 3))
for i in range(1, len(df)):
    position_zupt[i] = position_zupt[i-1] + 0.5 * (velocity_zupt[i-1] + velocity_zupt[i]) * dt_array[i]

# Compare trajectories
fig, (ax1, ax2) = plt.subplots(1, 2,num='ZUPT', figsize=(12, 8))

ax1.plot(position[:, 0], position[:, 1], label='Without ZUPT')
ax1.set_xlabel('X (m)')
ax1.set_ylabel('Y (m)')
ax1.set_title('Trajectory Without ZUPT')
ax1.axis('equal')
ax1.grid(True)

ax2.plot(position_zupt[:, 0], position_zupt[:, 1], label='With ZUPT', color='orange')
ax2.set_xlabel('X (m)')
ax2.set_ylabel('Y (m)')
ax2.set_title('Trajectory With ZUPT')
ax2.axis('equal')
ax2.grid(True)

plt.tight_layout()
plt.savefig('project-imu_tracking/figures/08_zupt_comparison.png', dpi=300)



from scipy.signal import savgol_filter

# Compare three filter types
cutoffs = [3, 5, 10]  # Hz
fig, axes = plt.subplots(1, 3,num='Different filter types', figsize=(12, 8))

for idx, fc in enumerate(cutoffs):
    # Apply Butterworth filter with different cutoffs
    df[f'accel_x_f{fc}'] = butter_lowpass_filter(df['accel_x'], fc, sampling_rate)
    
    # Recalculate trajectory (simplified - you would repeat full pipeline)
    # ... orientation, transformation, integration ...
    
    axes[idx].plot(df['pos_x'], df['pos_y'])
    axes[idx].set_title(f'Trajectory with {fc} Hz Cutoff')
    axes[idx].set_xlabel('X (m)')
    axes[idx].set_ylabel('Y (m)')
    axes[idx].axis('equal')
    axes[idx].grid(True)

plt.tight_layout()



# Use first stationary period to estimate bias
stationary_period = df[df['time'] <= 2.0]

# Estimate acceleration bias
accel_bias = stationary_period[['accel_x_filt', 'accel_y_filt', 'accel_z_filt']].mean()
print(f"Estimated acceleration bias: {accel_bias.values}")

# Estimate gyroscope bias
gyro_bias = stationary_period[['gyro_x_filt', 'gyro_y_filt', 'gyro_z_filt']].mean()
print(f"Estimated gyroscope bias: {gyro_bias.values}")

# Apply bias correction
df['accel_x_corrected'] = df['accel_x_filt'] - accel_bias['accel_x_filt']
df['accel_y_corrected'] = df['accel_y_filt'] - accel_bias['accel_y_filt']
df['accel_z_corrected'] = df['accel_z_filt'] - accel_bias['accel_z_filt']


# Show all plots
plt.show()
