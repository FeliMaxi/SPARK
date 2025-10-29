import sys
from PySide6.QtGui import QPixmap
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenuBar, QSizePolicy,
    QStatusBar, QWidget)

"""
from Archivo convertido con pyside2-uic archivo.ui > interfaz.py
import nombre de la clase del archivo convertido
"""
from UI_Spark import Ui_MainWindow

Distance = 20

if Distance > 23:
  Alert = 'Muy lejos'
elif 24 > Distance > 17:
    Alert = 'Perfecto'
elif 18 > Distance:
    Alert = 'Muy cerca'
else: 'Sin datos'



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Variables de ejemplo
        self.Distancia = Distance
        self.Alerta = Alert

        # Mostrar los valores en los labels
        self.actualizar_labels()

    def actualizar_labels(self):
        # Usa setText() para cambiar el texto de los labels
        self.ui.label.setText(f"Distancia: {self.Distancia}cm")
        self.ui.label_2.setText(self.Alerta)

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
    window = MainWindow() #crea una intancia de MainWindow 
    window.show() # IMPORTANT!!!!! la ventanas estan ocultas por defecto.
    sys.exit(app.exec()) # Start the event loop.

# Never gonna give you up