# -*- coding: utf-8 -*-
################################################################################
## Ventana de selección de planes (estilo gris minimalista)
################################################################################

from PySide6.QtCore import Qt, QRect, QMetaObject, QCoreApplication
from PySide6.QtGui import QFont, QPalette, QColor, QLinearGradient, QBrush
from PySide6.QtWidgets import (
    QApplication, QFrame, QMainWindow, QMenuBar,
    QPushButton, QStatusBar, QWidget, QLabel
)

class Ui_PlanesScreen(object):
    def setupUi(self, PlanesScreen):
        if not PlanesScreen.objectName():
            PlanesScreen.setObjectName(u"PlanesScreen")
        PlanesScreen.resize(800, 600)
        PlanesScreen.setMinimumSize(800, 600)

        # === Fondo degradado gris oscuro ===
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, 600)
        gradient.setColorAt(0.0, QColor("#1C1C1C"))
        gradient.setColorAt(0.5, QColor("#2E2E2E"))
        gradient.setColorAt(1.0, QColor("#3B3B3B"))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        PlanesScreen.setPalette(palette)

        # === Central widget ===
        self.centralwidget = QWidget(PlanesScreen)
        self.centralwidget.setObjectName(u"centralwidget")

        # === Título ===
        self.title_label = QLabel(self.centralwidget)
        self.title_label.setGeometry(QRect(0, 50, 800, 60))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: #E0E0E0; font: bold 26pt 'Segoe UI';")
        self.title_label.setText("Elige tu Plan SPARK")

        # === Frame para los planes ===
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(150, 140, 500, 300))
        self.frame.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 20);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 30);
            }
        """)

        # === Texto de planes ===
        self.label_estandar = QLabel(self.frame)
        self.label_estandar.setGeometry(QRect(30, 30, 440, 100))
        self.label_estandar.setStyleSheet("color: #CCCCCC; font: 13pt 'Segoe UI';")
        self.label_estandar.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.label_estandar.setText(
            "🟢 <b>Plan Estándar ($0)</b><br>"
            "• Detección de distancia<br>"
            "• Alerta visual<br>"
            "• Lectura de clima básica"
        )

        self.label_premium = QLabel(self.frame)
        self.label_premium.setGeometry(QRect(30, 160, 440, 80))
        self.label_premium.setStyleSheet("color: #CCCCCC; font: 13pt 'Segoe UI';")
        self.label_premium.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.label_premium.setText(
            "💎 <b>Plan Premium ($999)</b><br>"
            "• Es premium."
        )

        # === Botones ===
        self.btn_estandar = QPushButton(self.centralwidget)
        self.btn_estandar.setGeometry(QRect(180, 470, 180, 60))
        font = QFont("Segoe UI", 16, QFont.Bold)
        self.btn_estandar.setFont(font)
        self.btn_estandar.setCursor(Qt.PointingHandCursor)
        self.btn_estandar.setText("ESTÁNDAR")

        self.btn_estandar.setStyleSheet("""
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
            }
            QPushButton:pressed {
                background-color: #3C3C3C;
            }
        """)

        self.btn_premium = QPushButton(self.centralwidget)
        self.btn_premium.setGeometry(QRect(440, 470, 180, 60))
        self.btn_premium.setFont(font)
        self.btn_premium.setCursor(Qt.PointingHandCursor)
        self.btn_premium.setText("PREMIUM")

        self.btn_premium.setStyleSheet("""
            QPushButton {
                background-color: #777777;
                color: #F5F5F5;
                border: none;
                border-radius: 20px;
                padding: 10px;
                transition: all 0.3s ease;
            }
            QPushButton:hover {
                background-color: #999999;
            }
            QPushButton:pressed {
                background-color: #5A5A5A;
            }
        """)

        # === Configuración general ===
        PlanesScreen.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(PlanesScreen)
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        PlanesScreen.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(PlanesScreen)
        PlanesScreen.setStatusBar(self.statusbar)

        self.retranslateUi(PlanesScreen)
        QMetaObject.connectSlotsByName(PlanesScreen)

    def retranslateUi(self, PlanesScreen):
        PlanesScreen.setWindowTitle(QCoreApplication.translate("PlanesScreen", "SPARK — Planes", None))
        self.title_label.setText(QCoreApplication.translate("PlanesScreen", "Elige tu Plan SPARK", None))
