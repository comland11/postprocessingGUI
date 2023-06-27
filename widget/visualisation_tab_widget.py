from PyQt5.QtWidgets import QTabWidget, QPushButton, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout


class VisualisationTabWidget(QTabWidget):
    def __init__(self, parent, *args, **kwargs):
        super(VisualisationTabWidget, self).__init__(*args, **kwargs)
        self.main = parent

        # Button
        self.visualisation_button = QPushButton('Run')

        # Labels
        self.number_label = QLabel('From ... To ...')
        self.column_label = QLabel('Columns number')

        # Text Fields
        self.number_text_field = QLineEdit()
        self.number_text_field.setPlaceholderText("N0, Nend")

        self.column_text_field = QLineEdit()
        self.column_text_field.setText('1')

        # Layouts
        self.number_layout = QHBoxLayout()
        self.number_layout.addWidget(self.number_label)
        self.number_layout.addWidget(self.number_text_field)

        self.column_layout = QHBoxLayout()
        self.column_layout.addWidget(self.column_label)
        self.column_layout.addWidget(self.column_text_field)

        self.visualisation_layout = QVBoxLayout()
        self.visualisation_layout.addLayout(self.number_layout)
        self.visualisation_layout.addLayout(self.column_layout)
        self.visualisation_layout.addWidget(self.visualisation_button)

        self.setLayout(self.visualisation_layout)
