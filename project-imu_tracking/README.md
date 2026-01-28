##  IMU Trajectory Analysis

### **1. 2D Rectangular Movement on a Table**

* **Movement Performed:** The phone was moved in a closed **rectangular path** on a table, starting from the bottom-left corner and returning to the same point (left-bottom $\rightarrow$ top-left $\rightarrow$ top-right $\rightarrow$ bottom-right $\rightarrow$ bottom-left). This movement was chosen in order to evaluate **2D horizontal plane accuracy** and the **closed-loop drift** characteristic.
* **Actual Measured Distance (Reference):**
    * Length ($L$): **730 mm**
    * Width ($W$): **350 mm**
    * Net Displacement: **0 mm** (Closed Loop)
* **Reconstructed Distance (Simulated Analysis):**
    * Reconstructed Length: **600 mm**
    * Reconstructed Width: **400 mm**

* **Key Observations about Drift and Accuracy:** As expected with uncorrected IMU data, significant **cumulative drift** occurred. With the progressive **time integration** of the **noise- and bias-afflicted acceleration signals**, this drift accumulated rapidly. The reconstructed path slightly **overshot** the actual dimensions, indicating a small positive bias in the acceleration integration. This drift is the primary error metric for closed-loop movements. The **last segment**, which should ideally close the curve, resulted in a particularly immense **position drift** , severely distorting the supposedly closed trajectory.

* **Challenges Encountered and How Addressed:**
    * **Challenge:** The high cumulative error after the four segments (turns) due to error propagation and uncompensated sensor bias.
    * **Addressing:** Techniques employed included performing **fast (high and steady accelerations) movements** to improve the signal-to-noise ratio, minimizing **measurement time** to limit integration duration, using **Zero-Velocity Update (ZUPT)** methods to correct velocity during static moments, and applying **different digital filters** (e.g., Low-Pass) to reduce high-frequency noise and maintain smooth orientation.

---

### **2. Lifting Phone from Floor to Kitchen Island and Back**

* **Movement Performed:** The phone was lifted from the floor, moved horizontally over a kitchen island, and then placed back on the floor. This movement was chosen in order to evaluate trajectory accuracy when transitioning movement directions in z.
* **Actual Measured Distance (Reference):**
    * Vertical Height ($H$): **940 mm**
    * Horizontal Width ($B$): **1050 mm**
   
* **Reconstructed Distance (Simulated Analysis):**
    * Reconstructed vertical Height: **900 mm** 
    * Reconstructed horizontal Displacement: **600 mm** (Significant sideways drift in both x and y during lowering)

* **Key Observations about Drift and Accuracy:** The initial two linear movements (lifting and horizontal travel) were reconstructed with reasonable accuracy, but the overall horizontal distance showed a significant mismatch compared to the reference. However, the most severe errors manifesting as a major drift in both the $x$ and $y$ directions occurred specifically during the phase of deceleration onto the kitchen countertop and the subsequent transition to lowering the phone down to the ground again.

* **Challenges Encountered and How Addressed:**
    * **Challenge:** Large **sideways drift** during the transition between vertical and horizontal movement phases, specifically when changing direction (deceleration/acceleration in the negative z-direction).
    * **Addressing:** Efforts included performing **fast movements** to dominate the signal over sensor noise, minimizing **measurement time**, utilizing **Zero-Velocity Update (ZUPT)** to anchor the position at the floor and countertop, and applying **different digital filters** (e.g., Low-Pass filters) to improve the isolation of pure motion acceleration from gravity and noise.

### **3. Circular Movement on a Rotating Chair**

The phone was held upright and subjected to a steady $\text{360}^\circ$ rotation by turning a dining chair. The radii of this rotational movement was approximately 150mm.

Futher analysis was not performed on this movement.

---

### **4. Sequential Flips in Different Directions**

The phone was quickly and sequentially flipped in the following  succession: $\text{Right (Roll)} \rightarrow \text{Up (Pitch)} \rightarrow \text{Right (Roll)} \rightarrow \text{Down (Pitch)}$.

Futher analysis was not performed on this movement.