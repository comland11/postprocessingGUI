import scipy as sp
import numpy as np


from PyQt5.QtWidgets import QFileDialog
from widget.toolbar_widget import ToolBarWidget


class ToolBarController(ToolBarWidget):
    def __init__(self, *args, **kwargs):
        super(ToolBarController, self).__init__(*args, **kwargs)

        self.image_loading_button.clicked.connect(self.rawDataLoading)

    def rawDataLoading(self):
        self.main.history_widget.clear()
        self.main.history_controller.clear()
        self.main.history_controller.hist_dict.clear()
        self.main.history_controller.operations_dict.clear()

        file_path = self.loadFile()
        mat_data = sp.io.loadmat(file_path)
        self.k_space = mat_data['kSpace3D']

        k_space_absolute = np.abs(self.k_space)

        self.main.image_view_widget.main_matrix = k_space_absolute
        self.main.image_view_widget.setImage(self.main.image_view_widget.main_matrix)

        self.main.history_controller.addItemWithTimestamp("KSpace")

        self.main.history_controller.hist_dict[self.main.history_controller.matrix_infos] = \
            self.main.image_view_widget.main_matrix

        self.main.history_controller.uptadeOperationsHist(self.main.history_controller.matrix_infos, "Kspace")

    def loadFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        default_dir = "C:/Users/Portatil PC 6/PycharmProjects/pythonProject1/Results"
        file_name, _ = QFileDialog.getOpenFileName(self, "Select a .mat file", default_dir, "MAT Files (*.mat)",
                                                   options=options)

        return file_name
