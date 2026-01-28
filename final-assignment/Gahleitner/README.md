# DiceArt Converter 
**by Michael Gahleitner - 2025**

<br>

**DiceArt Converter** is a GUI application designed to transform digital images into mosaic art masterpieces made entirely of 6-sided dice. Motivation for this Project was a recent Pinterest find and an art enthusiastic mother :D

### 🎯 Overview
The goal of this project is to provide artists and hobbyists with a tool to visualize and plan physical dice mosaics. Unlike simple pixelation tools, this application uses advanced image analysis to calculate not just the brightness (value) of a die, but also its optimal **rotation** to mimic edges and gradients in the original image. Additionally to the option to save the dice mosaic as an image, the results can also be saved as Tabble representing the Matrix of the individual dice (value and orientation) in order to facilitate a tool for those willing to physically build the mosaic.

### ✨ Key Features

#### 🖼️ Image Processing & Manipulation
* **Load & Crop:** Import images (JPG, PNG, WEBP) and use an interactive, drag-and-drop green box to select the specific area to convert.
* **Aspect Ratio Locking:** Force specific ratios (1:1, 4:3, 16:9, etc.) or use the original image dimensions.
* **Resolution Control:** Define how many dice wide and high the final output should be.
* **Image Styling:** Option to invert colors (negative image) for specific artistic effects or better contrast from the background.

#### ⚙️ Advanced Algorithm Controls
* **Three Processing Modes:** Choose between speed and detail (Simple, Gradient, or Adaptive).
* **Variable Chunk Size:** Adjust the analysis chunk size (from 4px to 64px) via a slider to fine-tune how the algorithm detects edges versus noise.

#### 👁️ Visualization Tools
* **Synchronized Dual View:** The Original image and Result view are linked. Zooming or panning in one window automatically moves the other for pixel-perfect comparison.
* **Blend Overlay Mode:** Superimpose the DiceArt result over the original image with an adjustable **Opacity Slider** to verify accuracy.
* **Grid System:** Toggle a visual grid over the image with a customizable color wheel to see exactly where dice boundaries fall.

#### 💾 Export Capabilities
* **Save Image:** Export the high-resolution dice mosaic as a PNG.
* **Save Blueprint:** Export a text-based table (matrix) indicating the value (1-6) and rotation (N, E, S, W) for every single die, essential for physical construction.

---

### 🧠 Dicing Algorithms

The core of the project lies in its three distinct algorithms for determining dice placement:

1.  **Simple (Fast):**
    * Maps pixel brightness directly to dice values (1–6).
    * **No rotation** is applied (all dice face North).
    * *Best for:* Very large mosaics where individual die rotation is less visible, or for fast previews.

2.  **Gradient (High Quality):**
    * Analyzes specific "chunks" of the image corresponding to the dice size.
    * Compares the image chunk against a database of dice rotated at 0°, 90°, 180°, and 270°.
    * Uses **Mean Squared Error (MSE)** to mathematically determine which rotation best aligns with the visual structures (edges) in that chunk.

3.  **Adaptive (Hybrid) – *Standout Feature*:**
    * A smart combination of the previous two.
    * Calculates the **Standard Deviation (Variance)** of the image chunk.
    * **Logic:** If the variance is low (smooth wall, sky, skin), it forces a standard rotation to reduce visual "noise." If variance is high (eyes, hair strands, text), it performs a computationally expensive gradient search to find the perfect rotation.
    * **Significance Check:** Even if a rotation is calculated, it is only applied if it improves the error score by at least **15%** compared to the standard orientation. This results in the cleanest possible image with sharp details.

---

### 🛠️ Technologies Used

#### Python Libraries
* **PyQt6:** Used for the entire Graphical User Interface (Windows, Layouts, Signals/Slots, Custom Widgets).
* **Pillow (PIL):** Handles all image manipulation (Loading, Grayscale conversion, Resizing, Rotation, pasting dice assets).
* **PyInstaller:** Used to package the application and its image assets into a standalone `.exe` file.

#### Special Techniques
* **Multithreading (QThread):** The heavy image processing logic runs on a separate worker thread (`DiceWorker`). This ensures the GUI remains responsive and the progress bar updates smoothly, even when calculating matrices of large dice datasets.
* **Custom Graphics Items:** `DraggableCropItem` and `SyncedGraphicsView` were built by subclassing PyQt widgets to handle complex mouse events (dragging constraints, synchronized zooming/panning between two distinct viewports).

## Examples

### Christoph Waltz

| Original | | DiceArt (100x100) |
| :---: | :---: | :---: |
| <img src="assets/waltz_original.jpg" width="200" height="200" style="object-fit: cover;"> | ➔ | <img src="assets/waltz_dice_100x100.png" width="200" height="200" style="object-fit: cover;"> |

### Toto Wolff

| Original | | DiceArt (100x100) |
| :---: | :---: | :---: |
| <img src="assets/toto_original.jpg" width="200" height="200" style="object-fit: cover;"> | ➔ | <img src="assets/toto_dice_100x100.png" width="200" height="200" style="object-fit: cover;"> |