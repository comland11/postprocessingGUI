import threading
import numpy as np
from PyQt5.QtWidgets import QGridLayout
from pyqtgraph import ImageView
from widget.visualisation_tab_widget import VisualisationTabWidget


class VisualisationTabController(VisualisationTabWidget):
    """
    Controller class for the VisualisationTabWidget.

    Inherits from VisualisationTabWidget to provide additional functionality for managing visualisation tab actions.

    Attributes:
        visualisation_button: QPushButton for showing 2D slices.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the VisualisationTabController.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super(VisualisationTabController, self).__init__(*args, **kwargs)

        self.layout = QGridLayout()
        # Connect the visualisation_button clicked signal to the imageVisualisation method
        self.visualisation_button.clicked.connect(self.imageVisualisation)

    # def imageVisualisation(self):
    #    thread = threading.Thread(target=self.runFftReconstruction)
    #    thread.start()

    def imageVisualisation(self):
        """
        Perform image visualisation on the selected slices of the main matrix.

        Display the selected slices as images using a grid layout.
        """

        image = self.main.image_view_widget.main_matrix

        slices = self.range_text_field.text().split(',')
        n0 = int(slices[0])
        n_end = int(slices[1])

        aaa = self.column_text_field.text().split(',')
        step = int(aaa[0])
        column_number = int(aaa[1])

        # num_slices = n_end - n0
        # step = int(num_slices / (total_slices - 1))
        selected_slices = image[n0:n_end + 1:step]
        row_count = (len(selected_slices) + column_number - 1) // column_number

        i = 0
        for row in range(row_count):
            for col in range(column_number):
                if i < len(selected_slices):
                    image_widget = ImageView()
                    image_widget.setImage(abs(selected_slices[i]))
                    # image_widget.ui.histogram.hide()
                    # image_widget.ui.roiBtn.hide()
                    # image_widget.ui.menuBtn.hide()
                    self.layout.addWidget(image_widget, row, col)
                    i += 1

        self.main.image_view_layout.addLayout(self.layout)
