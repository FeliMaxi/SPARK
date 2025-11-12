import sys
import serial
import serial.tools.list_ports
import requests
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
from UI_Spark import Ui_SparkWindow
from UI_Inicio import Ui_InicioScreen
from UI_Config import Ui_ConfigWindow


# === FUNCIÓN PARA DETECTAR AUTOMÁTICAMENTE EL PUERTO ARDUINO ===
def detectar_puerto_arduino():
    puertos = serial.tools.list_ports.comports()
    for p in puertos:
        if "Arduino" in p.description or "CH340" in p.description or "USB" in p.description:
            return p.device
    return None

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
    clm = "Sin datos"


# === VENTANA CONFIGURACIÓN ===
class ConfigWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ConfigWindow()
        self.ui.setupUi(self)
        self.parent_window = parent

        # Configurar botón "Confirmar" para aplicar parámetros y volver
        self.ui.pushButton.clicked.connect(self.aplicar_parametros)

    def aplicar_parametros(self):
        """Lee los valores de los SpinBox y los aplica a la ventana Spark."""
        if not self.parent_window:
            return

        limite_rojo = self.ui.spinBox.value()
        limite_amarillo = self.ui.spinBox_2.value()

        # Validar coherencia
        if limite_rojo >= limite_amarillo:
            print("El límite rojo debe ser menor que el amarillo.")
            return

        # Enviar los límites a Spark
        self.parent_window.limite_rojo = limite_rojo
        self.parent_window.limite_amarillo = limite_amarillo

        print(f"Nuevos límites aplicados: rojo={limite_rojo} cm, amarillo={limite_amarillo} cm")

        # Volver a Spark
        self.close()
        self.parent_window.show()



# === MAIN WINDOW ===
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_SparkWindow()
        self.ui.setupUi(self)

        self.clima = clm
        self.ui.label_3.setText(f"Clima: {self.clima}")

        # Límites por defecto
        self.limite_rojo = 20
        self.limite_amarillo = 40

        # Botón que abre la ventana de configuración
        self.ui.configButton.clicked.connect(self.abrir_config)

        # === Conexión Arduino ===
        puerto = detectar_puerto_arduino()
        if puerto:
            try:
                self.arduino = serial.Serial(puerto, 9600, timeout=1)
                print(f"Conectado al Arduino en {puerto}")
            except serial.SerialException:
                print("No se pudo abrir el puerto del Arduino.")
                self.arduino = None
        else:
            print("No se detectó Arduino conectado.")
            self.arduino = None

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.leer_dato)
        self.timer.start(500)

    def abrir_config(self):
        """Abre la ventana de configuración y oculta la actual."""
        self.config_window = ConfigWindow(self)
        self.config_window.show()
        self.hide()

    def leer_dato(self):
        if self.arduino and self.arduino.in_waiting > 0:
            dato = self.arduino.readline().decode('utf-8').strip()
            if dato.isdigit():
                distancia = int(dato)
                self.actualizar_distancia(distancia)

    def actualizar_distancia(self, distancia):
        """Evalúa la distancia según los límites configurados."""
        self.ui.label.setText(f"{distancia} cm")

        if distancia > self.limite_amarillo:
            alerta = "Muy lejos"
        elif self.limite_amarillo >= distancia > self.limite_rojo:
            alerta = "Perfecto"
        elif distancia <= self.limite_rojo:
            alerta = "Muy cerca"
        else:
            alerta = "Sin datos"

        self.ui.label_2.setText(alerta)


# === INICIO SCREEN ===
class Inicioscreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_InicioScreen()
        self.ui.setupUi(self)

        # Mostrar imagen SPARK.png dentro del frame
        self.logo_label = QLabel(self.ui.frame)
        pixmap = QPixmap("SPARK.png")
        self.logo_label.setPixmap(pixmap)
        self.logo_label.setScaledContents(True)
        self.logo_label.setGeometry(self.ui.frame.rect())
        self.ui.frame.installEventFilter(self)

        # Conectar el botón para ir al principal
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Inicioscreen()
    window.show()
    sys.exit(app.exec())


