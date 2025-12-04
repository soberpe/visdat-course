---
title: IMU Motion Tracking Workshop
---

# IMU Motion Tracking Workshop

## Overview

This workshop guides you through the complete pipeline of sensor-based motion reconstruction. You will capture real IMU data from your smartphone, process and filter the measurements, estimate device orientation using quaternions, transform accelerations into global coordinates, and finally reconstruct the 3D trajectory through numerical integration.

## Goal of This Workshop

Your task is to reconstruct a simple movement performed with your smartphone from raw sensor data.

**What you will do:**
1. Record accelerometer and gyroscope data using a smartphone app
2. Load and preprocess the sensor measurements in Python
3. Estimate the device orientation over time using the Madgwick algorithm
4. Transform local accelerations into a global reference frame using quaternion rotations
5. Integrate accelerations twice to obtain velocity and position
6. Visualize the reconstructed 3D trajectory and analyze error sources

**What you will learn:**
- How IMU sensors work and their limitations
- The role of sensor fusion in orientation estimation
- How coordinate transformations affect motion reconstruction
- Why integration errors accumulate (drift) and how to identify them
- Practical techniques for filtering and processing time series data

:::note Expected Outcome
You will produce a 2D or 3D plot showing the reconstructed path of your smartphone movement. The trajectory will drift due to sensor noise and integration errors. Understanding why this happens is a key learning objective.
:::

## Learning Objectives

By completing this workshop, you will:

- Capture real IMU data (accelerometer and gyroscope) using a smartphone
- Import and structure time series sensor data in Python with pandas
- Apply signal filtering techniques (low-pass filters) to reduce noise
- Understand and implement quaternion-based orientation estimation (Madgwick algorithm)
- Transform vectors between local and global coordinate systems using rotation matrices
- Perform numerical integration to reconstruct velocity and position from acceleration
- Visualize sensor data and trajectories using matplotlib
- Critically evaluate error sources such as sensor bias, drift, and integration artifacts

## Prerequisites

- Smartphone with IMU sensors (any modern device)
- One of the following apps for sensor logging:
  - **MATLAB Mobile** (iOS/Android)
  - **PhyPhox** (iOS/Android, free)
  - **Sensor Logger** (iOS)
  - **Sensor Recorders** (Android)
- Python environment with the following packages:
  - `pandas`, `numpy`, `matplotlib`
  - `scipy` (for filtering)
  - `ahrs` (for orientation estimation)
- Basic understanding of vectors, coordinate systems, and integration

## Part 1: Data Acquisition

### Step 1: Choose and Install a Sensor App

Select one of the recommended apps from your app store. All provide CSV export of accelerometer and gyroscope data.

### Step 2: Configure Sensors

Enable the following sensors in your chosen app:

1. **Accelerometer** (measures linear acceleration in m/s²)
2. **Gyroscope** (measures angular velocity in rad/s)
3. Set sampling rate to **at least 50 Hz**, preferably **100 Hz**

:::info Background
The accelerometer measures linear acceleration in three axes (x, y, z). The gyroscope measures rotational velocity around each axis. Together, these sensors form an Inertial Measurement Unit (IMU) used in smartphones, drones, aircraft, and robotics for motion sensing and navigation.
:::

### Step 3: Perform a Controlled Movement

Execute a simple, repeatable movement with your smartphone:

**Recommended movements:**
- Forward/backward slide on a table (1-2 meters)
- Circular motion in the horizontal plane
- L-shaped path
- Up/down vertical motion

**Recording procedure:**
1. Start sensor recording
2. **Keep the phone completely still for 2-3 seconds** (baseline period)
3. Perform your chosen movement slowly and deliberately
4. **Keep still again for 2-3 seconds** at the end
5. Stop recording

:::tip Best Practice
Starting and ending with the phone at rest is critical. The stationary periods allow you to estimate sensor bias and validate your processing pipeline. Perform the movement slowly to minimize high-frequency noise.
:::

### Step 4: Export and Save Data

Export the recorded data as CSV. Most apps allow sharing via email, cloud storage, or direct file transfer.

