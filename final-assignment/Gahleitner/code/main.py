# GUI Python Application for Converting Images into Dice Art
# © 2026 - Michael Gahleitner

import sys
import os
import traceback
import math
from PIL import Image, ImageOps
from PIL.ImageQt import ImageQt

# PyQt6 components for the Graphical User Interface
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFileDialog, 
                             QSpinBox, QProgressBar, QGroupBox, QRadioButton, 
                             QMessageBox, QGraphicsView, QGraphicsScene, 
                             QSlider, QCheckBox, QGraphicsRectItem, QGraphicsItem,
                             QComboBox, QGraphicsPathItem, QButtonGroup)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QRectF, QPointF
from PyQt6.QtGui import QPixmap, QPainter, QPen, QColor, QWheelEvent, QBrush, QFont, QPainterPath

# --- RESOURCE HELPER ---
def resource_path(relative_path):
    """
    Locates external resources (images).
    Handles paths correctly for both the raw Python script and the compiled .exe.
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Development mode: use the script's directory
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

# --- WORKER THREAD ---
class DiceWorker(QThread):
    """
    Runs image processing algorithms in a background thread to keep the GUI responsive.
    """
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal(object, tuple, list) 
    error_signal = pyqtSignal(str)

    def __init__(self, input_image_path, h_dice, v_dice, dice_folder, crop_box, invert, algo_mode, chunk_size):
        super().__init__()
        self.input_image_path = input_image_path
        self.h_dice = h_dice        # Horizontal dice count
        self.v_dice = v_dice        # Vertical dice count
        self.dice_folder = dice_folder
        self.crop_box = crop_box    # (x, y, w, h) of the area to process
        self.invert = invert        # Boolean: Invert colors?
        self.algo_mode = algo_mode  # 'simple', 'gradient', or 'adaptive'
        self.chunk_size = chunk_size # Resolution for analysis (e.g., 32x32)
        self.is_running = True

    def run(self):
        """
        Main processing logic containing the three algorithms.
        """
        try:
            # Use the dynamic chunk size from the slider (replaces old hardcoded COMPARE_RES)
            c_res = self.chunk_size

            # Inner class to handle dice image variants
            class DiceVariant:
                def __init__(self, image, value, rotation, direction_char):
                    self.image = image
                    self.value = value
                    self.rotation = rotation
                    self.direction_char = direction_char
                    # Cache a resized version for fast pixel comparison
                    self.compare_data = list(image.resize((c_res, c_res)).getdata())

            # Helper: Calculate Mean Squared Error between two pixel sets
            def get_difference(pixels_a, pixels_b):
                diff = 0
                for a, b in zip(pixels_a, pixels_b):
                    d = a - b
                    diff += d * d
                return diff

            # --- 1. IMAGE LOADING & PREPARATION ---
            original_img = Image.open(self.input_image_path).convert('L')
            img_w, img_h = original_img.size
            
            # Apply cropping logic
            cx, cy, cw, ch = self.crop_box
            if cw > 0 and ch > 0:
                cropped_img = original_img.crop((cx, cy, cx + cw, cy + ch))
            else:
                cropped_img = original_img
            
            # --- MODIFIED: Invert Logic Swapped ---
            # If the checkbox 'Invert Colors' (self.invert) is NOT checked, we apply default inversion.
            # If it IS checked, we skip inversion (keeping original colors).
            if not self.invert: 
                cropped_img = ImageOps.invert(cropped_img)

            # --- 2. LOAD & PREPARE DICE ASSETS ---
            dice_variants = {}
            dice_render_size = 50 
            # Mapping degrees to cardinal directions for blueprint output
            rot_map = {0: 'N', 90: 'W', 180: 'S', 270: 'E'}

            for i in range(1, 7):
                path = os.path.join(self.dice_folder, f"{i}.png")
                if not os.path.exists(path):
                    self.error_signal.emit(f"Error: File {i}.png missing in 'dice' folder!")
                    return
                base_img = Image.open(path).resize((dice_render_size, dice_render_size)).convert('L')
                dice_variants[i] = []
                # Generate 4 rotations (0, 90, 180, 270) for each dice value
                for rot in [0, 90, 180, 270]:
                    dice_variants[i].append(DiceVariant(base_img.rotate(rot), i, rot, rot_map[rot]))

            # Create empty canvas for the result
            preview_img = Image.new('L', (self.h_dice * dice_render_size, self.v_dice * dice_render_size))
            total_dice = self.h_dice * self.v_dice
            matrix = [] 
            
            # --- 3. ALGORITHM EXECUTION ---
            
            if self.algo_mode == 'simple':
                # === MODE A: SIMPLE (Fast) ===
                # Logic: Direct resize (1 pixel = 1 dice). No rotation analysis.
                # Use case: Very large grids or when clean, non-rotated look is desired.
                small_img = cropped_img.resize((self.h_dice, self.v_dice), resample=Image.Resampling.LANCZOS)
                pixel_data = list(small_img.getdata())
                current_row = []
                
                for idx, brightness in enumerate(pixel_data):
                    if not self.is_running: break
                    
                    # Coordinate calculation
                    x = idx % self.h_dice
                    y = idx // self.h_dice
                    
                    # Map brightness (0-255) to dice value (1-6)
                    val = int(brightness / 256 * 6)
                    if val > 5: val = 5
                    target_val = 6 - val 
                    
                    current_row.append(f"{target_val}N")
                    if len(current_row) == self.h_dice:
                        matrix.append(current_row)
                        current_row = []

                    # Always use rotation 0 (Index 0)
                    dice_img = dice_variants[target_val][0].image
                    preview_img.paste(dice_img, (x * dice_render_size, y * dice_render_size))
                    
                    if idx % 500 == 0: self.progress_signal.emit(int(idx / total_dice * 100))
            
            else:
                # === MODE B: GRADIENT & MODE C: ADAPTIVE (Complex) ===
                # Logic: Analyze sub-chunks of the image to determine edge direction.
                
                # Resize source to match grid * chunk_size
                target_w = self.h_dice * self.chunk_size
                target_h = self.v_dice * self.chunk_size
                analyze_img = cropped_img.resize((target_w, target_h), resample=Image.Resampling.LANCZOS)
                
                count = 0
                for y in range(self.v_dice):
                    if not self.is_running: break
                    row_data = []
                    for x in range(self.h_dice):
                        # 1. Extract Chunk
                        box = (x * self.chunk_size, y * self.chunk_size, 
                               (x + 1) * self.chunk_size, (y + 1) * self.chunk_size)
                        chunk_data = list(analyze_img.crop(box).getdata())
                        
                        # 2. Determine Value (Brightness)
                        avg_brightness = sum(chunk_data) / len(chunk_data)
                        val = int(avg_brightness / 256 * 6)
                        if val > 5: val = 5
                        target_val = 6 - val 
                        
                        best_variant = None
                        
                        # 3. Hybrid / Adaptive Logic
                        
                        # Baseline: Calculate error for standard rotation (North/0°)
                        variant_north = dice_variants[target_val][0]
                        diff_north = get_difference(chunk_data, variant_north.compare_data)
                        
                        force_simple = False
                        
                        if self.algo_mode == 'adaptive':
                            # Variance Analysis:
                            # Calculate Standard Deviation to check for visual "noise" or edges.
                            # Low deviation = Flat/Smooth area -> Force simple rotation to reduce noise.
                            variance = sum((p - avg_brightness) ** 2 for p in chunk_data) / len(chunk_data)
                            std_dev = math.sqrt(variance)
                            
                            if std_dev < 18.0: # Threshold for flatness
                                force_simple = True
                        
                        if force_simple:
                            # Optimization: Skip search, use North
                            best_variant = variant_north
                        else:
                            # Gradient Search: Compare all 4 rotations
                            min_diff = float('inf')
                            temp_best = None
                            
                            for variant in dice_variants[target_val]:
                                diff = get_difference(chunk_data, variant.compare_data)
                                if diff < min_diff:
                                    min_diff = diff
                                    temp_best = variant
                            
                            # Significance Check (Adaptive Mode Only)
                            if self.algo_mode == 'adaptive':
                                # Only rotate if it improves the error by at least 15%
                                # compared to the standard north rotation.
                                if min_diff < (diff_north * 0.85):
                                    best_variant = temp_best
                                else:
                                    best_variant = variant_north
                            else:
                                # Gradient Mode: Strictly mathematical best fit
                                best_variant = temp_best
                        
                        # 4. Store & Paste
                        row_data.append(f"{target_val}{best_variant.direction_char}")
                        preview_img.paste(best_variant.image, (x * dice_render_size, y * dice_render_size))
                        
                        count += 1
                        if count % 100 == 0: self.progress_signal.emit(int(count / total_dice * 100))
                    
                    matrix.append(row_data)

            if self.is_running:
                self.finished_signal.emit(preview_img, (cx, cy, cw, ch), matrix)

        except Exception as e:
            traceback.print_exc()
            self.error_signal.emit(str(e))

    def stop(self):
        self.is_running = False

# --- UI COMPONENT: SELECTION BOX ---
class DraggableCropItem(QGraphicsRectItem):
    """
    Green selection box on the left image. 
    Handles resizing constraints and grid visualization.
    """
    def __init__(self, rect, h_dice, v_dice):
        super().__init__(rect)
        self.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsMovable | 
                      QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        self.setAcceptHoverEvents(True)
        self.h_dice = h_dice
        self.v_dice = v_dice
        self.show_grid = False
        self.grid_hue = 0
        self.crop_active = False
        self.setBrush(QBrush(QColor(255, 255, 255, 0)))

    def set_params(self, show_grid, hue, h, v, crop_active):
        self.show_grid = show_grid
        self.grid_hue = hue
        self.h_dice = h
        self.v_dice = v
        self.crop_active = crop_active
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, crop_active)
        self.update()

    def paint(self, painter, option, widget):
        rect = self.rect()
        # Draw green border only if cropping is active
        if self.crop_active:
            painter.setPen(QPen(QColor(0, 255, 0), 2))
            painter.drawRect(rect)
        
        # Draw grid overlay
        if self.show_grid:
            color = QColor.fromHsv(self.grid_hue, 255, 255); color.setAlpha(150)
            painter.setPen(QPen(color, 1.0))
            w = rect.width(); h = rect.height()
            if self.h_dice > 0 and self.v_dice > 0:
                step_x = w / self.h_dice; step_y = h / self.v_dice
                for i in range(1, self.h_dice):
                    x = rect.left() + i * step_x
                    painter.drawLine(QPointF(x, rect.top()), QPointF(x, rect.bottom()))
                for i in range(1, self.v_dice):
                    y = rect.top() + i * step_y
                    painter.drawLine(QPointF(rect.left(), y), QPointF(rect.right(), y))

    def itemChange(self, change, value):
        # Constrain movement within parent scene
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange and self.scene():
            if not self.crop_active: return QPointF(0,0)
            new_pos = value; rect = self.rect(); scene_rect = self.scene().sceneRect()
            new_tl_x = new_pos.x() + rect.left(); new_tl_y = new_pos.y() + rect.top()
            new_br_x = new_tl_x + rect.width(); new_br_y = new_tl_y + rect.height()
            
            if new_tl_x < scene_rect.left(): new_pos.setX(scene_rect.left() - rect.left())
            if new_tl_y < scene_rect.top(): new_pos.setY(scene_rect.top() - rect.top())
            if new_br_x > scene_rect.right(): new_pos.setX(scene_rect.right() - rect.width() - rect.left())
            if new_br_y > scene_rect.bottom(): new_pos.setY(scene_rect.bottom() - rect.height() - rect.top())
            return new_pos
        return super().itemChange(change, value)

# --- UI COMPONENT: STATIC GRID (RIGHT SIDE) ---
class StaticGridOverlay(QGraphicsRectItem):
    """
    Overlay grid for the result view. purely visual, no interaction.
    """
    def __init__(self, rect, h_dice, v_dice, hue):
        super().__init__(rect)
        self.h_dice = h_dice; self.v_dice = v_dice; self.hue = hue
        self.setBrush(QBrush(Qt.BrushStyle.NoBrush))
        self.setPen(QPen(Qt.PenStyle.NoPen))

    def paint(self, painter, option, widget):
        rect = self.rect()
        color = QColor.fromHsv(self.hue, 255, 255); color.setAlpha(150)
        painter.setPen(QPen(color, 1.0))
        w = rect.width(); h = rect.height()
        if self.h_dice > 0 and self.v_dice > 0:
            step_x = w / self.h_dice; step_y = h / self.v_dice
            for i in range(1, self.h_dice):
                x = rect.left() + i * step_x
                painter.drawLine(QPointF(x, rect.top()), QPointF(x, rect.bottom()))
            for i in range(1, self.v_dice):
                y = rect.top() + i * step_y
                painter.drawLine(QPointF(rect.left(), y), QPointF(rect.right(), y))

# --- UI COMPONENT: SYNCED VIEW ---
class SyncedGraphicsView(QGraphicsView):
    """
    A view that synchronizes Zoom and Scroll with another view instance.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self._scene = QGraphicsScene(self)
        self.setScene(self._scene)
        self.other_view = None
        self._is_syncing = False 
        
        self.horizontalScrollBar().valueChanged.connect(self.sync_h_scroll)
        self.verticalScrollBar().valueChanged.connect(self.sync_v_scroll)

    def set_image(self, pixmap, fit=True):
        self._scene.clear()
        self._scene.addPixmap(pixmap)
        rect = QRectF(pixmap.rect())
        self._scene.setSceneRect(rect)
        if fit: self.fitInView(rect, Qt.AspectRatioMode.KeepAspectRatio)

    def set_linked_view(self, view): self.other_view = view

    def sync_h_scroll(self, value):
        if self.other_view and not self._is_syncing:
            self.other_view._is_syncing = True
            self.other_view.horizontalScrollBar().setValue(value)
            self.other_view._is_syncing = False

    def sync_v_scroll(self, value):
        if self.other_view and not self._is_syncing:
            self.other_view._is_syncing = True
            self.other_view.verticalScrollBar().setValue(value)
            self.other_view._is_syncing = False

    def wheelEvent(self, event: QWheelEvent):
        if self._is_syncing: return
        zoom_in = 1.15; zoom_out = 1 / zoom_in
        factor = zoom_in if event.angleDelta().y() > 0 else zoom_out
        
        current_scale = self.transform().m11()
        if (factor > 1 and current_scale > 50.0) or (factor < 1 and current_scale < 0.01): return
        
        self.scale(factor, factor)
        
        if self.other_view:
            self.other_view._is_syncing = True
            self.other_view.setTransform(self.transform())
            self.other_view._is_syncing = False

