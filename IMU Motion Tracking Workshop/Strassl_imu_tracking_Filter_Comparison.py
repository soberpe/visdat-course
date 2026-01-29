#++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++
# Part 2: Data Import and Preprocessing:
#--------------------------------------
# Load and Normalize the Dataset:
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

# Load separate files
accel_df = pd.read_csv('c:/VIS3_GITHUP/visdat-course_my/IMU Motion Tracking Workshop/data/raw/Strassl_acceleration.csv')
gyro_df = pd.read_csv('c:/VIS3_GITHUP/visdat-course_my/IMU Motion Tracking Workshop/data/raw/Strassl_gyroscope.csv')

# MATLAB Mobile typically uses columns: Time, X, Y, Z
# Rename for consistency
accel_df.rename(columns={'timestamp': 'time', 'X': 'accel_x', 'Y': 'accel_y', 'Z': 'accel_z'}, inplace=True)
gyro_df.rename(columns={'timestamp': 'time', 'X': 'gyro_x', 'Y': 'gyro_y', 'Z': 'gyro_z'}, inplace=True)

#print(gyro_df['gyro_x'])

# Merge on timestamp (or use nearest time if sampling rates differ slightly) Messdaten UNIX Format in ms
df = pd.merge_asof(accel_df.sort_values('time'), 
                   gyro_df.sort_values('time'), 
                   on='time', 
                   direction='nearest',
                   tolerance=20)  # 20ms tolerance for sampling rate variations

#print(df['gyro_x'])

# Normalize time to start at zero and convert from ms to seconds
df['time'] = (df['time'] - df['time'].iloc[0]) / 1000.0

#--------------------------------------
# Calculate sampling rate (use median for robustness against jitter):
dt = df['time'].diff().median()
sampling_rate = 1 / dt

#++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++
# Part 3: Signal Filtering:
#--------------------------------------
# Apply Low-Pass Butterworth Filter:
from scipy.signal import butter, filtfilt

def butter_lowpass_filter(data, cutoff, fs, order=2):
    """Apply a Butterworth low-pass filter to the data."""
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    filtered_data = filtfilt(b, a, data)
    return filtered_data


#++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++
# Part 9: Optional Extensions
#--------------------------------------
# Challenge: Filter Comparison:
from scipy.signal import savgol_filter

# Compare three filter types
cutoffs = [3, 5, 10]  # Hz
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

for idx, fc in enumerate(cutoffs):
    # Apply Butterworth filter with different cutoffs
    df[f'accel_x_f{fc}'] = butter_lowpass_filter(df['accel_x'], fc, sampling_rate)
    
    # Recalculate trajectory (simplified) xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    # Apply filter to accelerometer & gyroscope data
    df['accel_x_filt'] = butter_lowpass_filter(df['accel_x'], fc, sampling_rate)
    df['accel_y_filt'] = butter_lowpass_filter(df['accel_y'], fc, sampling_rate)
    df['accel_z_filt'] = butter_lowpass_filter(df['accel_z'], fc, sampling_rate)
    
    # Optional: Filter gyroscope data as well
    df['gyro_x_filt'] = butter_lowpass_filter(df['gyro_x'], fc, sampling_rate)
    df['gyro_y_filt'] = butter_lowpass_filter(df['gyro_y'], fc, sampling_rate)
    df['gyro_z_filt'] = butter_lowpass_filter(df['gyro_z'], fc, sampling_rate)
        

    #++++++++++++++++++++++++++++++++++++++
    #++++++++++++++++++++++++++++++++++++++
    # Part 4: Orientation Estimation with Madgwick Algorithm:
    #--------------------------------------
    # Estimate Orientation Using AHRS Library:
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


    #++++++++++++++++++++++++++++++++++++++
    #++++++++++++++++++++++++++++++++++++++
    # Part 5: Transform Accelerations to Global Coordinates:
    #--------------------------------------
    # Apply Quaternion Rotation:
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

    #--------------------------------------
    # Remove Gravity from Global Accelerations:
    # Gravity is approximately 9.81 m/s² in the negative Z direction
    # Estimate gravity from the mean during stationary periods
    baseline_global = df.iloc[:int(2*sampling_rate)]  # First 2 seconds
    gravity_global = baseline_global[['accel_global_x', 'accel_global_y', 'accel_global_z']].mean()

    # Remove gravity
    df['accel_motion_x'] = df['accel_global_x'] - gravity_global['accel_global_x']
    df['accel_motion_y'] = df['accel_global_y'] - gravity_global['accel_global_y']
    df['accel_motion_z'] = df['accel_global_z'] - gravity_global['accel_global_z']

    #++++++++++++++++++++++++++++++++++++++
    #++++++++++++++++++++++++++++++++++++++
    # Part 6: Numerical Integration to Reconstruct Trajectory:
    #--------------------------------------
    # Integrate to Obtain Velocity and Position:
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
    # Ende Einschub xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    
    axes[idx].plot(df['pos_x'], df['pos_y'])
    axes[idx].set_title(f'Trajectory with {fc} Hz Cutoff')
    axes[idx].scatter(df['pos_x'].iloc[0], df['pos_y'].iloc[0], 
            c='green', s=200, marker='o', label='Start', zorder=5)
    axes[idx].scatter(df['pos_x'].iloc[-1], df['pos_y'].iloc[-1], 
                c='red', s=200, marker='X', label='End', zorder=5)
    axes[idx].set_xlabel('X (m)')
    axes[idx].set_ylabel('Y (m)')
    axes[idx].axis('equal')
    axes[idx].grid(True)
    axes[idx].legend()

plt.tight_layout()
plt.savefig('IMU Motion Tracking Workshop/figures/09_different_filtering.png', dpi=300)
plt.show()
