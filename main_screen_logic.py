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

import pandas as pd
from password_dialog import WachtwoordDialog
import main_ui  # Importa el archivo .py generado
from PyQt5.QtWidgets import QFileDialog

from path_mananger import PathManager
import os
import webbrowser
from PyQt5.QtWidgets import QListWidgetItem, QMessageBox

class MasterScreen(QtWidgets.QMainWindow, main_ui.Ui_MainWindow):  # Usa la clase generada
    def __init__(self,user_data=None):
        super().__init__()
        try:
            ui_file = os.path.join(os.path.dirname(__file__), "main.ui")
            uic.loadUi(ui_file, self)
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

            # Initialize path manager
            self.path_manager = PathManager()

            # Map UI elements to the JSON keys
            self.path_inputs = {
                "Zoek_Afscheiding": self.txtZoekAfs,
                "Zoek_Meting": self.txtZoekMeting,
                "Zoek_SVO": self.txtZoekSVO,
                "Zoek_Plan": self.txtZoekPlan,
                "Sjablonen": self.txtSjablonen,
                "Installatie": self.txtInstalla,
                "Opleiding": self.txtOpleiding,
                "WinCC": self.txtWincc,
                "Vragen": self.txtVragen,
                "E_Learning": self.txtELearning,
            }

            # Disable all text inputs and load paths
            self.load_paths()

            self.zoek_button.clicked.connect(self.search_by_number)
            self.zoek_button_2.clicked.connect(self.search_by_number_meting)

            self.btnZoekSUO.clicked.connect(self.search_all_zoek_svo_files)
            self.btnSearchZoekSVO.clicked.connect(self.filter_zoek_svo_files)
            self.btnZoekPlan.clicked.connect(self.search_all_zoek_plan_files)




            # Connect browse buttons to corresponding JSON keys
            self.btnBrowseZoekAfs.clicked.connect(lambda: self.browse_path("Zoek_Afscheiding"))
            self.btnBrowseZoekMeting.clicked.connect(lambda: self.browse_path("Zoek_Meting"))
            self.btnBrowseZoekSVO.clicked.connect(lambda: self.browse_path("Zoek_SVO"))
            self.btnBrowseZoekPlan.clicked.connect(lambda: self.browse_path("Zoek_Plan"))
            self.btnBrowseSjablonen.clicked.connect(lambda: self.browse_path("Sjablonen"))
            self.btnBrowseInstalla.clicked.connect(lambda: self.browse_path("Installatie"))
            self.btnBrowseOpleiding.clicked.connect(lambda: self.browse_path("Opleiding"))
            self.btnBrowseWincc.clicked.connect(lambda: self.browse_path("WinCC"))
            self.btnBrowseVragen.clicked.connect(lambda: self.browse_path("Vragen"))
            self.btnBrowseELearning.clicked.connect(lambda: self.browse_path("E_Learning"))

    
            # Assign menu button clicks
            self.btnZoek.clicked.connect(self.show_zoek_menu)
            self.btnBereken.clicked.connect(self.show_berek_menu)
            self.btnDocumenten.clicked.connect(self.show_documenten_menu)
            
            self.btnTestList.clicked.connect(self.check_password_and_open_test)
            # Modify btnInstellingen click to require password
            # Assign password-protected buttons with their respective stacked widgets
            self.btnInstellingen.clicked.connect(self.check_password_and_open_settings)

            
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
            
            self.btnZoekPlan.clicked.connect(lambda: self.set_page(13, self.btnZoekPlan))

            
        except Exception as e:
            error_message = f"Error loading UI: {str(e)}\n\nTraceback:\n{traceback.format_exc()}"
            print(error_message)  # Print to console for debugging
            self.show_message_box("Critical Error", error_message)


    def search_all_zoek_plan_files(self):
        """Retrieve and display all files from the Zoek_Plan folder in listWidgetPlan."""
        try:
            # Get the path from JSON
            folder_path = self.path_manager.get_path("Zoek_Plan")

            if not folder_path or not os.path.exists(folder_path):
                QMessageBox.warning(self, "Error", "Please set the path for Zoek Plan first.")
                return

            # Get all files in the folder (excluding subdirectories)
            self.all_plan_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

            # Clear previous results
            self.listWidgetPlan.clear()

            if not self.all_plan_files:
                self.listWidgetPlan.addItem("No files found in Zoek Plan.")
                return

            # Add each file to the list and store its path
            for file_name in self.all_plan_files:
                item = QListWidgetItem(file_name)
                item.setData(32, os.path.join(folder_path, file_name))  # Store file path
                self.listWidgetPlan.addItem(item)

            # Connect item click event to open file
            self.listWidgetPlan.setCursor(Qt.PointingHandCursor)
            self.listWidgetPlan.itemClicked.connect(self.open_file)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")

    def filter_zoek_svo_files(self):
        """Filter the QListWidget items based on zoek_entry text, and if no match is found, show all files again."""
        try:
            search_text = self.zoek_entry.text().strip().lower()

            # Clear list before adding new results
            self.listWidgetSVO.clear()

            if not search_text:
                # If search text is empty, show all files again
                for file_name in self.all_files_SVO:
                    item = QListWidgetItem(file_name)
                    item.setData(32, os.path.join(self.path_manager.get_path("Zoek_SVO"), file_name))
                    self.listWidgetSVO.addItem(item)
                return

            # Filter files containing the search text
            filtered_files = [f for f in self.all_files_SVO if search_text in f.lower()]

            if not filtered_files:
                # If no matches are found, show all files again
                for file_name in self.all_files_SVO:
                    item = QListWidgetItem(file_name)
                    item.setData(32, os.path.join(self.path_manager.get_path("Zoek_SVO"), file_name))
                    self.listWidgetSVO.addItem(item)
                return

            # Display only filtered files
            for file_name in filtered_files:
                item = QListWidgetItem(file_name)
                item.setData(32, os.path.join(self.path_manager.get_path("Zoek_SVO"), file_name))
                self.listWidgetSVO.addItem(item)
            self.listWidgetSVO.setCursor(Qt.PointingHandCursor)


        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while filtering: {e}")

    def search_all_zoek_svo_files(self):
        """Retrieve and display all files from the Zoek_SVO folder in a QListWidget."""
        try:
            # Get the path from JSON
            folder_path = self.path_manager.get_path("Zoek_SVO")

            if not folder_path or not os.path.exists(folder_path):
                QMessageBox.warning(self, "Error", "Please set the path for Zoek SVO first.")
                return

            # Get all files in the folder (excluding subdirectories)
            self.all_files_SVO = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

            # Clear previous results
            self.listWidgetSVO.clear()

            if not self.all_files_SVO:
                self.listWidgetSVO.addItem("No self.all_files_SVO found in Zoek SVO.")
                return

            # Add each file to the list
            for file_name in self.all_files_SVO:
                try:
                    item = QListWidgetItem(file_name)  # Fix: Use QListWidgetItem (not QlistWidgetItem)
                    item.setData(32, os.path.join(folder_path, file_name))  # Store file path
                    item.setFlags(item.flags() | Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    self.listWidgetSVO.addItem(item)
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to add file '{file_name}': {e}")

            # Connect item click event
             # Set Hand Cursor when hovering over the list
            self.listWidgetSVO.setCursor(Qt.PointingHandCursor)
            self.listWidgetSVO.itemClicked.connect(self.open_file)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")

    def open_file(self, item):
        """Open the selected file in Windows Explorer."""
        try:
            file_path = item.data(32)  # Retrieve file path stored in item
            if file_path and os.path.exists(file_path):
                webbrowser.open(file_path)
            else:
                QMessageBox.warning(self, "Error", "File not found or path is invalid.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open file: {e}")

    def search_by_number_meting(self):
        """Search for the entered number in the Zoek_Meting Excel file."""
        search_value = self.zoek_vak.text().strip()  # Read input from text field

        if not search_value:
            QMessageBox.warning(self, "Warning", "Please enter a search term.")
            return

        # Get the path from JSON
        excel_path = self.path_manager.get_path("Zoek_Meting")

        if not excel_path or not os.path.exists(excel_path):
            QMessageBox.warning(self, "Error", "Please set the path for Zoek_Meting first.")
            return

        try:
            # Read Excel file with header on the first row
            df = pd.read_excel(excel_path, engine="openpyxl", header=0)

            # **DEBUGGING: Print available column names**
            print("Column names in the file:", df.columns.tolist())

            # Ensure 'NUMMER' column exists
            if "NUMMER" not in df.columns:
                QMessageBox.critical(self, "Error", "The 'NUMMER' column was not found in the Excel file.")
                return

            # Convert 'NUMMER' column to string and remove whitespace
            search_column = df["NUMMER"].astype(str).str.strip()

            # Search for full or partial matches
            match_index = search_column[search_column.str.contains(search_value, case=False, na=False)].index

            if match_index.empty:
                QMessageBox.information(self, "No Result", "No matching records found.")
                return

            # Retrieve matching numbers and fill missing values with "X"
            results = df.loc[match_index, "NUMMER"].fillna("X").astype(str).tolist()

            # Update dropdown with results
            self.result_dropdown.clear()
            self.result_dropdown.addItems(results)
            self.result_dropdown.setCurrentIndex(0)

            # Bind selection change event to load details
            self.result_dropdown.currentTextChanged.connect(lambda: self.load_details_for_measurement(self.result_dropdown.currentText(), df))

            # Automatically load details for the first match
            self.load_details_for_measurement(results[0], df)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def search_by_number(self):
        """Search for the entered number in the Zoek_Afscheiding Excel file."""
        search_value = self.zoek_nummer.text().strip()  # Read input from text field

        if not search_value:
            QMessageBox.warning(self, "Warning", "Please enter a number to search.")
            return

        # Get the path from JSON
        excel_path = self.path_manager.get_path("Zoek_Afscheiding")

        if not excel_path or not os.path.exists(excel_path):
            QMessageBox.warning(self, "Error", "Please set the path for Zoek Afscheiding first.")
            return

        try:
            # Read Excel file
            df = pd.read_excel(excel_path, engine="openpyxl")

            # Extract column B from rows 2-1000
            column_B = df.iloc[2:1000, 1].astype(str)

            # Find matching indices
            match_index = column_B[column_B.str.contains(search_value, case=False, na=False)].index

            if match_index.empty:
                QMessageBox.information(self, "No Result", "No matching records found.")
                return

            # Convert to a list and update dropdown
            numbers = df.iloc[match_index, 1].fillna("X").astype(str).tolist()
            self.num_dropdown.clear()
            self.num_dropdown.addItems(numbers)
            self.num_dropdown.setCurrentIndex(0)

            # Automatically load details for the first found number

            self.load_details_for_number(numbers[0], df)
            self.num_dropdown.currentTextChanged.connect(lambda: self.load_details_for_number(self.num_dropdown.currentText(), df))

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")
    def load_details_for_measurement(self, selected_number, df):
        """Load details from the DataFrame based on the selected measurement number."""
        if not selected_number:
            return

        try:
            # Find the row corresponding to the selected number
            row = df[df["NUMMER"].astype(str) == selected_number]

            if not row.empty:
                row = row.iloc[0]  # Extract the first matching row

                # Extract relevant columns and replace missing values with "X"
                details = {
                    "txtLocatie": row["LOCATIE"] if pd.notna(row["LOCATIE"]) else "X",   # Location
                    "txtSoortMeting": row["SOORT METING"] if pd.notna(row["SOORT METING"]) else "X",  # Measurement Type
                    "txtDienst": row["DIENST"] if pd.notna(row["DIENST"]) else "X",       # Service
                    "txtRichtwaarde": row["RICHTWAARDE"] if pd.notna(row["RICHTWAARDE"]) else "X",  # Target Value
                    "txtAlarmWaardes": row["ALARM WAARDES"] if pd.notna(row["ALARM WAARDES"]) else "X",  # Alarm Values
                }

                # Extra info fields (QPlainTextEdit requires setPlainText)
                extra_info = {
                    "entry_spec_locatie_2": row["SPECIFIEKE LOCATIE"] if pd.notna(row["SPECIFIEKE LOCATIE"]) else "X",
                    "entry_opmerkingen_2": row["OPMRERKINGEN"] if pd.notna(row["OPMRERKINGEN"]) else "X",
                }

                # Update UI text fields
                for field, value in details.items():
                    widget = getattr(self, field, None)
                    if widget:
                        widget.setText(str(value))

                # Update QPlainTextEdit fields
                for field, value in extra_info.items():
                    widget = getattr(self, field, None)
                    if widget:
                        widget.setPlainText(str(value))

            else:
                # If no matching row is found, set all fields to "X"
                for field in ["txtLocatie", "txtSoortMeting", "txtDienst", "txtRichtwaarde", "txtAlarmWaardes"]:
                    widget = getattr(self, field, None)
                    if widget:
                        widget.setText("X")

                for field in ["entry_spec_locatie_2", "entry_opmerkingen_2"]:
                    widget = getattr(self, field, None)
                    if widget:
                        widget.setPlainText("X")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load details: {e}")

    def load_details_for_number(self, selected_number, df):
        """Load details from the DataFrame based on the selected number."""
        if not selected_number:
            return

        try:
            # Find the row corresponding to the selected number
            row = df[df.iloc[:, 1].astype(str) == selected_number]

            if not row.empty:
                row = row.iloc[0]  # Extract the first matching row

                # Extract relevant columns and replace missing values with "X"
                details = {
                    "txtLocaite": row.iloc[2] if pd.notna(row.iloc[2]) else "X",     # Location (Column C)
                    "txtSoort": row.iloc[4] if pd.notna(row.iloc[4]) else "X",       # Type (Column E)
                    "txtVenti": row.iloc[5] if pd.notna(row.iloc[5]) else "X",       # Valve Box (Column F)
                    "txtPFNumber": row.iloc[6] if pd.notna(row.iloc[6]) else "X",    # PF Number (Column G)
                    "txtYNummer": row.iloc[7] if pd.notna(row.iloc[7]) else "X",     # Y Number (Column H)
                    "txtPlanNumber": row.iloc[9] if pd.notna(row.iloc[9]) else "X",  # Plan Number (Column J)
                }

                extra_info = {
                    "entry_spec_locatie": row.iloc[3] if pd.notna(row.iloc[3]) else "X",  # Specific Location (Column D)
                    "entry_opmerkingen": row.iloc[11] if pd.notna(row.iloc[11]) else "X",  # Remarks (Column L)
                }

                # Update UI text fields
                for field, value in details.items():
                    widget = getattr(self, field, None)
                    if widget:
                        widget.setText(str(value))

                # Update QPlainTextEdit fields
                for field, value in extra_info.items():
                    widget = getattr(self, field, None)
                    if widget and isinstance(widget, QtWidgets.QPlainTextEdit):
                        widget.setPlainText(str(value))

            else:
                # If no matching row is found, set all fields to "X"
                for field in ["txtLocaite", "txtSoort", "txtVenti", "txtPFNumber", "txtYNummer", "txtPlanNumber"]:
                    widget = getattr(self, field, None)
                    if widget:
                        widget.setText("X")


                for field in ["entry_spec_locatie", "entry_opmerkingen"]:
                    widget = getattr(self, field, None)
                    if widget and isinstance(widget, QtWidgets.QPlainTextEdit):
                        widget.setPlainText("X")
                        widget.setStyleSheet("color: black;")  # Ensure text remains black


        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load details: {e}")

    def load_paths(self):
        """Load stored paths from JSON and set them in disabled text inputs."""
        for key, input_field in self.path_inputs.items():
            path = self.path_manager.get_path(key)
            input_field.setText(path)
            input_field.setDisabled(True)


    def browse_path(self, key):
        """Open a file or folder dialog based on the key type."""
        if key in ["Zoek_Afscheiding", "Zoek_Meting"]:
            # Open file dialog for Excel files
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Select Excel File", "", "Excel Files (*.xlsx *.xls *.xlsm)"
            )
            if file_path:
                self.path_manager.set_path(key, file_path)
                self.path_inputs[key].setText(file_path)
        else:
            # Open folder dialog for directories
            folder = QFileDialog.getExistingDirectory(self, "Select Folder")
            if folder:
                self.path_manager.set_path(key, folder)
                self.path_inputs[key].setText(folder)



    def check_password_and_open_settings(self):
        """Shows password dialog and changes the page in stackedWidget if successful."""
        try:
            wachtwoord_dialoog = WachtwoordDialog(self)
            if wachtwoord_dialoog.exec():  # If password is correct
                self.handleMenuClick(self.btnInstellingen, 4)  # Highlight the button
                self.stackedWidget_2.setCurrentIndex(12)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def check_password_and_open_test(self):
        """Shows password dialog and changes the page in stackedWidget_2 if successful."""
        try:
            wachtwoord_dialoog = WachtwoordDialog(self)
            if wachtwoord_dialoog.exec():  # If password is correct
                self.handleMenuClick(self.btnWincc,3)
                self.set_page(9, self.btnWincc)       
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
