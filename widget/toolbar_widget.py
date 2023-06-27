from PyQt5.QtWidgets import QToolBar, QPushButton


class ToolBarWidget(QToolBar):
    def __init__(self, parent, *args, **kwargs):
        super(ToolBarWidget, self).__init__(*args, **kwargs)
        self.main = parent

        self.image_loading_button = QPushButton('File')
        self.addWidget(self.image_loading_button)

