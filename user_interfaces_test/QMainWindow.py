from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QPushButton, QLabel
)
from PyQt6.QtGui import QAction

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()  # Initialize the QMainWindow base class
        self.setWindowTitle("QMainWindow Example")
        self.resize(600, 400)
        
        # QMainWindow uses a central widget for its main content area
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create layout for central widget
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Add content
        self.label = QLabel("Status: Ready")
        layout.addWidget(self.label)
        
        button = QPushButton("Do Something")
        button.clicked.connect(self.on_button_clicked)
        layout.addWidget(button)
        
        # Create menu bar
        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        
        # Add menu actions
        open_action = QAction("&Open", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        exit_action = QAction("E&xit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Create status bar
        self.statusBar().showMessage("Application started")
    
    def on_button_clicked(self):
        self.label.setText("Status: Button clicked")
        self.statusBar().showMessage("Action performed", 3000)  # 3 second timeout
    
    def open_file(self):
        self.label.setText("Status: Open file dialog (not implemented)")

app = QApplication([])
window = MainWindow()
window.show()
app.exec()