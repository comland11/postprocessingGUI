from PyQt5.QtWidgets import QPushButton, QTabWidget, QWidget, QVBoxLayout, QLabel, QCheckBox


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


        # BM4D layout
        self.bm4d_layout = QVBoxLayout(bm4d_tab)
        self.bm4d_layout.addWidget(self.std_label)
        self.bm4d_layout.addWidget(self.run_filter_button)
        self.bm4d_layout.addWidget(self.auto_checkbox)

        # Gaussian layout
        self.gaussian_layout = QVBoxLayout(gaussian_tab)
