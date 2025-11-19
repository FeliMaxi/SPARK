import sys
import os
import time
import serial
import serial.tools.list_ports # Necesario para detectar_puerto_arduino
import requests
import platform
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QTimer, QEvent, Qt # Importar Qt para alineación si se necesita
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QMessageBox # Importar QMessageBox para notificaciones de error

# === IMPORTACIÓN DE UI ===
from UI_Spark import Ui_SparkWindow # Versión A usa Ui_SparkWindow
from UI_Inicio import Ui_InicioScreen
from UI_Config import Ui_ConfigWindow # Necesario para la ventana de configuración


# --- PARTE 1: Funciones de Conexión y Clima ---

# === FUNCIÓN PARA DETECTAR AUTOMÁTICAMENTE EL PUERTO ARDUINO (Mejor de Versión A) ===
def detectar_puerto_arduino():
    """Detecta el puerto donde está conectado un Arduino, CH340, o dispositivo USB genérico."""
    puertos = serial.tools.list_ports.comports()
    for p in puertos:
        # La detección basada en descripción es más robusta que COMx fijo.
        if "Arduino" in p.description or "CH340" in p.description or ("USB" in p.description and platform.system() != "Linux"):
            return p.device
        # Para Linux, ttyACM0 y ttyUSB0 son comunes, se pueden añadir si no se detecta por descripción
        if platform.system() == "Linux" and ("ttyACM" in p.device or "ttyUSB" in p.device):
            return p.device
    return None

# === CONFIGURACIÓN CLIMA ===
API_KEY = 'c01a0cfb38073ea9a2b467ebd0287997'
CIUDAD = "Cordoba,AR"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CIUDAD}&appid={API_KEY}&units=metric&lang=es"


def obtener_clima():
    """Obtiene el clima actual y devuelve un texto para mostrar (Mejor de Versión B)."""
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


# --- PARTE 2: Ventana de Configuración (De Versión A) ---

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
        Lee los valores de los SpinBox, los aplica a la ventana Spark
        y los envía al Arduino.
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
        # Se envía una cadena de texto para que el Arduino actualice sus umbrales
        if self.parent_window.arduino and self.parent_window.arduino.is_open:
            try:
                # Protocolo 'L' de Versión A
                mensaje = f"L{limite_rojo}:{limite_amarillo}\n" 
                self.parent_window.arduino.write(mensaje.encode('utf-8'))
                print(f"DEBUG: Enviado a Arduino: {mensaje.strip()}")
            except Exception as e:
                print(f"DEBUG: Error al enviar límites al Arduino: {e}")
        
        print(f"Nuevos límites aplicados en Python: rojo={limite_rojo} cm, amarillo={limite_amarillo} cm")

        # 3. Vuelve a la pantalla principal
        self.close()
        self.parent_window.show()


