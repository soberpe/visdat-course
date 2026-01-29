from PyQt6.QtWidgets import QApplication, QWidget

# 1. Create the application object
app = QApplication([])

# 2. Create the main window
window = QWidget()
window.setWindowTitle("My First Qt App")
window.resize(400, 300)

# 3. Show the window
window.show()

# 4. Start the event loop
app.exec()

# Terminal starten: python User_Intertface\minimal_app.py