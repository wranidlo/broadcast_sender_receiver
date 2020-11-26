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
        Dialog.resize(400, 500)
        Dialog.setMinimumSize(QtCore.QSize(400, 500))
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.combo_box_ip = QtWidgets.QComboBox(Dialog)
        self.combo_box_ip.setObjectName("combo_box_ip")
        self.horizontalLayout_2.addWidget(self.combo_box_ip)
        self.button_ip = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.button_ip.setFont(font)
        self.button_ip.setAutoDefault(False)
        self.button_ip.setObjectName("button_ip")
        self.horizontalLayout_2.addWidget(self.button_ip)
        self.gridLayout.addLayout(self.horizontalLayout_2, 6, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.line_edit_messege = QtWidgets.QTextEdit(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_edit_messege.sizePolicy().hasHeightForWidth())
        self.line_edit_messege.setSizePolicy(sizePolicy)
        self.line_edit_messege.setBaseSize(QtCore.QSize(0, 0))
        self.line_edit_messege.setStyleSheet("QTextEdit{\n"
"border:2px solid gray;\n"
"border-radius:2 px;\n"
"selection-background-color:darkblue;\n"
"\n"
"}")
        self.line_edit_messege.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.line_edit_messege.setObjectName("line_edit_messege")
        self.horizontalLayout.addWidget(self.line_edit_messege)
        self.button_send = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.button_send.setFont(font)
        self.button_send.setToolTipDuration(-1)
        self.button_send.setAutoDefault(False)
        self.button_send.setDefault(True)
        self.button_send.setObjectName("button_send")
        self.horizontalLayout.addWidget(self.button_send)
        self.gridLayout.addLayout(self.horizontalLayout, 9, 0, 1, 1)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_info = QtWidgets.QLabel(Dialog)
        self.label_info.setText("")
        self.label_info.setObjectName("label_info")
        self.horizontalLayout_6.addWidget(self.label_info)
        self.button_synchronize = QtWidgets.QPushButton(Dialog)
        self.button_synchronize.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_synchronize.sizePolicy().hasHeightForWidth())
        self.button_synchronize.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.button_synchronize.setFont(font)
        self.button_synchronize.setObjectName("button_synchronize")
        self.horizontalLayout_6.addWidget(self.button_synchronize)
        self.gridLayout.addLayout(self.horizontalLayout_6, 1, 0, 1, 1)
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
"}\n"
"")
        self.list_chat.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.list_chat.setAlternatingRowColors(True)
        self.list_chat.setTextElideMode(QtCore.Qt.ElideNone)
        self.list_chat.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.list_chat.setProperty("isWrapping", False)
        self.list_chat.setResizeMode(QtWidgets.QListView.Fixed)
        self.list_chat.setWordWrap(True)
        self.list_chat.setObjectName("list_chat")
        self.verticalLayout.addWidget(self.list_chat)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 3, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Communicator"))
        self.button_ip.setText(_translate("Dialog", "Change broadcast"))
        self.button_send.setToolTip(_translate("Dialog", "<html><head/><body><p>Send message to all users</p></body></html>"))
        self.button_send.setText(_translate("Dialog", "Send"))
        self.button_synchronize.setToolTip(_translate("Dialog", "Update informations about available interfaces"))
        self.button_synchronize.setText(_translate("Dialog", "Synchronize"))
        self.list_chat.setToolTip(_translate("Dialog", "<html><head/><body><p>Send message to all users</p></body></html>"))
