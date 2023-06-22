import threading

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
        self.partial_acquisition_button.clicked.connect(self.partialAcquisition)

    def partialAcquisition(self):
        thread = threading.Thread(target=self.runPartialAcquisition)
        thread.start()

    def runPartialAcquisition(self):
        # self.main.history_widget.clear()
        k_space = self.k_space_raw.copy()
        nPoints = np.reshape(self.mat_data['nPoints'], -1)

        krd = np.real(k_space[:, 0])
        kph = np.real(k_space[:, 1])
        ksl = np.real(k_space[:, 2])
        signal = k_space[:, 3]

        ksl_min = ksl.min()
        ksl_max = ksl.max()

        k0 = 0.65 * (ksl_max - ksl_min) + ksl_min
        for i in range(len(ksl)):
            if ksl[i] > k0:
                signal[i] = 0

        k = np.column_stack((krd, kph, ksl, signal))
        k = np.reshape(k[:, 3], nPoints[-1::-1])

        # Update the main matrix of the image view widget with the k-space data
        self.main.image_view_widget.main_matrix = k

        # Add the "KSpace" operation to the history
        self.main.history_controller.addItemWithTimestamp("Partial Acquisition")

        # Update the history dictionary with the new main matrix for the current matrix info
        self.main.history_controller.hist_dict[self.main.history_controller.matrix_infos] = \
            self.main.image_view_widget.main_matrix

        # Update the operations history
        self.main.history_controller.operations_dict[self.main.history_controller.matrix_infos] = ["Partial "
                                                                                                   "Acquisition"]

    def rawDataLoading(self):
        # Load raw data from a .mat file and update the image view widget

        # Clear the console, history widget, history controller, and history dictionaries
        self.main.history_widget.clear()
        self.main.console.console.clear()
        self.main.history_controller.clear()
        self.main.history_controller.clearSecondImageView()
        self.main.history_controller.hist_dict.clear()
        self.main.history_controller.operations_dict.clear()

        # Prompt the user to select a .mat file
        file_path = self.loadFile()
        self.mat_data = sp.io.loadmat(file_path)
        nPoints = np.reshape(self.mat_data['nPoints'], -1)

        if self.mat_data['seqName'] == 'PETRA':
            kCartesian = self.mat_data['kCartesian']
            self.k_space_raw = self.mat_data['kSpaceRaw']

            kxOriginal = np.reshape(np.real(self.k_space_raw[:, 0]), -1)
            kyOriginal = np.reshape(np.real(self.k_space_raw[:, 1]), -1)
            kzOriginal = np.reshape(np.real(self.k_space_raw[:, 2]), -1)
            kxTarget = np.reshape(kCartesian[:, 0], -1)
            kyTarget = np.reshape(kCartesian[:, 1], -1)
            kzTarget = np.reshape(kCartesian[:, 2], -1)
            valCartesian = griddata((kxOriginal, kyOriginal, kzOriginal), np.reshape(self.k_space_raw[:, 3], -1),
                                    (kxTarget, kyTarget, kzTarget), method="linear", fill_value=0, rescale=False)

            self.k_space = np.reshape(valCartesian, (nPoints[2], nPoints[1], nPoints[0]))

        else:  # Cartesian
            # Extract the k-space data from the loaded .mat file
            self.k_space_raw = self.mat_data['sampled']
            self.k_space = np.reshape(self.k_space_raw[:, 3], nPoints[-1::-1])

        # Update the main matrix of the image view widget with the k-space data
        self.main.image_view_widget.main_matrix = self.k_space

        # Update the image view widget to display the new main matrix
        self.main.image_view_widget.setImage(np.abs(self.main.image_view_widget.main_matrix))

        # Add the "KSpace" operation to the history
        self.main.history_controller.addItemWithTimestamp("KSpace")

        # Update the history dictionary with the new main matrix for the current matrix info
        self.main.history_controller.hist_dict[self.main.history_controller.matrix_infos] = \
            self.main.image_view_widget.main_matrix

        # Update the operations history
        self.main.history_controller.updateOperationsHist(self.main.history_controller.matrix_infos, "KSpace")

    def loadFile(self):
        # Open a file dialog to select a .mat file and return its path
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        default_dir = "C:/Users/Portatil PC 6/PycharmProjects/pythonProject1/Results"

        # Open the file dialog and prompt the user to select a .mat file
        file_name, _ = QFileDialog.getOpenFileName(self, "Select a .mat file", default_dir, "MAT Files (*.mat)",
                                                   options=options)

        return file_name
