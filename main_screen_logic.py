import sys
import os
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QMessageBox,
    QMainWindow,
    QStackedWidget,
    QComboBox,
    QLineEdit,
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    
)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QPushButton, QMessageBox, QMainWindow
import os
import sys
import os

from PyQt5 import QtWidgets, uic
import traceback
from password_dialog import WachtwoordDialog
from ui_main import Ui_MainWindow  # Adjust based on your generated class name

class MasterScreen(QtWidgets.QMainWindow):
    def __init__(self,user_data=None):
        super().__init__()
        try:
            uic.loadUi("main.ui", self)  # Load UI file dynamically
            from modules.ui_functions import UIFunctions
            self.ui=self
            self.active_button = self.btnZoekAfse  # Set default active button
            self.active_button.setStyleSheet("text-decoration: underline; font-weight: bold;")
            self.set_buttons_cursor()
            self.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))
            UIFunctions.uiDefinitions(self)

            self.btnZoek.setStyleSheet(UIFunctions.selectMenu(self.btnZoek.styleSheet()))

            self.stacked_widget = self.findChild(QStackedWidget, "stackedWidget")  # Match the object name in Qt Designer
            self.init_pages()

            self.menu_buttons = [
                self.btnZoek,  
                self.btnBereken,
                self.btnDocumenten,
                self.btnTestList,
                self.btnInstellingen,
            ]

            # Assign menu button clicks
            self.btnZoek.clicked.connect(self.show_zoek_menu)
            self.btnBereken.clicked.connect(self.show_berek_menu)
            self.btnDocumenten.clicked.connect(self.show_documenten_menu)
            
            self.btnTestList.clicked.connect(self.show_test_menu)
            # Modify btnInstellingen click to require password
            # Assign password-protected buttons with their respective stacked widgets
            self.btnInstellingen.clicked.connect(self.check_password_and_open_settings)
            self.btnELearning.clicked.connect(self.check_password_and_open_elearning)

            
            self.btnZoekAfse.clicked.connect(lambda: self.set_page(0, self.btnZoekAfse))
            self.btnZoekMehi.clicked.connect(lambda: self.set_page(1, self.btnZoekMehi))
            self.btnZoekSUO.clicked.connect(lambda: self.set_page(2, self.btnZoekSUO))

            self.btnVriBerek.clicked.connect(lambda: self.set_page(3, self.btnVriBerek))
            self.btnDebBerek.clicked.connect(lambda: self.set_page(4, self.btnDebBerek))
            self.btnVerBerek.clicked.connect(lambda: self.set_page(5, self.btnVerBerek))

            self.btnSijabConen.clicked.connect(lambda: self.set_page(6, self.btnSijabConen))
            self.btnInstelli.clicked.connect(lambda: self.set_page(7, self.btnInstelli))
            self.btnOpleiding.clicked.connect(lambda: self.set_page(8, self.btnOpleiding))

            self.btnWincc.clicked.connect(lambda: self.set_page(9, self.btnWincc))
            self.btnUragen.clicked.connect(lambda: self.set_page(10, self.btnUragen))

            self.btnPaths.clicked.connect(lambda: self.set_page(12, self.btnPaths))
            self.btnLoggings.clicked.connect(lambda: self.set_page(13, self.btnLoggings))
            self.btnExtra.clicked.connect(lambda: self.set_page(14, self.btnExtra))

            
        except Exception as e:
            error_message = f"Error loading UI: {str(e)}\n\nTraceback:\n{traceback.format_exc()}"
            print(error_message)  # Print to console for debugging
            self.show_message_box("Critical Error", error_message)

    
    def check_password_and_open_settings(self):
        """Shows password dialog and changes the page in stackedWidget if successful."""
        try:
            wachtwoord_dialoog = WachtwoordDialog(self)
            if wachtwoord_dialoog.exec():  # If password is correct
                self.handleMenuClick(self.btnInstellingen, 4)  # Highlight the button
                self.set_page(12, self.btnPaths)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def check_password_and_open_elearning(self):
        """Shows password dialog and changes the page in stackedWidget_2 if successful."""
        try:
            wachtwoord_dialoog = WachtwoordDialog(self)
            if wachtwoord_dialoog.exec():  # If password is correct
                self.set_page(11, self.btnElearning)        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    # Assign password-protected buttons


    def set_page(self, idx, clicked_button):
        """Set the current page and update button styles."""
        self.stackedWidget_2.setCurrentIndex(idx)

        # Reset the previous button's style
        if self.active_button:
            self.active_button.setStyleSheet("")

        # Set underline for the active button
        clicked_button.setStyleSheet("text-decoration: underline; font-weight: bold;")
        self.active_button = clicked_button  # Update active button reference
    def show_message_box(self, title, message):
        """Displays a QMessageBox for general errors."""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()
    
    def init_pages(self):
        """Initialize backend logic for each page."""
        # Initialize ConfigSystem logic
        self.stackedWidget.setCurrentIndex(0)


    def show_zoek_menu(self):
        self.handleMenuClick(self.btnZoek, 0)
        self.set_page(0, self.btnZoekAfse)

    def show_berek_menu(self):
        self.handleMenuClick(self.btnBereken,1)
        self.set_page(3, self.btnVriBerek)
    def show_documenten_menu(self):
        self.handleMenuClick(self.btnDocumenten, 2)
        self.set_page(6, self.btnSijabConen)

    def show_test_menu(self):

        self.handleMenuClick(self.btnWincc,3)
        self.set_page(9, self.btnWincc)

    def show_offset_leech_menu(self):
        """Show the Offset Leech page."""
        # self.current_page = self.offset_leech
        self.handleMenuClick(self.btnInstellingen, 5)
    def show_multi_tool_menu(self):
        """Show the Multi-Tool page."""
        self.handleMenuClick(self.btnReport, 6)    
    def handleMenuClick(self, button, page_index):
        """
        Handles menu button clicks to update styles and switch pages.
        """
        from modules.ui_functions import UIFunctions

        # Deselect all buttons
        for btn in self.menu_buttons:
            btn.setStyleSheet(UIFunctions.deselectMenu(btn.styleSheet()))

        # Select the clicked button
        button.setStyleSheet(UIFunctions.selectMenu(button.styleSheet()))

        # Switch to the selected page
        self.stackedWidget.setCurrentIndex(page_index)


    def set_buttons_cursor(self):
        """Set the pointer cursor for all buttons in the UI."""
        buttons = self.findChildren(QPushButton)  # Find all QPushButton objects
        for button in buttons:
            button.setCursor(Qt.PointingHandCursor)

    def resizeEvent(self, event):
        # Update Size Grips
        from modules.ui_functions import UIFunctions
        UIFunctions.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

        # PRINT MOUSE EVENTS
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')
    



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    main_window = MasterScreen()
    main_window.show()
    sys.exit(app.exec_())
