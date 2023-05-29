from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider


class SliderWidget(QSlider):
    def __init__(self, parent, *args, **kwargs):
        super(SliderWidget, self).__init__(*args, **kwargs)
        self.main = parent

        self.setOrientation(Qt.Horizontal)