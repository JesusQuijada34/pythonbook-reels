import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QGroupBox, QMenuBar, QAction, QStatusBar, QFileDialog,
    QMessageBox, QProgressBar, QComboBox
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QThread, pyqtSignal

# Verifica si yt-dlp está instalado
try:
    import yt_dlp
    YTDLP_AVAILABLE = True
except ImportError:
    YTDLP_AVAILABLE = False

class DownloadThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, url, folder, format_code):
        super().__init__()
        self.url = url
        self.folder = folder
        self.format_code = format_code

    def run(self):
        if not YTDLP_AVAILABLE:
            self.error.emit("yt-dlp no está instalado. Instálalo con 'pip install yt-dlp'.")
            return
        try:
            ydl_opts = {
                'outtmpl': os.path.join(self.folder, '%(title)s.%(ext)s'),
                'format': self.format_code,
                'progress_hooks': [self.hook],
                'quiet': True,
            }
            self._last_progress = 0
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=True)
            output_file = ydl.prepare_filename(info)
            self.progress.emit(100)
            self.finished.emit(output_file)
        except Exception as e:
            self.error.emit(str(e))

    def hook(self, d):
        if d['status'] == 'downloading':
            percent = d.get('percent', 0)
            self.progress.emit(int(percent))
        elif d['status'] == 'finished':
            self.progress.emit(100)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PythonBook Reels Downloader")
        self.setWindowIcon(QIcon(os.path.join("app", "app-icon.ico")))
        self.resize(520, 340)
        self.init_ui()

    def init_ui(self):
        # Menubar
        menubar = self.menuBar()
        file_menu = menubar.addMenu("&Archivo")
        help_menu = menubar.addMenu("&Ayuda")

        exit_action = QAction("Salir", self)
        exit_action.setIcon(QIcon.fromTheme("application-exit"))
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        about_action = QAction("Acerca de", self)
        about_action.setIcon(QIcon.fromTheme("help-about"))
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        # Central widget
        central = QWidget()
        main_layout = QVBoxLayout()
        central.setLayout(main_layout)
        self.setCentralWidget(central)

        # Group: Facebook Reel Downloader
        group = QGroupBox("Descargar Facebook Reel")
        group_layout = QVBoxLayout()
        group.setLayout(group_layout)

        # URL input
        url_layout = QHBoxLayout()
        url_label = QLabel("URL del Reel:")
        url_label.setToolTip("Introduce la URL del Reel de Facebook")
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://facebook.com/reel/...")
        self.url_input.setToolTip("Introduce la URL del Reel de Facebook que deseas descargar")
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_input)
        group_layout.addLayout(url_layout)

        # Output folder
        folder_layout = QHBoxLayout()
        folder_label = QLabel("Carpeta de destino:")
        folder_label.setToolTip("Selecciona la carpeta donde se guardará el video descargado")
        self.folder_input = QLineEdit()
        self.folder_input.setReadOnly(True)
        self.folder_input.setToolTip("Carpeta donde se almacenará el archivo descargado")
        folder_btn = QPushButton("Elegir...")
        folder_btn.setToolTip("Selecciona la carpeta de destino")
        folder_btn.clicked.connect(self.select_folder)
        folder_layout.addWidget(folder_label)
        folder_layout.addWidget(self.folder_input)
        folder_layout.addWidget(folder_btn)
        group_layout.addLayout(folder_layout)

        # Format selection
        format_layout = QHBoxLayout()
        format_label = QLabel("Formato:")
        format_label.setToolTip("Elige el formato/calidad a descargar")
        self.format_combo = QComboBox()
        self.format_combo.setToolTip("Selecciona el formato/calidad del video")
        self.format_combo.addItems([
            "best (Automático)",
            "mp4 (Video MP4)",
            "webm (Video WEBM)",
            "audio only (Solo audio)"
        ])
        format_layout.addWidget(format_label)
        format_layout.addWidget(self.format_combo)
        group_layout.addLayout(format_layout)

        # Download Button
        self.download_btn = QPushButton("Descargar")
        self.download_btn.setToolTip("Descargar el Reel de Facebook a la carpeta seleccionada")
        self.download_btn.clicked.connect(self.start_download)
        group_layout.addWidget(self.download_btn)

        # Progress Bar
        self.progress = QProgressBar()
        self.progress.setValue(0)
        self.progress.setToolTip("Progreso de descarga")
        group_layout.addWidget(self.progress)

        main_layout.addWidget(group)

        # Status Bar
        self.status = QStatusBar()
        self.setStatusBar(self.status)

        # yt-dlp check
        if not YTDLP_AVAILABLE:
            self.status.showMessage("yt-dlp no está instalado. Instálalo con 'pip install yt-dlp'.")

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta de destino")
        if folder:
            self.folder_input.setText(folder)

    def start_download(self):
        if not YTDLP_AVAILABLE:
            QMessageBox.critical(self, "Error", "yt-dlp no está instalado. Instálalo con 'pip install yt-dlp'.")
            return

        url = self.url_input.text().strip()
        folder = self.folder_input.text().strip()
        format_index = self.format_combo.currentIndex()

        format_map = {
            0: "best",
            1: "mp4",
            2: "webm",
            3: "bestaudio"
        }
        format_code = format_map.get(format_index, "best")

        if not url or not folder:
            QMessageBox.warning(self, "Error", "Debes ingresar la URL y seleccionar la carpeta de destino.")
            return

        self.download_btn.setEnabled(False)
        self.progress.setValue(0)
        self.status.showMessage("Descargando...")

        self.thread = DownloadThread(url, folder, format_code)
        self.thread.progress.connect(self.progress.setValue)
        self.thread.finished.connect(self.download_finished)
        self.thread.error.connect(self.download_error)
        self.thread.start()

    def download_finished(self, filename):
        self.status.showMessage(f"Descarga completada: {filename}")
        QMessageBox.information(self, "Descarga completada", f"Archivo guardado en:\n{filename}")
        self.download_btn.setEnabled(True)
        self.progress.setValue(100)

    def download_error(self, error_msg):
        self.status.showMessage("Error en la descarga")
        QMessageBox.critical(self, "Error", f"Ocurrió un error: {error_msg}")
        self.download_btn.setEnabled(True)
        self.progress.setValue(0)

    def show_about(self):
        QMessageBox.information(self, "Acerca de", 
            "PythonBook Reels Downloader\n\n"
            "Descarga reels de Facebook fácilmente usando yt-dlp.\n"
            "Multiplataforma y personalizable.\n"
            "Icono: app/app-icon.ico"
        )

def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.join("app", "app-icon.ico")))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
