import scipy as sp
import numpy as np


from PyQt5.QtWidgets import QFileDialog
from widget.toolbar_widget import ToolBarWidget


class ToolBarController(ToolBarWidget):
    def __init__(self, *args, **kwargs):
        super(ToolBarController, self).__init__(*args, **kwargs)

        # Connect the image_loading_button clicked signal to the rawDataLoading method
        self.image_loading_button.clicked.connect(self.rawDataLoading)

    def rawDataLoading(self):
        # Load raw data from a .mat file and update the image view widget

        # Clear the history widget, history controller, and history dictionaries
        self.main.history_widget.clear()
        self.main.history_controller.clear()
        self.main.history_controller.hist_dict.clear()
        self.main.history_controller.operations_dict.clear()

        # Prompt the user to select a .mat file
        file_path = self.loadFile()
        mat_data = sp.io.loadmat(file_path)

        # Extract the k-space data from the loaded .mat file
        self.k_space = mat_data['kSpace3D']

        # Compute the absolute value of the k-space data
        k_space_absolute = np.abs(self.k_space)

        # Update the main matrix of the image view widget with the absolute k-space data
        self.main.image_view_widget.main_matrix = k_space_absolute

        # Update the image view widget to display the new main matrix
        self.main.image_view_widget.setImage(self.main.image_view_widget.main_matrix)

        # Add the "KSpace" operation to the history
        self.main.history_controller.addItemWithTimestamp("KSpace")

        # Update the history dictionary with the new main matrix for the current matrix info
        self.main.history_controller.hist_dict[self.main.history_controller.matrix_infos] = \
            self.main.image_view_widget.main_matrix

        # Update the operations history with the "KSpace" operation
        self.main.history_controller.uptadeOperationsHist(self.main.history_controller.matrix_infos, "Kspace")

    def loadFile(self):
        # Open a file dialog to select a .mat file and return its path
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        default_dir = "C:/Users/Portatil PC 6/PycharmProjects/pythonProject1/Results"

        # Open the file dialog and prompt the user to select a .mat file
        file_name, _ = QFileDialog.getOpenFileName(self, "Select a .mat file", default_dir, "MAT Files (*.mat)",
                                                   options=options)

        return file_name
