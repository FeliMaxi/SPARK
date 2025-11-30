import sys
import os
import time
import serial
import serial.tools.list_ports
import requests
import platform
import smtplib
from email.mime.text import MIMEText
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QTimer, QEvent, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QMessageBox 

# === IMPORTACIÓN DE UI ===
from UI_Spark import Ui_SparkWindow
from UI_Inicio import Ui_InicioScreen
from UI_Config import Ui_ConfigWindow


# --- CONFIGURACIÓN DE CORREO ELECTRÓNICO ---
SMTP_SERVER = 'smtp.gmail.com' 
SMTP_PORT = 587
EMAIL_SENDER = "sparkprojectitsv@gmail.com"
EMAIL_PASSWORD = 'ikmi wiqq iqxr eqpw' 
EMAIL_RECEIVER = 'f.arias@itsv.edu.ar' 


def enviar_correo_notificacion(limite_rojo, limite_amarillo):
    """Envía un correo electrónico notificando los nuevos límites establecidos."""
    
    if EMAIL_SENDER == 'tu_correo@gmail.com':
        print("\nADVERTENCIA CORREO: Las credenciales de correo no han sido configuradas. Correo de notificación omitido.")
        return False
        
    subject = "NOTIFICACIÓN SPARK: Nuevos Límites Establecidos"
    body = f"""
    Estimado usuario,

    Se han actualizado los límites de proximidad en el sistema SPARK.

    Nuevos Valores:
    - Límite Rojo (Peligro Inminente): {limite_rojo} cm
    - Límite Amarillo (Advertencia/Perfecto): {limite_amarillo} cm

    Fecha y Hora del cambio: {time.strftime('%Y-%m-%d %H:%M:%S')}

    Estos nuevos parámetros regirán la lógica de alerta del sistema y los LEDs del Arduino.

    Saludos,
    Sistema de Notificaciones SPARK
    """

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER

    try:
        # 1. Conexión y protocolo TLS
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        
        # 2. Inicio de sesión
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        
        # 3. Envío del correo
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        server.quit()
        print(f"DEBUG: Correo de notificación enviado a {EMAIL_RECEIVER}")
        return True
    except smtplib.SMTPAuthenticationError:
        print("\nERROR CORREO: Fallo de autenticación. Verifica EMAIL_SENDER y EMAIL_PASSWORD (¿Usaste Clave de Aplicación si usas Gmail?).")
        return False
    except Exception as e:
        print(f"\nERROR CORREO: No se pudo enviar el correo: {e}")
        return False


# --- PARTE 1: Funciones de Conexión y Clima ---

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
            print("Error API clima. Código:", response.status_code)
            return "Clima: error API"
    except requests.exceptions.RequestException as e:
        print("Error de red obteniendo clima:", e)
        return "Clima: sin conexión"
    except Exception as e:
        print("Error inesperado obteniendo clima:", e)
        return "Clima: error"


# --- PARTE 2: Ventana de Configuración ---

class ConfigWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ConfigWindow()
        self.ui.setupUi(self)
        self.parent_window = parent

        # Establecer valores iniciales en los SpinBox
        if parent:
            self.ui.spinBox.setValue(parent.limite_rojo)
            self.ui.spinBox_2.setValue(parent.limite_amarillo)

        self.ui.pushButton.clicked.connect(self.aplicar_parametros)

    def aplicar_parametros(self):
        """
        Lee los valores de los SpinBox, los aplica, envía al Arduino 
        y envía la notificación por correo.
        """
        if not self.parent_window:
            return

        limite_rojo = self.ui.spinBox.value()
        limite_amarillo = self.ui.spinBox_2.value()

        if limite_rojo >= limite_amarillo:
            QMessageBox.warning(self, "Error de Configuración", 
                                 "El Límite Rojo debe ser estrictamente menor que el Límite Amarillo.")
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
        
        # 3. **ENVÍO DE CORREO DE NOTIFICACIÓN**
        enviar_correo_notificacion(limite_rojo, limite_amarillo)

        print(f"Nuevos límites aplicados en Python: rojo={limite_rojo} cm, amarillo={limite_amarillo} cm")

        # 4. Vuelve a la pantalla principal
        self.close()
        self.parent_window.show()


