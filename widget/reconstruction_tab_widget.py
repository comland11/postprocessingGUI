from PyQt5.QtWidgets import QPushButton, QTabWidget, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout


class ReconstructionTabWidget(QTabWidget):
    """
    ReconstructionTabWidget class for displaying a tab widget for image reconstruction options.

    Inherits from QTabWidget provided by PyQt5 to display a tab widget for image reconstruction options.

    Attributes:
        main: The parent widget.
    """

    def __init__(self, parent, *args, **kwargs):
        """
        Initialize the ReconstructionTabWidget.

        Args:
            parent: The parent widget.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super(ReconstructionTabWidget, self).__init__(*args, **kwargs)
        self.main = parent

        # Buttons
        self.image_fft_button = QPushButton('FFT')
        self.image_art_button = QPushButton('ART')

        # Labels
        self.niter_label = QLabel('Number of iterations')
        self.lambda_label = QLabel('Lambda')

        # Text Fields
        self.niter_text_field = QLineEdit()
        self.niter_text_field.setText('1')
        self.lambda_text_field = QLineEdit()
        self.lambda_text_field.setText('1')

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
