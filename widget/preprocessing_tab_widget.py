from PyQt5.QtWidgets import QPushButton, QTabWidget, QVBoxLayout, QLabel, QCheckBox, QLineEdit, QHBoxLayout, QGroupBox


class PreProcessingTabWidget(QTabWidget):
    """
    PreProcessingTabWidget class for displaying a tab widget for image pre-processing options.

    Inherits from QTabWidget provided by PyQt5 to display a tab widget for image pre-processing options.

    Attributes:
        main: The parent widget.
    """

    def __init__(self, parent, *args, **kwargs):
        """
        Initialize the PreProcessingTabWidget.

        Args:
            parent: The parent widget.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super(PreProcessingTabWidget, self).__init__(*args, **kwargs)
        self.main = parent

        # Cosbell

        self.readout_checkbox = QCheckBox('Readout')
        self.readout_checkbox.setChecked(True)
        self.phase_checkbox = QCheckBox('Phase')
        self.slice_checkbox = QCheckBox('Slice')

        self.cosbell_order_label = QLabel('Order')

        self.cosbell_order_field = QLineEdit()
        self.cosbell_order_field.setText('1')

        self.image_cosbell_button = QPushButton('Cosbell filter')

        # Cosbell layout
        self.checkbox_layout = QHBoxLayout()
        self.checkbox_layout.addWidget(self.readout_checkbox)
        self.checkbox_layout.addWidget(self.phase_checkbox)
        self.checkbox_layout.addWidget(self.slice_checkbox)

        # Order layout
        self.cosbell_order_layout = QHBoxLayout()
        self.cosbell_order_layout.addWidget(self.cosbell_order_label)
        self.cosbell_order_layout.addWidget(self.cosbell_order_field)

        self.cosbell_layout = QVBoxLayout()
        self.cosbell_layout.addLayout(self.checkbox_layout)
        self.cosbell_layout.addLayout(self.cosbell_order_layout)
        self.cosbell_layout.addWidget(self.image_cosbell_button)

        self.cosbell_group = QGroupBox("Cosbell")
        self.cosbell_group.setLayout(self.cosbell_layout)

        # Zero Padding

        self.zero_padding_order_label = QLabel('Order')

        self.zero_padding_order_field = QLineEdit()
        self.zero_padding_order_field.setPlaceholderText("Readout, Phase, Slice")

        self.zero_padding_order_layout = QHBoxLayout()
        self.zero_padding_order_layout.addWidget(self.zero_padding_order_label)
        self.zero_padding_order_layout.addWidget(self.zero_padding_order_field)

        self.image_padding_button = QPushButton('Zero padding')

        self.zero_padding_layout = QVBoxLayout()
        self.zero_padding_layout.addLayout(self.zero_padding_order_layout)
        self.zero_padding_layout.addWidget(self.image_padding_button)

        self.zero_padding_group = QGroupBox("Zero Padding")
        self.zero_padding_group.setLayout(self.zero_padding_layout)

        # FOV change
        self.change_fov_label = QLabel('New FOV (mm)')

        self.change_fov_field = QLineEdit()
        self.change_fov_field.setPlaceholderText("Readout, Phase, Slice")

        self.change_fov_layout = QHBoxLayout()
        self.change_fov_layout.addWidget(self.change_fov_label)
        self.change_fov_layout.addWidget(self.change_fov_field)

        self.new_fov_button = QPushButton('Change FOV')

        self.new_fov_layout = QVBoxLayout()
        self.new_fov_layout.addLayout(self.change_fov_layout)
        self.new_fov_layout.addWidget(self.new_fov_button)

        self.new_fov_group = QGroupBox("FOV Change")
        self.new_fov_group.setLayout(self.new_fov_layout)

        # Partial Reconstruction

        self.partial_reconstruction_label = QLabel('Percentage')

        self.partial_reconstruction_field = QLineEdit()
        self.partial_reconstruction_field.setText('65')

        self.partial_reconstruction_order_layout = QHBoxLayout()
        self.partial_reconstruction_order_layout.addWidget(self.partial_reconstruction_label)
        self.partial_reconstruction_order_layout.addWidget(self.partial_reconstruction_field)

        self.partial_reconstruction_button = QPushButton('Partial reconstruction')

        self.partial_reconstruction_layout = QVBoxLayout()
        self.partial_reconstruction_layout.addLayout(self.partial_reconstruction_order_layout)
        self.partial_reconstruction_layout.addWidget(self.partial_reconstruction_button)

        self.partial_reconstruction_group = QGroupBox("Partial Reconstruction")
        self.partial_reconstruction_group.setLayout(self.partial_reconstruction_layout)

        # Main layout
        self.preprocessing_layout = QVBoxLayout()
        self.preprocessing_layout.addWidget(self.zero_padding_group)
        self.preprocessing_layout.addWidget(self.cosbell_group)
        self.preprocessing_layout.addWidget(self.new_fov_group)
        self.preprocessing_layout.addWidget(self.partial_reconstruction_group)
        self.setLayout(self.preprocessing_layout)
