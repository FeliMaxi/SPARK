import sys
import requests
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

"""
from Archivo convertido con pyside2-uic archivo.ui > interfaz.py
import nombre de la clase del archivo convertido
"""
from UI_Spark import Ui_MainWindow
from UI_Inicio import Ui_InicioScreen

# === DISTANCIA ===
Distance = 20

if Distance > 23:
  Alert = 'Muy lejos'
elif 24 > Distance > 17:
    Alert = 'Perfecto'
elif 18 > Distance:
    Alert = 'Muy cerca'
else: Alert = 'Sin datos'

# === CLIMA ===

API_KEY = 'c01a0cfb38073ea9a2b467ebd0287997'
CIUDAD = "Cordoba,AR"  
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CIUDAD}&appid={API_KEY}&units=metric&lang=es"

response = requests.get(URL)
data = response.json()

if response.status_code == 200:
    temp = data["main"]["temp"]
    descripcion = data["weather"][0]["description"]
    clm = f"{temp}°C — {descripcion.capitalize()}"
else:
    clm = "Error al obtener el clima"

# === MAIN WINDOW ===

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Variables de ejemplo
        self.Distancia = Distance
        self.Alerta = Alert
        self.clima = clm

        # Mostrar los valores en los labels
        self.actualizar_labels()

    def actualizar_labels(self):
        self.ui.label.setText(f"Distancia: {self.Distancia} cm")
        self.ui.label_2.setText(self.Alerta)
        self.ui.label_3.setText(self.clima)

# === INICIO SCREEN ===
class Inicioscreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_InicioScreen()
        self.ui.setupUi(self)

        # --- Mostrar imagen SPARK.png dentro del frame ---
        self.logo_label = QLabel(self.ui.frame)  # <--- QLabel con L mayúscula
        pixmap = QPixmap("SPARK.png")  # Ruta de la imagen
        self.logo_label.setPixmap(pixmap)
        self.logo_label.setScaledContents(True)  # Ajusta el tamaño al frame

        # Asegura que el label ocupe todo el frame
        self.logo_label.setGeometry(self.ui.frame.rect())

        # Si querés que se mantenga centrada y se actualice al redimensionar:
        self.ui.frame.installEventFilter(self)

        
        # Conectamos el botón para volver a la ventana principal
        self.ui.startButton.clicked.connect(self.ir_a_principal)

    def ir_a_principal(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()  # o self.hide()




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

# Never gonna give you up