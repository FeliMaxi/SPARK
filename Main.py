import sys
import serial
import serial.tools.list_ports
import requests
import time
import smtplib
import platform
from email.mime.text import MIMEText 
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
from UI_Spark import Ui_SparkWindow
from UI_Inicio import Ui_InicioScreen
from UI_Config import Ui_ConfigWindow

SMTP_SERVER = 'smtp.gmail.com' 
SMTP_PORT = 587
EMAIL_SENDER = "sparkprojectitsv@gmail.com"
EMAIL_PASSWORD = 'ikmi wiqq iqxr eqpw' 
EMAIL_RECEIVER = 'f.arias@itsv.edu.ar' 

def enviar_notificacion_limites(limite_rojo, limite_amarillo):
    """
    Envía una notificación por correo electrónico con los nuevos límites.
    """
    
    asunto = f" SPARK: Límites de Alerta Actualizados"
    cuerpo = (
        f"Estimado/a usuario/a,\n\n"
        f"Se ha establecido una nueva configuración en el sistema SPARK:\n"
        f"- Límite Rojo (Máximo Peligro): {limite_rojo} cm\n"
        f"- Límite Amarillo (Advertencia): {limite_amarillo} cm\n\n"
        f"El sistema está operando ahora con estos nuevos valores.\n"
        f"Atentamente,\nEl equipo SPARK."
    )
    
    msg = MIMEText(cuerpo)
    msg['Subject'] = asunto
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        server.quit()
        print(" CORREO: Notificación de límites enviada correctamente.")
    except Exception as e:
        print(f" CORREO: Falló el envío de la notificación. Error: {e}")


# === FUNCIÓN PARA DETECTAR AUTOMÁTICAMENTE EL PUERTO ARDUINO ===
def detectar_puerto_arduino():
    """Detecta el puerto donde está conectado un Arduino, CH340, o dispositivo USB genérico."""
    puertos = serial.tools.list_ports.comports()
    for p in puertos:
        # Compatibilidad con Linux/macOS
        if platform.system() == "Linux" and ("ttyACM" in p.device or "ttyUSB" in p.device):
             return p.device

        # Compatibilidad universal/Windows
        if "Arduino" in p.description or "CH340" in p.description or "USB" in p.description:
            return p.device

    return None

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

        self.ui.pushButton.clicked.connect(self.aplicar_parametros)

    def aplicar_parametros(self):
        """
        Lee los valores de los SpinBox, los aplica a la ventana Spark
        y los envía al Arduino para actualizar la lógica de los LEDs.
        """
        if not self.parent_window:
            return

        limite_rojo = self.ui.spinBox.value()
        limite_amarillo = self.ui.spinBox_2.value()

        if limite_rojo >= limite_amarillo:
            print("El límite rojo debe ser menor que el amarillo.")
            return

        # 1. Asigna los nuevos límites a la ventana principal de Python (para la UI)
        self.parent_window.limite_rojo = limite_rojo
        self.parent_window.limite_amarillo = limite_amarillo

        # 2. **ENVÍO DE LÍMITES AL ARDUINO**
        if self.parent_window.arduino and self.parent_window.arduino.is_open:
            try:
                mensaje = f"L{limite_rojo}:{limite_amarillo}\n"
                self.parent_window.arduino.write(mensaje.encode('utf-8'))
                print(f"DEBUG: Enviado a Arduino: {mensaje.strip()}")
            except Exception as e:
                print(f"DEBUG: Error al enviar límites al Arduino: {e}")
        
        print(f"Nuevos límites aplicados en Python: rojo={limite_rojo} cm, amarillo={limite_amarillo} cm")

        # 3. Vuelve a la pantalla principal
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

        
        self.limite_rojo = 20
        self.limite_amarillo = 40

        # Botón que abre la ventana de configuración
        self.ui.configButton.clicked.connect(self.abrir_config)

        # === Conexión Arduino ===
        puerto = detectar_puerto_arduino()
        if puerto:
            try:
                # CAMBIO 1: Reducción del timeout a 0.1 segundos para evitar bloqueos largos
                self.arduino = serial.Serial(puerto, 9600, timeout=0.1) 
                print(f"Conectado al Arduino en {puerto}")
                
                time.sleep(2) 
                self.arduino.flushInput() 
                
            except serial.SerialException:
                print("No se pudo abrir el puerto del Arduino.")
                self.arduino = None
        else:
            print("No se detectó Arduino conectado.")
            self.arduino = None

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.leer_dato)
        # CAMBIO 2: Aumento de la frecuencia del timer a 200ms
        self.timer.start(200) 

    def abrir_config(self):
        """Abre la ventana de configuración y oculta la actual."""
        self.config_window = ConfigWindow(self)
        self.config_window.show()
        self.hide()

    def leer_dato(self):
        if self.arduino and self.arduino.in_waiting > 0:
            try:
                # En este contexto, leer una línea a la vez es suficiente con el timeout bajo.
                linea_serial = self.arduino.readline() 
                dato_str = linea_serial.decode('utf-8').strip()
                
                # PROTOCOLO ESTRICTO CON PREFIJO 'D'
                if dato_str.startswith('D'):
                    distancia_data = dato_str[1:] 
                    
                    if distancia_data.isdigit():
                        distancia = int(distancia_data)
                        self.actualizar_distancia(distancia)
                    else:
                        print(f"DEBUG: Error -> Dato después del prefijo 'D' no es numérico: {distancia_data}. Ignorado.")
                
                else:
                    if dato_str:
                         print(f"DEBUG: Mensaje Serial Ignorado: {dato_str}")

            except UnicodeDecodeError:
                print("DEBUG: Error de decodificación Unicode. Dato ignorado.")
            except Exception as e:
                print(f"DEBUG: Error inesperado en lectura serial: {e}")


    def actualizar_distancia(self, distancia):
        """Evalúa la distancia según los límites configurados y actualiza la UI."""
        self.ui.label.setText(f"{distancia} cm")

        # Lógica de la UI que usa los límites dinámicos
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
   / ___// __ \/  |  / __ \/ //_/
   \__ \\/ /_/ / /| | / /_/ / ,<   
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