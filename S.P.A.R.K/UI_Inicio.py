# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitledKOsNdD.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QStatusBar, QWidget)

class Ui_InicioScreen(object):
    def setupUi(self, InicioScreen):
        if not InicioScreen.objectName():
            InicioScreen.setObjectName(u"InicioScreen")
        InicioScreen.resize(800, 600)
        self.centralwidget = QWidget(InicioScreen)
        self.centralwidget.setObjectName(u"centralwidget")
        self.startButton = QPushButton(self.centralwidget)
        self.startButton.setObjectName(u"startButton")
        self.startButton.setGeometry(QRect(290, 340, 201, 81))
        font = QFont()
        font.setPointSize(40)
        self.startButton.setFont(font)
        self.startButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(240, 10, 291, 261))
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        InicioScreen.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(InicioScreen)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        InicioScreen.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(InicioScreen)
        self.statusbar.setObjectName(u"statusbar")
        InicioScreen.setStatusBar(self.statusbar)

        self.retranslateUi(InicioScreen)

        QMetaObject.connectSlotsByName(InicioScreen)
    # setupUi

    def retranslateUi(self, InicioScreen):
        InicioScreen.setWindowTitle(QCoreApplication.translate("InicioScreen", u"MainWindow", None))
        self.startButton.setText(QCoreApplication.translate("InicioScreen", u"START", None))
    # retranslateUi