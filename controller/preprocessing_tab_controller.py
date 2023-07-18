import threading
import numpy as np
from widget.preprocessing_tab_widget import PreProcessingTabWidget


class PreProcessingTabController(PreProcessingTabWidget):
    """
    Controller class for the pre-processing tab widget.

    Inherits from PreProcessingTabWidget.

    Attributes:
        partial_reconstruction_button: QPushButton for applying Partial reconstruction.
        image_cosbell_button: QPushButton for applying Cosbell filter.
        image_padding_button: QPushButton for applying zero padding.
        new_fov_button: QPushButton for changing the field of view.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the PreProcessingTabController.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super(PreProcessingTabController, self).__init__(*args, **kwargs)

        # Connect the button click signal to the corresponding methods
        self.partial_reconstruction_button.clicked.connect(self.partialReconstruction)
        self.image_cosbell_button.clicked.connect(self.cosbellFilter)
        self.image_padding_button.clicked.connect(self.zeroPadding)
        self.new_fov_button.clicked.connect(self.fovShifting)

    def cosbellFilter(self):
        """
        Apply the Cosbell filter operation using threading.

        Starts a new thread to execute the runCosbellFilter method.
        """
        thread = threading.Thread(target=self.runCosbellFilter)
        thread.start()

    def runCosbellFilter(self):
        """
        Run the Cosbell filter operation.

        Retrieves the necessary parameters and performs the Cosbell filtering on the loaded image.
        Updates the main matrix of the image view widget with the filtered data, adds the operation to the history widget,
        and updates the operations history.
        """
        text = "Cosbell -"
        cosbell_order = float(self.cosbell_order_field.text())

        # Get the mat data from the loaded .mat file in the main toolbar controller
        mat_data = self.main.toolbar_controller.mat_data

        # Extract data from the loaded .mat file
        sampled = self.main.toolbar_controller.k_space_raw
        nPoints = np.reshape(mat_data['nPoints'], -1)

        # Check which checkboxes are selected
        if self.readout_checkbox.isChecked():
            k = np.reshape(sampled[:, 0], nPoints[-1::-1])
            kmax = np.max(np.abs(k[:]))
            text += ' RD,'
        if self.phase_checkbox.isChecked():
            k = np.reshape(sampled[:, 1], nPoints[-1::-1])
            kmax = np.max(np.abs(k[:]))
            text += ' PH,'
        if self.slice_checkbox.isChecked():
            k = np.reshape(sampled[:, 2], nPoints[-1::-1])
            kmax = np.max(np.abs(k[:]))
            text += ' SL,'

        theta = k / kmax
        s = np.reshape(sampled[:, 3], nPoints[-1::-1])
        cosbell = s * (np.cos(theta * (np.pi / 2)) ** cosbell_order)

        # Calculate logarithmic scale
        small_value = 1e-10
        cosbell_log = np.log10(cosbell + small_value)

        # Update the main matrix of the image view widget with the cosbell data
        self.main.image_view_widget.main_matrix = cosbell_log

        # Add the "Cosbell" operation to the history widget
        self.main.history_controller.addItemWithTimestamp("Cosbell")

        # Update the history dictionary with the new main matrix for the current matrix info
        self.main.history_controller.hist_dict[self.main.history_controller.matrix_infos] = \
            self.main.image_view_widget.main_matrix

        # Update the operations history
        self.main.history_controller.operations_dict[self.main.history_controller.matrix_infos] = [text + " Order : "
                                                                                                   + str(cosbell_order)]

    def zeroPadding(self):
        """
        Apply the zero-padding operation using threading.

        Starts a new thread to execute the runZeroPadding method.
        """
        thread = threading.Thread(target=self.runZeroPadding)
        thread.start()

    def runZeroPadding(self):
        """
        Run the zero-padding operation.

        Retrieves the necessary parameters and performs the zero-padding on the loaded image.
        Updates the main matrix of the image view widget with the padded image, adds the operation to the history
        widget, and updates the operations history.
        """
        zero_padding_order = self.zero_padding_order_field.text().split(',')
        rd_order = int(zero_padding_order[0])
        ph_order = int(zero_padding_order[1])
        sl_order = int(zero_padding_order[2])

        k_space = 10 ** self.main.image_view_widget.main_matrix

        # Get self.k_space shape
        current_shape = k_space.shape

        # Determine new shape
        new_shape = current_shape[0] * sl_order, current_shape[1] * ph_order, current_shape[2] * rd_order

        # Create an image matrix filled with zeros
        image_matrix = np.zeros(new_shape, dtype=np.complex128)

        image_height = current_shape[0]
        image_width = current_shape[1]
        image_depth = current_shape[2]

        # Calculate the centering offsets
        col_offset = (new_shape[0] - image_height) // 2
        row_offset = (new_shape[1] - image_width) // 2
        depth_offset = (new_shape[2] - image_depth) // 2

        # Calculate the start and end indices to center the k_space within the image_matrix
        col_start = col_offset
        col_end = col_start + image_height
        row_start = row_offset
        row_end = row_start + image_width
        depth_start = depth_offset
        depth_end = depth_start + image_depth

        # Copy the k_space into the image_matrix at the center
        image_matrix[col_start:col_end, row_start:row_end, depth_start:depth_end] = k_space

        # Calculate logarithmic scale
        small_value = 1e-10
        padded_image_log = np.log10(image_matrix + small_value)

        # Update the main matrix of the image view widget with the padded image
        self.main.image_view_widget.main_matrix = padded_image_log

        # Add the "Zero Padding" operation to the history widget
        self.main.history_controller.addItemWithTimestamp("Zero Padding")

        # Update the history dictionary with the new main matrix for the current matrix info
        self.main.history_controller.hist_dict[self.main.history_controller.matrix_infos] = \
            self.main.image_view_widget.main_matrix

        # Update the operations history
        self.main.history_controller.updateOperationsHist(self.main.history_controller.matrix_infos, "Zero Padding - " +
                                                          "RD : " + str(rd_order) + ", PH : " + str(ph_order) +
                                                          ", SL : " + str(sl_order))

    def fovShifting(self):
        """
        Perform the FOV change operation using threading.

        Starts a new thread to execute the runFovChange method.
        """
        thread = threading.Thread(target=self.runFovShifting)
        thread.start()

    def runFovShifting(self):
        """
        Run the FOV change operation.

        Retrieves the necessary parameters and performs the FOV change on the loaded image.
        Updates the main matrix of the image view widget with the new FOV image, adds the operation to the history
        widget, and updates the operations history.
        """
        k = self.main.toolbar_controller.k_space_raw.copy()
        nPoints = self.main.toolbar_controller.nPoints

        factors = self.change_fov_field.text().split(',')

        krd = k[:, 0]
        kph = k[:, 1]
        ksl = k[:, 2]
        s = k[:, 3]

        k = np.column_stack((krd, kph, ksl))

        delta_rd = (float(factors[0])) * 10 ** -3
        delta_ph = (float(factors[1])) * 10 ** -3
        delta_sl = (float(factors[2])) * 10 ** -3
        delta_r = np.array([delta_rd, delta_ph, delta_sl])

        phi = np.exp(-1j * 2 * np.pi * k @ np.reshape(delta_r, (3, 1)))
        s = np.reshape(s, (np.size(phi, 0), 1)) * phi

        signal = np.column_stack((k, s))
        new_k_space = np.reshape(signal[:, 3], nPoints[-1::-1])

        # Calculate logarithmic scale
        small_value = 1e-10
        new_k_space_log = np.log10(new_k_space + small_value)

        # Update the main matrix of the image view widget with the k-space data
        self.main.image_view_widget.main_matrix = new_k_space_log

        # Add the "New FOV" operation to the history
        self.main.history_controller.addItemWithTimestamp("New FOV")

        # Update the history dictionary with the new main matrix for the current matrix info
        self.main.history_controller.hist_dict[self.main.history_controller.matrix_infos] = \
            self.main.image_view_widget.main_matrix

        # Update the operations history
        self.main.history_controller.operations_dict[self.main.history_controller.matrix_infos] = ["New FOV - " +
                                                                                                   "RD : " +
                                                                                                   str(delta_rd) +
                                                                                                   ", PH : " +
                                                                                                   str(delta_ph) +
                                                                                                   ", SL : " +
                                                                                                   str(delta_sl)]

    def partialReconstruction(self):
        """
        Perform the partial reconstruction operation using threading.

        Starts a new thread to execute the runPartialReconstruction method.
        """
        thread = threading.Thread(target=self.runPartialReconstruction)
        thread.start()

    def runPartialReconstruction(self):
        """
        Run the partial reconstruction operation.

        Retrieves the necessary parameters and performs the partial reconstruction on the loaded image.
        Updates the main matrix of the image view widget with the partially reconstructed image, adds the operation to
        the history widget, and updates the operations history.
        """
        k_space = self.main.toolbar_controller.k_space_raw.copy()
        nPoints = self.main.toolbar_controller.nPoints
        percentage = float(self.partial_reconstruction_field.text()) * 10 ** -2

        krd = np.real(k_space[:, 0])
        kph = np.real(k_space[:, 1])
        ksl = np.real(k_space[:, 2])
        signal = k_space[:, 3]

        ksl_min = ksl.min()
        ksl_max = ksl.max()

        k0 = percentage * (ksl_max - ksl_min) + ksl_min
        for i in range(len(ksl)):
            if ksl[i] > k0:
                signal[i] = 0

        k = np.column_stack((krd, kph, ksl, signal))
        k = np.reshape(k[:, 3], nPoints[-1::-1])

        # Calculate logarithmic scale
        small_value = 1e-10
        k_log = np.log10(k + small_value)

        # Update the main matrix of the image view widget with the k-space data
        self.main.image_view_widget.main_matrix = k_log

        # Add the "Partial Reconstruction" operation to the history
        self.main.history_controller.addItemWithTimestamp("Partial Reconstruction")

        # Update the history dictionary with the new main matrix for the current matrix info
        self.main.history_controller.hist_dict[self.main.history_controller.matrix_infos] = \
            self.main.image_view_widget.main_matrix

        # Update the operations history
        self.main.history_controller.operations_dict[self.main.history_controller.matrix_infos] = ["Partial "
                                                                                                   "Reconstruction - "
                                                                                                   + str(percentage)]
