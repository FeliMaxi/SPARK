# -*- coding: utf-8 -*-
################################################################################
## Interfaz mejorada para la ventana principal (versión gris elegante)
################################################################################

from PySide6.QtCore import Qt, QRect, QMetaObject, QCoreApplication
from PySide6.QtGui import QFont, QPalette, QColor, QLinearGradient, QBrush
from PySide6.QtWidgets import (
    QApplication, QLabel, QMainWindow, QMenuBar,
    QStatusBar, QWidget, QFrame, QPushButton
)

class Ui_SparkWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(600, 500)
        MainWindow.setMinimumSize(600, 500)

        # === Fondo degradado gris ===
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, 500)
        gradient.setColorAt(0.0, QColor("#1C1C1C"))
        gradient.setColorAt(0.5, QColor("#2E2E2E"))
        gradient.setColorAt(1.0, QColor("#3B3B3B"))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        MainWindow.setPalette(palette)

        # === Central Widget ===
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")

        # === Contenedor principal con efecto vidrio ===
        self.frame = QFrame(self.centralwidget)
        self.frame.setGeometry(QRect(50, 70, 500, 350))
        self.frame.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 20);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 30);
            }
        """)

        # === Label: Distancia ===
        self.label = QLabel(self.frame)
        self.label.setGeometry(QRect(40, 40, 420, 80))
        font = QFont("Segoe UI", 30, QFont.Bold)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #F0F0F0;")
        self.label.setAlignment(Qt.AlignCenter)

        # === Label: Alerta ===
        self.label_2 = QLabel(self.frame)
        self.label_2.setGeometry(QRect(60, 150, 380, 60))
        font2 = QFont("Segoe UI", 26, QFont.Medium)
        self.label_2.setFont(font2)
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_2.setStyleSheet("color: #D9D9D9;")

        # === Label: Clima ===
        self.label_3 = QLabel(self.frame)
        self.label_3.setGeometry(QRect(70, 250, 360, 40))
        font3 = QFont("Segoe UI", 16)
        self.label_3.setFont(font3)
        self.label_3.setAlignment(Qt.AlignCenter)
        self.label_3.setStyleSheet("color: #B0B0B0;")

        # === Botón: Configurar parámetros ===
        self.configButton = QPushButton(self.centralwidget)
        self.configButton.setObjectName(u"configButton")
        self.configButton.setGeometry(QRect(225, 420, 150, 35))
        self.configButton.setText("Configurar parámetros")
        self.configButton.setStyleSheet("""
            QPushButton {
                background-color: #555555;
                color: #F5F5F5;
                border: none;
                border-radius: 10px;
                font: 11pt 'Segoe UI';
            }
            QPushButton:hover {
                background-color: #707070;
            }
            QPushButton:pressed {
                background-color: #3C3C3C;
            }
        """)

        # === Detalle visual inferior ===
        self.footer = QLabel(self.centralwidget)
        self.footer.setGeometry(QRect(0, 450, 600, 40))
        self.footer.setAlignment(Qt.AlignCenter)
        self.footer.setStyleSheet("color: #808080; font: 10pt 'Segoe UI';")
        self.footer.setText("S.P.A.R.K © 2025 — Sensor de Proximidad Automático para Riesgos Kinéticos")

        # === Configuración final ===
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 600, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", "SPARK — Panel Principal", None))
        self.label.setText(QCoreApplication.translate("MainWindow", "Distancia: 20 cm", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", "Perfecto", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", "Clima: 18°C — Despejado", None))
        self.configButton.setText(QCoreApplication.translate("MainWindow", "Configurar parámetros", None))
