from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SettingsWindow(object):
    def setupUi(self, SettingsWindow):
        SettingsWindow.setObjectName("SettingsWindow")
        SettingsWindow.resize(391, 292)
        self.centralwidget = QtWidgets.QWidget(SettingsWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(20, 20, 251, 211))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.add_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.add_pushButton.setGeometry(QtCore.QRect(290, 20, 81, 26))
        self.add_pushButton.setObjectName("add_pushButton")
        self.delete_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.delete_pushButton.setGeometry(QtCore.QRect(290, 50, 81, 26))
        self.delete_pushButton.setObjectName("delete_pushButton")
        self.edit_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.edit_pushButton.setGeometry(QtCore.QRect(290, 80, 81, 26))
        self.edit_pushButton.setObjectName("edit_pushButton")
        self.save_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.save_pushButton.setGeometry(QtCore.QRect(290, 170, 81, 26))
        self.save_pushButton.setObjectName("save_pushButton")
        self.cancel_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.cancel_pushButton.setGeometry(QtCore.QRect(290, 200, 81, 26))
        self.cancel_pushButton.setObjectName("cancel_pushButton")
        SettingsWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(SettingsWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 391, 21))
        self.menubar.setObjectName("menubar")
        SettingsWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(SettingsWindow)
        self.statusbar.setObjectName("statusbar")
        SettingsWindow.setStatusBar(self.statusbar)

        self.retranslateUi(SettingsWindow)
        QtCore.QMetaObject.connectSlotsByName(SettingsWindow)

    def retranslateUi(self, SettingsWindow):
        _translate = QtCore.QCoreApplication.translate
        SettingsWindow.setWindowTitle(_translate("SettingsWindow", "MainWindow"))
        self.add_pushButton.setText(_translate("SettingsWindow", "Add"))
        self.delete_pushButton.setText(_translate("SettingsWindow", "Delete"))
        self.edit_pushButton.setText(_translate("SettingsWindow", "Edit"))
        self.save_pushButton.setText(_translate("SettingsWindow", "Save"))
        self.cancel_pushButton.setText(_translate("SettingsWindow", "Cancel"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    SettingsWindow = QtWidgets.QMainWindow()
    ui = Ui_SettingsWindow()
    ui.setupUi(SettingsWindow)
    SettingsWindow.show()
    sys.exit(app.exec_())