**Note on file formats:**
- **MATLAB Mobile** exports separate CSV files for each sensor (e.g., `Acceleration.csv` and `AngularVelocity.csv`)
- **PhyPhox** and **Sensor Logger** typically export single CSV files with all sensors
- Check your app's export format and adjust the import code accordingly

Save your files in your project under:
```
data/raw/your_lastname_acceleration.csv
data/raw/your_lastname_gyroscope.csv
```

Or for single-file exports:
```
data/raw/your_lastname_imu.csv
```

## Part 2: Data Import and Preprocessing

### Load and Normalize the Dataset

The import process depends on whether your app exports a single file or separate files per sensor.

**Option A: Single CSV file (PhyPhox, Sensor Logger)**

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

# Load the data
df = pd.read_csv('data/raw/your_lastname_imu.csv')

# Normalize time to start at zero
df['time'] = df['time'] - df['time'].iloc[0]
```

**Option B: Separate CSV files (MATLAB Mobile)**

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

# Load separate files
accel_df = pd.read_csv('data/raw/your_lastname_acceleration.csv')
gyro_df = pd.read_csv('data/raw/your_lastname_gyroscope.csv')

# MATLAB Mobile typically uses columns: Time, X, Y, Z
# Rename for consistency
accel_df.rename(columns={'Time': 'time', 'X': 'accel_x', 'Y': 'accel_y', 'Z': 'accel_z'}, inplace=True)
gyro_df.rename(columns={'Time': 'time', 'X': 'gyro_x', 'Y': 'gyro_y', 'Z': 'gyro_z'}, inplace=True)

# Merge on timestamp (or use nearest time if sampling rates differ slightly)
df = pd.merge_asof(accel_df.sort_values('time'), 
                   gyro_df.sort_values('time'), 
                   on='time', 
                   direction='nearest',
                   tolerance=0.02)  # 20ms tolerance for sampling rate variations

# Normalize time to start at zero
df['time'] = df['time'] - df['time'].iloc[0]
```

### Calculate Sampling Rate

```python
# Calculate sampling rate (use median for robustness against jitter)
dt = df['time'].diff().median()
sampling_rate = 1 / dt

print(f"Total samples: {len(df)}")
print(f"Duration: {df['time'].max():.2f} seconds")
print(f"Sampling rate: {sampling_rate:.1f} Hz")
print(f"Average time step: {dt:.4f} seconds")
```

### Inspect Column Names

Different apps use different naming conventions. Identify your acceleration and gyroscope columns:

```python
print(df.columns)
# Common patterns:
# - accelX, accelY, accelZ or ax, ay, az
# - gyroX, gyroY, gyroZ or gx, gy, gz
# - acceleration_x, acceleration_y, acceleration_z
```

Rename columns for consistency if needed:

```python
df.rename(columns={
    'acceleration_x': 'accel_x',
    'acceleration_y': 'accel_y', 
    'acceleration_z': 'accel_z',
    'gyroscope_x': 'gyro_x',
    'gyroscope_y': 'gyro_y',
    'gyroscope_z': 'gyro_z'
}, inplace=True)
```

### Check and Convert Gyroscope Units

Many sensor apps export gyroscope data in degrees per second, but the Madgwick filter expects radians per second. Check and convert if needed:

```python
# Check gyroscope units - many apps export deg/s, but Madgwick expects rad/s
gyro_cols = ['gyro_x', 'gyro_y', 'gyro_z']
max_gyro_value = df[gyro_cols].abs().quantile(0.95).max()

if max_gyro_value > 20:  # Heuristic: >20 likely means deg/s
    print(f"Gyroscope values appear to be in deg/s (max: {max_gyro_value:.1f})")
    df[gyro_cols] = np.deg2rad(df[gyro_cols])
    print("Converted gyroscope data from deg/s to rad/s.")
else:
    print(f"Gyroscope values appear to be in rad/s (max: {max_gyro_value:.2f})")
```

:::warning Unit Conversion
Always verify your sensor units! The AHRS library expects **rad/s** for gyroscope and **m/s²** for accelerometer. Using wrong units will produce completely incorrect orientation estimates.
:::

