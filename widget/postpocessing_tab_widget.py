from PyQt5.QtWidgets import QPushButton, QTabWidget, QWidget, QVBoxLayout, QLabel, QCheckBox, QLineEdit, QHBoxLayout


class PostProcessingTabWidget(QTabWidget):
    def __init__(self, parent, *args, **kwargs):
        super(PostProcessingTabWidget, self).__init__(*args, **kwargs)
        self.main = parent

        # Tabs
        bm4d_tab = QWidget()
        gaussian_tab = QWidget()

        # Adding Tabs in the QTabWidget
        self.addTab(bm4d_tab, 'BM4D')
        self.addTab(gaussian_tab, 'Gaussian')

        # Label
        self.std_label = QLabel('Standard deviation')

        # Buttons
        self.run_filter_button = QPushButton('Run filter')

        # CheckBox
        self.auto_checkbox = QCheckBox('Automatic')

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
