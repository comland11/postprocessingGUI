from PyQt5.QtWidgets import QTabWidget, QPushButton, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QGroupBox


class VisualisationTabWidget(QTabWidget):
    """
    VisualisationTabWidget class for displaying a tab widget for visualization settings.

    Inherits from QTabWidget provided by PyQt5 to display a tab widget for visualization settings.

    Attributes:
        main: The parent widget.
    """

    def __init__(self, parent, *args, **kwargs):
        """
        Initialize the VisualisationTabWidget.

        Args:
            parent: The parent widget.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super(VisualisationTabWidget, self).__init__(*args, **kwargs)
        self.main = parent

        # Multiplot settings
        # Button for showing slices
        self.visualisation_button = QPushButton('Show slices')

        # Labels for input fields
        self.range_label = QLabel('Slices')
        self.column_label = QLabel('Rows and columns')

        # Text Fields for input
        self.range_text_field = QLineEdit()
        self.range_text_field.setPlaceholderText('First, Last')

        self.column_text_field = QLineEdit()
        self.column_text_field.setPlaceholderText('Rows, Columns')

        # Layout for the input fields related to the number of slices
        self.number_layout = QHBoxLayout()
        self.number_layout.addWidget(self.range_label)
        self.number_layout.addWidget(self.range_text_field)

        # Layout for the input fields related to the number of rows and columns
        self.column_layout = QHBoxLayout()
        self.column_layout.addWidget(self.column_label)
        self.column_layout.addWidget(self.column_text_field)

        # Main layout for the Multiplot settings
        self.multiplot_layout = QVBoxLayout()
        self.multiplot_layout.addLayout(self.number_layout)
        self.multiplot_layout.addLayout(self.column_layout)
        self.multiplot_layout.addWidget(self.visualisation_button)

        # Group Box for Multiplot settings
        self.multiplot_group = QGroupBox("Multiplot")
        self.multiplot_group.setLayout(self.multiplot_layout)

        # Main layout for the Visualisation tab
        self.visualisation_layout = QVBoxLayout()
        self.visualisation_layout.addWidget(self.multiplot_group)

        # Set the layout for the VisualisationTabWidget
        self.setLayout(self.visualisation_layout)
