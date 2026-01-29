from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QPushButton, QLabel, QLineEdit
)

app = QApplication([])
window = QWidget()
window.setWindowTitle("Layout Example")

# Create layout
layout = QVBoxLayout()

# Create widgets
label = QLabel("Enter your name:")
text_input = QLineEdit()
button = QPushButton("Greet")
result_label = QLabel("")

# Add widgets to layout
layout.addWidget(label)
layout.addWidget(text_input)
layout.addWidget(button)
layout.addWidget(result_label)

# Connect button to action
def on_button_clicked():
    name = text_input.text()
    result_label.setText(f"Hello, {name}!")

button.clicked.connect(on_button_clicked)

# Apply layout to window
window.setLayout(layout)

window.show()
app.exec()