# --- PARTE 3: Ventana Principal ---

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_SparkWindow() 
        self.ui.setupUi(self)

        # Variables de límites (De Versión A, ahora configurables)
        self.limite_rojo = 10 # Valor por defecto
        self.limite_amarillo = 20 # Valor por defecto

        # Variables de estado y clima
        self.Distancia = 0
        self.Alerta = "Cargando..."
        self.clima = obtener_clima()

        # Buffer para promedio móvil
        self.lecturas = []
        self.max_lecturas = 5

        # Tiempo de la última lectura válida
        self.ultimo_dato_time = None
        self.timeout_sin_datos = 3

        # Conexión Arduino
        puerto = detectar_puerto_arduino()
        if puerto:
            try:
                self.arduino = serial.Serial(puerto, 9600, timeout=0.1) 
                time.sleep(2) 
                self.arduino.flushInput() 
                print(f" Conectado al Arduino en {puerto}")
                
                # Enviar límites iniciales al Arduino (importante al inicio)
                self.enviar_limites_a_arduino()
            
            except serial.SerialException as e:
                if platform.system() == 'Linux' and 'Permission denied' in str(e):
                    print(f"\n¡ADVERTENCIA DE LINUX! Falta permiso para acceder al puerto {puerto}. Use 'sudo usermod -a -G dialout $USER'")
                else:
                    print(f" No se pudo abrir el puerto {puerto} del Arduino: {e}")
                self.arduino = None
                self.Alerta = "Arduino no conectado"
        else:
            print(" No se detectó Arduino conectado.")
            self.arduino = None
            self.Alerta = "Arduino no conectado"

        # Timer para lectura de datos (200ms)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar_datos)
        self.timer.start(200) 

        # Timer para actualizar el clima
        self.timer_clima = QTimer(self)
        self.timer_clima.timeout.connect(self.actualizar_clima)
        self.timer_clima.start(600000)

        # Conectar botón de configuración
        self.ui.configButton.clicked.connect(self.abrir_config) 
        
        self.actualizar_labels()


    def enviar_limites_a_arduino(self):
        """Función auxiliar para enviar límites al Arduino, usada al iniciar."""
        if self.arduino and self.arduino.is_open:
            try:
                mensaje = f"L{self.limite_rojo}:{self.limite_amarillo}\n"
                self.arduino.write(mensaje.encode('utf-8'))
                print(f"DEBUG: Enviado límites iniciales a Arduino: {mensaje.strip()}")
            except Exception as e:
                print(f"DEBUG: Error al enviar límites iniciales: {e}")

    def abrir_config(self):
        """Abre la ventana de configuración y oculta la actual."""
        self.config_window = ConfigWindow(self)
        self.config_window.show()
        self.hide()

    # === Lectura y Filtrado de datos desde Arduino ===
    def actualizar_datos(self):
        """Lee datos del Arduino, los filtra y actualiza la UI."""
        
        if self.arduino and self.arduino.in_waiting > 0:
            try:
                linea_serial = self.arduino.readline() 
                dato_str = linea_serial.decode('utf-8').strip()
                
                if dato_str.startswith('D'):
                    distancia_data = dato_str[1:] 
                else:
                    distancia_data = dato_str

                if distancia_data.isdigit():
                    distancia = int(distancia_data)
                    
                    # 1. Aplicar Filtro de Promedio Móvil
                    if distancia < 0 or distancia > 800:
                        return 

                    self.lecturas.append(distancia)
                    if len(self.lecturas) > self.max_lecturas:
                        self.lecturas.pop(0)

                    distancia_filtrada = sum(self.lecturas) / len(self.lecturas)
                    self.Distancia = distancia_filtrada
                    self.Alerta = self.calcular_alerta(distancia_filtrada)
                    self.ultimo_dato_time = time.time() 

                elif dato_str:
                    if not dato_str.startswith('L'): # Ignorar mensajes de límites
                        print(f"DEBUG: Mensaje Serial Ignorado: {dato_str}")

            except UnicodeDecodeError:
                print("DEBUG: Error de decodificación Unicode. Dato ignorado.")
            except Exception as e:
                print(f"DEBUG: Error inesperado en lectura serial: {e}")
                self.Alerta = "Error de lectura"
        
        # Lógica de timeout
        elif self.arduino and self.ultimo_dato_time is not None:
            if time.time() - self.ultimo_dato_time > self.timeout_sin_datos:
                self.Alerta = "Sin datos recientes"
                self.Distancia = 0 

        self.actualizar_labels()


    # === Cálculo de alerta según límites dinámicos ===
    def calcular_alerta(self, distancia):
        """Evalúa la distancia usando los límites configurables (rojo, amarillo)."""
        distance = float(distancia)

        if distance > self.limite_amarillo:
            return "Muy lejos"
        elif self.limite_amarillo >= distance > self.limite_rojo:
            return "Perfecto / Baja la velocidad"
        elif distance <= self.limite_rojo:
            return "Muy cerca / Cuidado"
        else:
            return "Sin datos"


    # === Actualizar la interfaz ===
    def actualizar_labels(self):
        """Actualiza los QLabel con los últimos datos."""
        
        try:
            if isinstance(self.Distancia, float):
                distancia_str = f"{self.Distancia:.2f}"
            else:
                distancia_str = str(int(self.Distancia))
        except (ValueError, TypeError):
             distancia_str = "N/A"

        self.ui.label.setText(f"Distancia: {distancia_str} cm")
        self.ui.label_2.setText(self.Alerta)
        self.ui.label_3.setText(f"Clima: {self.clima}")

        # Forzar repintado
        self.ui.label.repaint()
        self.ui.label_2.repaint()
        self.ui.label_3.repaint()

    def actualizar_clima(self):
        self.clima = obtener_clima()
        self.actualizar_labels()


# --- PARTE 4: Pantalla de Inicio ---

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
            print(" No se encontró la imagen:", ruta_logo)
        self.logo_label.setPixmap(pixmap)
        self.logo_label.setScaledContents(True)
        self.logo_label.setGeometry(self.ui.frame.rect())

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


# --- EJECUCIÓN ---

print("""
    _____ ____ ___    ____  __ __
  / ___// __ \/   |  / __ \/ //_/
  \__ \\/ /_/ / / | | / /_/ / ,< 
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