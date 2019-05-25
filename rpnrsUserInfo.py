# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rpnrsUserInfo.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import pymysql

conn = pymysql.connect(host='localhost', user='root', password='', database='rpnrsdb')

class Ui_userInformationWindow(object):
    def refresh(self):
        with conn.cursor() as cursor:
            cmd = "SELECT ownerId, ownerFirstname, ownerMiddlename, ownerLastname, ownerAge, ownerAddress, ownerContact, ownerEmail, ownerProf, ownerDept, vehicleColor, vehicleBrand, vehicleModel, vehicleType, vehicleId, dateReg from ownertbl INNER JOIN vehicletbl ON ownertbl.ownerId = vehicletbl.vehicleOwnerId ORDER BY ownerId"
            cursor.execute(cmd)
            data = cursor.fetchall()
            self.InformationtableWidget.setRowCount(0)
            for row_number, row_data in enumerate(data):
                self.InformationtableWidget.insertRow(row_number)
                for column_number, column_data in enumerate(row_data):
                    self.InformationtableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))
        conn.commit()
    def search(self):
        srch = self.searchEdit.text()
        box = str(self.FilterBox.currentText())

        if box == "OWNER ID":
            with conn.cursor() as cursor:
                sql = "SELECT ownerId, ownerFirstname, ownerMiddlename, ownerLastname, ownerAge, ownerAddress, ownerContact, ownerEmail, ownerProf, ownerDept, vehicleColor, vehicleBrand, vehicleModel, vehicleType, vehicleId, dateReg from ownertbl INNER JOIN vehicletbl ON ownertbl.ownerId = vehicletbl.vehicleOwnerId WHERE ownerId = %s"
                try:
                    cursor.execute(sql,(srch))
                    result = cursor.fetchall()
                    self.InformationtableWidget.setRowCount(0)
                    for row_number, row_data in enumerate(result):
                        self.InformationtableWidget.insertRow(row_number)
                        for column_number, column_data in enumerate(row_data):
                            self.InformationtableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))

     
                except:
                    print("Oops! Something wrong")

            conn.commit()
        elif box == "OWNER FIRSTNAME":
            with conn.cursor() as cursor:
                sql = "SELECT ownerId, ownerFirstname, ownerMiddlename, ownerLastname, ownerAge, ownerAddress, ownerContact, ownerEmail, ownerProf, ownerDept, vehicleColor, vehicleBrand, vehicleModel, vehicleType, vehicleId, dateReg from ownertbl INNER JOIN vehicletbl ON ownertbl.ownerId = vehicletbl.vehicleOwnerId WHERE ownerFirstname = %s"
                try:
                    cursor.execute(sql,(srch))
                    result = cursor.fetchall()
                    self.InformationtableWidget.setRowCount(0)
                    for row_number, row_data in enumerate(result):
                        self.InformationtableWidget.insertRow(row_number)
                        for column_number, column_data in enumerate(row_data):
                            self.InformationtableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))

     
                except:
                    print("Oops! Something wrong")

            conn.commit()
        elif box == "DATE REGISTERED":
            with conn.cursor() as cursor:
                sql = "SELECT ownerId, ownerFirstname, ownerMiddlename, ownerLastname, ownerAge, ownerAddress, ownerContact, ownerEmail, ownerProf, ownerDept, vehicleColor, vehicleBrand, vehicleModel, vehicleType, vehicleId, dateReg from ownertbl INNER JOIN vehicletbl ON ownertbl.ownerId = vehicletbl.vehicleOwnerId WHERE dateReg = %s"
                try:
                    cursor.execute(sql,(srch))
                    result = cursor.fetchall()
                    self.InformationtableWidget.setRowCount(0)
                    for row_number, row_data in enumerate(result):
                        self.InformationtableWidget.insertRow(row_number)
                        for column_number, column_data in enumerate(row_data):
                            self.InformationtableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))

     
                except:
                    print("Oops! Something wrong")

            conn.commit()
        elif box == "PLATE NUMBER":
            with conn.cursor() as cursor:
                sql = "SELECT ownerId, ownerFirstname, ownerMiddlename, ownerLastname, ownerAge, ownerAddress, ownerContact, ownerEmail, ownerProf, ownerDept, vehicleColor, vehicleBrand, vehicleModel, vehicleType, vehicleId, dateReg from ownertbl INNER JOIN vehicletbl ON ownertbl.ownerId = vehicletbl.vehicleOwnerId WHERE vehicleId = %s"
                try:
                    cursor.execute(sql,(srch))
                    result = cursor.fetchall()
                    self.InformationtableWidget.setRowCount(0)
                    for row_number, row_data in enumerate(result):
                        self.InformationtableWidget.insertRow(row_number)
                        for column_number, column_data in enumerate(row_data):
                            self.InformationtableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))

     
                except:
                    print("Oops! Something wrong")

            conn.commit()
        elif box == "VEHICLE TYPE":
            with conn.cursor() as cursor:
                sql = "SELECT ownerId, ownerFirstname, ownerMiddlename, ownerLastname, ownerAge, ownerAddress, ownerContact, ownerEmail, ownerProf, ownerDept, vehicleColor, vehicleBrand, vehicleModel, vehicleType, vehicleId, dateReg from ownertbl INNER JOIN vehicletbl ON ownertbl.ownerId = vehicletbl.vehicleOwnerId WHERE vehicleType = %s"
                try:
                    cursor.execute(sql,(srch))
                    result = cursor.fetchall()
                    self.InformationtableWidget.setRowCount(0)
                    for row_number, row_data in enumerate(result):
                        self.InformationtableWidget.insertRow(row_number)
                        for column_number, column_data in enumerate(row_data):
                            self.InformationtableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))

     
                except:
                    print("Oops! Something wrong")

            conn.commit()
        elif box == "VEHICLE BRAND":
            with conn.cursor() as cursor:
                sql = "SELECT ownerId, ownerFirstname, ownerMiddlename, ownerLastname, ownerAge, ownerAddress, ownerContact, ownerEmail, ownerProf, ownerDept, vehicleColor, vehicleBrand, vehicleModel, vehicleType, vehicleId, dateReg from ownertbl INNER JOIN vehicletbl ON ownertbl.ownerId = vehicletbl.vehicleOwnerId WHERE vehicleBrand = %s"
                try:
                    cursor.execute(sql,(srch))
                    result = cursor.fetchall()
                    self.InformationtableWidget.setRowCount(0)
                    for row_number, row_data in enumerate(result):
                        self.InformationtableWidget.insertRow(row_number)
                        for column_number, column_data in enumerate(row_data):
                            self.InformationtableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))

     
                except:
                    print("Oops! Something wrong")

            conn.commit()
        else:
            self.refresh()
    def setupUi5(self, userInformationWindow):
        userInformationWindow.setObjectName("userInformationWindow")
        userInformationWindow.resize(1057, 466)
        userInformationWindow.setMinimumSize(QtCore.QSize(1057, 466))
        userInformationWindow.setMaximumSize(QtCore.QSize(1057, 466))
        userInformationWindow.setStyleSheet("background-color: rgb(0, 84, 139);")
        self.centralwidget = QtWidgets.QWidget(userInformationWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.InformationtableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.InformationtableWidget.setGeometry(QtCore.QRect(370, 7, 681, 451))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        self.InformationtableWidget.setFont(font)
        self.InformationtableWidget.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.InformationtableWidget.setRowCount(1000000)
        self.InformationtableWidget.setColumnCount(16)
        self.InformationtableWidget.setObjectName("InformationtableWidget")
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(9)
        item.setFont(font)
        self.InformationtableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(9)
        item.setFont(font)
        self.InformationtableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(9)
        item.setFont(font)
        self.InformationtableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(9)
        item.setFont(font)
        self.InformationtableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(9)
        item.setFont(font)
        self.InformationtableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(9)
        item.setFont(font)
        self.InformationtableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(9)
        item.setFont(font)
        self.InformationtableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(9)
        item.setFont(font)
        self.InformationtableWidget.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(9)
        item.setFont(font)
        self.InformationtableWidget.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(9)
        item.setFont(font)
        self.InformationtableWidget.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(9)
        item.setFont(font)
        self.InformationtableWidget.setHorizontalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(9)
        item.setFont(font)
        self.InformationtableWidget.setHorizontalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(9)
        item.setFont(font)
        self.InformationtableWidget.setHorizontalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(9)
        item.setFont(font)
        self.InformationtableWidget.setHorizontalHeaderItem(13, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(9)
        item.setFont(font)
        self.InformationtableWidget.setHorizontalHeaderItem(14, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(9)
        item.setFont(font)
        self.InformationtableWidget.setHorizontalHeaderItem(15, item)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 371, 461))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(20)
        self.frame.setFont(font)
        self.frame.setStyleSheet("background-color: rgb(0, 84, 139);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.lblRegistered = QtWidgets.QLabel(self.frame)
        self.lblRegistered.setGeometry(QtCore.QRect(49, 29, 171, 58))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.lblRegistered.setFont(font)
        self.lblRegistered.setStyleSheet("font: 16pt \"Century Gothic\";\n"
"color: rgb(255, 255, 255);")
        self.lblRegistered.setTextFormat(QtCore.Qt.RichText)
        self.lblRegistered.setAlignment(QtCore.Qt.AlignCenter)
        self.lblRegistered.setObjectName("lblRegistered")
        self.lblPlateNumber = QtWidgets.QLabel(self.frame)
        self.lblPlateNumber.setGeometry(QtCore.QRect(40, 89, 251, 58))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.lblPlateNumber.setFont(font)
        self.lblPlateNumber.setStyleSheet("font: 16pt \"Century Gothic\";\n"
"color: rgb(255, 255, 255);")
        self.lblPlateNumber.setTextFormat(QtCore.Qt.RichText)
        self.lblPlateNumber.setAlignment(QtCore.Qt.AlignCenter)
        self.lblPlateNumber.setObjectName("lblPlateNumber")
        self.lblRecognition = QtWidgets.QLabel(self.frame)
        self.lblRecognition.setGeometry(QtCore.QRect(37, 149, 221, 58))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.lblRecognition.setFont(font)
        self.lblRecognition.setStyleSheet("font: 16pt \"Century Gothic\";\n"
"color: rgb(255, 255, 255);")
        self.lblRecognition.setTextFormat(QtCore.Qt.RichText)
        self.lblRecognition.setAlignment(QtCore.Qt.AlignCenter)
        self.lblRecognition.setObjectName("lblRecognition")
        self.lblSystem = QtWidgets.QLabel(self.frame)
        self.lblSystem.setGeometry(QtCore.QRect(19, 204, 180, 58))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.lblSystem.setFont(font)
        self.lblSystem.setStyleSheet("font: 16pt \"Century Gothic\";\n"
"color: rgb(255, 255, 255);")
        self.lblSystem.setTextFormat(QtCore.Qt.RichText)
        self.lblSystem.setAlignment(QtCore.Qt.AlignCenter)
        self.lblSystem.setObjectName("lblSystem")
        self.searchButton = QtWidgets.QPushButton(self.frame)
        self.searchButton.setGeometry(QtCore.QRect(259, 400, 80, 30))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.searchButton.setFont(font)
        self.searchButton.setCursor(QtGui.QCursor(QtCore.Qt.BusyCursor))
        self.searchButton.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.searchButton.setObjectName("searchButton")
        self.searchButton.clicked.connect(self.search)
        self.searchEdit = QtWidgets.QLineEdit(self.frame)
        self.searchEdit.setGeometry(QtCore.QRect(32, 399, 220, 30))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.searchEdit.setFont(font)
        self.searchEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.searchEdit.setObjectName("searchEdit")
        self.FilterBox = QtWidgets.QComboBox(self.frame)
        self.FilterBox.setGeometry(QtCore.QRect(32, 365, 121, 30))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(9)
        self.FilterBox.setFont(font)
        self.FilterBox.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.FilterBox.setObjectName("FilterBox")
        self.FilterBox.addItem("")
        self.FilterBox.addItem("")
        self.FilterBox.addItem("")
        self.FilterBox.addItem("")
        self.FilterBox.addItem("")
        self.FilterBox.addItem("")
        self.FilterBox.addItem("")
        self.line = QtWidgets.QFrame(self.frame)
        self.line.setGeometry(QtCore.QRect(2, 268, 305, 16))
        self.line.setMinimumSize(QtCore.QSize(305, 16))
        self.line.setMaximumSize(QtCore.QSize(305, 16))
        self.line.setStyleSheet("color: rgb(255, 255, 255);")
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setLineWidth(9)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.lblInfo = QtWidgets.QLabel(self.frame)
        self.lblInfo.setGeometry(QtCore.QRect(93, 301, 181, 41))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.lblInfo.setFont(font)
        self.lblInfo.setStyleSheet("font: 16pt \"Century Gothic\";\n"
"color: rgb(255, 255, 255);")
        self.lblInfo.setLineWidth(1)
        self.lblInfo.setTextFormat(QtCore.Qt.RichText)
        self.lblInfo.setAlignment(QtCore.Qt.AlignCenter)
        self.lblInfo.setObjectName("lblInfo")
        userInformationWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(userInformationWindow)
        self.FilterBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(userInformationWindow)

    def retranslateUi(self, userInformationWindow):
        _translate = QtCore.QCoreApplication.translate
        userInformationWindow.setWindowTitle(_translate("userInformationWindow", "RPNRS - INFORMATIONS"))
        item = self.InformationtableWidget.horizontalHeaderItem(0)
        item.setText(_translate("userInformationWindow", "Owner ID"))
        item = self.InformationtableWidget.horizontalHeaderItem(1)
        item.setText(_translate("userInformationWindow", "Firstname"))
        item = self.InformationtableWidget.horizontalHeaderItem(2)
        item.setText(_translate("userInformationWindow", "Middlename"))
        item = self.InformationtableWidget.horizontalHeaderItem(3)
        item.setText(_translate("userInformationWindow", "Lastname"))
        item = self.InformationtableWidget.horizontalHeaderItem(4)
        item.setText(_translate("userInformationWindow", "Age"))
        item = self.InformationtableWidget.horizontalHeaderItem(5)
        item.setText(_translate("userInformationWindow", "Address"))
        item = self.InformationtableWidget.horizontalHeaderItem(6)
        item.setText(_translate("userInformationWindow", "Contact Number"))
        item = self.InformationtableWidget.horizontalHeaderItem(7)
        item.setText(_translate("userInformationWindow", "Email Address"))
        item = self.InformationtableWidget.horizontalHeaderItem(8)
        item.setText(_translate("userInformationWindow", "Profession"))
        item = self.InformationtableWidget.horizontalHeaderItem(9)
        item.setText(_translate("userInformationWindow", "Department"))
        item = self.InformationtableWidget.horizontalHeaderItem(10)
        item.setText(_translate("userInformationWindow", "Vehicle Color"))
        item = self.InformationtableWidget.horizontalHeaderItem(11)
        item.setText(_translate("userInformationWindow", "Vehicle Brand"))
        item = self.InformationtableWidget.horizontalHeaderItem(12)
        item.setText(_translate("userInformationWindow", "Vehicle Model"))
        item = self.InformationtableWidget.horizontalHeaderItem(13)
        item.setText(_translate("userInformationWindow", "Vehicle Type"))
        item = self.InformationtableWidget.horizontalHeaderItem(14)
        item.setText(_translate("userInformationWindow", "Plate Number"))
        item = self.InformationtableWidget.horizontalHeaderItem(15)
        item.setText(_translate("userInformationWindow", "Date Registered"))
        self.lblRegistered.setText(_translate("userInformationWindow", "<html><head/><body><p><span style=\" font-size:36pt; font-weight:600;\">R</span><span style=\" font-size:24pt;\">egistered</span></p></body></html>"))
        self.lblPlateNumber.setText(_translate("userInformationWindow", "<html><head/><body><p><span style=\" font-size:36pt; font-weight:600;\">P</span><span style=\" font-size:24pt;\">late </span><span style=\" font-size:36pt; font-weight:600;\">N</span><span style=\" font-size:24pt;\">umber</span></p></body></html>"))
        self.lblRecognition.setText(_translate("userInformationWindow", "<html><head/><body><p><span style=\" font-size:36pt; font-weight:600;\">R</span><span style=\" font-size:24pt;\">ecognition</span></p></body></html>"))
        self.lblSystem.setText(_translate("userInformationWindow", "<html><head/><body><p><span style=\" font-size:36pt; font-weight:600;\">S</span><span style=\" font-size:24pt;\">ystem</span></p></body></html>"))
        self.searchButton.setText(_translate("userInformationWindow", "Search"))
        self.FilterBox.setCurrentText(_translate("userInformationWindow", "ALL"))
        self.FilterBox.setItemText(0, _translate("userInformationWindow", "ALL"))
        self.FilterBox.setItemText(1, _translate("userInformationWindow", "DATE REGISTERED"))
        self.FilterBox.setItemText(2, _translate("userInformationWindow", "OWNER ID"))
        self.FilterBox.setItemText(3, _translate("userInformationWindow", "OWNER NAME"))
        self.FilterBox.setItemText(4, _translate("userInformationWindow", "PLATE NUMBER"))
        self.FilterBox.setItemText(5, _translate("userInformationWindow", "VEHICLE TYPE"))
        self.FilterBox.setItemText(6, _translate("userInformationWindow", "VEHICLE BRAND"))
        self.lblInfo.setText(_translate("userInformationWindow", "<html><head/><body><p><span style=\" font-weight:600;\">INFORMATIONS</span></p></body></html>"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    userInformationWindow = QtWidgets.QMainWindow()
    ui = Ui_userInformationWindow()
    ui.setupUi5(userInformationWindow)
    userInformationWindow.show()
    sys.exit(app.exec_())
