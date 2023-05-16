# /Users/marcelloamadeus/Desktop/Code/Application/Insert_To_MsWord/venv/lib/python3.11/site-packages/qt5_applications/Qt/bin/Designer.app

import os
import re
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QTableWidgetItem

from db import extract_db, initiate_db, save_db
from edit_window import Ui_EditWindow
from insert import auto_insert, filter_by_document
from main_window import Ui_MainWindow
from settings_window import Ui_SettingsWindow


class Window(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super(Window, self).__init__()
        self.open_main_window()
        self.main_window_function()

    def open_main_window(self) -> None:
        self.main_window = Ui_MainWindow()
        self.main_window.setupUi(self)
        self.setWindowTitle("Insert To Ms Word")

    def main_window_function(self) -> None:
        self.main_window.filePath_label.setAlignment(QtCore.Qt.AlignRight)
        self.main_window.folderPath_label.setAlignment(QtCore.Qt.AlignRight)
        self.main_window.filePath_pushButton.clicked.connect(
            self.filePath_pushButton_clicked
        )
        self.main_window.folderPath_pushButton.clicked.connect(
            self.folderPath_pushButton_clicked
        )
        self.main_window.run_pushButton.clicked.connect(self.run_program)
        self.main_window.settings_pushButton.clicked.connect(self.init_settings_window)

    def init_settings_window(self) -> None:
        self.open_settings_window()
        self.settings_window_function()

    def open_settings_window(self) -> None:
        self.swindow = QtWidgets.QMainWindow()
        self.settings_window = Ui_SettingsWindow()
        self.settings_window.setupUi(self.swindow)
        self.swindow.setWindowTitle("Settings")
        self.swindow.show()

    def settings_window_function(self) -> None:
        self.settings_window.add_pushButton.clicked.connect(self.add)
        self.settings_window.delete_pushButton.clicked.connect(self.delete)
        self.settings_window.edit_pushButton.clicked.connect(self.edit)
        self.settings_window.save_pushButton.clicked.connect(self.save)
        self.settings_window.cancel_pushButton.clicked.connect(self.cancel)
        self.settings_window.tableWidget.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows
        )
        # self.settings_window.tableWidget.selectionModel().selectionChanged.connect(
        #     self.row_selected
        # )
        self.settings_window.tableWidget.setColumnCount(6)
        self.settings_window.tableWidget.setHorizontalHeaderLabels(
            (
                "File Name",
                "Extension",
                "Prompt",
                "File Number",
                "Priority",
                "Priority Value",
            )
        )
        self.settings_window.tableWidget.setColumnWidth(2, 500)

        data = extract_db()

        self.settings_window.tableWidget.setRowCount(len(data))

        if data:
            for i in range(len(data)):
                for j in range(len(data[0])):
                    self.settings_window.tableWidget.setItem(
                        i, j, QTableWidgetItem(str(data[i][j]))
                    )

        # for i in range(len())
        # self.settings_window.tableWidget.setItem

    def init_edit_window(self) -> None:
        self.open_edit_window()
        self.edit_window_function()

    def open_edit_window(self) -> None:
        self.ewindow = QtWidgets.QMainWindow()
        self.edit_window = Ui_EditWindow()
        self.edit_window.setupUi(self.ewindow)
        self.ewindow.setWindowTitle("Edit")
        self.ewindow.show()

    def edit_window_function(self) -> None:
        self.edit_window.okay_pushButton.clicked.connect(self.okay)

    def init_addedit_window(self) -> None:
        self.open_addedit_window()
        self.addedit_window_function()

    def open_addedit_window(self) -> None:
        self.awindow = QtWidgets.QMainWindow()
        self.add_window = Ui_EditWindow()
        self.add_window.setupUi(self.awindow)
        self.awindow.setWindowTitle("Add")
        self.awindow.show()

    def addedit_window_function(self) -> None:
        self.add_window.okay_pushButton.clicked.connect(self.addokay)

    def filePath_pushButton_clicked(self) -> None:
        file_path = QFileDialog.getOpenFileName(
            self,
            "Open File",
            "",
            "Word Document (*.docx)",
        )

        if file_path:
            self.main_window.file_path = str(file_path[0])
            self.main_window.filePath_label.setText(self.main_window.file_path)

    def folderPath_pushButton_clicked(self) -> None:
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "Open Folder",
            "",
            QFileDialog.ShowDirsOnly
            | QFileDialog.DontResolveSymlinks
            | QFileDialog.DontUseNativeDialog,
        )

        if folder_path:
            self.main_window.folder_path = str(folder_path)
            self.main_window.folderPath_label.setText(self.main_window.folder_path)

    def run_program(self) -> None:
        try:
            data = extract_db()
            document_instruction = filter_by_document(
                self.main_window.filePath_label.text()
            )
            if len(set(document_instruction[3])) != len(data):
                document_response = QMessageBox.warning(
                    self,
                    "Warning",
                    "Not all of the settings entries is found in Document! Proceed?",
                    QMessageBox.Yes | QMessageBox.No,
                )
                if document_response == QMessageBox.No:
                    return
            # image_instruction = filter_by_image(
            #     self.main_window.folderPath_label.text()
            # )

            files = [
                f
                for f in os.listdir(self.main_window.folderPath_label.text())
                if os.path.isfile(
                    "/".join([self.main_window.folderPath_label.text(), f])
                )
                and not f.startswith(".")
            ]

            file_name_from_settings = [entry[0] for entry in data]
            extension_from_settings = [ent[1] for ent in data]
            file_number_from_settings = [com[3] for com in data]
            matches = []
            # for file in files:
            #     matches.append(
            #         any(file_name in file for file_name in file_name_from_settings)
            #     )

            for i in range(len(data)):
                count = []
                for file in files:
                    if file_number_from_settings[i] == "Single":
                        count.append(
                            "".join(
                                [file_name_from_settings[i], extension_from_settings[i]]
                            )
                            == file
                        )
                    else:
                        count.append(
                            bool(
                                re.findall(
                                    "".join(
                                        [
                                            file_name_from_settings[i],
                                            "_",
                                            "\\d+",
                                            extension_from_settings[i],
                                        ]
                                    ),
                                    file,
                                )
                            )
                        )
                        # print(
                        #     re.findall(
                        #         "".join(
                        #             [
                        #                 file_name_from_settings[i],
                        #                 "_",
                        #                 "\\d+",
                        #                 extension_from_settings[i],
                        #             ]
                        #         ),
                        #         file,
                        #     )
                        # )
                matches.append(count)
            # print(matches)

            index = []
            for j in range(len(matches[0])):
                arr = []
                for k in range(len(matches)):
                    arr.append(matches[k][j])
                index.append(any(arr))

            not_identified = any(x == False for x in index)
            if not_identified:
                image_response = QMessageBox.warning(
                    self,
                    "Warning",
                    "Some files inside the folder is not identified in settings. Proceed?",
                    QMessageBox.Yes | QMessageBox.No,
                )
                if image_response == QMessageBox.No:
                    return

            for element in matches:
                if any(element) == False:
                    image1_response = QMessageBox.warning(
                        self,
                        "Warning",
                        "Not all of the settings entries (file names) is found in folder! Proceed?",
                        QMessageBox.Yes | QMessageBox.No,
                    )
                    if image1_response == QMessageBox.No:
                        return

            # np_files = np.array(files)
            # np_matches = np.array(matches, dtype=bool)
            # np_filtered = np_files[np_matches]
            # image_instruction = np_filtered.tolist()

            total_true = 0
            for m in range(len(matches)):
                for n in range(len(matches[0])):
                    if matches[m][n] == True:
                        total_true += 1
            if len(document_instruction[0]) != total_true:
                not_matched = QMessageBox.information(
                    self,
                    "Information",
                    "The numbers of file needed to be inserted is not equivalent to the numbers of slot detected in document. Please go to the document or file for more analysis!",
                )

            image_instruction = []  # index of the file that don't need to be inserted

            for id in range(len(index)):
                if index[id] == False:
                    image_instruction.append(id)

            response = QMessageBox.question(
                self,
                "",
                "Do you want to perform the insertion?",
                QMessageBox.Yes | QMessageBox.No,
            )
            if response == QMessageBox.Yes:
                auto_insert(
                    self.main_window.filePath_label.text(),
                    self.main_window.folderPath_label.text(),
                    document_instruction,
                    image_instruction,
                    files,
                )
                finish = QMessageBox.information(self, "", "Inserted!")

        except:
            QMessageBox.warning(
                self,
                "Warning",
                "The program cannot insert properly.\n\nPlease do check the document file for further information or check the settings as there might be nothing to insert. (Could not detect any line to be inserted in Ms Word)",
            )

    def add(self) -> None:
        self.init_addedit_window()
        # if not self.valid():
        #     return
        # row = self.settings_window.tableWidget.rowCount()
        # self.settings_window.tableWidget.insertRow(row)
        # self.settings_window.tableWidget.setItem(row, 0, QTableWidgetItem(self.))

    def delete(self) -> None:
        current_row = self.settings_window.tableWidget.currentRow()
        if current_row < 0:
            return QMessageBox.warning(
                self, "Warning", "Please select a record to delete"
            )

        button = QMessageBox.question(
            self,
            "Confirmation",
            "Are you sure that you want to delete the selected row?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if button == QMessageBox.StandardButton.Yes:
            self.settings_window.tableWidget.removeRow(current_row)

    def edit(self) -> None:
        current_row = self.settings_window.tableWidget.currentRow()
        if current_row < 0:
            return QMessageBox.warning(
                self, "Warning", "Please select a record to delete"
            )

        self.init_edit_window()

    def save(self) -> None:
        data = []
        for i in range(self.settings_window.tableWidget.rowCount()):
            subdata = []
            for j in range(6):
                if j == 5:
                    subdata.append(
                        float(self.settings_window.tableWidget.item(i, j).text())
                    )
                else:
                    subdata.append(self.settings_window.tableWidget.item(i, j).text())
            subdata = tuple(subdata)
            data.append(subdata)
        save_db(data)
        self.swindow.close()

    def cancel(self) -> None:
        self.swindow.close()

    # def row_selected(self) -> int:
    #     row = self.settings_window.tableWidget.selectionModel().selectedRows()[0].row()
    #     return row

    def okay(self) -> None:
        if not self.valid():
            return
        current_row = self.settings_window.tableWidget.currentRow()
        self.settings_window.tableWidget.setItem(
            current_row, 0, QTableWidgetItem(self.edit_window.fileName_lineEdit.text())
        )
        self.settings_window.tableWidget.setItem(
            current_row, 1, QTableWidgetItem(self.edit_window.extension_lineEdit.text())
        )
        self.settings_window.tableWidget.setItem(
            current_row, 2, QTableWidgetItem(self.edit_window.prompt_lineEdit.text())
        )
        self.settings_window.tableWidget.setItem(
            current_row,
            3,
            QTableWidgetItem(self.edit_window.fileNumber_lineEdit.text().capitalize()),
        )
        self.settings_window.tableWidget.setItem(
            current_row,
            4,
            QTableWidgetItem(self.edit_window.priority_lineEdit.text().capitalize()),
        )
        self.settings_window.tableWidget.setItem(
            current_row,
            5,
            QTableWidgetItem(self.edit_window.priorityValue_lineEdit.text()),
        )
        self.ewindow.close()

    def addokay(self) -> None:
        if not self.addvalid():
            return
        row = self.settings_window.tableWidget.rowCount()
        self.settings_window.tableWidget.insertRow(row)
        self.settings_window.tableWidget.setItem(
            row, 0, QTableWidgetItem(self.add_window.fileName_lineEdit.text())
        )
        self.settings_window.tableWidget.setItem(
            row, 1, QTableWidgetItem(self.add_window.extension_lineEdit.text())
        )
        self.settings_window.tableWidget.setItem(
            row, 2, QTableWidgetItem(self.add_window.prompt_lineEdit.text())
        )
        self.settings_window.tableWidget.setItem(
            row,
            3,
            QTableWidgetItem(self.add_window.fileNumber_lineEdit.text().capitalize()),
        )
        self.settings_window.tableWidget.setItem(
            row,
            4,
            QTableWidgetItem(self.add_window.priority_lineEdit.text().capitalize()),
        )
        self.settings_window.tableWidget.setItem(
            row, 5, QTableWidgetItem(self.add_window.priorityValue_lineEdit.text())
        )
        self.awindow.close()

    def valid(self) -> bool:
        if not self.edit_window.fileName_lineEdit.text():
            QMessageBox.critical(self, "Error", "Please enter file name!")
            self.edit_window.fileName_lineEdit.setFocus()
            return False
        fileName_list = []
        for i in range(self.settings_window.tableWidget.rowCount()):
            fileName_list.append(self.settings_window.tableWidget.item(i, 0).text())
        fileName_list.remove(
            self.settings_window.tableWidget.item(
                self.settings_window.tableWidget.currentRow(), 0
            ).text()
        )
        if any(x == self.edit_window.fileName_lineEdit.text() for x in fileName_list):
            QMessageBox.critical(self, "Error", "File name has already existed!")
            self.edit_window.fileName_lineEdit.setFocus()
            return False

        if not self.edit_window.extension_lineEdit.text().startswith("."):
            QMessageBox.critical(self, "Error", "The extension should begin with '.'!")
            self.edit_window.extension_lineEdit.setFocus()
            return False

        if not self.edit_window.prompt_lineEdit.text():
            QMessageBox.critical(self, "Error", "Please enter prompt!")
            self.edit_window.prompt_lineEdit.setFocus()
            return False
        prompt_list = []
        for i in range(self.settings_window.tableWidget.rowCount()):
            prompt_list.append(self.settings_window.tableWidget.item(i, 2).text())
        prompt_list.remove(
            self.settings_window.tableWidget.item(
                self.settings_window.tableWidget.currentRow(), 2
            ).text()
        )
        if any(y == self.edit_window.prompt_lineEdit.text() for y in prompt_list):
            QMessageBox.critical(self, "Error", "Prompt has already existed!")
            self.edit_window.prompt_lineEdit.setFocus()
            return False

        if not (
            (self.edit_window.fileNumber_lineEdit.text().strip().lower() == "single")
            or (
                self.edit_window.fileNumber_lineEdit.text().strip().lower()
                == "multiple"
            )
        ):
            QMessageBox.critical(
                self,
                "Error",
                "Please enter the correct file number (single or multiple)!",
            )
            self.edit_window.fileNumber_lineEdit.setFocus()
            return False

        if not (
            (self.edit_window.priority_lineEdit.text().strip().lower() == "height")
            or (self.edit_window.priority_lineEdit.text().strip().lower() == "width")
        ):
            QMessageBox.critical(
                self,
                "Error",
                "Please enter the correct priority (height or width)!",
            )
            self.edit_window.priority_lineEdit.setFocus()
            return False

        try:
            priority_value = float(
                self.edit_window.priorityValue_lineEdit.text().strip()
            )
        except ValueError:
            QMessageBox.critical(
                self,
                "Error",
                "Please enter the correct priority value!",
            )
            return False
        return True

    def addvalid(self) -> bool:
        if not self.add_window.fileName_lineEdit.text():
            QMessageBox.critical(self, "Error", "Please enter file name!")
            self.add_window.fileName_lineEdit.setFocus()
            return False
        fileName_list = []
        for i in range(self.settings_window.tableWidget.rowCount()):
            fileName_list.append(self.settings_window.tableWidget.item(i, 0).text())
        if any(x == self.add_window.fileName_lineEdit.text() for x in fileName_list):
            QMessageBox.critical(self, "Error", "File name has already existed!")
            self.add_window.fileName_lineEdit.setFocus()
            return False

        if not self.add_window.extension_lineEdit.text().startswith("."):
            QMessageBox.critical(self, "Error", "The extension should begin with '.'!")
            self.add_window.extension_lineEdit.setFocus()
            return False

        if not self.add_window.prompt_lineEdit.text():
            QMessageBox.critical(self, "Error", "Please enter prompt!")
            self.add_window.prompt_lineEdit.setFocus()
            return False
        prompt_list = []
        for i in range(self.settings_window.tableWidget.rowCount()):
            prompt_list.append(self.settings_window.tableWidget.item(i, 2).text())
        if any(y == self.add_window.prompt_lineEdit.text() for y in prompt_list):
            QMessageBox.critical(self, "Error", "Prompt has already existed!")
            self.add_window.prompt_lineEdit.setFocus()
            return False

        if not (
            (self.add_window.fileNumber_lineEdit.text().strip().lower() == "single")
            or (
                self.add_window.fileNumber_lineEdit.text().strip().lower() == "multiple"
            )
        ):
            QMessageBox.critical(
                self,
                "Error",
                "Please enter the correct file number (single or multiple)!",
            )
            self.add_window.fileNumber_lineEdit.setFocus()
            return False

        if not (
            (self.add_window.priority_lineEdit.text().strip().lower() == "height")
            or (self.add_window.priority_lineEdit.text().strip().lower() == "width")
        ):
            QMessageBox.critical(
                self,
                "Error",
                "Please enter the correct priority (height or width)!",
            )
            self.add_window.priority_lineEdit.setFocus()
            return False

        try:
            priority_value = float(
                self.add_window.priorityValue_lineEdit.text().strip()
            )
        except ValueError:
            QMessageBox.critical(
                self,
                "Error",
                "Please enter the correct priority value!",
            )
            return False
        return True


def create_app() -> None:
    app = QtWidgets.QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())


def main() -> None:
    initiate_db()
    create_app()


if __name__ == "__main__":
    main()
