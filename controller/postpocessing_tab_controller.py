import threading

import bm4d
import numpy as np

from widget.postpocessing_tab_widget import PostProcessingTabWidget


class PostProcessingTabController(PostProcessingTabWidget):
    def __init__(self, *args, **kwargs):
        super(PostProcessingTabController, self).__init__(*args, **kwargs)

        # Connect the button click signal to the bm4dFilter method
        self.run_filter_button.clicked.connect(self.bm4dFilter)

        self.image_data = None
        self.denoised_image = None

    def bm4dFilter(self):
        thread = threading.Thread(target=self.RunBm4dFilter)
        thread.start()

    def RunBm4dFilter(self):
        # Get the image data from the main matrix
        image_data = np.abs(self.main.image_view_widget.main_matrix).astype(float)

        # Rescale the image between 0 and 100
        image_rescaled = np.interp(image_data, (np.min(image_data), np.max(image_data)), (0, 100))

        # Compute median and median absolute deviation (MAD)
        med = np.median(image_rescaled)
        mad = np.median(np.abs(image_rescaled - med))

        if self.auto_checkbox.isChecked():
            sigma_psd = 1.4826 * mad
        else:
            std_value = float(self.std_text_field.text())
            sigma_psd = std_value

        print('BM4D is loading')

        # Apply the BM4D filter to the rescaled image
        denoised_rescaled = bm4d.bm4d(image_rescaled, sigma_psd=sigma_psd)

        # Restore the denoised image to its original dimensions
        denoised_image = np.interp(denoised_rescaled, (np.min(denoised_rescaled), np.max(denoised_rescaled)),
                                   (np.min(image_data), np.max(image_data)))

        # Update the main matrix of the image view widget with the denoised image data
        self.main.image_view_widget.main_matrix = denoised_image

        # Add the "BM4D" operation to the history widget
        self.main.history_controller.addItemWithTimestamp("BM4D")

        # Update the history dictionary with the new main matrix for the current matrix info
        self.main.history_controller.hist_dict[self.main.history_controller.matrix_infos] = \
            self.main.image_view_widget.main_matrix

        # Update the operations history
        self.main.history_controller.updateOperationsHist(self.main.history_controller.matrix_infos, "BM4D - Standard "
                                                                                                     "deviation : " +
                                                          str(sigma_psd))
        print('BM4D filter has been applied')
