import bm4d
import numpy as np

from widget.tab_widget import TabWidget


class TabController(TabWidget):
    def __init__(self, *args, **kwargs):
        super(TabController, self).__init__(*args, **kwargs)

        self.image_fft_button.clicked.connect(self.fftReconstruction)

    def fftReconstruction(self):
        k_space = self.main.toolbar_controller.k_space

        image_fft = np.fft.ifftshift(np.fft.ifftn(np.fft.ifftshift(k_space)))
        image_amp = np.abs(image_fft)

        self.main.image_view_widget.main_matrix = image_amp
        self.main.image_view_widget.setImage(self.main.image_view_widget.main_matrix)

        self.main.history_controller.addItemWithTimestamp("FFT")

        self.main.history_controller.hist_dict[self.main.history_controller.matrix_infos] = \
            self.main.image_view_widget.main_matrix

        self.main.history_controller.uptadeOperationsHist(self.main.history_controller.matrix_infos, "FFT")





