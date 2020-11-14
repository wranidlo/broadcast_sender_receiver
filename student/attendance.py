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
        self.button_send.setFont(font)
        self.button_send.setDefault(True)
        self.button_send.setObjectName("button_send")
        self.gridLayout.addWidget(self.button_send, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(Attendance)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.edit_full_name = QtWidgets.QLineEdit(Attendance)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.edit_full_name.setFont(font)
        self.edit_full_name.setObjectName("edit_full_name")
        self.gridLayout.addWidget(self.edit_full_name, 1, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(Attendance)
        QtCore.QMetaObject.connectSlotsByName(Attendance)

    def retranslateUi(self, Attendance):
        _translate = QtCore.QCoreApplication.translate
        Attendance.setWindowTitle(_translate("Attendance", "Form"))
        self.button_send.setText(_translate("Attendance", "Confirm attendance"))
        self.label.setText(_translate("Attendance", "Enter your full name"))