# --- MAIN WINDOW ---
class DiceArtApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DiceArt Converter")
        self.resize(1350, 950)

        # State Variables
        self.image_path = None
        self.original_pixmap = None
        self.result_image_pil = None 
        self.result_pixmap = None    
        self.result_matrix = [] 
        self.last_crop_box = None 
        self.crop_item = None 
        self.img_w = 0; self.img_h = 0
        self.ignore_spin_change = False 
        
        # Chunk sizes available on the slider
        self.chunk_steps = [4, 8, 16, 32, 64]

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # --- LEFT PANEL ---
        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("<b>Original Image</b>"))
        self.view_left = SyncedGraphicsView()
        self.view_left.setStyleSheet("border: 1px solid #555;")
        left_layout.addWidget(self.view_left)
        
        self.show_startup_message()

        self.crop_controls_widget = QWidget()
        crop_layout = QHBoxLayout(self.crop_controls_widget)
        crop_layout.setContentsMargins(0,0,0,0)
        crop_layout.addWidget(QLabel("Crop Zoom:"))
        self.slider_crop_scale = QSlider(Qt.Orientation.Horizontal)
        self.slider_crop_scale.setRange(10, 100); self.slider_crop_scale.setValue(90)
        self.slider_crop_scale.valueChanged.connect(self.update_crop_rect)
        crop_layout.addWidget(self.slider_crop_scale)
        left_layout.addWidget(self.crop_controls_widget); self.crop_controls_widget.setVisible(False)

        self.btn_load = QPushButton("Load Image 📂")
        self.btn_load.clicked.connect(self.load_image)
        left_layout.addWidget(self.btn_load)
        main_layout.addLayout(left_layout, stretch=5)

        # --- MIDDLE PANEL (Settings) ---
        mid_layout = QVBoxLayout()
        mid_layout.setContentsMargins(15, 20, 15, 20)
        grp_settings = QGroupBox("Settings")
        grp_layout = QVBoxLayout()
        
        self.lbl_h = QLabel("Width (Dice):"); self.spin_h = QSpinBox()
        self.spin_h.setRange(1, 3000); self.spin_h.setValue(80)
        self.spin_h.valueChanged.connect(self.on_width_changed)
        
        self.lbl_v = QLabel("Height (Dice):"); self.spin_v = QSpinBox()
        self.spin_v.setRange(1, 3000); self.spin_v.setValue(80)
        self.spin_v.valueChanged.connect(self.on_height_changed)

        grp_layout.addWidget(self.lbl_h); grp_layout.addWidget(self.spin_h)
        grp_layout.addWidget(self.lbl_v); grp_layout.addWidget(self.spin_v)

        ar_layout = QHBoxLayout()
        self.chk_lock_ratio = QCheckBox("Lock Aspect Ratio")
        self.chk_lock_ratio.toggled.connect(self.toggle_lock_ratio)
        ar_layout.addWidget(self.chk_lock_ratio)
        self.combo_ratio = QComboBox()
        self.combo_ratio.addItems(["Original", "1:1", "3:2", "4:3", "4:5", "5:7", "16:9", "21:9"])
        self.combo_ratio.setEnabled(False)
        self.combo_ratio.currentIndexChanged.connect(self.apply_aspect_ratio)
        ar_layout.addWidget(self.combo_ratio)
        grp_layout.addLayout(ar_layout)
        
        grp_layout.addWidget(QLabel("Algorithm:"))
        self.combo_algo = QComboBox()
        self.combo_algo.addItem("Adaptive (Recommended)", "adaptive")
        self.combo_algo.addItem("Gradient", "gradient")
        self.combo_algo.addItem("Simple (Fast)", "simple")
        self.combo_algo.currentIndexChanged.connect(self.toggle_chunk_slider)
        grp_layout.addWidget(self.combo_algo)
        
        # Chunk Size Slider
        self.chunk_widget = QWidget()
        chunk_layout = QHBoxLayout(self.chunk_widget)
        chunk_layout.setContentsMargins(0,0,0,0)
        self.lbl_chunk = QLabel("Chunk Size: 32 px")
        chunk_layout.addWidget(self.lbl_chunk)
        self.slider_chunk = QSlider(Qt.Orientation.Horizontal)
        self.slider_chunk.setRange(0, 4) 
        self.slider_chunk.setValue(3)    
        self.slider_chunk.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider_chunk.setTickInterval(1)
        self.slider_chunk.valueChanged.connect(self.update_chunk_label)
        chunk_layout.addWidget(self.slider_chunk)
        grp_layout.addWidget(self.chunk_widget)

        self.chk_invert = QCheckBox("Invert Colors"); grp_layout.addWidget(self.chk_invert)
        self.chk_enable_crop = QCheckBox("Enable Cropping")
        self.chk_enable_crop.toggled.connect(self.toggle_crop_mode); grp_layout.addWidget(self.chk_enable_crop)
        grp_settings.setLayout(grp_layout); mid_layout.addWidget(grp_settings)

        self.btn_grid = QPushButton("Show Grid: OFF"); self.btn_grid.setCheckable(True)
        self.btn_grid.clicked.connect(self.toggle_grid); mid_layout.addWidget(self.btn_grid)

        self.lbl_grid_color = QLabel("Grid Color:"); self.lbl_grid_color.setVisible(False); mid_layout.addWidget(self.lbl_grid_color)
        self.slider_grid_color = QSlider(Qt.Orientation.Horizontal); self.slider_grid_color.setRange(0, 359); self.slider_grid_color.setVisible(False)
        self.slider_grid_color.setStyleSheet("QSlider::groove:horizontal { border: 1px solid #999; height: 10px; background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.166 rgba(255, 255, 0, 255), stop:0.333 rgba(0, 255, 0, 255), stop:0.5 rgba(0, 255, 255, 255), stop:0.666 rgba(0, 0, 255, 255), stop:0.833 rgba(255, 0, 255, 255), stop:1 rgba(255, 0, 0, 255)); margin: 2px 0; border-radius: 5px; } QSlider::handle:horizontal { background: white; border: 1px solid #5c5c5c; width: 18px; height: 18px; margin: -4px 0; border-radius: 9px; }")
        self.slider_grid_color.valueChanged.connect(self.update_crop_item_params); mid_layout.addWidget(self.slider_grid_color)
        mid_layout.addStretch()

        self.btn_start = QPushButton("CONVERT 🎲"); self.btn_start.setMinimumHeight(50)
        self.btn_start.setStyleSheet("QPushButton { background-color: #2e8b57; color: white; font-weight: bold; font-size: 14px; border-radius: 5px; } QPushButton:hover { background-color: #3cb371; } QPushButton:disabled { background-color: #888; }")
        self.btn_start.clicked.connect(self.start_processing); mid_layout.addWidget(self.btn_start)
        self.btn_reset = QPushButton("Reset Settings ↺"); self.btn_reset.clicked.connect(self.reset_app); mid_layout.addWidget(self.btn_reset)

        self.progress_bar = QProgressBar(); self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter); mid_layout.addWidget(self.progress_bar)
        self.lbl_status = QLabel(""); self.lbl_status.setAlignment(Qt.AlignmentFlag.AlignCenter); mid_layout.addWidget(self.lbl_status)
        mid_layout.addStretch(); main_layout.addLayout(mid_layout, stretch=2)

        # 3. RIGHT PANEL (Result & Export)
        right_layout = QVBoxLayout()
        right_header = QHBoxLayout()
        right_header.addWidget(QLabel("<b>Result (Synced)</b>"))
        
        self.radio_show_orig = QRadioButton("Original")
        self.radio_show_res = QRadioButton("DiceArt")
        self.radio_show_blend = QRadioButton("Blend Overlay")
        
        self.bg_view = QButtonGroup()
        self.bg_view.addButton(self.radio_show_orig)
        self.bg_view.addButton(self.radio_show_res)
        self.bg_view.addButton(self.radio_show_blend)
        self.radio_show_res.setChecked(True)
        self.bg_view.buttonToggled.connect(self.switch_right_view)
        
        right_header.addStretch()
        right_header.addWidget(self.radio_show_orig)
        right_header.addWidget(self.radio_show_res)
        right_header.addWidget(self.radio_show_blend)
        right_layout.addLayout(right_header)
        
        self.blend_ctrl_layout = QHBoxLayout()
        self.blend_ctrl_layout.addWidget(QLabel("Opacity:"))
        self.slider_blend = QSlider(Qt.Orientation.Horizontal)
        self.slider_blend.setRange(0, 100); self.slider_blend.setValue(50)
        self.slider_blend.valueChanged.connect(self.switch_right_view)
        self.blend_ctrl_layout.addWidget(self.slider_blend)
        self.blend_container = QWidget()
        self.blend_container.setLayout(self.blend_ctrl_layout)
        self.blend_container.setVisible(False)
        right_layout.addWidget(self.blend_container)
        
        self.view_right = SyncedGraphicsView()
        self.view_right.setStyleSheet("border: 1px solid #555;")
        right_layout.addWidget(self.view_right)
        
        save_layout = QHBoxLayout()
        self.btn_save_img = QPushButton("Save Image as... 💾")
        self.btn_save_img.clicked.connect(self.save_result)
        self.btn_save_img.setEnabled(False)
        self.btn_save_img.setMinimumHeight(40)
        
        self.btn_save_bp = QPushButton("Save Blueprint... 📝")
        self.btn_save_bp.clicked.connect(self.save_blueprint)
        self.btn_save_bp.setEnabled(False)
        self.btn_save_bp.setMinimumHeight(40)

        save_layout.addWidget(self.btn_save_img, stretch=3)
        save_layout.addWidget(self.btn_save_bp, stretch=1)
        right_layout.addLayout(save_layout)
        main_layout.addLayout(right_layout, stretch=5)

        self.view_left.set_linked_view(self.view_right)
        self.view_right.set_linked_view(self.view_left)

    # --- LOGIC METHODS ---
    def toggle_chunk_slider(self):
        mode = self.combo_algo.currentData()
        self.chunk_widget.setVisible(mode != 'simple')

    def update_chunk_label(self):
        idx = self.slider_chunk.value()
        val = self.chunk_steps[idx]
        self.lbl_chunk.setText(f"Chunk Size: {val} px")

    def show_startup_message(self):
        scene = self.view_left.scene()
        scene.clear()
        text_str = "Load Picture from File"
        text_item = scene.addText(text_str)
        font = QFont("Arial", 20, QFont.Weight.Bold)
        text_item.setFont(font)
        text_item.setDefaultTextColor(QColor(150, 150, 150))
        
        # White Vector Arrow
        arrow_path = QPainterPath()
        arrow_path.moveTo(-15, 0); arrow_path.lineTo(15, 0)
        arrow_path.lineTo(15, 40); arrow_path.lineTo(30, 40)
        arrow_path.lineTo(0, 70);  arrow_path.lineTo(-30, 40)
        arrow_path.lineTo(-15, 40); arrow_path.closeSubpath()
        arrow_item = QGraphicsPathItem(arrow_path)
        arrow_item.setBrush(QBrush(QColor(255, 255, 255)))
        arrow_item.setPen(QPen(QColor(200, 200, 200), 1)) 
        
        scene.addItem(arrow_item)
        scene.setSceneRect(0, 0, 400, 400)
        tr = text_item.boundingRect()
        text_item.setPos((400 - tr.width())/2, 100)
        arrow_item.setPos(200, 160)

    def load_image(self):
        # Using Native Windows File Dialog
        fname, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.jpg *.png *.jpeg *.webp)")
        if fname:
            self.crop_item = None 
            self.view_left.scene().clear(); self.view_right.scene().clear()
            self.result_image_pil = None; self.result_pixmap = None; self.last_crop_box = None
            self.result_matrix = []
            
            self.image_path = fname
            self.original_pixmap = QPixmap(fname)
            self.img_w = self.original_pixmap.width(); self.img_h = self.original_pixmap.height()

            self.progress_bar.setValue(0); self.progress_bar.setStyleSheet("")
            self.lbl_status.setText("")
            self.btn_save_img.setEnabled(False); self.btn_save_img.setStyleSheet("")
            self.btn_save_bp.setEnabled(False); self.btn_save_bp.setStyleSheet("")
            
            self.radio_show_orig.setChecked(True)
            self.view_left.set_image(self.original_pixmap, fit=True)
            self.view_right.scene().setSceneRect(0, 0, self.img_w, self.img_h)
            self.view_right.setTransform(self.view_left.transform())
            
            self.initialize_crop_item()
            if self.chk_lock_ratio.isChecked(): self.apply_aspect_ratio()

    def initialize_crop_item(self):
        if not self.original_pixmap: return
        scene = self.view_left.scene()
        rect = QRectF(0, 0, self.img_w, self.img_h)
        self.crop_item = DraggableCropItem(rect, self.spin_h.value(), self.spin_v.value())
        scene.addItem(self.crop_item)
        self.update_crop_item_params()
        self.update_crop_rect()

    def toggle_lock_ratio(self):
        is_locked = self.chk_lock_ratio.isChecked()
        self.combo_ratio.setEnabled(is_locked)
        self.spin_v.setReadOnly(is_locked)
        if is_locked: 
            self.chk_enable_crop.setChecked(True)
            self.apply_aspect_ratio()

    def apply_aspect_ratio(self):
        if not self.chk_lock_ratio.isChecked() or self.ignore_spin_change: return
        w = self.spin_h.value()
        ratio_str = self.combo_ratio.currentText()
        numerator = 1; denominator = 1
        if ratio_str == "Original":
            if self.img_w > 0: numerator = self.img_w; denominator = self.img_h
            else: return 
        else:
            parts = ratio_str.split(':')
            if len(parts) == 2: numerator = int(parts[0]); denominator = int(parts[1])

        if ratio_str != "Original":
            steps = w / numerator; nearest_step = round(steps)
            if nearest_step < 1: nearest_step = 1
            new_w = nearest_step * numerator; new_h = int(nearest_step * denominator)
        else:
            ratio = numerator / denominator; new_w = w
            new_h = int(w / ratio)
            if new_h < 1: new_h = 1

        self.ignore_spin_change = True
        self.spin_h.setValue(new_w); self.spin_v.setValue(new_h)
        self.ignore_spin_change = False
        self.update_crop_rect()

    def on_width_changed(self):
        if self.chk_lock_ratio.isChecked(): self.apply_aspect_ratio()
        else: self.update_crop_rect()

    def on_height_changed(self):
        if not self.chk_lock_ratio.isChecked(): self.update_crop_rect()

    def reset_app(self):
        self.ignore_spin_change = True
        self.spin_h.setValue(80); self.spin_v.setValue(80)
        self.chk_invert.setChecked(False); self.chk_enable_crop.setChecked(False)
        self.chk_lock_ratio.setChecked(False); self.toggle_lock_ratio()
        self.combo_ratio.setCurrentIndex(0)
        self.btn_grid.setChecked(False); self.toggle_grid()
        self.slider_crop_scale.setValue(90); self.slider_grid_color.setValue(0)
        self.combo_algo.setCurrentIndex(0)
        self.slider_chunk.setValue(3)
        self.ignore_spin_change = False
        self.btn_save_img.setEnabled(False); self.btn_save_img.setStyleSheet("")
        self.btn_save_bp.setEnabled(False); self.btn_save_bp.setStyleSheet("")
        if self.image_path: self.initialize_crop_item()
        else: self.show_startup_message()
        self.lbl_status.setText("Settings Reset")

    def toggle_crop_mode(self):
        is_crop = self.chk_enable_crop.isChecked()
        self.crop_controls_widget.setVisible(is_crop)
        self.update_crop_rect()

    def toggle_grid(self):
        is_on = self.btn_grid.isChecked()
        self.btn_grid.setText(f"Show Grid: {'ON' if is_on else 'OFF'}")
        self.lbl_grid_color.setVisible(is_on); self.slider_grid_color.setVisible(is_on)
        self.update_crop_item_params()
        self.switch_right_view()

    def update_crop_item_params(self):
        if self.crop_item:
            self.crop_item.set_params(self.btn_grid.isChecked(), self.slider_grid_color.value(), self.spin_h.value(), self.spin_v.value(), self.chk_enable_crop.isChecked())
            self.switch_right_view()

    def update_crop_rect(self):
        if not self.crop_item or not self.original_pixmap: return
        self.update_crop_item_params()
        if not self.chk_enable_crop.isChecked():
            self.crop_item.setRect(0, 0, self.img_w, self.img_h); self.crop_item.setPos(0, 0)
            return
        dice_h = self.spin_h.value(); dice_v = self.spin_v.value()
        if dice_v == 0: dice_v = 1 
        ratio = dice_h / dice_v
        scale_pct = self.slider_crop_scale.value() / 100.0
        target_w = self.img_w * scale_pct; target_h = target_w / ratio
        if target_h > self.img_h: target_h = self.img_h * scale_pct; target_w = target_h * ratio
        self.crop_item.setRect(0, 0, target_w, target_h)
        if self.crop_item.pos() == QPointF(0,0):
             cx = (self.img_w - target_w) / 2; cy = (self.img_h - target_h) / 2
             self.crop_item.setPos(cx, cy)

    def start_processing(self):
        if not self.image_path or not self.crop_item:
            QMessageBox.warning(self, "Warning", "Please load an image first!")
            return
        
        dice_folder = resource_path("dice")
        
        if self.chk_enable_crop.isChecked():
            pos = self.crop_item.pos(); rect = self.crop_item.rect()
            crop_box = (int(pos.x()), int(pos.y()), int(rect.width()), int(rect.height()))
        else:
            crop_box = (0, 0, self.img_w, self.img_h)

        algo_mode = self.combo_algo.currentData()
        chunk_idx = self.slider_chunk.value()
        chunk_size = self.chunk_steps[chunk_idx]

        self.btn_start.setEnabled(False); self.progress_bar.setValue(0); self.progress_bar.setStyleSheet("")
        self.lbl_status.setText(f"Calculating ({algo_mode})...")
        
        self.btn_save_img.setEnabled(False); self.btn_save_img.setStyleSheet("")
        self.btn_save_bp.setEnabled(False); self.btn_save_bp.setStyleSheet("")
        
        self.worker = DiceWorker(self.image_path, self.spin_h.value(), self.spin_v.value(), dice_folder, crop_box, self.chk_invert.isChecked(), algo_mode, chunk_size)
        self.worker.progress_signal.connect(self.progress_bar.setValue)
        self.worker.error_signal.connect(self.on_error)
        self.worker.finished_signal.connect(self.on_finished)
        self.worker.start()

    def on_error(self, msg):
        QMessageBox.critical(self, "Error", msg); self.btn_start.setEnabled(True); self.lbl_status.setText("Error!")

    def on_finished(self, result_img_pil, crop_box, matrix):
        self.result_image_pil = result_img_pil
        self.result_pixmap = QPixmap.fromImage(ImageQt(result_img_pil))
        self.last_crop_box = crop_box 
        self.result_matrix = matrix
        
        self.radio_show_res.setChecked(True); self.switch_right_view()
        self.btn_start.setEnabled(True)
        self.btn_save_img.setEnabled(True)
        self.btn_save_img.setStyleSheet("background-color: #2e8b57; color: white; font-weight: bold;")
        self.btn_save_bp.setEnabled(True)
        self.btn_save_bp.setStyleSheet("background-color: #5f9ea0; color: white; font-weight: bold;") 
        self.progress_bar.setValue(100); self.progress_bar.setStyleSheet("QProgressBar::chunk { background-color: #4CAF50; width: 10px; }")
        self.lbl_status.setText("Done!")

    def switch_right_view(self):
        scene = self.view_right.scene()
        scene.clear()
        
        self.blend_container.setVisible(self.radio_show_blend.isChecked())
        if self.img_w > 0: scene.setSceneRect(0, 0, self.img_w, self.img_h)

        if self.radio_show_orig.isChecked() or self.radio_show_blend.isChecked():
            if self.original_pixmap: scene.addPixmap(self.original_pixmap)

        res_item = None
        if (self.radio_show_res.isChecked() or self.radio_show_blend.isChecked()) and self.result_pixmap:
             res_item = scene.addPixmap(self.result_pixmap)
             if self.last_crop_box:
                cx, cy, cw, ch = self.last_crop_box
                res_item.setPos(cx, cy)
                if self.result_pixmap.width() > 0:
                    scale_factor = cw / self.result_pixmap.width()
                    res_item.setScale(scale_factor)

        if self.radio_show_blend.isChecked() and res_item:
            opacity = self.slider_blend.value() / 100.0
            res_item.setOpacity(opacity)

        if self.btn_grid.isChecked():
            box_x, box_y, box_w, box_h = 0, 0, self.img_w, self.img_h
            if self.result_pixmap and self.last_crop_box:
                 box_x, box_y, box_w, box_h = self.last_crop_box
            elif self.crop_item and self.chk_enable_crop.isChecked():
                 pos = self.crop_item.pos()
                 rect = self.crop_item.rect()
                 box_x, box_y, box_w, box_h = pos.x(), pos.y(), rect.width(), rect.height()
            
            grid = StaticGridOverlay(QRectF(box_x, box_y, box_w, box_h), self.spin_h.value(), self.spin_v.value(), self.slider_grid_color.value())
            scene.addItem(grid)

    def save_result(self):
        if not self.result_image_pil: return
        initial_name = f"dice_art_{self.spin_h.value()}x{self.spin_v.value()}.png"
        path, _ = QFileDialog.getSaveFileName(self, "Save Image As", initial_name, "PNG Images (*.png)")
        if path:
            self.result_image_pil.save(path)
            QMessageBox.information(self, "Saved", f"Image saved successfully!")

    def save_blueprint(self):
        if not self.result_matrix: return
        initial_name = f"blueprint_{self.spin_h.value()}x{self.spin_v.value()}.txt"
        path, _ = QFileDialog.getSaveFileName(self, "Save Blueprint As", initial_name, "Text Files (*.txt)")
        if path:
            try:
                with open(path, "w") as f:
                    f.write(f"Dice Art Blueprint ({self.spin_h.value()}x{self.spin_v.value()})\n")
                    f.write("="*30 + "\n\n")
                    for row in self.result_matrix:
                        line = "\t".join(row)
                        f.write(line + "\n")
                QMessageBox.information(self, "Saved", f"Blueprint saved successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save blueprint:\n{e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DiceArtApp()
    window.show()
    sys.exit(app.exec())