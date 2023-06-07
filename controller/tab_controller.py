import numpy as np

from widget.tab_widget import TabWidget


class TabController(TabWidget):
    def __init__(self, *args, **kwargs):
        super(TabController, self).__init__(*args, **kwargs)

        # Connect the image_fft_button clicked signal to the fftReconstruction method
        self.image_fft_button.clicked.connect(self.fftReconstruction)

    def fftReconstruction(self):
        # Get the k-space data from the main matrix
        k_space = self.main.image_view_widget.main_matrix

        # Perform inverse FFT shift, inverse FFT, and inverse FFT shift to reconstruct the image in the spatial domain
        image_fft = np.fft.ifftshift(np.fft.ifftn(np.fft.ifftshift(k_space)))

        # Update the main matrix of the image view widget with the image fft data
        self.main.image_view_widget.main_matrix = image_fft

        # Update the image view widget with the new main matrix
        self.main.image_view_widget.setImage(np.abs(self.main.image_view_widget.main_matrix))

        # Add the "FFT" operation to the history widget
        self.main.history_controller.addItemWithTimestamp("FFT")

        # Update the history dictionary with the new main matrix for the current matrix info
        self.main.history_controller.hist_dict[self.main.history_controller.matrix_infos] = \
            self.main.image_view_widget.main_matrix

        # Update the operations history
        self.main.history_controller.updateOperationsHist(self.main.history_controller.matrix_infos, "FFT")
