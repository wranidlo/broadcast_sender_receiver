# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'help_com.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Help_com(object):
    def setupUi(self, Help_com):
        Help_com.setObjectName("Help_com")
        Help_com.resize(500, 426)
        self.gridLayout_2 = QtWidgets.QGridLayout(Help_com)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_help = QtWidgets.QLabel(Help_com)
        self.label_help.setAlignment(QtCore.Qt.AlignCenter)
        self.label_help.setObjectName("label_help")
        self.gridLayout.addWidget(self.label_help, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(Help_com)
        QtCore.QMetaObject.connectSlotsByName(Help_com)

    def retranslateUi(self, Help_com):
        _translate = QtCore.QCoreApplication.translate
        Help_com.setWindowTitle(_translate("Help_com", "Help"))
        self.label_help.setText(_translate("Help_com", "This is place for help"))
