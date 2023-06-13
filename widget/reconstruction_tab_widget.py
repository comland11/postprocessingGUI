from PyQt5.QtWidgets import QPushButton, QTabWidget, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout


class ReconstructionTabWidget(QTabWidget):
    def __init__(self, parent, *args, **kwargs):
        super(ReconstructionTabWidget, self).__init__(*args, **kwargs)
        self.main = parent

        # Buttons
        self.image_fft_button = QPushButton('FFT')
        self.image_art_button = QPushButton('ART')

        # Labels
        self.niter_label = QLabel('Number of iteration')
        self.lambda_label = QLabel('Lambda')

        # Text Fields
        self.niter_text_field = QLineEdit()
        self.lambda_text_field = QLineEdit()

        # Layouts
        self.art_layout = QHBoxLayout()
        self.art_layout.addWidget(self.niter_label)
        self.art_layout.addWidget(self.niter_text_field)
        self.art_layout.addWidget(self.lambda_label)
        self.art_layout.addWidget(self.lambda_text_field)

        self.reconstruction_layout = QVBoxLayout()
        self.reconstruction_layout.addLayout(self.art_layout)
        self.reconstruction_layout.addWidget(self.image_art_button)
        self.reconstruction_layout.addWidget(self.image_fft_button)

        self.setLayout(self.reconstruction_layout)
