# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitledZthAOk.ui'
##
## Created by: Qt User Interface Compiler version 5.15.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_UselessWindow(object):
    def setupUi(self, UselessWindow):
        if not UselessWindow.objectName():
            UselessWindow.setObjectName(u"UselessWindow")
        UselessWindow.resize(800, 600)
        self.centralwidget = QWidget(UselessWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.catButton = QPushButton(self.centralwidget)
        self.catButton.setObjectName(u"catButton")
        self.catButton.setGeometry(QRect(700, 530, 89, 25))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(200, 390, 271, 17))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(280, 140, 241, 151))
        UselessWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(UselessWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        UselessWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(UselessWindow)
        self.statusbar.setObjectName(u"statusbar")
        UselessWindow.setStatusBar(self.statusbar)

        self.retranslateUi(UselessWindow)

        QMetaObject.connectSlotsByName(UselessWindow)
    # setupUi

    def retranslateUi(self, UselessWindow):
        UselessWindow.setWindowTitle(QCoreApplication.translate("UselessWindow", u"MainWindow", None))
        self.catButton.setText(QCoreApplication.translate("UselessWindow", u"Pop a cat", None))
        self.label.setText(QCoreApplication.translate("UselessWindow", u"Nombre de personne: ", None))
        self.label_2.setText(QCoreApplication.translate("UselessWindow", u"TextLabel", None))
    # retranslateUi