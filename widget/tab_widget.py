from PyQt5.QtWidgets import QPushButton, QTabWidget, QWidget, QVBoxLayout, QGridLayout, QHBoxLayout, QCheckBox


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

        # Buttons
        self.image_cosbell_button = QPushButton('Cosbell filter')
        self.image_padding_button = QPushButton('Zero padding')

        self.image_fft_button = QPushButton('FFT')
        self.image_art_button = QPushButton('ART')

        # Cosbell layout
        self.cosbell_layout = QHBoxLayout()

        # Preprocessing layout
        self.preprocessing_layout = QVBoxLayout(preprocessing_tab)
        self.preprocessing_layout.addLayout(self.cosbell_layout)
        self.preprocessing_layout.addWidget(self.image_cosbell_button)
        self.preprocessing_layout.addWidget(self.image_padding_button)

        #Checkbox
        self.readout_checkbox = QCheckBox('Readout')
        self.phase_checkbox = QCheckBox('Phase')
        self.slice_checkbox = QCheckBox('Slice')

        self.cosbell_layout.addWidget(self.readout_checkbox)
        self.cosbell_layout.addWidget(self.phase_checkbox)
        self.cosbell_layout.addWidget(self.slice_checkbox)

        # Reconstruction layout
        self.reconstruction_layout = QVBoxLayout(reconstruction_tab)
        self.reconstruction_layout.addWidget(self.image_fft_button)
        self.reconstruction_layout.addWidget(self.image_art_button)

        # Postprocessing layout
        self.postprocessing_layout = QGridLayout(postprocessing_tab)
