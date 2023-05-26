import bm4d
import numpy as np

from widget.tab_widget import TabWidget


class TabController(TabWidget):
    def __init__(self, *args, **kwargs):
        super(TabController, self).__init__(*args, **kwargs)

        self.image_bm4d_button.clicked.connect(self.bm4dFilter)
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

    def bm4dFilter(self):
        image_data = self.main.image_view_widget.main_matrix.astype(float)

        med = np.median(image_data)
        mad = np.median(np.abs(image_data - med))
        sigma_psd = 1.4826 * mad
        denoised_image = bm4d.bm4d(image_data, sigma_psd=sigma_psd)
        denoised_image[14, :, :]

        self.main.image_view_widget.main_matrix = denoised_image[14, :, :]
        self.main.image_view_widget.setImage(self.main.image_view_widget.main_matrix)

        self.main.history_controller.addItemWithTimestamp("BM4D")

        self.main.history_controller.hist_dict[self.main.history_controller.matrix_infos] = \
            self.main.image_view_widget.main_matrix

        self.main.history_controller.uptadeOperationsHist(self.main.history_controller.matrix_infos, "BM4D")



