# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rpnrsMonitoring.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

import numpy as np
import pytesseract
import pymysql
from PIL import Image

import qimage2ndarray
import cv2
import imutils
import sys
import pandas as pd
import time
from datetime import datetime

conn = pymysql.connect(host='localhost', user='root', password='', database='rpnrsdb')
class Ui_MainWindowMonitor(object):
    def process(self):
        self.displayImage = cv2.imread('capturedImage.jpg')
        #self.displayImage = cv2.imread('car1.jpg')

        displayImage1 = qimage2ndarray.array2qimage(self.displayImage)
        #cv2.imshow("todisplay", self.displayImage)
        self.cameraView.setPixmap(QtGui.QPixmap(displayImage1))

        display_image = imutils.resize(self.displayImage, width=640)

        gray = cv2.cvtColor(display_image, cv2.COLOR_BGR2GRAY)

        # Threshold after color conversion
        # new_gray = cv2.bilateralFilter(gray, 11, 17, 17)
        # ret, thresh = cv2.threshold(new_gray, 127, 255, cv2.THRESH_BINARY_INV)
        # cv2.imshow("thresh", thresh)
        # REMOVE AFTER TESTING

        gray1 = cv2.bilateralFilter(gray, 11, 17, 17)
        edged = cv2.Canny(gray1, 170, 200)
        (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:30]
        NumberPlateCnt = None
        #cv2.imshow("edge", edged)

        count = 0
        for c in cnts:
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.02 * peri, True)
                if len(approx) == 4 or len(approx) == 6:  
                    NumberPlateCnt = approx 
                    break


        new = cv2.drawContours(display_image,[NumberPlateCnt],0,(0,255,0),3)
        #new = cv2.drawContours(edged,[NumberPlateCnt],0,(0,255,0),3)
        #cv2.imshow("5 - Contoured Image", new)

        #new = cv2.cvtColor(new, cv2.COLOR_BGR2RGB)
        #displayImage1 = qimage2ndarray.array2qimage(new)
        #cv2.imshow("todisplay", self.displayImage)
        #self.cameraView.setPixmap(QtGui.QPixmap(displayImage1))

        # Masking the part other than the number plate
        mask = np.zeros(gray.shape,np.uint8)
        new_image = cv2.drawContours(mask,[NumberPlateCnt],-1,255,-1)
        #cv2.imshow("6 - Masked Image", new_image)

        out = np.zeros(gray.shape,np.uint8)
        out[mask == 255] = gray[mask == 255]

        (x, y) = np.where(mask == 255)
        (topx, topy) = (np.min(x), np.min(y))
        (bottomx, bottomy) = (np.max(x), np.max(y))
        out = out[topx:bottomx+1, topy:bottomy+1]
        #cv2.imshow('output', out)

        #new_image = cv2.bitwise_and(display_image,display_image,mask=mask)
        #cv2.namedWindow("Final_image",cv2.WINDOW_NORMAL)
        #cv2.imshow("Final_image",new_image)

        #new_gray = cv2.cvtColor(out, cv2.COLOR_BGR2GRAY)
        #new_gray = cv2.bilateralFilter(new_image, 11, 17, 17)
        #ret, thresh = cv2.threshold(new_gray, 127, 255, cv2.THRESH_BINARY_INV)
        #cv2.imshow("thresh", thresh)

        # Configuration for tesseract
        config = ('-l eng --oem 1 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 --psm 10')

        # Run tesseract OCR on image
        text = pytesseract.image_to_string(out, config=config)
        print('Plate number detected: %s' % text)

        self.plateTextbox.setText(text)

        if text == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("NO PLATE NUMBER DETECTED!")
            msg.setWindowTitle("ALERT")
            msg.exec_()

    def captureImage(self):
        sImage = cv2.cvtColor(self.frame1, cv2.COLOR_BGR2RGB)
        sImage = cv2.cvtColor(sImage, cv2.COLOR_BGR2RGB)
        cv2.imwrite("capturedImage.jpg", sImage)
        
        self.timer.stop()
        self.capture.release()
        self.process()

    def display_video_stream(self):
        """Read frame from camera and repaint QLabel widget.
        """
        _, self.frame = self.capture.read()
        self.frame1 = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        #self.frame2 = cv2.flip(self.frame1, 1)
        self.image = qimage2ndarray.array2qimage(self.frame1)  #SOLUTION FOR MEMORY LEAK
        self.cameraView.setPixmap(QtGui.QPixmap(self.image))

    def setup_camera(self):
        """Initialize camera.
        """

        self.plateTextbox.clear()
        self.ownerTextbox.clear()
        self.dateRegisteredBox.clear()
        video_size = QtCore.QSize(640, 480)

        self.capture = cv2.VideoCapture(1)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, video_size.width())
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, video_size.height())

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.display_video_stream)
        self.timer.start(10)

    def check(self):
        plate = self.plateTextbox.text()

        with conn.cursor() as cursor:
            sql = "SELECT ownerId,ownerFirstname,vehicleType,dateReg,vehicleId FROM ownertbl INNER JOIN vehicletbl ON ownertbl.ownerId = vehicletbl.vehicleOwnerId WHERE vehicleId LIKE %s"
            cursor.execute(sql,("%" + plate + "%"))
            data = cursor.fetchone()

            if data == None:
                self.ownerTextbox.setText("Guest")
                self.dateRegisteredBox.setText("UNREGISTERED")

            else:
                self.plateTextbox.setText(data[4])
                self.ownerTextbox.setText(data[1])
                self.dateRegisteredBox.setText(data[3])
        conn.commit()

    def reportSave(self):
        dte = datetime.today().strftime('%Y-%m-%d')
        tme = datetime.today().strftime('%H:%M')
        plate = self.plateTextbox.text()

        with conn.cursor() as cursor:
            sql = "SELECT ownerId,ownerFirstname,vehicleType,dateReg,vehicleId FROM ownertbl INNER JOIN vehicletbl ON ownertbl.ownerId = vehicletbl.vehicleOwnerId WHERE vehicleId LIKE %s"
            cursor.execute(sql,("%" + plate + "%"))
            data = cursor.fetchone()
            
            if data == None:
                sql1 = "INSERT INTO reporttbl (`reportOwnerId`,`reportOwnerName`,`reportVehicleType`,`reportVehicleId`,`reportVehicleDate`,`reportVehicleTime`,`reportStatus`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql1,("0","UNREGISTERED","UNREGISTERED",plate,dte,tme,"UNREGISTERED"))
                print("Plate Number is not registered.")
                self.notif()

            else:
                value = data[0]
                name = data[1]
                vtype = data[2]
                print("registered")
                sql1 = "INSERT INTO reporttbl (`reportOwnerId`,`reportOwnerName`,`reportVehicleType`,`reportVehicleId`,`reportVehicleDate`,`reportVehicleTime`,`reportStatus`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql1,(value,name,vtype,plate,dte,tme,"REGISTERED"))
                self.notif()

        conn.commit()

    def notif(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Success")
        msg.setWindowTitle("RPNRS")
        msg.exec_()

    def setupUi4(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1131, 412)
        MainWindow.setMinimumSize(QtCore.QSize(1131, 412))
        MainWindow.setMaximumSize(QtCore.QSize(1131, 412))
        MainWindow.setStyleSheet("background-color: rgb(0, 84, 139);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.cameraView = QtWidgets.QLabel(self.centralwidget)
        self.cameraView.setGeometry(QtCore.QRect(480, 10, 640, 361))
        self.cameraView.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.cameraView.setText("")
        self.cameraView.setObjectName("cameraView")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 481, 411))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(20)
        self.frame.setFont(font)
        self.frame.setStyleSheet("background-color: rgb(0, 84, 139);")
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
"color: rgb(255, 255, 255);")
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
"color: rgb(255, 255, 255);")
        self.lblPlateNumber.setTextFormat(QtCore.Qt.RichText)
        self.lblPlateNumber.setAlignment(QtCore.Qt.AlignCenter)
        self.lblPlateNumber.setObjectName("lblPlateNumber")
        self.lblRecognition = QtWidgets.QLabel(self.frame)
        self.lblRecognition.setGeometry(QtCore.QRect(51, 93, 211, 60))
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
        self.lblSystem.setGeometry(QtCore.QRect(261, 93, 131, 60))
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
        self.line = QtWidgets.QFrame(self.frame)
        self.line.setGeometry(QtCore.QRect(0, 192, 330, 16))
        self.line.setMinimumSize(QtCore.QSize(330, 16))
        self.line.setMaximumSize(QtCore.QSize(330, 16))
        self.line.setStyleSheet("color: rgb(255, 255, 255);")
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setLineWidth(10)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.lblInfo = QtWidgets.QLabel(self.frame)
        self.lblInfo.setGeometry(QtCore.QRect(140, 220, 181, 41))
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
        self.entanceCaptureBtn = QtWidgets.QPushButton(self.frame)
        self.entanceCaptureBtn.setGeometry(QtCore.QRect(15, 321, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.entanceCaptureBtn.setFont(font)
        self.entanceCaptureBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.entanceCaptureBtn.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.entanceCaptureBtn.setObjectName("entanceCaptureBtn")
        self.entanceCaptureBtn.clicked.connect(self.captureImage)
        self.startCamBtn = QtWidgets.QPushButton(self.frame)
        self.startCamBtn.setGeometry(QtCore.QRect(15, 281, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.startCamBtn.setFont(font)
        self.startCamBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.startCamBtn.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.startCamBtn.setObjectName("startCamBtn")
        self.startCamBtn.clicked.connect(self.setup_camera)
        self.dateRegisteredBox = QtWidgets.QLineEdit(self.frame)
        self.dateRegisteredBox.setGeometry(QtCore.QRect(280, 335, 180, 26))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.dateRegisteredBox.setFont(font)
        self.dateRegisteredBox.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.dateRegisteredBox.setObjectName("dateRegisteredBox")
        self.dateRegisteredLBl = QtWidgets.QLabel(self.frame)
        self.dateRegisteredLBl.setGeometry(QtCore.QRect(170, 338, 131, 21))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.dateRegisteredLBl.setFont(font)
        self.dateRegisteredLBl.setStyleSheet("color: rgb(255, 255, 255);")
        self.dateRegisteredLBl.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.dateRegisteredLBl.setObjectName("dateRegisteredLBl")
        self.plateNumLbl = QtWidgets.QLabel(self.frame)
        self.plateNumLbl.setGeometry(QtCore.QRect(170, 278, 130, 21))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.plateNumLbl.setFont(font)
        self.plateNumLbl.setStyleSheet("color: rgb(255, 255, 255);")
        self.plateNumLbl.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.plateNumLbl.setObjectName("plateNumLbl")
        self.vehicleOwnerLbl = QtWidgets.QLabel(self.frame)
        self.vehicleOwnerLbl.setGeometry(QtCore.QRect(170, 308, 130, 21))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.vehicleOwnerLbl.setFont(font)
        self.vehicleOwnerLbl.setStyleSheet("color: rgb(255, 255, 255);")
        self.vehicleOwnerLbl.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.vehicleOwnerLbl.setObjectName("vehicleOwnerLbl")
        self.ownerTextbox = QtWidgets.QLineEdit(self.frame)
        self.ownerTextbox.setGeometry(QtCore.QRect(280, 305, 180, 26))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.ownerTextbox.setFont(font)
        self.ownerTextbox.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.ownerTextbox.setObjectName("ownerTextbox")
        self.plateTextbox = QtWidgets.QLineEdit(self.frame)
        self.plateTextbox.setGeometry(QtCore.QRect(280, 275, 180, 26))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.plateTextbox.setFont(font)
        self.plateTextbox.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.plateTextbox.setObjectName("plateTextbox")
        self.checkPlateBtn = QtWidgets.QPushButton(self.frame)
        self.checkPlateBtn.setGeometry(QtCore.QRect(190, 370, 141, 31))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        self.checkPlateBtn.setFont(font)
        self.checkPlateBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.checkPlateBtn.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.checkPlateBtn.setObjectName("checkPlateBtn")
        self.checkPlateBtn.clicked.connect(self.check)
        self.saveReportBtn = QtWidgets.QPushButton(self.frame)
        self.saveReportBtn.setGeometry(QtCore.QRect(340, 370, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        self.saveReportBtn.setFont(font)
        self.saveReportBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.saveReportBtn.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.saveReportBtn.setObjectName("saveReportBtn")
        self.saveReportBtn.clicked.connect(self.reportSave)
        self.lblInfo.raise_()
        self.lblRegistered.raise_()
        self.lblPlateNumber.raise_()
        self.lblSystem.raise_()
        self.line.raise_()
        self.lblRecognition.raise_()
        self.entanceCaptureBtn.raise_()
        self.startCamBtn.raise_()
        self.dateRegisteredLBl.raise_()
        self.plateNumLbl.raise_()
        self.vehicleOwnerLbl.raise_()
        self.ownerTextbox.raise_()
        self.plateTextbox.raise_()
        self.dateRegisteredBox.raise_()
        self.checkPlateBtn.raise_()
        self.saveReportBtn.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "RPNRS - MONITORING"))
        self.lblRegistered.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:36pt; font-weight:600;\">R</span><span style=\" font-size:24pt;\">egistered</span></p></body></html>"))
        self.lblPlateNumber.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:36pt; font-weight:600;\">P</span><span style=\" font-size:24pt;\">late </span><span style=\" font-size:36pt; font-weight:600;\">N</span><span style=\" font-size:24pt;\">umber</span></p></body></html>"))
        self.lblRecognition.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:36pt; font-weight:600;\">R</span><span style=\" font-size:24pt;\">ecognition</span></p></body></html>"))
        self.lblSystem.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:36pt; font-weight:600;\">S</span><span style=\" font-size:24pt;\">ystem</span></p></body></html>"))
        self.lblInfo.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">MONITORING</span></p></body></html>"))
        self.entanceCaptureBtn.setText(_translate("MainWindow", "CAPTURE"))
        self.startCamBtn.setText(_translate("MainWindow", "START CAMERA"))
        self.dateRegisteredLBl.setText(_translate("MainWindow", "Date Registered:"))
        self.plateNumLbl.setText(_translate("MainWindow", "Plate Number:"))
        self.vehicleOwnerLbl.setText(_translate("MainWindow", "Vehicle Owner:"))
        self.checkPlateBtn.setText(_translate("MainWindow", "CHECK PLATE NUMBER"))
        self.saveReportBtn.setText(_translate("MainWindow", "SAVE REPORT"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindowMonitor()
    ui.setupUi4(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
