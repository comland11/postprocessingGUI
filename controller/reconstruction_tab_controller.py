import numpy as np

from widget.reconstruction_tab_widget import ReconstructionTabWidget


class ReconstructionTabController(ReconstructionTabWidget):
    def __init__(self, *args, **kwargs):
        super(ReconstructionTabController, self).__init__(*args, **kwargs)

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
        self.sampled = self.main.toolbar_controller.k_space_raw
        fov = np.reshape(mat_data['fov'], -1)
        nPoints = np.reshape(mat_data['nPoints'], -1)
        s = np.reshape(self.sampled[:, 3], nPoints[-1::-1])
        rho = np.zeros((nPoints[0]*nPoints[1]*nPoints[2]))

        x = np.linspace(-fov[0] / 2, fov[0] / 2, nPoints[0])
        y = np.linspace(-fov[1] / 2, fov[1] / 2, nPoints[1])
        z = np.linspace(-fov[2] / 2, fov[2] / 2, nPoints[2])

        y, z, x = np.meshgrid(y, z, x)

        x = np.reshape(x, -1)
        y = np.reshape(y, -1)
        z = np.reshape(z, -1)

        NZ = nPoints[2]
        kk = list(range(NZ))
        FoVz = fov[2]
        dz2 = FoVz / NZ
        a = (-(NZ - 1) / 2 + kk) * dz2

        Ny = nPoints[1]
        ky = list(range(Ny))
        FoVy = fov[1]
        dzy = FoVy / Ny
        b = (-(Ny - 1) / 2 + ky) * dzy

        Nx = nPoints[0]
        kx = list(range(Nx))
        FoVx = fov[0]
        dzx = FoVx / Nx
        c = (-(Nx - 1) / 2 + kx) * dzx


        for t in range(len(s)):
            Mt_k = np.exp(-1j * (2 * np.pi * self.sampled[t, 2] * z))
            Mt_j = np.exp(-1j * (2 * np.pi * self.sampled[t, 1] * y))

            Mt_jk = np.reshape((np.transpose(Mt_j) * Mt_k), (1, -1))
            # Mt = np.reshape((np.exp(-1j * (2 * np.pi * self.sampled[t, 0] * x)) * Mt_jk, (1,  nPoints[0] * nPoints[1] * nPoints[2])))
            # M = np.exp(-1j * (2 * np.pi * self.sampled[t, 0] * x)) * Mt_k * Mt_j
            Mt = np.reshape(np.exp(-1j * (2 * np.pi * self.sampled[t, 0] * x)) * Mt_jk, (1, -1))

            norm = np.matmul(Mt, np.transpose(Mt))
            delta_t = (s[t] - np.sum(Mt * rho)) / norm

            delta_t_conj_Mt = np.reshape(np.abs(delta_t) * np.conj(Mt), rho.shape)
            rho = rho + delta_t_conj_Mt

            # rho = rho + 1 * np.abs(delta_t) * np.conj(Mt)  # Effectuer l'addition

            self.main.image_view_widget.setImage(np.abs(rho))
