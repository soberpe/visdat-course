"""
Startskript für Statistische Versuchsplanung
Stellt sicher, dass alle benötigten Pakete installiert sind
Erstellt von: Lukas Musser
Version: 1.0
Datum: 28.01.2026
"""

import subprocess
import sys

# Liste der benötigten Pakete
REQUIRED_PACKAGES = [
    "PyQt6",
    "matplotlib",
    "numpy"
]

def install_missing_packages():
    """Installiert alle fehlenden Pakete automatisch"""
    for package in REQUIRED_PACKAGES:
        try:
            __import__(package.lower() if package != "PyQt6" else "PyQt6")
        except ImportError:
            print(f"📦 Paket '{package}' wird installiert …")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

if __name__ == "__main__":
    print("🔍 Überprüfe Python-Pakete …")
    install_missing_packages()
    print("✅ Alle Pakete sind installiert!\n Anwendung kann jetzt gestartet werden.")
