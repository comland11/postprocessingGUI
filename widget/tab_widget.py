from PyQt5.QtWidgets import QPushButton, QTabWidget, QWidget, QVBoxLayout, QGridLayout


class TabWidget(QTabWidget):
    def __init__(self, parent, *args, **kwargs):
        super(TabWidget, self).__init__(*args, **kwargs)
        self.main = parent

        # Tabs
        preprocessing_tab = QWidget()
        reconstruction_tab = QWidget()
        postprocessing_tab = QWidget()

        # Adding Tabs in the QTabWidget
        self.addTab(preprocessing_tab, 'PreProcessing')
        self.addTab(reconstruction_tab, 'Reconstruction')
        self.addTab(postprocessing_tab, 'PostProcessing')

        # Buttons
        self.image_cosbell_button = QPushButton('Cosbell filter')
        self.image_padding_button = QPushButton('Zero padding')

        self.image_fft_button = QPushButton('FFT')
        self.image_art_button = QPushButton('ART')

        # Preprocessing layout
        self.preprocessing_layout = QVBoxLayout(preprocessing_tab)
        self.preprocessing_layout.addWidget(self.image_cosbell_button)
        self.preprocessing_layout.addWidget(self.image_padding_button)

        # Reconstruction layout
        self.reconstruction_layout = QVBoxLayout(reconstruction_tab)
        self.reconstruction_layout.addWidget(self.image_fft_button)
        self.reconstruction_layout.addWidget(self.image_art_button)

        # Postprocessing layout
        self.postprocessing_layout = QGridLayout(postprocessing_tab)