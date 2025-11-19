# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'designermSQNme.ui'
##
## Created by: Qt User Interface Compiler version 6.9.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QSpinBox, QStatusBar,
    QWidget)

class Ui_ConfigWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(150, 30, 429, 54))
        font = QFont()
        font.setPointSize(30)
        self.label.setFont(font)
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(100, 170, 166, 32))
        font1 = QFont()
        font1.setPointSize(18)
        self.label_2.setFont(font1)
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(430, 170, 209, 32))
        self.label_3.setFont(font1)
        self.spinBox = QSpinBox(self.centralwidget)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setGeometry(QRect(140, 240, 88, 43))
        font2 = QFont()
        font2.setPointSize(20)
        self.spinBox.setFont(font2)
        self.spinBox_2 = QSpinBox(self.centralwidget)
        self.spinBox_2.setObjectName(u"spinBox_2")
        self.spinBox_2.setGeometry(QRect(490, 240, 88, 43))
        self.spinBox_2.setFont(font2)
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(290, 400, 140, 47))
        font3 = QFont()
        font3.setPointSize(22)
        self.pushButton.setFont(font3)
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(90, 320, 559, 26))
        font4 = QFont()
        font4.setPointSize(14)
        self.label_4.setFont(font4)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Configuracion de limites", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Limite rojo (cm)", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Limite amarillo (cm)", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Confirmar", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Precaucion: el limite rojo debe ser menor que al del limite amarillo.", None))
    # retranslateUi

