import sys
import time
import serial
from PySide6.QtGui import QPixmap
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenuBar, QSizePolicy,
    QStatusBar, QWidget, QLabel)
from PySide6.QtCore import QTimer

"""
from Archivo convertido con pyside2-uic archivo.ui > interfaz.py
import nombre de la clase del archivo convertido
"""
from UI_Spark import Ui_MainWindow
from UI_Inicio import Ui_InicioScreen


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.Distancia = 0
        self.Alerta = "Sin datos"

        try:
            self.arduino = serial.Serial('COM3', 9600)
            time.sleep(2)
            print(" Conectado a Arduino correctamente.")
        except Exception as e:
            print("No se pudo conectar al Arduino:", e)
            self.arduino = None

        self.timer = QTimer()
        self.timer.timeout.connect(self.actualizar_datos)
        self.timer.start(200)

        self.actualizar_labels()

    def actualizar_labels(self):
        self.ui.label.setText(f"Distancia: {self.Distancia} cm")
        self.ui.label_2.setText(self.Alerta)

    def actualizar_datos(self):
        if self.arduino and self.arduino.in_waiting > 0:
            try:
                linea = self.arduino.readline().decode().strip()
                if linea.isdigit():
                    distancia = int(linea)
                    alerta = self.calcular_alerta(distancia)
                    self.Distancia = distancia
                    self.Alerta = alerta
                    self.actualizar_labels()
            except Exception as e:
                print("Error leyendo del Arduino:", e)

    def calcular_alerta(self, distancia):
        if distancia > 23:
            return "Muy lejos"
        elif 17 < distancia <= 23:
            return "Perfecto"
        elif distancia <= 17:
            return "Muy cerca"
        else:
            return "Sin datos"

class Inicioscreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_InicioScreen()
        self.ui.setupUi(self)
        
        self.logo_label = QLabel(self.ui.frame)  
        pixmap = QPixmap("SPARK.png")  
        self.logo_label.setPixmap(pixmap)
        self.logo_label.setScaledContents(True)  
       
        self.logo_label.setGeometry(self.ui.frame.rect())

        self.ui.frame.installEventFilter(self)

        self.ui.startButton.clicked.connect(self.ir_a_principal)

    def ir_a_principal(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()  

print("""
   _____ ____  ___    ____  __ __
  / ___// __ \/   |  / __ \/ //_/
  \__ \/ /_/ / /| | / /_/ / ,<   
 ___/ / ____/ ___ |/ _, _/ /| |  
/____/_/   /_/  |_/_/ |_/_/ |_|  
Sensor de Proximidad Automático 
    para Riesgos Kinéticos                             
      """)

if __name__ == "__main__": #checkea si el script está siendo ejecutado como el prog principal (no importado como un modulo).
    app = QApplication(sys.argv)    # Crea un Qt widget, la cual va ser nuestra ventana.
    window = Inicioscreen() #crea una intancia de MainWindow 
    window.show() # IMPORTANT!!!!! la ventanas estan ocultas por defecto.
    sys.exit(app.exec()) # Start the event loop.