# --- PARTE 3: Ventana Principal (Combinando ambas) ---

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Se usa Ui_SparkWindow de Versión A (asumiendo que tiene el botón de config)
        self.ui = Ui_SparkWindow() 
        self.ui.setupUi(self)

        # Variables de límites (De Versión A, ahora configurables)
        self.limite_rojo = 10 # Valor por defecto
        self.limite_amarillo = 20 # Valor por defecto

        # Variables de estado y clima
        self.Distancia = 0
        self.Alerta = "Cargando..."
        self.clima = obtener_clima()

        # Buffer para promedio móvil (De Versión B)
        self.lecturas = []
        self.max_lecturas = 5

        # Tiempo de la última lectura válida (De Versión B)
        self.ultimo_dato_time = None
        self.timeout_sin_datos = 3

        # Conexión Arduino
        puerto = detectar_puerto_arduino()
        if puerto:
            try:
                # Usar timeout bajo de Versión A
                self.arduino = serial.Serial(puerto, 9600, timeout=0.1) 
                time.sleep(2) # Espera por si el Arduino se reinicia
                self.arduino.flushInput() 
                print(f"✅ Conectado al Arduino en {puerto}")
                
                # Enviar límites iniciales al Arduino (importante al inicio)
                self.enviar_limites_a_arduino()
            
            except serial.SerialException as e:
                print(f"⚠️ No se pudo abrir el puerto {puerto} del Arduino: {e}")
                self.arduino = None
                self.Alerta = "Arduino no conectado"
        else:
            print("⚠️ No se detectó Arduino conectado.")
            self.arduino = None
            self.Alerta = "Arduino no conectado"

        # Timer para lectura de datos (De Versión A, 200ms)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar_datos)
        self.timer.start(200) 

        # Timer para actualizar el clima cada 10 minutos (De Versión B)
        self.timer_clima = QTimer(self)
        self.timer_clima.timeout.connect(self.actualizar_clima)
        self.timer_clima.start(600000)

        # Conectar botón de configuración (De Versión A)
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
        """Abre la ventana de configuración y oculta la actual (De Versión A)."""
        self.config_window = ConfigWindow(self)
        self.config_window.show()
        self.hide()

    # === Lectura y Filtrado de datos desde Arduino (Combinación A y B) ===
    def actualizar_datos(self):
        """Lee datos del Arduino, los filtra y actualiza la UI."""
        
        if self.arduino and self.arduino.in_waiting > 0:
            try:
                linea_serial = self.arduino.readline() 
                dato_str = linea_serial.decode('utf-8').strip()
                
                # PROTOCOLO: El Arduino DEBE enviar el dato con el prefijo 'D' o solo el número
                # Priorizaremos el uso del número limpio o el protocolo 'D' de Versión A
                
                if dato_str.startswith('D'):
                    distancia_data = dato_str[1:] 
                else:
                    distancia_data = dato_str

                if distancia_data.isdigit():
                    distancia = int(distancia_data)
                    
                    # 1. Aplicar Filtro de Promedio Móvil (De Versión B)
                    if distancia < 0 or distancia > 800:
                        return # Ignorar valores fuera de rango

                    self.lecturas.append(distancia)
                    if len(self.lecturas) > self.max_lecturas:
                        self.lecturas.pop(0)

                    distancia_filtrada = sum(self.lecturas) / len(self.lecturas)
                    self.Distancia = distancia_filtrada
                    self.Alerta = self.calcular_alerta(distancia_filtrada)
                    self.ultimo_dato_time = time.time() # Guardar hora del último dato bueno

                elif dato_str:
                    # Ignorar mensajes de depuración o de límite
                    if not dato_str.startswith('L'):
                        print(f"DEBUG: Mensaje Serial Ignorado: {dato_str}")

            except UnicodeDecodeError:
                print("DEBUG: Error de decodificación Unicode. Dato ignorado.")
            except Exception as e:
                print(f"DEBUG: Error inesperado en lectura serial: {e}")
                self.Alerta = "Error de lectura"
        
        # Lógica de timeout (De Versión B)
        elif self.arduino and self.ultimo_dato_time is not None:
             if time.time() - self.ultimo_dato_time > self.timeout_sin_datos:
                self.Alerta = "Sin datos recientes"
                self.Distancia = 0 # Opcional: Resetear Distancia

        self.actualizar_labels()


    # === Cálculo de alerta según límites dinámicos (Combinando A y B) ===
    def calcular_alerta(self, distancia):
        """Evalúa la distancia usando los límites configurables (rojo, amarillo)."""
        distance = float(distancia)

        # Lógica de Versión A, usando los límites configurables
        if distance > self.limite_amarillo:
            return "Muy lejos"
        elif self.limite_amarillo >= distance > self.limite_rojo:
            return "Perfecto / Baja la velocidad" # Combinando las ideas
        elif distance <= self.limite_rojo:
            return "Muy cerca / Cuidado"
        else:
            return "Sin datos" # Caso por defecto o error


    # === Actualizar la interfaz (De Versión B con mejoras) ===
    def actualizar_labels(self):
        """Actualiza los QLabel con los últimos datos."""
        
        # Distancia: Mostrar solo 2 decimales o entero
        try:
            if isinstance(self.Distancia, float):
                distancia_str = f"{self.Distancia:.2f}"
            else:
                distancia_str = str(int(self.Distancia))
        except (ValueError, TypeError):
             distancia_str = "N/A"

        self.ui.label.setText(f"Distancia: {distancia_str} cm")

        # Mensaje de alerta
        self.ui.label_2.setText(self.Alerta)

        # Clima
        self.ui.label_3.setText(f"Clima: {self.clima}")

        # Forzar repintado
        self.ui.label.repaint()
        self.ui.label_2.repaint()
        self.ui.label_3.repaint()

    def actualizar_clima(self):
        self.clima = obtener_clima()
        self.actualizar_labels()


# --- PARTE 4: Pantalla de Inicio (De Versión B) ---

class Inicioscreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_InicioScreen()
        self.ui.setupUi(self)

        # === Imagen dentro del frame ===
        # Mejor manejo de ruta de imagen (De Versión B)
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


# --- PARTE 5: Ejecución ---

# === ASCII ART ===
print("""
    _____ ____  ___   ____  __ __
  / ___// __ \/   | / __ \/ //_/
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