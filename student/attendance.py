# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'attendance.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Attendance(object):
    def setupUi(self, Attendance):
        Attendance.setObjectName("Attendance")
        Attendance.resize(400, 200)
        Attendance.setMinimumSize(QtCore.QSize(400, 200))
        self.gridLayout_2 = QtWidgets.QGridLayout(Attendance)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.button_send = QtWidgets.QPushButton(Attendance)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.button_send.setFont(font)
        self.button_send.setDefault(True)
        self.button_send.setObjectName("button_send")
        self.gridLayout.addWidget(self.button_send, 3, 0, 1, 1)
        self.label_attendance = QtWidgets.QLabel(Attendance)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_attendance.setFont(font)
        self.label_attendance.setAlignment(QtCore.Qt.AlignCenter)
        self.label_attendance.setObjectName("label_attendance")
        self.gridLayout.addWidget(self.label_attendance, 0, 0, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_surname = QtWidgets.QLabel(Attendance)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_surname.setFont(font)
        self.label_surname.setObjectName("label_surname")
        self.gridLayout_3.addWidget(self.label_surname, 1, 0, 1, 1)
        self.label_name = QtWidgets.QLabel(Attendance)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_name.setFont(font)
        self.label_name.setObjectName("label_name")
        self.gridLayout_3.addWidget(self.label_name, 0, 0, 1, 1)
        self.label_index = QtWidgets.QLabel(Attendance)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_index.setFont(font)
        self.label_index.setObjectName("label_index")
        self.gridLayout_3.addWidget(self.label_index, 2, 0, 1, 1)
        self.line_edit_name = QtWidgets.QLineEdit(Attendance)
        self.line_edit_name.setObjectName("line_edit_name")
        self.gridLayout_3.addWidget(self.line_edit_name, 0, 2, 1, 1)
        self.line_edit_surname = QtWidgets.QLineEdit(Attendance)
        self.line_edit_surname.setObjectName("line_edit_surname")
        self.gridLayout_3.addWidget(self.line_edit_surname, 1, 2, 1, 1)
        self.line_edit_index = QtWidgets.QLineEdit(Attendance)
        self.line_edit_index.setObjectName("line_edit_index")
        self.gridLayout_3.addWidget(self.line_edit_index, 2, 2, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_3, 1, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(Attendance)
        QtCore.QMetaObject.connectSlotsByName(Attendance)

    def retranslateUi(self, Attendance):
        _translate = QtCore.QCoreApplication.translate
        Attendance.setWindowTitle(_translate("Attendance", "Form"))
        self.button_send.setToolTip(_translate("Attendance", "Send information about your presence"))
        self.button_send.setText(_translate("Attendance", "Confirm attendance"))
        self.label_attendance.setText(_translate("Attendance", "Attendance check"))
        self.label_surname.setText(_translate("Attendance", "Surname"))
        self.label_name.setText(_translate("Attendance", "Name"))
        self.label_index.setText(_translate("Attendance", "Index"))
        self.line_edit_name.setToolTip(_translate("Attendance", "Enetr your name"))
        self.line_edit_surname.setToolTip(_translate("Attendance", "Enetr your surname"))
        self.line_edit_index.setToolTip(_translate("Attendance", "Enetr your index"))
