# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 400)
        Dialog.setMinimumSize(QtCore.QSize(300, 400))
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.line_edit_messege = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.line_edit_messege.setFont(font)
        self.line_edit_messege.setStyleSheet("QLineEdit{\n"
"border:2px solid gray;\n"
"border-radius:2 px;\n"
"selection-background-color:darkblue;\n"
"\n"
"}")
        self.line_edit_messege.setObjectName("line_edit_messege")
        self.horizontalLayout.addWidget(self.line_edit_messege)
        self.button_send = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.button_send.setFont(font)
        self.button_send.setToolTipDuration(-1)
        self.button_send.setObjectName("button_send")
        self.horizontalLayout.addWidget(self.button_send)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.list_chat = QtWidgets.QListWidget(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.list_chat.setFont(font)
        self.list_chat.setAutoFillBackground(False)
        self.list_chat.setStyleSheet("QListWidget{\n"
"border:2px solid gray;\n"
"}")
        self.list_chat.setObjectName("list_chat")
        self.verticalLayout.addWidget(self.list_chat)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Communicator"))
        self.line_edit_messege.setToolTip(_translate("Dialog", "Input message"))
        self.button_send.setToolTip(_translate("Dialog", "<html><head/><body><p>Send message to all users</p></body></html>"))
        self.button_send.setText(_translate("Dialog", "Send"))
        self.list_chat.setToolTip(_translate("Dialog", "<html><head/><body><p>Send message to all users</p></body></html>"))