### Plot Raw Sensor Data

```python
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
```

## Part 3: Signal Filtering

### Apply Low-Pass Butterworth Filter

Raw sensor data contains high-frequency noise. Apply a second-order Butterworth low-pass filter to smooth the signals.

```python
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
```

:::note Terminology
A **low-pass filter** attenuates high-frequency components while preserving low-frequency trends. The cutoff frequency determines which frequencies are preserved. A value of 5 Hz is appropriate for slow human movements.
:::

### Visualize Filtering Effect

```python
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
plt.show()
```

## Part 4: Orientation Estimation with Madgwick Algorithm

### Understanding the Problem

The accelerometer measures acceleration in the **phone's local coordinate system**. To reconstruct the actual trajectory in global (world) coordinates, we must track how the phone is oriented at each moment. This is where the gyroscope becomes essential.

:::info Background
The **Madgwick algorithm** is a computationally efficient orientation filter that fuses accelerometer and gyroscope data to estimate device orientation. Developed by Sebastian Madgwick in 2010, it uses quaternions to represent 3D rotations and combines the high-frequency accuracy of the gyroscope with the long-term stability of the accelerometer (which senses gravity direction).

Unlike simple integration of gyroscope data, Madgwick applies a gradient descent optimization to correct drift by ensuring the estimated orientation aligns with the gravity vector measured by the accelerometer. The algorithm is widely used in robotics, drones, and motion tracking applications due to its low computational cost and good performance.

