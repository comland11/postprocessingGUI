import os
import time
import sys
import threading
import numpy as np
import matlab.engine
from widget.reconstruction_tab_widget import ReconstructionTabWidget


class ReconstructionTabController(ReconstructionTabWidget):
    """
    Controller class for the ReconstructionTabWidget.

    Inherits from ReconstructionTabWidget to provide additional functionality for image reconstruction.

    Attributes:
        image_fft_button: QPushButton for performing FFT reconstruction.
        image_art_button: QPushButton for performing ART reconstruction.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the ReconstructionTabController.

        Connects the image_fft_button clicked signal to the fftReconstruction method.
        Connects the image_art_button clicked signal to the artReconstruction method.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super(ReconstructionTabController, self).__init__(*args, **kwargs)

        # Connect the image_fft_button clicked signal to the fftReconstruction method
        self.pocs_button.clicked.connect(self.pocsReconstruction)
        self.image_fft_button.clicked.connect(self.fftReconstruction)
        self.image_art_button.clicked.connect(self.artReconstruction)

    def fftReconstruction(self):
        """
        Perform FFT reconstruction in a separate thread.

        Creates a new thread and runs the runFftReconstruction method in that thread.
        """
        thread = threading.Thread(target=self.runFftReconstruction)
        thread.start()

    def runFftReconstruction(self):
        """
        Perform FFT reconstruction.

        Retrieves the k-space data from the main matrix of the image view widget.
        Performs inverse FFT shift, inverse FFT, and inverse FFT shift to reconstruct the image in the spatial domain.
        Updates the main matrix of the image view widget with the reconstructed image.
        Adds the "FFT" operation to the history widget and updates the history dictionary and operations history.
        """
        # Get the k-space data from the main matrix
        k_space = 10 ** self.main.image_view_widget.main_matrix

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
        """
        Perform ART reconstruction in a separate thread.

        Creates a new thread and runs the runArtReconstruction method in that thread.
        """
        thread = threading.Thread(target=self.runArtReconstruction)
        thread.start()

    def runArtReconstruction(self):
        """
        Perform ART reconstruction.

        Retrieves the mat data from the loaded .mat file in the main toolbar controller.
        Extracts the necessary data from the mat file.
        Performs the ART reconstruction algorithm.
        Updates the main matrix of the image view widget with the reconstructed image.
        Adds the "ART" operation to the history widget and updates the history dictionary and operations history.
        """
        # Get the mat data from the loaded .mat file in the main toolbar controller
        mat_data = self.main.toolbar_controller.mat_data

        print('ART is loading')

        # Extract datas data from the loaded .mat file
        self.sampled = self.main.toolbar_controller.k_space_raw
        fov = np.reshape(mat_data['fov'], -1) * 1e-2
        nPoints = np.reshape(mat_data['nPoints'], -1)
        s = self.sampled[:, 3]
        rho = np.zeros((nPoints[0] * nPoints[1] * nPoints[2]))
        lbda = float(self.lambda_text_field.text())
        niter = int(self.niter_text_field.text())

        eng = matlab.engine.start_matlab()

        eng.workspace['fov'] = matlab.double(fov.tolist(), is_complex=True)
        eng.workspace['nPoints'] = matlab.double(nPoints.tolist(), is_complex=True)
        eng.workspace['sampled'] = matlab.double(self.sampled.tolist(), is_complex=True)
        eng.workspace['s'] = matlab.double(s.tolist(), is_complex=True)
        eng.workspace['niter'] = matlab.double(niter, is_complex=True)
        eng.workspace['lbda'] = matlab.double(lbda, is_complex=True)
        eng.workspace['rho'] = matlab.double(rho.tolist(), is_complex=True)

        start_time = time.time()

        matlab_script_path = self.getPath()

        # Exécuter le script MATLAB
        eng.run(matlab_script_path, nargout=0)


        rho = eng.workspace['rho']

        # Close MATLAB engine
        eng.quit()

        rho = np.array(rho)

        print('ART has been applied')

        # Update the main matrix of the image view widget with the cosbell data
        self.main.image_view_widget.main_matrix = rho

        # Add the "Cosbell" operation to the history widget
        self.main.history_controller.addItemWithTimestamp("ART")

        # Update the history dictionary with the new main matrix for the current matrix info
        self.main.history_controller.hist_dict[self.main.history_controller.matrix_infos] = \
            self.main.image_view_widget.main_matrix

        # Update the operations history
        self.main.history_controller.operations_dict[self.main.history_controller.matrix_infos] = ["ART"]

        # Obtenir le temps d'arrêt
        end_time = time.time()

        # Calculer le temps écoulé en secondes
        elapsed_time = end_time - start_time

        # Calculer les composantes du temps
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = int(elapsed_time % 60)

        print(f"Time : {hours} hours, {minutes} minutes, {seconds} seconds")


    def pocsReconstruction(self):
        """
        Perform ART reconstruction in a separate thread.

        Creates a new thread and runs the runArtReconstruction method in that thread.
        """
        thread = threading.Thread(target=self.runPocsReconstruction)
        thread.start()

    def runPocsReconstruction(self):
        # Number of point before m+n where we begin to go to zero
        nb_point = int(self.nb_points_text_field.text())
        # Set the correlation threshold for stopping the iterations
        correlation_threshold = int(self.threshold_text_field.text())

        m = self.main.preprocessing_controller.m
        n = self.main.preprocessing_controller.n
        kSpace_center = self.main.preprocessing_controller.kSpace_center
        kSpace_ref = self.main.preprocessing_controller.kSpace_ref
        img_ref = np.fft.ifftshift(np.fft.ifftn(np.fft.ifftshift(10 ** self.main.image_view_widget.main_matrix)))

        kSpace_partial = np.copy(kSpace_ref)
        kSpace_partial[:, :, n + m::] = 0.0
        img_partial = np.abs(np.fft.ifftshift(np.fft.ifftn(np.fft.ifftshift(kSpace_partial))))  # IFFT on kspace
        img_full = np.concatenate((np.abs(img_ref), img_partial), axis=2)

        img_center = np.fft.ifftshift(np.fft.ifftn(np.fft.ifftshift(kSpace_center)))  # Compute the inverse Fast Fourier Transform of the modified signal to obtain the corresponding image
        phase = img_center / abs(img_center)  # An alternative way to accomplish the desired phase correction is to compute a normalized version of the complex image p

        # Generate the corresponding image with a ramp filter
        kSpace_ramp = self.ramp(kSpace_ref, n, m, nb_point)
        img_ramp = np.abs(np.fft.ifftshift(np.fft.ifftn(np.fft.ifftshift(kSpace_ramp))))  # IFFT on kspace

        # Generate the corresponding image with the Hanning filter
        kSpace_hanning = self.hanning_filter(kSpace_ref, n, m, nb_point)

        img_hanning = np.abs(np.fft.ifftshift(np.fft.ifftn(np.fft.ifftshift(kSpace_hanning))))  # IFFT on kspace

        num_iterations = 0  # Initialize the iteration counter
        previous_img = img_hanning  # you have the choice between img_hanning or img_ramp

        while True:
            # Iterative reconstruction
            img_iterative = previous_img * phase  # Multiply with the phase
            kSpace_new = np.fft.fftshift(np.fft.fftn(np.fft.fftshift(img_iterative)))  # Compute the FFT

            # Apply constraint: Keep the region of k-space from n+m onwards and restore the rest
            kSpace_new[:, :, 0:n + m] = kSpace_ref[:, :, 0:n + m]

            # Reconstruct the image from the modified k-space
            img_reconstructed = np.abs(np.fft.ifftshift(np.fft.ifftn(np.fft.ifftshift(kSpace_new))))

            # Compute correlation between consecutive reconstructed images
            correlation = np.corrcoef(previous_img.flatten(), img_reconstructed.flatten())[0, 1]

            # Display correlation and current iteration number
            print(f"Iteration: {num_iterations}, Correlation: {correlation}")

            # Check if correlation reaches the desired threshold
            if correlation >= correlation_threshold:
                break

            # Update previous_img for the next iteration
            previous_img = img_reconstructed.copy()

            # Increment the iteration counter
            num_iterations += 1

        # Display the final reconstructed image
        img_reconstructed = np.abs(img_reconstructed)

        img_full = np.concatenate((img_full, img_reconstructed), axis=2)

        # Update the main matrix of the image view widget with the interpolated image
        self.main.image_view_widget.main_matrix = img_full

        # Add the "Interpolation" operation to the history widget
        self.main.history_controller.addItemWithTimestamp("POCS")

        # Update the history dictionary with the new main matrix for the current matrix info
        self.main.history_controller.hist_dict[self.main.history_controller.matrix_infos] = \
            self.main.image_view_widget.main_matrix

        # Update the operations history
        self.main.history_controller.updateOperationsHist(self.main.history_controller.matrix_infos, "POCS")

    def ramp(self, kSpace, n, m, nb_point):
        kSpace_ramp = np.copy(kSpace)
        kSpace_ramp[:, :, n + m::] = 0.0

        # index of the gradient
        start_point = n + m - nb_point
        end_point = n + m
        facteur_gradient = kSpace_ramp[:, :, n + m - nb_point] / nb_point

        # go progressively to 0
        for i in range(start_point, end_point):
            kSpace_ramp[:, :, i + 1] *= kSpace_ramp[:, :, i] - facteur_gradient

        return kSpace_ramp


    def hanning_filter(self, kSpace, n, m, nb_point):
        kSpace_hanning = np.copy(kSpace)
        kSpace_hanning[:, :, n + m::] = 0.0

        # Calculate the Hanning window
        hanning_window = np.hanning(nb_point * 2)

        # Apply the Hanning filter to the k-space
        start_point = n + m - nb_point
        end_point = n + m

        for i in range(start_point, end_point):
            window_index = i - (n + m - nb_point)
            kSpace_hanning[:, :, i] *= hanning_window[window_index]

        return kSpace_hanning

    def getPath(self):
        # Obtenir le chemin absolu du dossier du script Python en cours d'exécution
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Chemin relatif vers le dossier "scripts" dans votre projet
        scripts_dir = os.path.join(current_dir, '..', 'scripts')

        # Chemin absolu vers le fichier regridding.m
        matlab_script_path = os.path.join(scripts_dir, 'art.m')

        return matlab_script_path