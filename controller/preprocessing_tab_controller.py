import threading

import numpy as np

from widget.preprocessing_tab_widget import PreProcessingTabWidget


class PreProcessingTabController(PreProcessingTabWidget):
    def __init__(self, *args, **kwargs):
        super(PreProcessingTabController, self).__init__(*args, **kwargs)

        # Connect the button click signal to the bm4dFilter method and showSlider method
        self.image_cosbell_button.clicked.connect(self.cosbellFilter)
        self.image_padding_button.clicked.connect(self.zeroPadding)

    def cosbellFilter(self):
        thread = threading.Thread(target=self.RunCosbellFilter)
        thread.start()

    def RunCosbellFilter(self):
        text = "Cosbell :"
        order = float(self.order_field.text())

        # Get the mat data from the loaded .mat file in the main toolbar controller
        mat_data = self.main.toolbar_controller.mat_data

        # Extract datas data from the loaded .mat file
        self.sampled = self.main.toolbar_controller.k_space_raw
        nPoints = np.reshape(mat_data['nPoints'], -1)

        if self.readout_checkbox.isChecked():
            k = np.reshape(self.sampled[:, 0], nPoints[-1::-1])
            kmax = np.max(np.abs(k[:]))
            text += ' RD,'
        if self.phase_checkbox.isChecked():
            k = np.reshape(self.sampled[:, 1], nPoints[-1::-1])
            kmax = np.max(np.abs(k[:]))
            text += ' PH,'
        if self.slice_checkbox.isChecked():
            k = np.reshape(self.sampled[:, 2], nPoints[-1::-1])
            kmax = np.max(np.abs(k[:]))
            text += ' SL,'

        theta = k / kmax
        s = np.reshape(self.sampled[:, 3], nPoints[-1::-1])
        cosbell = s * (np.cos(theta * (np.pi / 2)) ** order)

        # Update the main matrix of the image view widget with the cosbell data
        self.main.image_view_widget.main_matrix = cosbell

        # Add the "Cosbell" operation to the history widget
        self.main.history_controller.addItemWithTimestamp("Cosbell")

        # Update the history dictionary with the new main matrix for the current matrix info
        self.main.history_controller.hist_dict[self.main.history_controller.matrix_infos] = \
            self.main.image_view_widget.main_matrix

        # Update the operations history
        self.main.history_controller.operations_dict[self.main.history_controller.matrix_infos] = [text + " Order : "
                                                                                                   + str(order)]

    def zeroPadding(self):
        k_space = self.main.image_view_widget.main_matrix

        # Get self.k_space shape
        current_shape = k_space.shape

        # Determine new shape
        desired_shape = np.multiply(current_shape, 2)

        pad_width = ((0, desired_shape[0] - current_shape[0]), (0, desired_shape[1] - current_shape[1]),
                     (0, desired_shape[2] - current_shape[2]))

        self.k_space = np.pad(k_space, pad_width, mode='constant', constant_values=0)

        # Update the main matrix of the image view widget with the image fft data
        self.main.image_view_widget.main_matrix = self.k_space

        # Add the "FFT" operation to the history widget
        self.main.history_controller.addItemWithTimestamp("Zero Padding")

        # Update the history dictionary with the new main matrix for the current matrix info
        self.main.history_controller.hist_dict[self.main.history_controller.matrix_infos] = \
            self.main.image_view_widget.main_matrix

        # Update the operations history
        self.main.history_controller.updateOperationsHist(self.main.history_controller.matrix_infos, "Zero Padding")
