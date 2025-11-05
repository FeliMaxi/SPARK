# -*- coding: utf-8 -*-
################################################################################
## Interfaz mejorada para la pantalla de inicio (versión gris minimalista)
################################################################################

from PySide6.QtCore import Qt, QRect, QMetaObject, QCoreApplication
from PySide6.QtGui import QFont, QPalette, QColor, QLinearGradient, QBrush
from PySide6.QtWidgets import (
    QFrame, QMainWindow, QMenuBar,
    QPushButton, QStatusBar, QWidget, QLabel
)

class Ui_InicioScreen(object):
    def setupUi(self, InicioScreen):
        if not InicioScreen.objectName():
            InicioScreen.setObjectName(u"InicioScreen")
        InicioScreen.resize(800, 600)
        InicioScreen.setMinimumSize(800, 600)

        # === Fondo degradado gris oscuro ===
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, 600)
        gradient.setColorAt(0.0, QColor("#1C1C1C"))
        gradient.setColorAt(0.5, QColor("#2E2E2E"))
        gradient.setColorAt(1.0, QColor("#3B3B3B"))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        InicioScreen.setPalette(palette)

        # === Central widget ===
        self.centralwidget = QWidget(InicioScreen)
        self.centralwidget.setObjectName(u"centralwidget")

        # === Frame del logo (efecto vidrio) ===
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(250, 80, 300, 260))
        self.frame.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 20);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 30);
            }
        """)

        # === Subtítulo ===
        self.sub_label = QLabel(self.centralwidget)
        self.sub_label.setGeometry(QRect(0, 360, 800, 40))
        self.sub_label.setAlignment(Qt.AlignCenter)
        self.sub_label.setStyleSheet("color: #B0B0B0; font: 14pt 'Segoe UI';")
        self.sub_label.setText("Sensor de Proximidad Automático para Riesgos Kinéticos")

        # === Botón START (gris metálico) ===
        self.startButton = QPushButton(self.centralwidget)
        self.startButton.setObjectName(u"startButton")
        self.startButton.setGeometry(QRect(300, 430, 200, 70))
        font = QFont("Segoe UI", 24, QFont.Bold)
        self.startButton.setFont(font)
        self.startButton.setCursor(Qt.PointingHandCursor)
        self.startButton.setText("START")

        # Estilo gris metálico con hover y transiciones suaves
        self.startButton.setStyleSheet("""
            QPushButton {
                background-color: #555555;
                color: #F5F5F5;
                border: none;
                border-radius: 20px;
                padding: 10px;
                transition: all 0.3s ease;
            }
            QPushButton:hover {
                background-color: #707070;
                letter-spacing: 1px;
            }
            QPushButton:pressed {
                background-color: #3C3C3C;
            }
        """)

        # === Configuración general ===
        InicioScreen.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(InicioScreen)
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        InicioScreen.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(InicioScreen)
        InicioScreen.setStatusBar(self.statusbar)

        self.retranslateUi(InicioScreen)
        QMetaObject.connectSlotsByName(InicioScreen)

    def retranslateUi(self, InicioScreen):
        InicioScreen.setWindowTitle(QCoreApplication.translate("InicioScreen", "SPARK — Inicio", None))
        self.startButton.setText(QCoreApplication.translate("InicioScreen", "START", None))

