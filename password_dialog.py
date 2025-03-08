from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QDialog
import wachtwoord_dialog_ui  
class WachtwoordDialog(QDialog,wachtwoord_dialog_ui.Ui_Dialog):
    def __init__(self, parent=None, target_page=None, caller_button=None):
        """
        Password dialog to protect specific pages.
        
        :param parent: Parent window
        :param target_page: The page index to switch to upon successful login
        :param caller_button: The button associated with the page switch
        """
        super().__init__(parent)
        self.target_page = target_page
        self.caller_button = caller_button

        try:
            self.setupUi(self)  # Inicializa la UI
            self.btn_inloggen.clicked.connect(self.controleer_wachtwoord)
        except Exception as e:
            QMessageBox.critical(self, "UI Fout", f"Error loading password dialog UI: {str(e)}")

    def controleer_wachtwoord(self):
        """Validates password and navigates to the target page if correct."""
        if self.entry_wachtwoord.text() == "intranerd":
            self.accept()  # Close dialog successfully
        else:
            QMessageBox.critical(self, "Fout", "Ongeldig wachtwoord.")
            self.entry_wachtwoord.clear()
