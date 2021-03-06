# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rpnrsRegistration.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import pymysql

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem

from PyQt5.QtGui import QPixmap

from rpnrsHome import *
from datetime import datetime

conn = pymysql.connect(host='localhost', user='root', password='', database='rpnrsdb')

class Ui_RegistrationWindow(object):
    def clik(self):
        row = self.tableWidget.currentRow()

        val = (self.tableWidget.item(row, 0).text())
        self.idnoEdit.setText(val)
        fname = (self.tableWidget.item(row, 1).text())
        self.firstnameEdit.setText(fname)
        mname = (self.tableWidget.item(row, 2).text())
        self.middlenameEdit.setText(mname)
        lname = (self.tableWidget.item(row, 3).text())
        self.lastnameEdit.setText(lname)
        age = (self.tableWidget.item(row, 4).text())
        self.ageBox.setValue(int(age))
        add = (self.tableWidget.item(row, 5).text())
        self.addressEdit.setText(add)
        contact = (self.tableWidget.item(row, 6).text())
        self.contactnoEdit.setText(contact)
        email = (self.tableWidget.item(row, 7).text())
        self.emailaddEdit.setText(email)
        prof = (self.tableWidget.item(row, 8).text())
        str(self.professionBox.setCurrentText(prof))
        dept = (self.tableWidget.item(row, 9).text())
        self.deptEdit.setText(dept)
        color = (self.tableWidget.item(row, 10).text())
        self.vColorEdit.setText(color)
        brand = (self.tableWidget.item(row, 11).text())
        str(self.vBrandBox.setCurrentText(brand))
        model = (self.tableWidget.item(row, 12).text())
        self.vModelBox.setText(model)
        vtype = (self.tableWidget.item(row, 13).text())
        str(self.vTypeBox.setCurrentText(vtype))
        plate = (self.tableWidget.item(row, 14).text())
        self.vPlateNumberEdit.setText(plate)

    def refresh(self):
        with conn.cursor() as cursor:
            cmd = "SELECT * from ownertbl INNER JOIN vehicletbl ON ownertbl.ownerId = vehicletbl.vehicleOwnerId ORDER BY ownerId"
            cursor.execute(cmd)
            data = cursor.fetchall()
            self.tableWidget.setRowCount(0)
            for row_number, row_data in enumerate(data):
                self.tableWidget.insertRow(row_number)
                for column_number, column_data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))
        conn.commit()
        self.deptEdit.clear()
        self.idnoEdit.clear()
        self.firstnameEdit.clear()
        self.middlenameEdit.clear()
        self.lastnameEdit.clear()
        self.addressEdit.clear()
        self.contactnoEdit.clear()
        self.emailaddEdit.clear()
        self.professionBox.setCurrentIndex(-1)
        self.vColorEdit.clear()
        self.vBrandBox.setCurrentIndex(-1)
        self.vModelBox.clear()
        self.vTypeBox.setCurrentIndex(-1)
        self.vPlateNumberEdit.clear()

    def save(self):
        idno = self.idnoEdit.text()
        vid = idno
        fname = self.firstnameEdit.text()
        mname = self.middlenameEdit.text()
        lname = self.lastnameEdit.text()
        age = self.ageBox.value();
        address = self.addressEdit.text()
        contact = self.contactnoEdit.text()
        email = self.emailaddEdit.text()
        prof = str(self.professionBox.currentText())
        dept = self.deptEdit.text()
        color = self.vColorEdit.text()
        brand = str(self.vBrandBox.currentText())
        model = self.vModelBox.text()
        vtype = str(self.vTypeBox.currentText())
        vnumber = self.vPlateNumberEdit.text()
        dte = datetime.today().strftime('%Y-%m-%d')

        if idno == "" or fname == "" or mname == "" or lname == "" or address == "" or contact == "" or email == "" or prof == "" or dept == "" or color == "" or brand == "" or model == "" or vtype == "" or vnumber == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Please complete information")
            msg.setWindowTitle("ALERT")
            msg.exec_()
            self.refresh()
        else:

            with conn.cursor() as cursor:
                cmd = "SELECT ownerId from ownertbl WHERE `ownerId`=%s"
                cursor.execute(cmd,(idno))
                data = cursor.fetchall()

                #if data == 0:
                sql = "INSERT INTO ownertbl(ownerId,`ownerFirstname`,`ownerMiddlename`,`ownerLastname`,`ownerAge`,`ownerAddress`,`ownerContact`,`ownerEmail`,`ownerProf`,`ownerDept`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                sql1 = "INSERT INTO vehicletbl (vehicleOwnerId,`vehicleColor`,`vehicleBrand`,`vehicleModel`,`vehicleType`,`vehicleId`,`dateReg`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                try:
                    cursor.execute(sql,(idno,fname,mname,lname,age,address,contact,email,prof,dept))
                    cursor.execute(sql1,(vid,color,brand,model,vtype,vnumber,dte))
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Saved Successfully!")
                    msg.setWindowTitle("RPNRS")
                    msg.exec_()
                    self.refresh()
                except:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Error.")
                    msg.setWindowTitle("ALERT")
                    msg.exec_()
                    self.refresh()
                #else:    
                #        msg = QMessageBox()
                #        msg.setIcon(QMessageBox.Critical)
                #        msg.setText("ID Number Already Exist.")
                #        msg.setWindowTitle("ALERT")
                #        msg.exec_()
                #        self.refresh()
                    
                conn.commit()

    def update(self):

        idno = self.idnoEdit.text()
        vid = idno
        fname = self.firstnameEdit.text()
        mname = self.middlenameEdit.text()
        lname = self.lastnameEdit.text()
        age = self.ageBox.value();
        address = self.addressEdit.text()
        contact = self.contactnoEdit.text()
        email = self.emailaddEdit.text()
        prof = str(self.professionBox.currentText())
        dept = self.deptEdit.text()
        color = self.vColorEdit.text()
        brand = str(self.vBrandBox.currentText())
        model = self.vModelBox.text()
        vtype = str(self.vTypeBox.currentText())
        vnumber = self.vPlateNumberEdit.text()

        if idno == "" or fname == "" or mname == "" or lname == "" or address == "" or contact == "" or email == "" or prof == "" or dept == "" or color == "" or brand == "" or model == "" or vtype == "" or vnumber == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Please complete information")
            msg.setWindowTitle("ALERT")
            msg.exec_()
            self.refresh()
        else:
            with conn.cursor() as cursor:
                sql = "UPDATE ownertbl SET `ownerFirstname`=%s,`ownerMiddlename`=%s,`ownerLastname`=%s,`ownerAge`=%s,`ownerAddress`=%s,`ownerContact`=%s,`ownerEmail`=%s,`ownerProf`=%s,`ownerDept`=%s WHERE `ownerId` = %s"
                sql1 = "UPDATE vehicletbl SET `vehicleColor`=%s,`vehicleBrand`=%s,`vehicleModel`=%s,`vehicleType`=%s,`vehicleId`=%s WHERE `vehicleOwnerId`= %s"
                try:
                    cursor.execute(sql,(fname,mname,lname,age,address,contact,email,prof,dept,idno))
                    cursor.execute(sql1,(color,brand,model,vtype,vnumber,vid))
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Updated Successfully!")
                    msg.setWindowTitle("RPNRS")
                    msg.exec_()
                    self.refresh()
                except:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Error.")
                    msg.setWindowTitle("ALERT")
                    msg.exec_()
                    self.refresh()

            conn.commit()

    def delete(self):

        idno = self.idnoEdit.text()
        vid = idno

        with conn.cursor() as cursor:
            cmd = "SELECT ownerId from ownertbl WHERE `ownerId`=%s"
            cursor.execute(cmd,(idno))
            data = cursor.fetchall()

            if data == None:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error.")
                msg.setWindowTitle("ALERT")
                msg.exec_()
                self.refresh()
            else:
                sql = "DELETE FROM ownertbl WHERE `ownerId` = %s"
                sql1 = "DELETE FROM vehicletbl WHERE `vehicleOwnerId` = %s"
                try:
                    cursor.execute(sql,(idno))
                    cursor.execute(sql1,(vid))
                    if idno == "":
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Critical)
                        msg.setText("Error.")
                        msg.setWindowTitle("ALERT")
                        msg.exec_()
                        self.refresh()
                    else:
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Information)
                        msg.setText("Deleted Successfully!")
                        msg.setWindowTitle("RPNRS")
                        msg.exec_()
                        self.refresh()
                except:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Error.")
                    msg.setWindowTitle("ALERT")
                    msg.exec_()
                    self.refresh()

        conn.commit()
    def search(self):
        srch = self.searchEdit.text()

        with conn.cursor() as cursor:
            sql = "SELECT * from ownertbl INNER JOIN vehicletbl ON ownertbl.ownerId = vehicletbl.vehicleOwnerId WHERE ownerId = %s"
            try:
                cursor.execute(sql,(srch))
                result = cursor.fetchall()
                self.tableWidget.setRowCount(0)
                for row_number, row_data in enumerate(result):
                    self.tableWidget.insertRow(row_number)
                    for column_number, column_data in enumerate(row_data):
                        self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))

 
            except:
                print("Oops! Something wrong")

        conn.commit()
    def setupUi7(self, RegistrationWindow):
        RegistrationWindow.setObjectName("RegistrationWindow")
        RegistrationWindow.resize(1222, 650)
        RegistrationWindow.setMinimumSize(QtCore.QSize(1222, 650))
        RegistrationWindow.setMaximumSize(QtCore.QSize(1222, 650))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        RegistrationWindow.setFont(font)
        RegistrationWindow.setStyleSheet("background-color: rgb(0, 84, 139);")
        self.centralwidget = QtWidgets.QWidget(RegistrationWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.firstnameLabel = QtWidgets.QLabel(self.centralwidget)
        self.firstnameLabel.setGeometry(QtCore.QRect(485, 110, 101, 16))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.firstnameLabel.setFont(font)
        self.firstnameLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.firstnameLabel.setObjectName("firstnameLabel")
        self.middlenameLabel = QtWidgets.QLabel(self.centralwidget)
        self.middlenameLabel.setGeometry(QtCore.QRect(485, 137, 101, 16))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.middlenameLabel.setFont(font)
        self.middlenameLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.middlenameLabel.setObjectName("middlenameLabel")
        self.lastnameLabel = QtWidgets.QLabel(self.centralwidget)
        self.lastnameLabel.setGeometry(QtCore.QRect(485, 164, 101, 16))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.lastnameLabel.setFont(font)
        self.lastnameLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.lastnameLabel.setObjectName("lastnameLabel")
        self.ageLabel = QtWidgets.QLabel(self.centralwidget)
        self.ageLabel.setGeometry(QtCore.QRect(484, 191, 101, 16))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.ageLabel.setFont(font)
        self.ageLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.ageLabel.setObjectName("ageLabel")
        self.vColorLabel = QtWidgets.QLabel(self.centralwidget)
        self.vColorLabel.setGeometry(QtCore.QRect(836, 31, 111, 16))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.vColorLabel.setFont(font)
        self.vColorLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.vColorLabel.setObjectName("vColorLabel")
        self.vBrandLabel = QtWidgets.QLabel(self.centralwidget)
        self.vBrandLabel.setGeometry(QtCore.QRect(836, 60, 111, 16))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.vBrandLabel.setFont(font)
        self.vBrandLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.vBrandLabel.setObjectName("vBrandLabel")
        self.vTypeLabel = QtWidgets.QLabel(self.centralwidget)
        self.vTypeLabel.setGeometry(QtCore.QRect(836, 120, 111, 16))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.vTypeLabel.setFont(font)
        self.vTypeLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.vTypeLabel.setObjectName("vTypeLabel")
        self.vPlateNumberLabel = QtWidgets.QLabel(self.centralwidget)
        self.vPlateNumberLabel.setGeometry(QtCore.QRect(836, 148, 151, 16))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.vPlateNumberLabel.setFont(font)
        self.vPlateNumberLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.vPlateNumberLabel.setObjectName("vPlateNumberLabel")
        self.firstnameEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.firstnameEdit.setGeometry(QtCore.QRect(590, 110, 215, 20))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.firstnameEdit.setFont(font)
        self.firstnameEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.firstnameEdit.setObjectName("firstnameEdit")
        self.middlenameEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.middlenameEdit.setGeometry(QtCore.QRect(590, 136, 215, 20))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.middlenameEdit.setFont(font)
        self.middlenameEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.middlenameEdit.setObjectName("middlenameEdit")
        self.lastnameEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lastnameEdit.setGeometry(QtCore.QRect(590, 162, 215, 20))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.lastnameEdit.setFont(font)
        self.lastnameEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.lastnameEdit.setObjectName("lastnameEdit")
        self.ageBox = QtWidgets.QSpinBox(self.centralwidget)
        self.ageBox.setGeometry(QtCore.QRect(590, 188, 51, 22))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.ageBox.setFont(font)
        self.ageBox.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);\n"
