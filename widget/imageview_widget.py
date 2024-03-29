from pyqtgraph import ImageView


class ImageViewWidget(ImageView):
    """
    ImageViewWidget class for displaying an image view.

    Inherits from ImageView provided by pyqtgraph to display an image view.

    Attributes:
        main: The parent widget.
    """

    def __init__(self, parent, *args, **kwargs):
        """
        Initialize the ImageViewWidget.

        Args:
            parent: The parent widget.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super(ImageViewWidget, self).__init__(*args, **kwargs)

        # The 'main' attribute represents the parent widget, which is used to access the main window or controller.
        self.main = parent

        # Set the minimum size of the image view widget to 400x400 pixels.
        self.setMinimumSize(400, 400)
