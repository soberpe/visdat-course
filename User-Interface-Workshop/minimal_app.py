#Minimal Application Structure
# from PyQt6.QtWidgets import QApplication, QWidget

# # 1. Create the application object
# app = QApplication([])

# # 2. Create the main window
# window = QWidget()
# window.setWindowTitle("My First Qt App")
# window.resize(400, 300)

# # 3. Show the window
# window.show()

# # 4. Start the event loop
# app.exec()






# Adding a Single Widget

# from PyQt6.QtWidgets import QApplication, QWidget, QPushButton

# app = QApplication([])
# window = QWidget()
# window.setWindowTitle("Button Example")
# window.resize(400, 300)

# # Create button with text and parent
# button = QPushButton("Click Me", parent=window)
# button.move(150, 120)  # Position manually (not recommended, but works for one widget)

# # Connect signal to slot
# button.clicked.connect(lambda: print("Button clicked!"))

# window.show()
# app.exec()






# # #Multiple Widgets with Layouts
# from PyQt6.QtWidgets import (
#     QApplication, QWidget, QVBoxLayout,
#     QPushButton, QLabel, QLineEdit
# )

# app = QApplication([])
# window = QWidget()
# window.setWindowTitle("Layout Example")

# # Create layout
# layout = QVBoxLayout()

# # Create widgets
# label = QLabel("Enter your name:")
# text_input = QLineEdit()
# button = QPushButton("Greet")
# result_label = QLabel("")

# # Add widgets to layout
# layout.addWidget(label)
# layout.addWidget(text_input)
# layout.addWidget(button)
# layout.addWidget(result_label)

# # Connect button to action
# def on_button_clicked():
#     name = text_input.text()
#     result_label.setText(f"Hello, {name}!")

# button.clicked.connect(on_button_clicked)

# # Apply layout to window
# window.setLayout(layout)

# window.show()
# app.exec()






# #Using QMainWindow for Complex Applications
# from PyQt6.QtWidgets import (
#     QApplication, QMainWindow, QWidget,
#     QVBoxLayout, QPushButton, QLabel
# )
# from PyQt6.QtGui import QAction

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()  # Initialize the QMainWindow base class
#         self.setWindowTitle("QMainWindow Example")
#         self.resize(600, 400)
        
#         # QMainWindow uses a central widget for its main content area
#         central_widget = QWidget()
#         self.setCentralWidget(central_widget)
        
#         # Create layout for central widget
#         layout = QVBoxLayout()
#         central_widget.setLayout(layout)
        
#         # Add content
#         self.label = QLabel("Status: Ready")
#         layout.addWidget(self.label)
        
#         button = QPushButton("Do Something")
#         button.clicked.connect(self.on_button_clicked)
#         layout.addWidget(button)
        
#         # Create menu bar
#         menu = self.menuBar()
#         file_menu = menu.addMenu("&File")
        
#         # Add menu actions
#         open_action = QAction("&Open", self)
#         open_action.triggered.connect(self.open_file)
#         file_menu.addAction(open_action)
        
#         exit_action = QAction("E&xit", self)
#         exit_action.triggered.connect(self.close)
#         file_menu.addAction(exit_action)
        
#         # Create status bar
#         self.statusBar().showMessage("Application started")
    
#     def on_button_clicked(self):
#         self.label.setText("Status: Button clicked")
#         self.statusBar().showMessage("Action performed", 3000)  # 3 second timeout
    
#     def open_file(self):
#         self.label.setText("Status: Open file dialog (not implemented)")

# app = QApplication([])
# window = MainWindow()
# window.show()
# app.exec()







#File Dialogs and User Input
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QPushButton, QLabel, QFileDialog
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Dialog Example")
        self.resize(500, 300)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        self.label = QLabel("No file selected")
        layout.addWidget(self.label)
        
        open_button = QPushButton("Open File")
        open_button.clicked.connect(self.open_file)
        layout.addWidget(open_button)
        
        save_button = QPushButton("Save File")
        save_button.clicked.connect(self.save_file)
        layout.addWidget(save_button)
    
    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select File",
            "",  # Starting directory (empty = last used)
            "Data Files (*.csv *.h5);;All Files (*.*)"
        )
        
        if filename:  # User might cancel
            self.label.setText(f"Selected: {filename}")
            # Here you would load the file
    
    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save File",
            "output.csv",
            "CSV Files (*.csv);;All Files (*.*)"
        )
        
        if filename:
            self.label.setText(f"Would save to: {filename}")
            # Here you would save data

app = QApplication([])
window = MainWindow()
window.show()
app.exec()