from PyQt5.QtWidgets import QToolBar, QPushButton


class ToolBarWidget(QToolBar):
    """
    ToolBarWidget class for displaying a toolbar with buttons.

    Inherits from QToolBar provided by PyQt5 to display a toolbar with buttons.

    Attributes:
        main: The parent widget.
    """

    def __init__(self, parent, *args, **kwargs):
        """
        Initialize the ToolBarWidget.

        Args:
            parent: The parent widget.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super(ToolBarWidget, self).__init__(*args, **kwargs)

        # The 'main' attribute represents the parent widget, which is used to access the main window or controller.
        self.main = parent

        # Create a button for image loading
        self.image_loading_button = QPushButton('File')

        # Add the image loading button to the toolbar
        self.addWidget(self.image_loading_button)
