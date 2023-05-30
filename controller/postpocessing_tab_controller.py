import bm4d
import numpy as np

from widget.postpocessing_tab_widget import PostProcessingTabWidget


class PostProcessingTabController(PostProcessingTabWidget):
    def __init__(self, *args, **kwargs):
        super(PostProcessingTabController, self).__init__(*args, **kwargs)

        # Connect the button click signal to the bm4dFilter method and showSlider method
        self.run_filter_button.clicked.connect(self.bm4dFilter)
        self.run_filter_button.clicked.connect(self.main.bm4d_slider.showSlider)

        self.image_data = None
        self.denoised_image = None

    def bm4dFilter(self):
        # Get the image data from the fft in the main tab controller
        image_data = self.main.tab_controller.image_amp.astype(float)

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

        # Apply the BM4D filter to the rescaled image
        denoised_rescaled = bm4d.bm4d(image_rescaled, sigma_psd=sigma_psd)

        # Restore the denoised image to its original dimensions
        self.denoised_image = np.interp(denoised_rescaled, (np.min(denoised_rescaled), np.max(denoised_rescaled)),
                                   (np.min(image_data), np.max(image_data)))

        # Update the slider values
        self.main.bm4d_slider.setSliderValues()

        # Add the "BM4D" operation to the history widget and update the operations history
        self.main.history_controller.addItemWithTimestamp("BM4D")
        self.main.history_controller.uptadeOperationsHist(self.main.history_controller.matrix_infos, "BM4D - Standard "
                                                                                                     "deviation : " +
                                                          str(sigma_psd))
