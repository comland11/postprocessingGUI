from PyQt5.QtWidgets import QPushButton, QTabWidget, QVBoxLayout


class ReconstructionTabWidget(QTabWidget):
    def __init__(self, parent, *args, **kwargs):
        super(ReconstructionTabWidget, self).__init__(*args, **kwargs)
        self.main = parent

        self.image_fft_button = QPushButton('FFT')
        self.image_art_button = QPushButton('ART')

        self.reconstruction_layout = QVBoxLayout()
        self.reconstruction_layout.addWidget(self.image_fft_button)
        self.reconstruction_layout.addWidget(self.image_art_button)

        self.setLayout(self.reconstruction_layout)
