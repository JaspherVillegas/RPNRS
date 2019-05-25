# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rpnrsReports.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import pymysql

from PyQt5.QtWidgets import QMessageBox

from arrow import utcnow, get
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.colors import black, purple, white 
from reportlab.pdfgen import canvas

conn = pymysql.connect(host='localhost', user='root', password='', database='rpnrsdb')

class reportPDF(object):
    
    def __init__(self, title, header, data, pdfname):
        super(reportPDF, self).__init__()

        self.title = title
        self.header = header
        self.data = data
        self.pdfname = pdfname

        self.style = getSampleStyleSheet()

    @staticmethod
    def _headerPage(canvas, archivePDF):        
        canvas.saveState()
        style = getSampleStyleSheet()

        align = ParagraphStyle(name="align", alignment=TA_LEFT,
                                    parent=style["Normal"])
        algn = ParagraphStyle(name="algn", alignment=TA_CENTER,
                                    parent=style["Heading1"])
        align1 = ParagraphStyle(name="align", alignment=TA_CENTER,
                                    parent=style["Normal"])

 
        headerName = Paragraph("CAVITE STATE UNIVERSITY - CCAT",algn)
        wdth, hght = headerName.wrap(archivePDF.width, archivePDF.topMargin)
        headerName.drawOn(canvas, archivePDF.leftMargin, 736)

        header1 = Paragraph("ROSARIO, CAVITE",align1)
        wdth, hght = header1.wrap(archivePDF.width, archivePDF.topMargin)
        header1.drawOn(canvas, archivePDF.leftMargin, 720)

        dates = utcnow().to("local").format("MMMM - DD , YYYY - dddd", locale="en")
        datereport = dates.replace("-", " ")

        headerDate = Paragraph("DATE GENEREATED: " + datereport, align)
        wdth, hght = headerDate.wrap(archivePDF.width, archivePDF.bottomMargin)
        headerDate.drawOn(canvas, archivePDF.leftMargin, 15 * mm + (0.2 * inch))
 
        

        dates = utcnow().to("local").format("dddd, MMMM - DD - YYYY", locale="en")
        datereport = dates.replace("-", " ")
 
        # Suelta el lienzo
        canvas.restoreState()

    def convertData(self):

        headerStyle = ParagraphStyle(name="headerStyle", alignment=TA_LEFT,
                                          fontSize=10, textColor=black,
                                          fontName="Helvetica-Bold",
                                          parent=self.style["Normal"])

        styleNormal = self.style["Normal"]
        styleNormal.alignment = TA_LEFT

        keys, names = zip(*[[k, n] for k, n in self.header])

        head = [Paragraph(name, headerStyle) for name in names]
        newData = [tuple(head)]

        for data1 in self.data:
            newData.append([Paragraph(str(data1[key]), styleNormal) for key in keys])
            
        return newData
        
    def Export(self):

        titleAlign = ParagraphStyle(name="center", alignment=TA_CENTER, fontSize=13,
                                          leading=10, textColor=black,
                                          parent=self.style["Heading2"])
        
        self.wd, self.hgt = letter

        convertData = self.convertData()
    
        tbl = Table(convertData, colWidths=(self.wd-100)/len(self.header), hAlign="CENTER")
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0),(-1, 0), white),
            ("ALIGN", (0, 0),(0, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), 
            ("INNERGRID", (0, 0), (-1, -1), 0.50, black),
            ("BOX", (0, 0), (-1, -1), 0.25, black),
            ]))

        history = []
        history.append(Paragraph(self.title, titleAlign))
        history.append(Spacer(1, 0.16 * inch))
        history.append(tbl)

        archivePDF = SimpleDocTemplate(self.pdfname, leftMargin=50, rightMargin=50, pagesize=letter,
                                       title="Report PDF")
        
        try:
            archivePDF.build(history, onFirstPage=self._headerPage,
                             onLaterPages=self._headerPage,
                             canvasmaker=numberPages)
            
            #return "Report generated."
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Report generated.")
            msg.setWindowTitle("RPNRS")
            msg.exec_()
        except PermissionError:
            return "Error!"


class numberPages(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        numPage = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(numPage)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)
 
    def draw_page_number(self, conteoPaginas):
        self.drawRightString(204 * mm, 15 * mm + (0.2 * inch),
                             "Page {} of {}".format(self._pageNumber, conteoPaginas))

