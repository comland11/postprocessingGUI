import numpy as np
from widget.visualisation_tab_widget import VisualisationTabWidget


class VisualisationTabController(VisualisationTabWidget):
    """
    Controller class for the VisualisationTabWidget.

    Inherits from VisualisationTabWidget to provide additional functionality for managing visualisation tab actions.

    Attributes:
        visualisation_button: QPushButton for showing 2D slices.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the VisualisationTabController.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super(VisualisationTabController, self).__init__(*args, **kwargs)

        # Connect the visualisation_button clicked signal to the imageVisualisation method
        self.visualisation_button.clicked.connect(self.imageVisualisation)

    def imageVisualisation(self):
        """
        Perform image visualisation on the selected slices of the main matrix.

        Display the selected slices as images using a grid layout.
        """

        # Get the main matrix containing the image data
        image = self.main.image_view_widget.main_matrix

        # Get the selected range of slices to display
        slices = self.range_text_field.text().split(',')
        n0 = int(slices[0])
        n_end = int(slices[1])
        selected_slices = image[n0:n_end + 1]

        # Get the number of rows and columns for the grid layout
        rows_columns = self.column_text_field.text().split(',')
        rows_number = int(rows_columns[0])
        columns_number = int(rows_columns[1])

        # Get the height and width of each slice
        slice_height, slice_width = image.shape[1], image.shape[2]

        # Create an empty image matrix to hold the visualized slices
        image_matrix = np.zeros((slice_height * columns_number, slice_width * rows_number), dtype=np.complex128)

        i = 0
        while i < len(selected_slices):
            # Calculate the row and column indices for the current slice in the grid layout
            row = i // columns_number
            col = i % columns_number

            # Calculate the start and end indices for the rows and columns in the image matrix
            row_start = row * slice_height
            row_end = row_start + slice_height
            col_start = col * slice_width
            col_end = col_start + slice_width

            # Copy the current slice (selected_slices[i]) to its corresponding position in the image matrix
            image_matrix[col_start:col_end, row_start:row_end] = selected_slices[i]

            # Move to the next slice
            i += 1

        # Update the main image view widget with the visualized image matrix
        self.main.image_view_widget.setImage(abs(image_matrix))

        # Clear the second image view
        self.main.history_controller.clearSecondImageView()
