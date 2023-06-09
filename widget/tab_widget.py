from PyQt5.QtWidgets import QPushButton, QTabWidget, QWidget, QVBoxLayout, QGridLayout, QHBoxLayout, QCheckBox, QLabel, \
    QLineEdit


class TabWidget(QTabWidget):
    def __init__(self, parent, *args, **kwargs):
        super(TabWidget, self).__init__(*args, **kwargs)
        self.main = parent

        self.setMaximumWidth(400)

        # Tabs
        preprocessing_tab = QWidget()
        reconstruction_tab = QWidget()
        postprocessing_tab = QWidget()

        # Adding Tabs in the QTabWidget
        self.addTab(preprocessing_tab, 'PreProcessing')
        self.addTab(reconstruction_tab, 'Reconstruction')
        self.addTab(postprocessing_tab, 'PostProcessing')

        self.image_fft_button = QPushButton('FFT')
        self.image_art_button = QPushButton('ART')

        # Preprocessing layout
        self.preprocessing_layout = QVBoxLayout(preprocessing_tab)

        # Reconstruction layout
        self.reconstruction_layout = QVBoxLayout(reconstruction_tab)
        self.reconstruction_layout.addWidget(self.image_fft_button)
        self.reconstruction_layout.addWidget(self.image_art_button)

        # Postprocessing layout
        self.postprocessing_layout = QVBoxLayout(postprocessing_tab)