#################################
def generateReport(self):
  
    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]

        return d

    with conn.cursor() as cursor:
        datas = {}
        dict_datas = []

        srch = self.SearchEdit.text()
        box = str(self.FilterBox.currentText())
        

        if box == "DATE":
            cmd = "SELECT * FROM reporttbl WHERE reportVehicleDate = %s"
            cursor.execute(cmd,(srch))
            data = cursor.fetchall()

            for row in data:
                datas = {"reportId": row[0], "reportOwnerId": row[1], "reportOwnerName": row[2], "reportVehicleType": row[3], "reportVehicleId": row[4], "reportVehicleDate": row[5], "reportVehicleTime": row[6], "reportVehicleStatus": row[7]}
                #print(datas)
                dict_datas.append(datas)

        elif box == "PLATE NUMBER":
            cmd = "SELECT * FROM reporttbl WHERE reportVehicleId = %s"
            cursor.execute(cmd,(srch))
            data = cursor.fetchall()


            for row in data:
                datas = {"reportId": row[0], "reportOwnerId": row[1], "reportOwnerName": row[2], "reportVehicleType": row[3], "reportVehicleId": row[4], "reportVehicleDate": row[5], "reportVehicleTime": row[6], "reportVehicleStatus": row[7]}
                #print(datas)
                dict_datas.append(datas)

        elif box == "OWNER NAME":
            cmd = "SELECT * FROM reporttbl WHERE reportOwnerName = %s"
            cursor.execute(cmd,(srch))
            data = cursor.fetchall()


            for row in data:
                datas = {"reportId": row[0], "reportOwnerId": row[1], "reportOwnerName": row[2], "reportVehicleType": row[3], "reportVehicleId": row[4], "reportVehicleDate": row[5], "reportVehicleTime": row[6], "reportVehicleStatus": row[7]}
                #print(datas)
                dict_datas.append(datas)

        else:
            cursor.execute("SELECT * FROM reporttbl")
            data = cursor.fetchall()

            for row in data:
                datas = {"reportId": row[0], "reportOwnerId": row[1], "reportOwnerName": row[2], "reportVehicleType": row[3], "reportVehicleId": row[4], "reportVehicleDate": row[5], "reportVehicleTime": row[6], "reportVehicleStatus": row[7]}
                #print(datas)
                dict_datas.append(datas)
    conn.commit()
    #print(range(len(data)))
    #print(data)
    #print(dict_datas)


    title = "CVSU-CCAT RPNRS"

    header = (("reportId", "REPORT ID"),
                        ("reportOwnerId", "OWNER ID"),
                            ("reportOwnerName", "OWNER NAME"),
                            ("reportVehicleType", "VEHICLE TYPE"),
                            ("reportVehicleId", "PLATE NUMBER"),
                            ("reportVehicleDate", "DATE OF ENTRANCE"),
                            ("reportVehicleTime", "TIME OF ENTRANCE"),
                            ("reportVehicleStatus", "STATUS"))
   
    pdfname = "report.pdf"

    report = reportPDF(title, header, dict_datas, pdfname).Export()
    print(report)
