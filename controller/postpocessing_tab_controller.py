import bm4d
import numpy as np
from PyQt5.QtCore import Qt

from widget.postpocessing_tab_widget import PostProcessingTabWidget


class PostProcessingTabController(PostProcessingTabWidget):
    def __init__(self, *args, **kwargs):
        super(PostProcessingTabController, self).__init__(*args, **kwargs)

        self.auto_checkbox.stateChanged.connect(self.applyFilter)

    def bm4dFilter(self):
        image_data = self.main.image_view_widget.main_matrix.astype(float)

        med = np.median(image_data)
        mad = np.median(np.abs(image_data - med))
        sigma_psd = 1.4826 * mad
        denoised_image = bm4d.bm4d(image_data, sigma_psd=sigma_psd)

        self.main.image_view_widget.main_matrix = denoised_image[14, :, :]
        self.main.image_view_widget.setImage(self.main.image_view_widget.main_matrix)

        self.main.history_controller.addItemWithTimestamp("BM4D")

        self.main.history_controller.hist_dict[self.main.history_controller.matrix_infos] = \
            self.main.image_view_widget.main_matrix

        self.main.history_controller.uptadeOperationsHist(self.main.history_controller.matrix_infos, "BM4D")

    def applyFilter(self, state):
        if state == Qt.Checked:
            self.bm4dFilter()