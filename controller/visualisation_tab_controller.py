import threading

import numpy as np
from PyQt5.QtWidgets import QGridLayout
from pyqtgraph import ImageView

from widget.visualisation_tab_widget import VisualisationTabWidget


class VisualisationTabController(VisualisationTabWidget):
    def __init__(self, *args, **kwargs):
        super(VisualisationTabController, self).__init__(*args, **kwargs)

        # Connect the image_fft_button clicked signal to the fftReconstruction method
        self.visualisation_button.clicked.connect(self.imageVisualisation)

    # def imageVisualisation(self):
    #    thread = threading.Thread(target=self.runFftReconstruction)
    #    thread.start()

    def imageVisualisation(self):
        image = self.main.image_view_widget.main_matrix
        # view = image[10, :, :]

        step = 2
        n0 = 2
        nend = 14
        column_number = 4

        selected_slices = image[n0:nend + 1:step]
        row_count = (len(selected_slices) + column_number - 1) // column_number

        layout = QGridLayout()

        i = 0
        for row in range(row_count):
            for col in range(column_number):
                if i < len(selected_slices):
                    image_widget = ImageView()
                    image_widget.setImage(abs(selected_slices[i]))
                    #image_widget.ui.histogram.hide()
                    #image_widget.ui.roiBtn.hide()
                    #image_widget.ui.menuBtn.hide()
                    layout.addWidget(image_widget, row, col)
                    i += 1

        self.main.right_layout.addLayout(layout)
