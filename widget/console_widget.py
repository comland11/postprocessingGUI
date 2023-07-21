from PyQt5.QtWidgets import QTextEdit, QMainWindow, QSizePolicy


class ConsoleWidget(QMainWindow):
    """
    Console widget class for displaying console output.

    Inherits from QMainWindow to provide a window for the console widget.

    Attributes:
        console (QTextEdit): Text edit widget for displaying the console output.
    """

    def __init__(self):
        """
        Initialize the ConsoleWidget.

        Args:
            None
        """
        super().__init__()

        # Create the console widget
        self.console = QTextEdit()
        self.console.setReadOnly(True)  # Make the text edit read-only to prevent user input
        self.setCentralWidget(self.console)  # Set the text edit as the central widget for the main window
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)  # Set the size policy for the widget
        self.setMaximumWidth(400)  # Set the maximum width of the widget to 400 pixels
