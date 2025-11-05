import sys
import requests
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget

# Interfaces importadas
from UI_Spark import Ui_MainWindow
from UI_Inicio import Ui_InicioScreen
from UI_Planes import Ui_PlanesScreen


# === DISTANCIA ===
Distance = 20
if Distance > 20:
    Alert = 'Muy lejos'
elif 20 >= Distance > 10:
   Alert = 'Baja la velocidad'
elif 10 >= Distance >0:
    Alert = 'Cuidado'
elif 0 >= Distance:
    Alert = 'R.I.P'
else:
    Alert = 'Sin datos'


# === CLIMA ===
API_KEY = 'c01a0cfb38073ea9a2b467ebd0287997'
CIUDAD = "Cordoba,AR"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CIUDAD}&appid={API_KEY}&units=metric&lang=es"

response = requests.get(URL)
data = response.json()

if response.status_code == 200:
    temp = data["main"]["temp"]
    descripcion = data["weather"][0]["description"]
    clima = f"{temp}°C — {descripcion.capitalize()}"
    clm = "Clima actual: " + clima
else:
    clm = "Error al obtener el clima"


# === MAIN WINDOW ===
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.label.setText(f"Distancia: {Distance} cm")
        self.ui.label_2.setText(Alert)
        self.ui.label_3.setText(clm)


# === RICKROLL WINDOW ===
class RickrollScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SPARK Premium 💎")
        self.resize(800, 450)

        layout = QVBoxLayout(self)

        # Video player setup
        self.videoWidget = QVideoWidget()
        layout.addWidget(self.videoWidget)

        self.player = QMediaPlayer(self)
        self.audio = QAudioOutput(self)
        self.player.setAudioOutput(self.audio)
        self.player.setVideoOutput(self.videoWidget)

        # Ruta al archivo (asegúrate de que exista)
        video_url = QUrl.fromLocalFile("???.mp4")
        self.player.setSource(video_url)
        self.player.play()

        # Cierra la ventana cuando termina el video
        self.player.mediaStatusChanged.connect(self.check_end)

    def check_end(self, status):
        from PySide6.QtMultimedia import QMediaPlayer
        if status == QMediaPlayer.EndOfMedia:
            self.close()


# === PLANES SCREEN ===
class PlanesScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_PlanesScreen()
        self.ui.setupUi(self)

        # Conectar los botones
        self.ui.btn_estandar.clicked.connect(self.ir_a_principal)
        self.ui.btn_premium.clicked.connect(self.abrir_rickroll)

    def ir_a_principal(self):
        self.main = MainWindow()
        self.main.show()
        self.close()

    def abrir_rickroll(self):
        self.rickroll = RickrollScreen()
        self.rickroll.show()
        self.close()


# === INICIO SCREEN ===
class Inicioscreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_InicioScreen()
        self.ui.setupUi(self)

        # Mostrar el logo SPARK
        self.logo_label = QLabel(self.ui.frame)
        pixmap = QPixmap("SPARK.png")
        self.logo_label.setPixmap(pixmap)
        self.logo_label.setScaledContents(True)
        self.logo_label.setGeometry(self.ui.frame.rect())

        # Conexión del botón Start
        self.ui.startButton.clicked.connect(self.ir_a_planes)

    def ir_a_planes(self):
        self.planes = PlanesScreen()
        self.planes.show()
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