"")
        self.ageBox.setMinimum(18)
        self.ageBox.setObjectName("ageBox")
        self.vColorEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.vColorEdit.setGeometry(QtCore.QRect(990, 31, 215, 20))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.vColorEdit.setFont(font)
        self.vColorEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.vColorEdit.setObjectName("vColorEdit")
        self.vBrandBox = QtWidgets.QComboBox(self.centralwidget)
        self.vBrandBox.setGeometry(QtCore.QRect(990, 58, 215, 22))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.vBrandBox.setFont(font)
        self.vBrandBox.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.vBrandBox.setObjectName("vBrandBox")
        self.vBrandBox.addItem("")
        self.vBrandBox.addItem("")
        self.vBrandBox.addItem("")
        self.vBrandBox.addItem("")
        self.vBrandBox.addItem("")
        self.vTypeBox = QtWidgets.QComboBox(self.centralwidget)
        self.vTypeBox.setGeometry(QtCore.QRect(990, 118, 215, 22))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.vTypeBox.setFont(font)
        self.vTypeBox.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.vTypeBox.setObjectName("vTypeBox")
        self.vTypeBox.addItem("")
        self.vTypeBox.addItem("")
        self.vPlateNumberEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.vPlateNumberEdit.setGeometry(QtCore.QRect(990, 148, 215, 20))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.vPlateNumberEdit.setFont(font)
        self.vPlateNumberEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.vPlateNumberEdit.setObjectName("vPlateNumberEdit")
        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveButton.setGeometry(QtCore.QRect(834, 218, 90, 23))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.saveButton.setFont(font)
        self.saveButton.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.saveButton.setObjectName("saveButton")
        self.saveButton.clicked.connect(self.save)
        self.updateButton = QtWidgets.QPushButton(self.centralwidget)
        self.updateButton.setGeometry(QtCore.QRect(928, 218, 90, 23))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.updateButton.setFont(font)
        self.updateButton.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.updateButton.setObjectName("updateButton")
        self.updateButton.clicked.connect(self.update)
        self.deleteButton = QtWidgets.QPushButton(self.centralwidget)
        self.deleteButton.setGeometry(QtCore.QRect(1022, 218, 90, 23))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.deleteButton.setFont(font)
        self.deleteButton.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.deleteButton.setObjectName("deleteButton")
        self.deleteButton.clicked.connect(self.delete)
        self.searchEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.searchEdit.setGeometry(QtCore.QRect(832, 260, 280, 21))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.searchEdit.setFont(font)
        self.searchEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.searchEdit.setObjectName("searchEdit")
        self.searchButton = QtWidgets.QPushButton(self.centralwidget)
        self.searchButton.setGeometry(QtCore.QRect(1116, 259, 90, 23))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.searchButton.setFont(font)
        self.searchButton.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.searchButton.setObjectName("searchButton")
        self.searchButton.clicked.connect(self.search)
        self.addressEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.addressEdit.setGeometry(QtCore.QRect(589, 215, 215, 51))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.addressEdit.setFont(font)
        self.addressEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.addressEdit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.addressEdit.setObjectName("addressEdit")
        self.addressLabel = QtWidgets.QLabel(self.centralwidget)
        self.addressLabel.setGeometry(QtCore.QRect(484, 215, 101, 16))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.addressLabel.setFont(font)
        self.addressLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.addressLabel.setObjectName("addressLabel")
        self.contactnoEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.contactnoEdit.setGeometry(QtCore.QRect(589, 271, 215, 20))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.contactnoEdit.setFont(font)
        self.contactnoEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.contactnoEdit.setObjectName("contactnoEdit")
        self.contactLabel = QtWidgets.QLabel(self.centralwidget)
        self.contactLabel.setGeometry(QtCore.QRect(482, 273, 101, 16))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.contactLabel.setFont(font)
        self.contactLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.contactLabel.setObjectName("contactLabel")
        self.vModelLabel = QtWidgets.QLabel(self.centralwidget)
        self.vModelLabel.setGeometry(QtCore.QRect(836, 90, 111, 16))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.vModelLabel.setFont(font)
        self.vModelLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.vModelLabel.setObjectName("vModelLabel")
        self.emailLabel = QtWidgets.QLabel(self.centralwidget)
        self.emailLabel.setGeometry(QtCore.QRect(483, 301, 101, 16))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.emailLabel.setFont(font)
        self.emailLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.emailLabel.setObjectName("emailLabel")
        self.emailaddEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.emailaddEdit.setGeometry(QtCore.QRect(589, 299, 215, 20))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.emailaddEdit.setFont(font)
        self.emailaddEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.emailaddEdit.setObjectName("emailaddEdit")
        self.professionBox = QtWidgets.QComboBox(self.centralwidget)
        self.professionBox.setGeometry(QtCore.QRect(590, 30, 215, 22))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.professionBox.setFont(font)
        self.professionBox.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.professionBox.setObjectName("professionBox")
        self.professionBox.addItem("")
        self.professionBox.addItem("")
        self.professionLbl = QtWidgets.QLabel(self.centralwidget)
        self.professionLbl.setGeometry(QtCore.QRect(485, 32, 101, 16))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.professionLbl.setFont(font)
        self.professionLbl.setStyleSheet("color: rgb(255, 255, 255);")
        self.professionLbl.setObjectName("professionLbl")
        self.idnoEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.idnoEdit.setGeometry(QtCore.QRect(590, 84, 215, 20))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.idnoEdit.setFont(font)
        self.idnoEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.idnoEdit.setObjectName("idnoEdit")
        self.label_15 = QtWidgets.QLabel(self.centralwidget)
        self.label_15.setGeometry(QtCore.QRect(485, 84, 101, 16))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.label_15.setFont(font)
        self.label_15.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_15.setObjectName("label_15")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(9, 341, 1201, 300))
        self.tableWidget.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.tableWidget.setRowCount(100)
        self.tableWidget.setColumnCount(14)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.doubleClicked.connect(self.clik)
        self.refreshButton = QtWidgets.QPushButton(self.centralwidget)
        self.refreshButton.setGeometry(QtCore.QRect(1116, 218, 90, 23))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.refreshButton.setFont(font)
        self.refreshButton.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.refreshButton.setObjectName("refreshButton")
        self.refreshButton.clicked.connect(self.refresh)
        self.deptEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.deptEdit.setGeometry(QtCore.QRect(590, 58, 215, 20))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.deptEdit.setFont(font)
        self.deptEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.deptEdit.setObjectName("deptEdit")
        self.label_16 = QtWidgets.QLabel(self.centralwidget)
        self.label_16.setGeometry(QtCore.QRect(485, 58, 101, 16))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.label_16.setFont(font)
        self.label_16.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_16.setObjectName("label_16")
        self.vModelBox = QtWidgets.QLineEdit(self.centralwidget)
        self.vModelBox.setGeometry(QtCore.QRect(990, 90, 215, 20))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.vModelBox.setFont(font)
        self.vModelBox.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.vModelBox.setObjectName("vModelBox")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(10, 10, 451, 321))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(20)
        self.frame.setFont(font)
        self.frame.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.lblRegistered = QtWidgets.QLabel(self.frame)
        self.lblRegistered.setGeometry(QtCore.QRect(27, 39, 171, 58))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.lblRegistered.setFont(font)
        self.lblRegistered.setStyleSheet("font: 16pt \"Century Gothic\";\n"
"color: rgb(0, 84, 139);")
        self.lblRegistered.setTextFormat(QtCore.Qt.RichText)
        self.lblRegistered.setAlignment(QtCore.Qt.AlignCenter)
        self.lblRegistered.setObjectName("lblRegistered")
        self.lblPlateNumber = QtWidgets.QLabel(self.frame)
        self.lblPlateNumber.setGeometry(QtCore.QRect(200, 39, 251, 58))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.lblPlateNumber.setFont(font)
        self.lblPlateNumber.setStyleSheet("font: 16pt \"Century Gothic\";\n"
"color: rgb(0, 84, 139);")
        self.lblPlateNumber.setTextFormat(QtCore.Qt.RichText)
        self.lblPlateNumber.setAlignment(QtCore.Qt.AlignCenter)
        self.lblPlateNumber.setObjectName("lblPlateNumber")
        self.lblRecognition = QtWidgets.QLabel(self.frame)
        self.lblRecognition.setGeometry(QtCore.QRect(51, 121, 211, 60))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.lblRecognition.setFont(font)
        self.lblRecognition.setStyleSheet("font: 16pt \"Century Gothic\";\n"
"color: rgb(0, 84, 139);")
        self.lblRecognition.setTextFormat(QtCore.Qt.RichText)
        self.lblRecognition.setAlignment(QtCore.Qt.AlignCenter)
        self.lblRecognition.setObjectName("lblRecognition")
        self.lblSystem = QtWidgets.QLabel(self.frame)
        self.lblSystem.setGeometry(QtCore.QRect(261, 121, 131, 60))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.lblSystem.setFont(font)
        self.lblSystem.setStyleSheet("font: 16pt \"Century Gothic\";\n"
"color: rgb(0, 84, 139);")
        self.lblSystem.setTextFormat(QtCore.Qt.RichText)
        self.lblSystem.setAlignment(QtCore.Qt.AlignCenter)
        self.lblSystem.setObjectName("lblSystem")
        self.line = QtWidgets.QFrame(self.frame)
        self.line.setGeometry(QtCore.QRect(56, 201, 330, 16))
        self.line.setMinimumSize(QtCore.QSize(330, 16))
        self.line.setMaximumSize(QtCore.QSize(330, 16))
        self.line.setStyleSheet("font: 16pt \"Century Gothic\";\n"
"color: rgb(0, 84, 139);")
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setLineWidth(10)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.lblInfo = QtWidgets.QLabel(self.frame)
        self.lblInfo.setGeometry(QtCore.QRect(138, 253, 181, 30))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.lblInfo.setFont(font)
        self.lblInfo.setStyleSheet("font: 16pt \"Century Gothic\";\n"
"color: rgb(0, 84, 139);")
        self.lblInfo.setLineWidth(1)
        self.lblInfo.setTextFormat(QtCore.Qt.RichText)
        self.lblInfo.setAlignment(QtCore.Qt.AlignCenter)
        self.lblInfo.setObjectName("lblInfo")
        self.lblRegistered.raise_()
        self.lblPlateNumber.raise_()
        self.lblSystem.raise_()
        self.line.raise_()
        self.lblInfo.raise_()
        self.lblRecognition.raise_()
        self.frame.raise_()
        self.firstnameLabel.raise_()
        self.middlenameLabel.raise_()
        self.lastnameLabel.raise_()
        self.ageLabel.raise_()
        self.vColorLabel.raise_()
        self.vBrandLabel.raise_()
        self.vTypeLabel.raise_()
        self.vPlateNumberLabel.raise_()
        self.saveButton.raise_()
        self.updateButton.raise_()
        self.deleteButton.raise_()
        self.searchEdit.raise_()
        self.searchButton.raise_()
        self.addressLabel.raise_()
        self.contactLabel.raise_()
        self.vModelLabel.raise_()
        self.emailLabel.raise_()
        self.professionLbl.raise_()
        self.label_15.raise_()
        self.tableWidget.raise_()
        self.refreshButton.raise_()
        self.label_16.raise_()
        self.vColorEdit.raise_()
        self.vBrandBox.raise_()
        self.vModelBox.raise_()
        self.ageBox.raise_()
        self.lastnameEdit.raise_()
        self.middlenameEdit.raise_()
        self.firstnameEdit.raise_()
        self.vPlateNumberEdit.raise_()
        self.vTypeBox.raise_()
        self.addressEdit.raise_()
        self.idnoEdit.raise_()
        self.emailaddEdit.raise_()
        self.deptEdit.raise_()
        self.contactnoEdit.raise_()
        self.professionBox.raise_()
        RegistrationWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(RegistrationWindow)
        self.vBrandBox.setCurrentIndex(-1)
        self.vTypeBox.setCurrentIndex(-1)
        self.professionBox.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(RegistrationWindow)

    def retranslateUi(self, RegistrationWindow):
        _translate = QtCore.QCoreApplication.translate
        RegistrationWindow.setWindowTitle(_translate("RegistrationWindow", "RPNRS - REGISTRATION"))
        self.firstnameLabel.setText(_translate("RegistrationWindow", "First Name:"))
        self.middlenameLabel.setText(_translate("RegistrationWindow", "Middle Name:"))
        self.lastnameLabel.setText(_translate("RegistrationWindow", "Last Name:"))
        self.ageLabel.setText(_translate("RegistrationWindow", "Age:"))
        self.vColorLabel.setText(_translate("RegistrationWindow", "Vehicle Color:"))
        self.vBrandLabel.setText(_translate("RegistrationWindow", "Vehicle Brand:"))
        self.vTypeLabel.setText(_translate("RegistrationWindow", "Vehicle Type:"))
        self.vPlateNumberLabel.setText(_translate("RegistrationWindow", "Vehicle Plate Number:"))
        self.vBrandBox.setItemText(0, _translate("RegistrationWindow", "Honda"))
        self.vBrandBox.setItemText(1, _translate("RegistrationWindow", "Isuzu"))
        self.vBrandBox.setItemText(2, _translate("RegistrationWindow", "Suzuki"))
        self.vBrandBox.setItemText(3, _translate("RegistrationWindow", "Mitsubishi"))
        self.vBrandBox.setItemText(4, _translate("RegistrationWindow", "Toyota"))
        self.vTypeBox.setItemText(0, _translate("RegistrationWindow", "Motorcycle"))
        self.vTypeBox.setItemText(1, _translate("RegistrationWindow", "4-Wheeled"))
        self.saveButton.setText(_translate("RegistrationWindow", "SAVE"))
        self.updateButton.setText(_translate("RegistrationWindow", "UPDATE"))
        self.deleteButton.setText(_translate("RegistrationWindow", "DELETE"))
        self.searchButton.setText(_translate("RegistrationWindow", "SEARCH"))
        self.addressLabel.setText(_translate("RegistrationWindow", "Address:"))
        self.contactLabel.setText(_translate("RegistrationWindow", "Contact No.:"))
        self.vModelLabel.setText(_translate("RegistrationWindow", "Vehicle Model:"))
        self.emailLabel.setText(_translate("RegistrationWindow", "E-mail Address:"))
        self.professionBox.setItemText(0, _translate("RegistrationWindow", "Faculty Member"))
        self.professionBox.setItemText(1, _translate("RegistrationWindow", "Student"))
        self.professionLbl.setText(_translate("RegistrationWindow", "Profession:"))
        self.label_15.setText(_translate("RegistrationWindow", "Student No.:"))
        self.refreshButton.setText(_translate("RegistrationWindow", "REFRESH"))
        self.label_16.setText(_translate("RegistrationWindow", "Department:"))
        self.lblRegistered.setText(_translate("RegistrationWindow", "<html><head/><body><p><span style=\" font-size:36pt; font-weight:600;\">R</span><span style=\" font-size:24pt;\">egistered</span></p></body></html>"))
        self.lblPlateNumber.setText(_translate("RegistrationWindow", "<html><head/><body><p><span style=\" font-size:36pt; font-weight:600;\">P</span><span style=\" font-size:24pt;\">late </span><span style=\" font-size:36pt; font-weight:600;\">N</span><span style=\" font-size:24pt;\">umber</span></p></body></html>"))
        self.lblRecognition.setText(_translate("RegistrationWindow", "<html><head/><body><p><span style=\" font-size:36pt; font-weight:600;\">R</span><span style=\" font-size:24pt;\">ecognition</span></p></body></html>"))
        self.lblSystem.setText(_translate("RegistrationWindow", "<html><head/><body><p><span style=\" font-size:36pt; font-weight:600;\">S</span><span style=\" font-size:24pt;\">ystem</span></p></body></html>"))
        self.lblInfo.setText(_translate("RegistrationWindow", "<html><head/><body><p><span style=\" font-weight:600;\">REGISTRATION</span></p></body></html>"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    RegistrationWindow = QtWidgets.QMainWindow()
    ui = Ui_RegistrationWindow()
    ui.setupUi7(RegistrationWindow)
    RegistrationWindow.show()
    sys.exit(app.exec_())
