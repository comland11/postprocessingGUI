import time
import subprocess
import scipy as sp
import numpy as np
import matlab.engine

from scipy.interpolate import griddata
from PyQt5.QtWidgets import QFileDialog
from widget.toolbar_widget import ToolBarWidget


class ToolBarController(ToolBarWidget):
    """
    Controller class for the ToolBarWidget.

    Inherits from ToolBarWidget to provide additional functionality for managing toolbar actions.

    Attributes:
        k_space_raw (ndarray): Raw k-space data loaded from a .mat file.
        mat_data (dict): Data loaded from a .mat file.
        nPoints (ndarray): Array containing the number of points in each dimension.
        k_space (ndarray): Processed k-space data.
        image_loading_button: QPushButton for loading the file and getting the k-space.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the ToolBarController.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super(ToolBarController, self).__init__(*args, **kwargs)

        # Connect the image_loading_button clicked signal to the rawDataLoading method
        self.k_space_raw = None
        self.mat_data = None
        self.nPoints = None
        self.k_space = None
        self.image_loading_button.clicked.connect(self.rawDataLoading)

    def rawDataLoading(self):
        """
        Load raw data from a .mat file and update the image view widget.
        """
        # Prompt the user to select a .mat file
        file_path = self.loadFile()
        self.mat_data = sp.io.loadmat(file_path)
        self.nPoints = np.reshape(self.mat_data['nPoints'], -1)

        start_time = time.time()

        if self.mat_data['seqName'] == 'PETRA':
            kCartesian = self.mat_data['kCartesian']
            self.k_space_raw = self.mat_data['kSpaceRaw']

            eng = matlab.engine.start_matlab()

            eng.workspace['kSpaceRaw'] = matlab.double(self.k_space_raw.tolist(), is_complex=True)
            eng.workspace['kCartesian'] = matlab.double(kCartesian.tolist(), is_complex=True)
            eng.workspace['nPoints'] = matlab.double(self.nPoints.tolist(), is_complex=True)

            # Chemin vers votre script MATLAB
            matlab_script_path = 'C:/Users/Portatil PC 6/PycharmProjects/postprocessingGUI/scripts/test.m'

            # Exécuter le script MATLAB
            eng.run(matlab_script_path, nargout=0)

            k_space = eng.workspace['k_space']

            # Fermer le moteur MATLAB
            eng.quit()

            k_space = np.array(k_space)
            self.k_space = k_space

        else:  # Cartesian
            # Extract the k-space data from the loaded .mat file
            self.k_space_raw = self.mat_data['sampled']
            self.k_space = np.reshape(self.k_space_raw[:, 3], self.nPoints[-1::-1])

        # Clear the console, history widget, history controller, and history dictionaries
        self.main.history_widget.clear()
        self.main.console.console.clear()
        self.main.history_controller.clear()
        self.main.history_controller.hist_dict.clear()
        self.main.visualisation_controller.clear2DImage()
        self.main.history_controller.clearSecondImageView()
        self.main.history_controller.operations_dict.clear()

        # Calculate logarithmic scale
        small_value = 1e-10
        k_space_log = np.log10(self.k_space + small_value)

        # Update the main matrix of the image view widget with the k-space data
        self.main.image_view_widget.main_matrix = k_space_log

        # Update the image view widget to display the new main matrix
        self.main.image_view_widget.setImage(np.abs(self.main.image_view_widget.main_matrix))

        # Add the "KSpace" operation to the history
        self.main.history_controller.addItemWithTimestamp("K Space")

        # Update the history dictionary with the new main matrix for the current matrix info
        self.main.history_controller.hist_dict[self.main.history_controller.matrix_infos] = \
            self.main.image_view_widget.main_matrix

        # Update the operations history
        self.main.history_controller.updateOperationsHist(self.main.history_controller.matrix_infos, "K Space")

        end_time = time.time()
        execution_time = end_time - start_time
        print("Time :", execution_time, "s")

    def loadFile(self):
        """
        Open a file dialog to select a .mat file and return its path.

        Returns:
            str: The path of the selected .mat file.
        """
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        default_dir = "C:/Users/Portatil PC 6/PycharmProjects/pythonProject1/Results"

        # Open the file dialog and prompt the user to select a .mat file
        file_name, _ = QFileDialog.getOpenFileName(self, "Select a .mat file", default_dir, "MAT Files (*.mat)",
                                                   options=options)

        return file_name