**Key reference:**  
Madgwick, S. (2010). *An efficient orientation filter for inertial and inertial/magnetic sensor arrays*. Report x-io and University of Bristol (UK), 25, 113-118.  
Available at: [https://x-io.co.uk/open-source-imu-and-ahrs-algorithms/](https://x-io.co.uk/open-source-imu-and-ahrs-algorithms/)
:::

### Implementation Options

You have two options for implementing the Madgwick filter:

**Option A: Use the AHRS library** (recommended for this workshop)

```python
# Install using pip
# pip install ahrs
```

**Option B: Implement Madgwick yourself** (advanced, see below for simplified implementation)

### Estimate Orientation Using AHRS Library

```python
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
```

:::note Terminology
A **quaternion** is a four-dimensional representation of 3D rotation: `q = [w, x, y, z]`. Quaternions avoid gimbal lock and provide smooth interpolation, making them ideal for continuous orientation tracking.
:::

### Convert Quaternions to Euler Angles (Optional)

For visualization and intuition, you can convert quaternions to roll, pitch, and yaw angles.

```python
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
plt.show()
```

### Understanding the Madgwick Algorithm

:::note Optional Appendix
The following section explains the mathematical foundations of the Madgwick algorithm. **You do NOT need this for the assignment** - the AHRS library handles all the math for you. This section is provided for those who want to understand how the filter works internally.
:::

For those interested in the mathematical foundation, here is how the Madgwick algorithm works.

:::info Algorithm Overview
The Madgwick filter estimates orientation by fusing gyroscope and accelerometer measurements. It combines:
1. **Gyroscope integration** for high-frequency tracking (but accumulates drift)
2. **Accelerometer correction** for long-term stability (uses gravity as reference)
:::

#### Quaternion Representation

Orientation is represented as a unit quaternion:

$$
\mathbf{q} = \begin{bmatrix} q_0 & q_1 & q_2 & q_3 \end{bmatrix}^T = \begin{bmatrix} w & x & y & z \end{bmatrix}^T
$$

where $||\mathbf{q}|| = 1$.

**Quaternion multiplication** $\mathbf{p} \otimes \mathbf{q}$ combines two rotations. Given $\mathbf{p} = [p_0, p_1, p_2, p_3]^T$ and $\mathbf{q} = [q_0, q_1, q_2, q_3]^T$:

$$
\mathbf{p} \otimes \mathbf{q} = \begin{bmatrix}
p_0 q_0 - p_1 q_1 - p_2 q_2 - p_3 q_3 \\
p_0 q_1 + p_1 q_0 + p_2 q_3 - p_3 q_2 \\
p_0 q_2 - p_1 q_3 + p_2 q_0 + p_3 q_1 \\
p_0 q_3 + p_1 q_2 - p_2 q_1 + p_3 q_0
\end{bmatrix}
$$

**Relationship to rotation matrices:** Quaternion multiplication is equivalent to matrix multiplication of the corresponding rotation matrices. If $\mathbf{R}_a$ is the rotation matrix for quaternion $\mathbf{q}_a$ and $\mathbf{R}_b$ for $\mathbf{q}_b$, then the composition satisfies:

$$
\mathbf{q}_a \otimes \mathbf{q}_b \quad \Leftrightarrow \quad \mathbf{R}_a \cdot \mathbf{R}_b
$$

This means composing rotations with quaternions gives the same result as multiplying rotation matrices, but quaternions are more computationally efficient and avoid gimbal lock.

This operation is **non-commutative**: $\mathbf{p} \otimes \mathbf{q} \neq \mathbf{q} \otimes \mathbf{p}$ (order matters, just like matrix multiplication).

The **quaternion conjugate** is $\mathbf{q}^* = [q_0, -q_1, -q_2, -q_3]^T$, which represents the inverse rotation for unit quaternions.

:::note Terminology
Quaternion multiplication allows us to:
- **Compose rotations**: Apply rotation $\mathbf{p}$ followed by rotation $\mathbf{q}$ as $\mathbf{q} \otimes \mathbf{p}$
- **Rotate vectors**: Transform vector $\mathbf{v}$ by rotation $\mathbf{q}$ as $\mathbf{q} \otimes \mathbf{v} \otimes \mathbf{q}^*$
- **Compute orientation rate**: From angular velocity to quaternion derivative
:::

#### Gyroscope-Based Prediction

The rate of change of the quaternion from gyroscope measurements $\boldsymbol{\omega} = [\omega_x, \omega_y, \omega_z]^T$ is:

$$
\dot{\mathbf{q}}_{\omega} = \frac{1}{2} \mathbf{q} \otimes \begin{bmatrix} 0 & \omega_x & \omega_y & \omega_z \end{bmatrix}^T
$$

This formula converts the angular velocity (in rad/s) into the rate of change of the orientation quaternion. The factor $\frac{1}{2}$ comes from the quaternion derivative relationship, and the angular velocity is treated as a pure quaternion (zero scalar part).

**Interpretation:** This is the time derivative of the orientation quaternion. If we think of rotation matrices, this would be equivalent to:

$$
\dot{\mathbf{R}} = \mathbf{R} \cdot [\boldsymbol{\omega}]_{\times}
$$

where $[\boldsymbol{\omega}]_{\times}$ is the skew-symmetric matrix of angular velocity. The quaternion formulation provides the same result but with simpler arithmetic and better numerical stability.

#### Accelerometer-Based Correction

The accelerometer measures gravity in the sensor frame. The algorithm computes the error between:
- **Predicted gravity direction** (from current quaternion)
- **Measured gravity** (from accelerometer)

**How predicted gravity is computed:**

The world frame gravity vector is $\mathbf{g}_{world} = [0, 0, -g]^T$ where $g \approx 9.81$ m/s² points downward. Given the current orientation quaternion $\mathbf{q}$, we can predict what gravity should look like in the sensor frame by applying the inverse rotation:

$$
\mathbf{g}_{sensor} = \mathbf{q}^* \otimes \begin{bmatrix} 0 \\ 0 \\ 0 \\ -g \end{bmatrix} \otimes \mathbf{q}
$$

where $\mathbf{q}^*$ is the conjugate quaternion. This is what the terms in the objective function represent.

**Does this only work for static cases?**

No, but with important limitations:
- **During static periods**: The accelerometer measures only gravity, so the predicted and measured gravity should match perfectly
- **During dynamic motion**: The accelerometer measures gravity plus linear acceleration, so the match is imperfect
- **Algorithm response**: The Madgwick filter uses the gain parameter $\beta$ to control how much it trusts accelerometer corrections during motion

:::warning Limitation
The Madgwick filter assumes that most of the time, the sensor experiences primarily rotational motion without sustained linear acceleration. For highly dynamic scenarios with constant acceleration (e.g., vehicles, high-speed motion), more sophisticated filters like Extended Kalman Filters with explicit linear acceleration modeling are needed.
:::

**Computing the error between predicted and measured gravity:**

To quantify how well the current orientation estimate matches the accelerometer measurement, we need a mathematical expression. The Madgwick algorithm uses gradient descent to minimize the difference between:
- The gravity direction predicted by the current quaternion $\mathbf{q}$
- The normalized accelerometer reading $\mathbf{a}$

The objective function expresses this difference. It is derived by rotating the known world-frame gravity vector $[0, 0, -1]^T$ into the sensor frame using the quaternion, then subtracting the measured acceleration:

$$
f(\mathbf{q}, \mathbf{a}) = \begin{bmatrix}
2(q_1 q_3 - q_0 q_2) - a_x \\
2(q_0 q_1 + q_2 q_3) - a_y \\
2(0.5 - q_1^2 - q_2^2) - a_z
\end{bmatrix}
$$

where $\mathbf{a} = [a_x, a_y, a_z]^T$ is the normalized accelerometer measurement. The left-hand terms represent the predicted gravity components in the sensor frame, derived from the quaternion rotation formula.

**Gradient descent optimization:**

To find the correction that minimizes this error, we need the gradient of $f$ with respect to the quaternion. This is captured by the Jacobian:

$$
J(\mathbf{q}) = \begin{bmatrix}
-2q_2 & 2q_3 & -2q_0 & 2q_1 \\
2q_1 & 2q_0 & 2q_3 & 2q_2 \\
0 & -4q_1 & -4q_2 & 0
\end{bmatrix}
$$

The gradient descent correction step is:

$$
\Delta \mathbf{q} = \frac{J^T(\mathbf{q}) f(\mathbf{q}, \mathbf{a})}{||J^T(\mathbf{q}) f(\mathbf{q}, \mathbf{a})||}
$$

#### Sensor Fusion

The two estimates are combined:

$$
\dot{\mathbf{q}} = \dot{\mathbf{q}}_{\omega} - \beta \Delta \mathbf{q}
$$

where $\beta$ is the algorithm gain that controls the balance between gyroscope and accelerometer influence.

#### Integration

Finally, the quaternion is updated through numerical integration:

$$
\mathbf{q}_{t+1} = \frac{\mathbf{q}_t + \dot{\mathbf{q}} \Delta t}{||\mathbf{q}_t + \dot{\mathbf{q}} \Delta t||}
$$

The normalization ensures the quaternion remains a unit quaternion.

:::tip Parameter Selection
The gain parameter $\beta$ determines convergence speed vs. noise rejection:
- **Higher $\beta$** (e.g., 0.5): Faster convergence, but more sensitive to accelerometer noise
- **Lower $\beta$** (e.g., 0.033): Slower convergence, better noise rejection
- **Typical values**: 0.1 for general motion tracking
:::

## Part 5: Transform Accelerations to Global Coordinates

### Apply Quaternion Rotation

Now that we have the orientation at each time step, we can rotate the local accelerations into the global reference frame.

```python
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
```

### Remove Gravity from Global Accelerations

After transformation, gravity appears as a constant acceleration vector in the global frame. The direction depends on how the device was oriented initially, but it's constant during stationary periods. We estimate and subtract this gravity vector to obtain only the motion-induced accelerations.

```python
# Gravity is approximately 9.81 m/s² in the negative Z direction
# Estimate gravity from the mean during stationary periods
baseline_global = df.iloc[:int(2*sampling_rate)]  # First 2 seconds
gravity_global = baseline_global[['accel_global_x', 'accel_global_y', 'accel_global_z']].mean()

print(f"Estimated gravity vector: {gravity_global.values}")

# Remove gravity
df['accel_motion_x'] = df['accel_global_x'] - gravity_global['accel_global_x']
df['accel_motion_y'] = df['accel_global_y'] - gravity_global['accel_global_y']
df['accel_motion_z'] = df['accel_global_z'] - gravity_global['accel_global_z']
```

:::tip Best Practice
If your device was not perfectly horizontal during the stationary period, the gravity vector will not align exactly with the Z-axis. The mean acceleration during rest provides the best estimate of the gravity vector in global coordinates.
:::

### Visualize Global Accelerations

```python
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
plt.show()
```

## Part 6: Numerical Integration to Reconstruct Trajectory

### Integrate to Obtain Velocity and Position

Now integrate the global motion accelerations twice: first to get velocity, then to get position.

```python
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
```

:::warning Common Pitfall
Double integration amplifies errors exponentially. Even small sensor biases (on the order of 0.01 m/s²) accumulate into meter-scale position errors within seconds. This is the fundamental challenge of inertial navigation. Professional systems use sensor fusion with GPS, magnetometers, or visual odometry to correct drift.
:::

### Visualize Velocity Over Time

```python
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
```

## Part 7: Trajectory Visualization

### Plot 2D Trajectory (Top View)

```python
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
```

### Plot 3D Trajectory

```python
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
```

## Part 8: Analysis and Discussion

### Calculate Reconstructed Distance

```python
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
```

### Reflection Questions

Answer these questions based on your results:

1. **Drift observation**: Does the trajectory drift away from the expected path? Where does drift appear most prominently?

2. **Error accumulation**: How do small sensor errors grow over time through integration?

3. **Orientation accuracy**: Does the Madgwick filter provide stable orientation estimates? How would errors in orientation affect the final trajectory?

4. **Filter impact**: Compare filtered vs. unfiltered accelerations. How does the cutoff frequency affect results?

5. **Stationary periods**: Did starting and ending at rest help calibrate the sensors? What happens if you skip the baseline?

### Understanding Drift and Error Sources

Sensor drift is a fundamental challenge in inertial navigation. The primary error sources are:

- **Sensor bias**: Constant offset in acceleration measurements (even 0.01 m/s² bias causes meter-scale drift in seconds)
- **Integration error**: Numerical integration amplifies small errors exponentially
- **Orientation errors**: Small errors in estimated orientation cause accelerations to be projected incorrectly
- **Noise**: High-frequency measurement noise affects integration accuracy

:::info Background
Professional inertial navigation systems (INS) address drift through sensor fusion. Common approaches include:
- **GPS integration**: Periodic position corrections from satellite navigation
- **Magnetometer**: Heading reference to correct yaw drift
- **Zero-velocity updates (ZUPT)**: Reset velocity during detected stationary periods
- **Kalman filtering**: Optimal fusion of multiple sensor modalities
- **Visual odometry**: Camera-based motion estimation
:::

## Part 9: Optional Extensions

### Advanced: Zero-Velocity Update (ZUPT)

Detect stationary periods and reset velocity to zero, reducing drift accumulation.

```python
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
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

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
plt.savefig('08_zupt_comparison.png', dpi=300)
plt.show()
```

### Experiment with Different Movements

Try recording these movement patterns and observe how well they can be reconstructed:

- **Straight line**: Simplest case, best for validating your pipeline
- **Circle**: Tests orientation tracking and centripetal acceleration handling
- **Figure-eight**: More complex, reveals orientation drift
- **Vertical motion**: Tests gravity compensation
- **Sharp turns**: Challenges orientation estimation

### Challenge: Filter Comparison

Compare different filtering approaches and their impact on trajectory accuracy:

```python
from scipy.signal import savgol_filter

# Compare three filter types
cutoffs = [3, 5, 10]  # Hz
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

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
plt.show()
```

### Challenge: Sensor Bias Estimation

Estimate and compensate for constant sensor biases from stationary periods:

```python
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

# Repeat full pipeline with corrected data and compare results
```

## Assignment Deliverables

### Required Submission

Submit your work via **Pull Request** to the course repository.

**Work in your existing `dev` branch of your fork.** At the end, open a PR against the upstream repository. The PR will not be merged and serves as a timestamped submission for grading and feedback.

**What to submit:**

1. **Python Script** (`your_lastname_imu_tracking.py`)
   - Complete, executable code
   - Well-commented and structured
   - All steps from data import to visualization included
   - Should run without errors when executed

2. **Raw Data Files**
   - Your recorded sensor data (CSV format)
   - Place in `data/raw/` folder

3. **Documentation** (`README.md` in your submission folder)
   - Brief description (200-400 words) including:
     - What movement you performed
     - Actual measured distance (if applicable)
     - Reconstructed distance from your analysis
     - Key observations about drift and accuracy
     - Challenges encountered and how you addressed them

4. **Visualizations** (PNG format, at least 5 plots)
   - Raw sensor data (acceleration and gyroscope)
   - Filtered vs. unfiltered signals
   - Orientation over time (roll, pitch, yaw)
   - 2D trajectory (top view)
   - 3D trajectory (optional but recommended)

**Bonus points (max +3):**
- Zero-velocity update implementation
- Filter comparison analysis
- Multiple movement types recorded and analyzed

### Submission Instructions

1. Work in your fork's `dev` branch
2. Add your files to the repository:
   ```
   imu-workshop/
   ├── data/
   │   └── raw/
   │       ├── your_lastname_acceleration.csv
   │       └── your_lastname_gyroscope.csv
   ├── your_lastname_imu_tracking.py
   ├── figures/
   │   ├── 01_raw_sensor_data.png
   │   ├── 02_filtered_acceleration.png
   │   └── ...
   └── README.md
   ```
3. Commit your changes with meaningful messages
4. Create a Pull Request with title: **"IMU Workshop - Your Name"**
5. Ensure the PR description includes:
   - Brief summary of your approach
   - Any issues or questions
   - Links to key visualizations

**Deadline: December 2, 2025, 23:59**

:::warning Important
The Pull Request will **not be merged**. It serves only as documentation of your submission and allows for code review and feedback. Do not wait until the last moment - start early and ask questions if you encounter problems!
:::

## Summary

This workshop demonstrated the complete pipeline for IMU-based motion tracking:

1. ✅ Sensor data acquisition from smartphone
2. ✅ Signal filtering to reduce noise
3. ✅ Orientation estimation using Madgwick algorithm and quaternions
4. ✅ Coordinate transformation from local to global frame
5. ✅ Numerical integration to reconstruct trajectory
6. ✅ Visualization and error analysis

**Key takeaways:**
- IMU-only tracking suffers from drift due to integration error accumulation
- Sensor fusion (GPS, magnetometer, visual odometry) is essential for practical applications
- Quaternions provide a robust representation for 3D rotations
- The Madgwick algorithm effectively fuses accelerometer and gyroscope data
- Starting with stationary periods helps calibrate sensor biases

## References and Resources

### Academic References

1. **Madgwick, S. O. H.** (2010). *An efficient orientation filter for inertial and inertial/magnetic sensor arrays*. Report x-io and University of Bristol (UK), 25, 113-118.  
   [PDF available at x-io.co.uk](https://x-io.co.uk/open-source-imu-and-ahrs-algorithms/)

2. **Mahony, R., Hamel, T., & Pflimlin, J. M.** (2008). Nonlinear complementary filters on the special orthogonal group. *IEEE Transactions on Automatic Control*, 53(5), 1203-1218.

3. **Sabatini, A. M.** (2006). Quaternion-based extended Kalman filter for determining orientation by inertial and magnetic sensing. *IEEE Transactions on Biomedical Engineering*, 53(7), 1346-1356.

### Software and Tools

- [AHRS Python Library Documentation](https://ahrs.readthedocs.io/) - Comprehensive attitude and heading reference system implementations
- [Scipy Spatial Transformations](https://docs.scipy.org/doc/scipy/reference/spatial.transform.html) - Rotation representations and conversions
- [PhyPhox App](https://phyphox.org/) - Physics experiments on smartphone, excellent for sensor data collection
- [Understanding Quaternions](https://eater.net/quaternions) - Interactive visualization of quaternion rotations

:::tip Best Practice
Save your raw sensor data immediately after recording. You can reprocess and experiment with different parameters, but you cannot recreate lost data. Keep a lab notebook documenting your movements and observations.
:::
