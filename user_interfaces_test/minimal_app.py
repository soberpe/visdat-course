from PyQt6.QtWidgets import QApplication, QWidget, QPushButton

# 1. Create the application object
app = QApplication([])

# 2. Create the main window
window = QWidget()
window.setWindowTitle("Button Example")
window.resize(400, 300)


# Create button with text and parent
button = QPushButton("Click Me", parent=window)
button.move(150, 120)  # Position manually (not recommended, but works for one widget)

# Connect signal to slot
button.clicked.connect(lambda: print("Button clicked!"))

# 3. Show the window
window.show()

# 4. Start the event loop
app.exec()