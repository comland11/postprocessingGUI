import numpy as np

from widget.tab_widget import TabWidget


class TabController(TabWidget):
    def __init__(self, *args, **kwargs):
        super(TabController, self).__init__(*args, **kwargs)

        # Connect the image_fft_button clicked signal to the fftReconstruction method
        self.image_fft_button.clicked.connect(self.fftReconstruction)
        self.image_art_button.clicked.connect(self.artReconstruction)

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

    def artReconstruction(self):
        # Get the mat data from the loaded .mat file in the main toolbar controller
        mat_data = self.main.toolbar_controller.mat_data

        # Extract datas data from the loaded .mat file
        self.sampled = mat_data['sampled']
        fov = mat_data['fov']
        nPoints = np.reshape(mat_data['nPoints'], -1)

        kx = np.linspace(-fov[:, 0]/2, fov[:, 0]/2, nPoints[0])
        ky = np.linspace(-fov[:, 1]/2, fov[:, 1]/2, nPoints[1])
        kz = np.linspace(-fov[:, 2]/2, fov[:, 2]/2, nPoints[2])

        y, z, x = np.meshgrid(ky, kz, kx)

        newx = np.reshape(x, -1)
        newy = np.reshape(y, -1)
        newz = np.reshape(z, -1)
        print(newx)
        print(newy)
        print(newz)
