from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QDialog

class WachtwoordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        try:
            uic.loadUi("wachtwoord_dialog.ui", self)  # Load UI file
            self.setWindowTitle("Wachtwoord vereist")
            self.btn_inloggen.clicked.connect(self.controleer_wachtwoord)
        except Exception as e:
            error_message = f"Error loading password dialog UI: {str(e)}"
            print(error_message)  # Log error for debugging
            QMessageBox.critical(self, "UI Fout", error_message)  # Show error popup

    def controleer_wachtwoord(self):
        try:
            if self.entry_wachtwoord.text() == "intranerd":
                self.accept()  # Close dialog successfully
            else:
                QMessageBox.critical(self, "Fout", "Ongeldig wachtwoord.")
                self.entry_wachtwoord.clear()
        except Exception as e:
            error_message = f"Error checking password: {str(e)}"
            print(error_message)  # Log error for debugging
            QMessageBox.critical(self, "Fout", error_message)  # Show error popup
