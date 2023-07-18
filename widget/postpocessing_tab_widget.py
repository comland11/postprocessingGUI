from PyQt5.QtWidgets import QPushButton, QTabWidget, QWidget, QVBoxLayout, QLabel, QCheckBox, QLineEdit, QHBoxLayout, \
    QGroupBox


class PostProcessingTabWidget(QTabWidget):
    """
    PostProcessingTabWidget class for displaying a tab widget for post-processing options.

    Inherits from QTabWidget provided by PyQt5 to display a tab widget for post-processing options.

    Attributes:
        main: The parent widget.
    """

    def __init__(self, parent, *args, **kwargs):
        """
        Initialize the PostProcessingTabWidget.

        Args:
            parent: The parent widget.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super(PostProcessingTabWidget, self).__init__(*args, **kwargs)
        self.main = parent

        # Tabs
        bm4d_tab = QWidget()
        gaussian_tab = QWidget()
        interpolation_tab = QWidget()

        # Adding Tabs in the QTabWidget
        self.addTab(bm4d_tab, 'BM4D')
        self.addTab(gaussian_tab, 'Gaussian')
        self.addTab(interpolation_tab, 'Interpolation')

        # Label
        self.std_label = QLabel('Standard deviation')

        # Buttons
        self.run_filter_button = QPushButton('Run filter')

        # CheckBox
        self.auto_checkbox = QCheckBox('Auto')
        self.auto_checkbox.setChecked(True)

        # Text Field
        self.std_text_field = QLineEdit()

        # BM4D layout
        self.bm4d_layout = QVBoxLayout(bm4d_tab)
        self.std_layout = QHBoxLayout()

        self.bm4d_layout.addLayout(self.std_layout)
        self.std_layout.addWidget(self.std_label)
        self.std_layout.addWidget(self.std_text_field)
        self.bm4d_layout.addWidget(self.auto_checkbox)
        self.bm4d_layout.addWidget(self.run_filter_button)

        # Gaussian layout
        self.gaussian_layout = QVBoxLayout(gaussian_tab)
        self.gaussian_std_layout = QHBoxLayout()

        self.gaussian_label = QLabel('Standard deviation')
        self.gaussian_text_field = QLineEdit()
        self.gaussian_std_layout.addWidget(self.gaussian_label)
        self.gaussian_std_layout.addWidget(self.gaussian_text_field)

        self.gaussian_button = QPushButton('Gaussian')
        self.gaussian_layout.addLayout(self.gaussian_std_layout)
        self.gaussian_layout.addWidget(self.gaussian_button)

        # Interpolation

        self.shape_label = QLabel('New Shape')
        self.shape_text_field = QLineEdit()
        self.shape_text_field.setPlaceholderText('Readout, Phase, Slice')

        self.shape_layout = QHBoxLayout()
        self.shape_layout.addWidget(self.shape_label)
        self.shape_layout.addWidget(self.shape_text_field)

        self.image_resizing_button = QPushButton('Resize image')

        self.image_resizing_layout = QVBoxLayout()
        self.image_resizing_layout.addLayout(self.shape_layout)
        self.image_resizing_layout.addWidget(self.image_resizing_button)

        self.image_resizing_group = QGroupBox("Image resizing")
        self.image_resizing_group.setLayout(self.image_resizing_layout)

        self.interpolation_layout = QVBoxLayout(interpolation_tab)
        self.interpolation_layout.addWidget(self.image_resizing_group)
