from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QCheckBox, QLineEdit, QPushButton, QFileDialog
)
import pandas as pd


class ExportCSVDialog(QDialog):
    def __init__(self, available_signals, parent=None):
        super().__init__(parent)
        self.setWindowTitle("CSV Export")
        self.available_signals = available_signals
        self.rows = {}

        layout = QVBoxLayout(self)

        for key in available_signals.keys():
            row = QHBoxLayout()

            checkbox = QCheckBox(key)
            name_edit = QLineEdit(key)

            row.addWidget(checkbox)
            row.addWidget(QLabel("Spaltenname:"))
            row.addWidget(name_edit)

            layout.addLayout(row)

            self.rows[key] = (checkbox, name_edit)

        btn_export = QPushButton("CSV exportieren")
        btn_export.clicked.connect(self.export_csv)
        layout.addWidget(btn_export)

    def export_csv(self):
        data = {}

        for key, (checkbox, name_edit) in self.rows.items():
            if checkbox.isChecked():
                col_name = name_edit.text()
                data[col_name] = self.available_signals[key]

        if not data:
            return

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "CSV speichern",            #Bezeichnung vom CSV-Speicherfenster
            "export.csv",               #Dateiname CSV
            "CSV File (*.csv)"          #Dateityp
        )

        if not filename:
            return

        df = pd.DataFrame(data)
        df.to_csv(filename, sep="\t", decimal=",",index=False)
        
        self.accept()
