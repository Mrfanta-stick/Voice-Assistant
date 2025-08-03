# rose_ai_app.py
import sys
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QMovie, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QTextEdit, QVBoxLayout, QWidget

import RoseAI_Moreoptimized as rose

class VoiceWorker(QThread):
    def run(self):
        rose.listen_for_wakeword()

class RoseAIUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rose AI - Siri Style")
        self.setGeometry(200, 100, 500, 700)

        container = QWidget()
        self.setCentralWidget(container)
        layout = QVBoxLayout(container)

        # Avatar placeholder
        self.companion_label = QLabel()
        self.companion_label.setAlignment(Qt.AlignCenter)
        self.movie = QMovie("companion_placeholder.gif")
        self.companion_label.setMovie(self.movie)
        self.movie.start()
        layout.addWidget(self.companion_label)

        # Chat area
        self.chat_area = QTextEdit()
        self.chat_area.setFont(QFont("Arial", 12))
        self.chat_area.setReadOnly(True)
        layout.addWidget(self.chat_area)

        # Mic button
        self.mic_button = QPushButton("🎤 Start Listening")
        self.mic_button.clicked.connect(self.toggle_listening)
        layout.addWidget(self.mic_button)

        # Waveform animation
        self.waveform_label = QLabel()
        self.waveform_label.setAlignment(Qt.AlignCenter)
        self.waveform_movie = QMovie("waveform.gif")
        self.waveform_label.setMovie(self.waveform_movie)
        layout.addWidget(self.waveform_label)

        rose.set_ui_callback(self.handle_ai_message)

        self.worker = None
        self.listening = False

    def toggle_listening(self):
        if not self.listening:
            self.start_listening()
        else:
            self.stop_listening()

    def start_listening(self):
        self.listening = True
        self.mic_button.setText("🛑 Stop Listening")
        self.waveform_movie.start()
        self.worker = VoiceWorker()
        self.worker.start()

    def stop_listening(self):
        self.listening = False
        self.mic_button.setText("🎤 Start Listening")
        self.waveform_movie.stop()
        if self.worker:
            self.worker.terminate()

    def handle_ai_message(self, text, msg_type):
        if msg_type == "user":
            self.chat_area.append(f"🧍‍♂️ You: {text}")
        elif msg_type == "rose":
            self.chat_area.append(f"🤖 Rose: {text}")
        else:
            self.chat_area.append(f"[{text}]")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = RoseAIUI()
    ui.show()
    sys.exit(app.exec_())
