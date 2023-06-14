import threading

import numpy as np

from widget.reconstruction_tab_widget import ReconstructionTabWidget


class ReconstructionTabController(ReconstructionTabWidget):
    def __init__(self, *args, **kwargs):
        super(ReconstructionTabController, self).__init__(*args, **kwargs)

        # Connect the image_fft_button clicked signal to the fftReconstruction method
        self.image_fft_button.clicked.connect(self.fftReconstruction)
        self.image_art_button.clicked.connect(self.artReconstruction)

    def fftReconstruction(self):
        thread = threading.Thread(target=self.runFftReconstruction)
        thread.start()

    def runFftReconstruction(self):
        # Get the k-space data from the main matrix
        k_space = self.main.image_view_widget.main_matrix

        # Perform inverse FFT shift, inverse FFT, and inverse FFT shift to reconstruct the image in the spatial domain
        image_fft = np.fft.ifftshift(np.fft.ifftn(np.fft.ifftshift(k_space)))

        # Update the main matrix of the image view widget with the image fft data
        self.main.image_view_widget.main_matrix = image_fft

        # Add the "FFT" operation to the history widget
        self.main.history_controller.addItemWithTimestamp("FFT")

        # Update the history dictionary with the new main matrix for the current matrix info
        self.main.history_controller.hist_dict[self.main.history_controller.matrix_infos] = \
            self.main.image_view_widget.main_matrix

        # Update the operations history
        self.main.history_controller.updateOperationsHist(self.main.history_controller.matrix_infos, "FFT")

    def artReconstruction(self):
        thread = threading.Thread(target=self.runArtReconstruction)
        thread.start()

    def runArtReconstruction(self):
        #  Get the mat data from the loaded .mat file in the main toolbar controller
        mat_data = self.main.toolbar_controller.mat_data

        print('The ART is applying')

        # Extract datas data from the loaded .mat file
        self.sampled = self.main.toolbar_controller.k_space_raw
        fov = np.reshape(mat_data['fov'], -1)*1e-2
        nPoints = np.reshape(mat_data['nPoints'], -1)
        s = self.sampled[:, 3]
        rho = np.zeros((nPoints[0] * nPoints[1] * nPoints[2]))
        lbda = float(self.lambda_text_field.text())
        niter = int(self.niter_text_field.text())

        x = np.linspace(-fov[0] / 2, fov[0] / 2, nPoints[0])
        y = np.linspace(-fov[1] / 2, fov[1] / 2, nPoints[1])
        z = np.linspace(-fov[2] / 2, fov[2] / 2, nPoints[2])

        y, z, x = np.meshgrid(y, z, x)

        x = np.reshape(x, -1)
        y = np.reshape(y, -1)
        z = np.reshape(z, -1)

        for n in range(0, niter):
            for t in np.random.permutation(range(len(s))):
            # for t in range(len(s)):
                mt_z = np.exp(-1j * 2 * np.pi * self.sampled[t, 2] * z)
                mt_y = np.exp(+1j * 2 * np.pi * self.sampled[t, 1] * y)
                mt_x = np.exp(-1j * 2 * np.pi * self.sampled[t, 0] * x)

                mt = mt_y * mt_z * mt_x

                norm = np.dot(mt, np.conj(mt))
                delta_t = (-s[t] + np.dot(mt, rho)) / norm

                rho = rho - lbda * delta_t * np.conj(mt)

                print("Iteration %i of %i" % (t, len(s)))

        rho = np.reshape(rho, nPoints[-1::-1])

        print('The ART is applied')

        # Update the main matrix of the image view widget with the cosbell data
        self.main.image_view_widget.main_matrix = rho

        # Add the "Cosbell" operation to the history widget
        self.main.history_controller.addItemWithTimestamp("ART")

        # Update the history dictionary with the new main matrix for the current matrix info
        self.main.history_controller.hist_dict[self.main.history_controller.matrix_infos] = \
            self.main.image_view_widget.main_matrix

        # Update the operations history
        self.main.history_controller.updateOperationsHist(self.main.history_controller.matrix_infos, "ART")
