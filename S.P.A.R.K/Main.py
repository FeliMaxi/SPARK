# -*- coding: utf-8 -*-
import sys
import time
import os
import serial
import requests
import platform
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QTimer, QEvent
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel

# === IMPORTACIÓN DE UI ===
from UI_Spark import Ui_MainWindow
from UI_Inicio import Ui_InicioScreen

# === CONFIGURACIÓN CLIMA ===
API_KEY = 'c01a0cfb38073ea9a2b467ebd0287997'
CIUDAD = "Cordoba,AR"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CIUDAD}&appid={API_KEY}&units=metric&lang=es"


def obtener_clima():
    """Obtiene el clima actual y devuelve un texto para mostrar."""
    try:
        response = requests.get(URL, timeout=5)
        if response.status_code == 200:
            data = response.json()
            temp = data["main"]["temp"]
            descripcion = data["weather"][0]["description"]
            return f"{temp}°C — {descripcion.capitalize()}"
        else:
            return "Sin datos"
    except Exception as e:
        print("Error obteniendo clima:", e)
        return "Sin datos"


# === FUNCIÓN PARA DETECTAR SISTEMA OPERATIVO Y PUERTO ===
def puerto_arduino():
    """Devuelve el nombre del puerto correcto según el sistema operativo."""
    sistema = platform.system()
    if sistema == "Windows":
        return "COM3"  # ⚠️ Cambiar si tu Arduino usa otro COM
    elif sistema == "Linux":
        return "/dev/ttyACM0"
    else:
        print("⚠️ Sistema operativo no reconocido. Usando /dev/ttyACM0 por defecto.")
        return "/dev/ttyACM0"


# === VENTANA PRINCIPAL ===
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Variables iniciales
        self.Distancia = 0
        self.Alerta = "Sin datos"
        self.clima = obtener_clima()

        # Intentar conectar con Arduino según la plataforma
        try:
            puerto = puerto_arduino()
            print(f"Intentando conectar al Arduino en {puerto}...")
            self.arduino = serial.Serial(puerto, 9600)
            time.sleep(2)
            print("✅ Conectado a Arduino correctamente.")
        except Exception as e:
            print("⚠️ No se pudo conectar al Arduino:", e)
            self.arduino = None

        # Timer para leer datos del Arduino
        self.timer = QTimer()
        self.timer.timeout.connect(self.actualizar_datos)
        self.timer.start(200)

        # Timer para actualizar el clima cada 10 minutos
        self.timer_clima = QTimer()
        self.timer_clima.timeout.connect(self.actualizar_clima)
        self.timer_clima.start(600000)

        self.actualizar_labels()

    # === Actualizar la interfaz ===
    def actualizar_labels(self):
        self.ui.label.setText(f"Distancia: {int(self.Distancia/10)} cm")
        self.ui.label_2.setText(self.Alerta)
        self.ui.label_3.setText(f"Clima: {self.clima}")
        self.ui.label.repaint()
        self.ui.label_2.repaint()
        self.ui.label_3.repaint()

    # === Lectura de datos desde Arduino ===
    def actualizar_datos(self):
        if self.arduino and self.arduino.in_waiting > 0:
            try:
                linea = self.arduino.readline().decode(errors="ignore").strip()
                print("Dato recibido:", linea)  # 👈 DEBUG
                if linea.isdigit():
                    distancia = int(linea)
                    alerta = self.calcular_alerta(distancia)
                    self.Distancia = distancia
                    self.Alerta = alerta
                    self.actualizar_labels()
            except Exception as e:
                print("Error leyendo del Arduino:", e)

    # === Cálculo de alerta según distancia ===
    def calcular_alerta(self, distancia):
        distance = distancia / 10
        if distance > 20:
            return 'Muy lejos'
        elif 20 >= distance > 10:
            return 'Baja la velocidad'
        elif 10 >= distance > 0:
            return 'Cuidado'
        elif 0 >= distance:
            return 'R.I.P'
        else:
            return 'Sin datos'

    # === Actualiza el clima periódicamente ===
    def actualizar_clima(self):
        self.clima = obtener_clima()
        self.actualizar_labels()


# === PANTALLA DE INICIO ===
class Inicioscreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_InicioScreen()
        self.ui.setupUi(self)

        # === Imagen dentro del frame ===
        ruta_logo = os.path.join(os.path.dirname(__file__), "SPARK.png")
        self.logo_label = QLabel(self.ui.frame)
        pixmap = QPixmap(ruta_logo)
        if pixmap.isNull():
            print("⚠️ No se encontró la imagen:", ruta_logo)
        self.logo_label.setPixmap(pixmap)
        self.logo_label.setScaledContents(True)
        self.logo_label.setGeometry(self.ui.frame.rect())

        # Para redimensionar automáticamente con el frame
        self.ui.frame.installEventFilter(self)

        # Botón para abrir la ventana principal
        self.ui.startButton.clicked.connect(self.ir_a_principal)

    def eventFilter(self, source, event):
        """Ajusta el tamaño del logo cuando se cambia el tamaño del frame."""
        if source == self.ui.frame and event.type() == QEvent.Resize:
            self.logo_label.setGeometry(self.ui.frame.rect())
        return super().eventFilter(source, event)

    def ir_a_principal(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()


# === ASCII ART ===
print("""
   _____ ____  ___    ____  __ __
  / ___// __ \/   |  / __ \/ //_/
  \__ \/ /_/ / /| | / /_/ / ,<   
 ___/ / ____/ ___ |/ _, _/ /| |  
/____/_/   /_/  |_/_/ |_/_/ |_|  
Sensor de Proximidad Automático 
    para Riesgos Kinéticos                             
""")


# === MAIN ===
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Inicioscreen()
    window.show()
    sys.exit(app.exec())

# Never gonna give you up