class Ui_ReportsWindow(object):
    def generate(self):
        generateReport(self)
    def refresh(self):
        with conn.cursor() as cursor:
            cmd = "SELECT * from reporttbl ORDER BY reportId"
            cursor.execute(cmd)
            data = cursor.fetchall()
            self.reportsTable.setRowCount(0)
            for row_number, row_data in enumerate(data):
                self.reportsTable.insertRow(row_number)
                for column_number, column_data in enumerate(row_data):
                    self.reportsTable.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))
        conn.commit()
    def clik(self):
        srch = self.SearchEdit.text()
        box = str(self.FilterBox.currentText())
        if box == "DATE":
            with conn.cursor() as cursor:
                cmd = "SELECT * FROM reporttbl WHERE reportVehicleDate = %s"
                cursor.execute(cmd,(srch))
                data = cursor.fetchall()
                self.reportsTable.setRowCount(0)
                for row_number, row_data in enumerate(data):
                    self.reportsTable.insertRow(row_number)
                    for column_number, column_data in enumerate(row_data):
                        self.reportsTable.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))
            conn.commit()
        elif box == "PLATE NUMBER":
            with conn.cursor() as cursor:
                cmd = "SELECT * FROM reporttbl WHERE reportVehicleId = %s"
                cursor.execute(cmd,(srch))
                data = cursor.fetchall()
                self.reportsTable.setRowCount(0)
                for row_number, row_data in enumerate(data):
                    self.reportsTable.insertRow(row_number)
                    for column_number, column_data in enumerate(row_data):
                        self.reportsTable.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))

            conn.commit()
        elif box == "OWNER NAME":
            with conn.cursor() as cursor:
                cmd = "SELECT * FROM reporttbl WHERE reportOwnerName = %s"
                cursor.execute(cmd,(srch))
                data = cursor.fetchall()
                self.reportsTable.setRowCount(0)
                for row_number, row_data in enumerate(data):
                    self.reportsTable.insertRow(row_number)
                    for column_number, column_data in enumerate(row_data):
                        self.reportsTable.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(column_data)))

            conn.commit()
        else:
            self.refresh()
    def setupUi6(self, ReportsWindow):
        ReportsWindow.setObjectName("ReportsWindow")
        ReportsWindow.resize(1120, 470)
        ReportsWindow.setMinimumSize(QtCore.QSize(1120, 470))
        ReportsWindow.setMaximumSize(QtCore.QSize(1500, 470))
        ReportsWindow.setStyleSheet("background-color: rgb(0, 84, 139);")
        self.centralwidget = QtWidgets.QWidget(ReportsWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.reportsTable = QtWidgets.QTableWidget(self.centralwidget)
        self.reportsTable.setGeometry(QtCore.QRect(378, 10, 731, 451))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        self.reportsTable.setFont(font)
        self.reportsTable.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.reportsTable.setObjectName("reportsTable")
        self.reportsTable.setColumnCount(8)
        self.reportsTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(9)
        item.setFont(font)
        self.reportsTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(9)
        item.setFont(font)
        self.reportsTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(9)
        item.setFont(font)
        self.reportsTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        item.setFont(font)
        self.reportsTable.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        item.setFont(font)
        self.reportsTable.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        item.setFont(font)
        self.reportsTable.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setBold(False)
        font.setWeight(50)
        item.setFont(font)
        self.reportsTable.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        item.setFont(font)
        self.reportsTable.setHorizontalHeaderItem(7, item)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 371, 461))
        self.frame.setMinimumSize(QtCore.QSize(371, 461))
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
        self.searchButton.setGeometry(QtCore.QRect(259, 380, 80, 30))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.searchButton.setFont(font)
        self.searchButton.setCursor(QtGui.QCursor(QtCore.Qt.BusyCursor))
        self.searchButton.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.searchButton.setObjectName("searchButton")
        self.searchButton.clicked.connect(self.clik)
        self.SearchEdit = QtWidgets.QLineEdit(self.frame)
        self.SearchEdit.setGeometry(QtCore.QRect(32, 379, 220, 30))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.SearchEdit.setFont(font)
        self.SearchEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.SearchEdit.setObjectName("SearchEdit")
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(199, 430, 161, 30))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.generate)
        self.FilterBox = QtWidgets.QComboBox(self.frame)
        self.FilterBox.setGeometry(QtCore.QRect(32, 345, 121, 30))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(9)
        self.FilterBox.setFont(font)
        self.FilterBox.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.FilterBox.setObjectName("FilterBox")
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
        self.lblInfo.setGeometry(QtCore.QRect(131, 291, 111, 41))
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
        ReportsWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(ReportsWindow)
        self.FilterBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ReportsWindow)

    def retranslateUi(self, ReportsWindow):
        _translate = QtCore.QCoreApplication.translate
        ReportsWindow.setWindowTitle(_translate("ReportsWindow", "RPNRS - REPORTS"))
        item = self.reportsTable.horizontalHeaderItem(0)
        item.setText(_translate("ReportsWindow", "REPORT ID"))
        item = self.reportsTable.horizontalHeaderItem(1)
        item.setText(_translate("ReportsWindow", "OWNER ID"))
        item = self.reportsTable.horizontalHeaderItem(2)
        item.setText(_translate("ReportsWindow", "OWNER NAME"))
        item = self.reportsTable.horizontalHeaderItem(3)
        item.setText(_translate("ReportsWindow", "VEHICLE TYPE"))
        item = self.reportsTable.horizontalHeaderItem(4)
        item.setText(_translate("ReportsWindow", "PLATE NUMBER"))
        item = self.reportsTable.horizontalHeaderItem(5)
        item.setText(_translate("ReportsWindow", "DATE OF ENTRANCE"))
        item = self.reportsTable.horizontalHeaderItem(6)
        item.setText(_translate("ReportsWindow", "TIME OF ENTRANCE"))
        item = self.reportsTable.horizontalHeaderItem(7)
        item.setText(_translate("ReportsWindow", "STATUS"))
        self.lblRegistered.setText(_translate("ReportsWindow", "<html><head/><body><p><span style=\" font-size:36pt; font-weight:600;\">R</span><span style=\" font-size:24pt;\">egistered</span></p></body></html>"))
        self.lblPlateNumber.setText(_translate("ReportsWindow", "<html><head/><body><p><span style=\" font-size:36pt; font-weight:600;\">P</span><span style=\" font-size:24pt;\">late </span><span style=\" font-size:36pt; font-weight:600;\">N</span><span style=\" font-size:24pt;\">umber</span></p></body></html>"))
        self.lblRecognition.setText(_translate("ReportsWindow", "<html><head/><body><p><span style=\" font-size:36pt; font-weight:600;\">R</span><span style=\" font-size:24pt;\">ecognition</span></p></body></html>"))
        self.lblSystem.setText(_translate("ReportsWindow", "<html><head/><body><p><span style=\" font-size:36pt; font-weight:600;\">S</span><span style=\" font-size:24pt;\">ystem</span></p></body></html>"))
        self.searchButton.setText(_translate("ReportsWindow", "Search"))
        self.pushButton.setText(_translate("ReportsWindow", "Generate Report"))
        self.FilterBox.setCurrentText(_translate("ReportsWindow", "Filter By:"))
        self.FilterBox.setItemText(0, _translate("ReportsWindow", "Filter By:"))
        self.FilterBox.setItemText(1, _translate("ReportsWindow", "DATE"))
        self.FilterBox.setItemText(2, _translate("ReportsWindow", "PLATE NUMBER"))
        self.lblInfo.setText(_translate("ReportsWindow", "<html><head/><body><p><span style=\" font-weight:600;\">REPORTS</span></p></body></html>"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ReportsWindow = QtWidgets.QMainWindow()
    ui = Ui_ReportsWindow()
    ui.setupUi6(ReportsWindow)
    ReportsWindow.show()
    sys.exit(app.exec_())
