import json
import os
from PyQt5.QtWidgets import QMessageBox, QDialog
import wachtwoord_dialog_ui  

class WachtwoordDialog(QDialog, wachtwoord_dialog_ui.Ui_Dialog):
    def __init__(self, parent=None):
        """Initialize the password dialog and load passwords from JSON."""
        super().__init__(parent)
        self.passwords = self.load_passwords()

        try:
            self.setupUi(self)
            self.btn_inloggen.clicked.connect(self.check_password)
        except Exception as e:
            QMessageBox.critical(self, "UI Error", f"Error loading password dialog UI: {str(e)}")

    def load_passwords(self):
        """Load the passwords from paths_config.json."""
        config_path = "paths_config.json"
        default_passwords = {"password_wincc": "", "password_education": ""}

        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    return {
                        "password_wincc": data.get("password_wincc", ""),
                        "password_education": data.get("password_education", "")
                    }
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load passwords: {str(e)}")
                return default_passwords
        else:
            QMessageBox.warning(self, "Warning", "Configuration file not found.")
            return default_passwords

    def check_password(self):
        """Validate the entered password and return which type was used."""
        entered_password = self.entry_wachtwoord.text().strip()

        if entered_password == self.passwords["password_wincc"]:
            self.accept()  # Close dialog successfully
            self.result = "wincc"
        elif entered_password == self.passwords["password_education"]:
            self.accept()  # Close dialog successfully
            self.result = "education"
        else:
            QMessageBox.critical(self, "Error", "Invalid password.")
            self.entry_wachtwoord.clear()
            self.result = None  # Reset result if incorrect
