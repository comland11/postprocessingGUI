from PyQt5.QtWidgets import QPushButton, QTabWidget, QVBoxLayout, QLabel, QCheckBox, QLineEdit, QHBoxLayout


class PreProcessingTabWidget(QTabWidget):
    def __init__(self, parent, *args, **kwargs):
        super(PreProcessingTabWidget, self).__init__(*args, **kwargs)
        self.main = parent

        # Label
        self.cosbell_order_label = QLabel('Order')
        self.zero_padding_order_label = QLabel('Order')
        self.change_fov_label = QLabel('New FOV (mm)')

        # Text Field
        self.cosbell_order_field = QLineEdit()
        self.cosbell_order_field.setText('1')

        self.zero_padding_order_field = QLineEdit()
        self.zero_padding_order_field.setText('2')

        self.change_fov_field = QLineEdit()
        self.change_fov_field.setPlaceholderText("Readout, Phase, Slice")

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
        self.cosbell_order_layout = QHBoxLayout()
        self.cosbell_order_layout.addWidget(self.cosbell_order_label)
        self.cosbell_order_layout.addWidget(self.cosbell_order_field)

        self.zero_padding_order_layout = QHBoxLayout()
        self.zero_padding_order_layout.addWidget(self.zero_padding_order_label)
        self.zero_padding_order_layout.addWidget(self.zero_padding_order_field)

        self.change_fov_layout = QHBoxLayout()
        self.change_fov_layout.addWidget(self.change_fov_label)
        self.change_fov_layout.addWidget(self.change_fov_field)

        # Buttons
        self.image_cosbell_button = QPushButton('Cosbell filter')
        self.image_padding_button = QPushButton('Zero padding')
        self.new_fov_button = QPushButton('Change FOV')

        # Main layout
        self.preprocessing_layout = QVBoxLayout()
        self.preprocessing_layout.addLayout(self.cosbell_layout)
        self.preprocessing_layout.addLayout(self.cosbell_order_layout)
        self.preprocessing_layout.addWidget(self.image_cosbell_button)
        self.preprocessing_layout.addLayout(self.zero_padding_order_layout)
        self.preprocessing_layout.addWidget(self.image_padding_button)
        self.preprocessing_layout.addLayout(self.change_fov_layout)
        self.preprocessing_layout.addWidget(self.new_fov_button)
        self.setLayout(self.preprocessing_layout)
