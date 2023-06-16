from PyQt5.QtWidgets import QPushButton, QTabWidget, QVBoxLayout, QLabel, QCheckBox, QLineEdit, QHBoxLayout


class PreProcessingTabWidget(QTabWidget):
    def __init__(self, parent, *args, **kwargs):
        super(PreProcessingTabWidget, self).__init__(*args, **kwargs)
        self.main = parent

        # Label
        self.order_label = QLabel('Order')

        # Text Field
        self.order_field = QLineEdit()
        self.order_field.setText('1')

        # Checkbox
        self.readout_checkbox = QCheckBox('Readout')
        self.readout_checkbox.setChecked(True)
        self.phase_checkbox = QCheckBox('Phase')
        self.slice_checkbox = QCheckBox('Slice')

        # Cosbell layout
        self.cosbell_layout = QHBoxLayout()
        self.cosbell_layout.addWidget(self.readout_checkbox)
        self.cosbell_layout.addWidget(self.phase_checkbox)
        self.cosbell_layout.addWidget(self.slice_checkbox)

        # Order layout
        self.order_layout = QHBoxLayout()
        self.order_layout.addWidget(self.order_label)
        self.order_layout.addWidget(self.order_field)

        # Buttons
        self.image_cosbell_button = QPushButton('Cosbell filter')
        self.image_padding_button = QPushButton('Zero padding')

        # Main layout
        self.preprocessing_layout = QVBoxLayout()
        self.preprocessing_layout.addLayout(self.cosbell_layout)
        self.preprocessing_layout.addLayout(self.order_layout)
        self.preprocessing_layout.addWidget(self.image_cosbell_button)
        self.preprocessing_layout.addWidget(self.image_padding_button)
        self.setLayout(self.preprocessing_layout)

