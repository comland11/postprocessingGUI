from widget.slider_widget import SliderWidget


class SliderController(SliderWidget):
    def __init__(self, *args, **kwargs):
        super(SliderController, self).__init__(*args, **kwargs)

        # Connect the valueChanged signal to the updateSlice method
        self.valueChanged.connect(self.updateSlice)

        # Set the slider initially hidden
        self.setVisible(False)

    def showSlider(self):
        # Show the slider
        self.setVisible(True)

    def setSliderValues(self):
        # Set the minimum, maximum, and initial value of the slider based on the number of slices in the denoised image
        num_slices = self.main.postprocessing_controller.denoised_image.shape[0]
        self.setMinimum(0)
        self.setMaximum(num_slices - 1)
        self.setValue(0)

    def updateSlice(self):
        # Update the image view with the selected slice from the denoised image

        # Check if the denoised image exists
        if self.main.postprocessing_controller.denoised_image is not None:
            # Get the selected slice number from the slider
            slice_number = self.value()

            # Extract the slice data from the denoised image
            slice_data = self.main.postprocessing_controller.denoised_image[slice_number, :, :]

            # Update the main matrix of the image view widget with the slice data
            self.main.image_view_widget.main_matrix = slice_data

            # Update the image view widget with the new main matrix
            self.main.image_view_widget.setImage(self.main.image_view_widget.main_matrix)

            # Update the history dictionary with the new main matrix for the current matrix info
            self.main.history_controller.hist_dict[self.main.history_controller.matrix_infos] = \
                self.main.image_view_widget.main_matrix
