import numpy as np

from widget.preprocessing_tab_widget import PreProcessingTabWidget


class PreProcessingTabController(PreProcessingTabWidget):
    def __init__(self, *args, **kwargs):
        super(PreProcessingTabController, self).__init__(*args, **kwargs)

        # Connect the button click signal to the bm4dFilter method and showSlider method
        self.image_cosbell_button.clicked.connect(self.cosbellFilter)

    def cosbellFilter(self):
        text = "Cosbell :"
        order = float(self.order_field.text())
        mat_data = self.main.toolbar_controller.mat_data

        self.sampled = mat_data['sampled']
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
        # abs_cosbell = np.abs(cosbell)

        self.main.image_view_widget.main_matrix = cosbell

        # Update the image view widget with the new main matrix
        self.main.image_view_widget.setImage(np.abs(self.main.image_view_widget.main_matrix))

        # Add the "FFT" operation to the history widget
        self.main.history_controller.addItemWithTimestamp("Cosbell")

        # Update the history dictionary with the new main matrix for the current matrix info
        self.main.history_controller.hist_dict[self.main.history_controller.matrix_infos] = \
            self.main.image_view_widget.main_matrix

        # Update the operations history with the "FFT" operation
        self.main.history_controller.updateOperationsHist(self.main.history_controller.matrix_infos, text
                                                          + " Filter order : " +
                                                          str(order))
