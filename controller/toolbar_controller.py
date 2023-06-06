import scipy as sp
import numpy as np

from PyQt5.QtWidgets import QFileDialog
from scipy.interpolate import griddata

from widget.toolbar_widget import ToolBarWidget


class ToolBarController(ToolBarWidget):
    def __init__(self, *args, **kwargs):
        super(ToolBarController, self).__init__(*args, **kwargs)

        # Connect the image_loading_button clicked signal to the rawDataLoading method
        self.k_space = None
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
        self.mat_data = sp.io.loadmat(file_path)

        if self.mat_data['seqName'] == 'PETRA':
            kSpace = self.mat_data['kSpaceRaw']
            nPoints = np.reshape(self.mat_data['nPoints'], -1)
            print(nPoints)
            kCartesian = self.mat_data['kCartesian']

            kxOriginal = np.reshape(np.real(kSpace[:, 0]), -1)
            kyOriginal = np.reshape(np.real(kSpace[:, 1]), -1)
            kzOriginal = np.reshape(np.real(kSpace[:, 2]), -1)
            kxTarget = np.reshape(kCartesian[:, 0], -1)
            kyTarget = np.reshape(kCartesian[:, 1], -1)
            kzTarget = np.reshape(kCartesian[:, 2], -1)
            valCartesian = griddata((kxOriginal, kyOriginal, kzOriginal), np.reshape(kSpace[:, 3], -1),
                                    (kxTarget, kyTarget, kzTarget), method="linear", fill_value=0, rescale=False)

            self.k_space = np.reshape(valCartesian, (nPoints[2], nPoints[1], nPoints[0]))
            print(nPoints)

        else:
            # Extract the k-space data from the loaded .mat file
            self.k_space = self.mat_data['kSpace3D']

        # Compute the absolute value of the k-space data
        # k_space_absolute = np.abs(self.k_space)

        # Update the main matrix of the image view widget with the absolute k-space data
        self.main.image_view_widget.main_matrix = self.k_space

        # Update the image view widget to display the new main matrix
        self.main.image_view_widget.setImage(np.abs(self.main.image_view_widget.main_matrix))

        # Add the "KSpace" operation to the history
        self.main.history_controller.addItemWithTimestamp("KSpace")

        # Update the history dictionary with the new main matrix for the current matrix info
        self.main.history_controller.hist_dict[self.main.history_controller.matrix_infos] = \
            self.main.image_view_widget.main_matrix

        # Update the operations history with the "KSpace" operation
        self.main.history_controller.updateOperationsHist(self.main.history_controller.matrix_infos, "Kspace")

    def loadFile(self):
        # Open a file dialog to select a .mat file and return its path
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        default_dir = "C:/Users/Portatil PC 6/PycharmProjects/pythonProject1/Results"

        # Open the file dialog and prompt the user to select a .mat file
        file_name, _ = QFileDialog.getOpenFileName(self, "Select a .mat file", default_dir, "MAT Files (*.mat)",
                                                   options=options)

        return file_name
